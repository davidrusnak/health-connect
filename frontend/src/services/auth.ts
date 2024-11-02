import router from "@/router";
import { ref } from "vue";

export enum UserRole {
  Doctor = "doctor",
  Patient = "patient",
  SurveyRespondent = "surveyRespondent",
}

export type UserProfile = {
  id: string;
  role: UserRole;
  email: string;
  preferred_username: string;
};

const MOCK_PROFILE: UserProfile = {
  id: 'user12345',
  role: 'Doctor' as UserRole,
  email: "mock@test.cz",
  preferred_username: "test-user",
};

async function authFetch(
  method: "POST" | "GET",
  endpoint: string,
  { body, ...cfg }: any = {}
) {
  const config = {
    method,
    ...cfg,
    headers: {
      "X-FusionAuth-TenantId": window._env_.VITE_AUTH_TENANT_ID,
      "Content-Type": "application/json",
    },
    credentials: "include",
  };
  if (body) {
    config.body = JSON.stringify(body);
  }

  return window
    .fetch(`${window._env_.VITE_AUTH_API_URL}/${endpoint}`, config)
    .then(async (response) => {
      if (response.ok) {
        return { data: await response.json(), status: response.status };
      } else {
        return Promise.reject({
          error: new Error(await response.text()),
          status: response.status,
        });
      }
    });
}

const api = {
  get: (endpoint: string, cfg = {}) => authFetch("GET", endpoint, cfg),
  post: (endpoint: string, body: any, cfg = {}) =>
    authFetch("POST", endpoint, { ...cfg, body }),
};

/**
 * Service for handling authentication with FusionAuth
 *
 * - integrates https://fusionauth.io/docs/v1/tech/apis/hosted-backend
 * - performs OAuth2 with PKCE, and uses optional state parameter to further protect from CSRF
 *   (see https://auth0.com/docs/secure/attack-protection/state-parameters)
 * - the state param is client-side check, the user who started the flow must be the one to finish it
 */
class AuthService {
  user_profile = ref<UserProfile | null>(null);
  token_expiration = ref<Date | null>(null);

  init() {
    if (DEV_MOCKING) {
      log.info("Auth: mocking user profile.");
      if (
        !DEV_MOCKING_USER_ID ||
        !DEV_MOCKING_USER_ROLE ||
        !Object.values(UserRole).includes(DEV_MOCKING_USER_ROLE as UserRole)
      ) {
        throw new Error("Auth: mocking enbled, but has incorrect env settings");
      }
      this.user_profile.value = MOCK_PROFILE;
      this.token_expiration.value = new Date("01-01-2099");
    }
    log.info("AuthService: initialized.");
  }

  /**
   * Start the login flow and redirect to FusionAuth
   * @param original_path after login redirect, relative to the root of the app, don't include leading slash
   */
  async start_login(): Promise<void> {
    if (DEV_MOCKING) {
      log.info("AuthService: mocking login, start login ignored.");
      return;
    }
    log.trace(
      "AuthService: Start login procedure with redirect to FusionAuth."
    );

    // FA hosted backend ignores the locale parameter, so we set it as a cookie
    document.cookie =
      "fusionauth.locale=cs_CZ; Path=/; Expires=Thu, 01 Jan 2030 00:00:01 GMT;";

    // generate and save nonce for state param
    const state_param = this.#generate_urlsafe_nonce();
    sessionStorage.setItem(SESSIONS_STORAGE_LOGIN_STATE_PARAM, state_param);
    const encoded_state = base64.encode(state_param, true, false); // no padding

    window.location.replace(
      `${FA_api_url}/app/login/${FA_client_id}?locale=cs_CZ&redirect_uri=${APP_FINISH_LOGIN_URL}&state=${encoded_state}`
    );
  }

