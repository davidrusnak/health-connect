import resourcesApiTypes from "@/helpers/api/resources-v1";
import createClient from "openapi-fetch";
import { default as authService } from "./auth";

//
// REST endpoints
//

const resources = createClient<resourcesApiTypes.paths>({ baseUrl: window._env_.VITE_SURVEYS_API_URL, credentials: "include" });

export { resources };