  /**
   * Receive redirect back to the app from FusionAuth, and redirect to original path.
   * @param query vue router's LocationQuery with params from the url
   * @throws AuthErrors.ResponseUnexpected if the response from FusionAuth is not as expected
   * @throws AuthErrors.OAuthStateSecurityCheckFailed if the state param or redirect url was tampered with
   * @throws AuthErrors.InvalidRedirect if the redirect url is absolute
   */
  async complete_login(
    query: LocationQuery,
    redirectHome: boolean = true
  ): Promise<void> {
    if (DEV_MOCKING) return;
    log.debug("AuthService: completing login. Query:", query);

    if (query.userState !== "Authenticated")
      throw new Error(AuthErrors.ResponseUnexpected);

    const savedStateParam = sessionStorage.getItem(
      SESSIONS_STORAGE_LOGIN_STATE_PARAM
    );
    sessionStorage.removeItem(SESSIONS_STORAGE_LOGIN_STATE_PARAM);
    const receivedStateParam = String(base64.decode(String(query.state), true));
    // check that attacked didn't tamper with the state param
    if (savedStateParam !== receivedStateParam) {
      throw new Error(AuthErrors.OAuthStateSecurityCheckFailed);
    }
    // save token expiration unix timestamp
    this.token_expiration.value = new Date(
      String(this.#get_cookie("app.at_exp"))
    );

    // ID token doesn't contain roles, so we need to fetch the user profile
    this.user_profile.value = await this.fetch_user_profile();
    log.info("AuthService: fetched user profile: ", this.user_profile.value);
    // must be saved to storage, as this will be accessed early on, before fetch resolves
    localStorage.setItem(LOCAL_STORAGE_USER_ROLE, this.user_profile.value.role);

    // do not redirect to previous url to prevent open redirection attacks
    // https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#open_redirection
    if (redirectHome) router.push({ name: "home" });
  }

  /**
   * Request user profile from FusionAuth and save it
   * @returns user profile from FusionAuth
   * @throws AuthErrors.Unauthorized if the user is not logged in
   * @throws AuthErrors.ServiceCrashed if the FusionAuth service is not available
   */
  async fetch_user_profile(): Promise<UserProfile> {
    if (DEV_MOCKING) return MOCK_PROFILE;

    return api
      .get("app/me")
      .then((resp) => {
        log.trace(resp);
        if (resp.status === 200) {
          log.debug("AuthService: fetched user profile: ", resp.data);
          if (resp.data.roles.includes(UserRole.Doctor))
            resp.data.role = UserRole.Doctor;
          else if (resp.data.roles.includes(UserRole.Patient))
            resp.data.role = UserRole.Patient;
          else if (resp.data.roles.includes(UserRole.SurveyRespondent))
            resp.data.role = UserRole.SurveyRespondent;
          else throw new Error(AuthErrors.ResponseUnexpected);
          delete resp.data.roles;
          this.user_profile.value = resp.data;
          localStorage.setItem(LOCAL_STORAGE_USER_ROLE, resp.data.role);
          return resp.data;
        } else if (resp.status === 401) {
          throw new Error(AuthErrors.Unauthorized);
        } else {
          throw new Error(AuthErrors.ServiceCrashed);
        }
      })
      .catch((e) => {
        log.error(e);
        throw new Error(AuthErrors.Unauthorized + e);
      });
  }

  /**
   * Extract token expiration date from cookie set by FA
   * @returns date or null if not logged in
   */
  get_auth_token_expiration(): Date | null {
    if (DEV_MOCKING) return new Date("01-01-2099");

    const cookie = this.#get_cookie("app.at_exp");
    if (!cookie) return null;
    return new Date(parseInt(cookie, 10) * 1000);
  }

  /**
   * Generate url-safe cryptographically-secure random nonce of 40 characters
   * to be used with OAuth2 state param
   */
  #generate_urlsafe_nonce() {
    const validChars =
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let array = new Uint8Array(40);
    window.crypto.getRandomValues(array);
    array = array.map((x) => validChars.charCodeAt(x % validChars.length));
    return String.fromCharCode.apply(null, Array.from(array));
  }

  #get_cookie(name: string): string | null {
    const escapedName = name.replace(/([.*+?^${}()|\[\]\/\\])/g, "\\$1");
    const query = new RegExp(`(?:^|;\\s*)${escapedName}=([^;]*)`);
    const match = document.cookie.match(query);
    return match && match[1] ? decodeURIComponent(match[1]) : null;
  }

  /**
   * Refresh auth token by calling FA
   */
  async refresh_token(): Promise<boolean> {
    if (DEV_MOCKING) return true;

    try {
      const resp = await api.post(`app/refresh/${FA_client_id}`, {});

      if (resp.status == 200) {
        log.debug("AuthService: refreshed tokens.");
        return true;
      } else if (resp.status == 400) {
        log.debug("AuthService: needs re-auth.");
      } else {
        log.warn("AuthService: refresh failed.");
      }
    } catch (e) {
      log.error("AuthService: Error refreshing token: ", e);
    }
    return false;
  }

  async refresh_token_or_start_login(): Promise<void> {
    if (DEV_MOCKING) return;

    const refresh_ok = await this.refresh_token();
    if (!refresh_ok) {
      this.start_login();
    }
  }

  /**
   * Redirect to FA to logout
   */
  logout(): void {
    this.user_profile.value = null;
    localStorage.removeItem(LOCAL_STORAGE_USER_ROLE);
    window.location.replace(
      `${FA_api_url}/app/logout/${FA_client_id}?redirect_uri=${APP_FINISH_LOGOUT_URL}&locale=cs`
    );
  }

  is_logged_in(): boolean {
    if (DEV_MOCKING) return true;

    const cookie_exp = this.#get_cookie("app.at_exp");
    const cookie_idt = this.#get_cookie("app.idt");
    if (!cookie_exp || !cookie_idt) return false;
    if (this.has_login_expired()) return false;
    return true;
  }

  has_login_expired(): boolean {
    if (DEV_MOCKING) return false;

    const token_expiration_date = this.get_auth_token_expiration();
    if (!token_expiration_date) return true; // possibly logged out / expired
    if (token_expiration_date < new Date()) return true; // expired
    return false;
  }

  is_user_doctor(): boolean {
    if (DEV_MOCKING) return DEV_MOCKING_USER_ROLE == String(UserRole.Doctor);
    return (
      localStorage.getItem(LOCAL_STORAGE_USER_ROLE) == String(UserRole.Doctor)
    );
  }

  get_saved_user_role(): UserRole | null {
    return localStorage.getItem(LOCAL_STORAGE_USER_ROLE) as UserRole | null;
  }
}

const auth = new AuthService(); // this will not call constructor!

export default auth;
