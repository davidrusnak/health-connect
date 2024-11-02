import { createRouter, createWebHistory } from 'vue-router';
declare module 'vue-router' {
  interface RouteMeta {
    headline?: string;
    description?: string;
    parentName?: string;
  }
}

export const default_route_name = "home";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: () => import("@/layouts/MainLayout.vue"),
      children: [
        {
          path: "",
          name: default_route_name,
          components: {
            default: () => import("@/views/HomeView.vue"),
          },
          props: {
            default: true,
            LeftSidebar: false,
          },
          meta: {
            headline: "HealthConnect demo - výběr role",
          }
        },
        {
          path: '/doktor',
          children: [
            {
              path: "",
              name: "doctor-home",
              components: {
                default: () => import("@/views/doctor/HomeView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Přehled",
              },
            },
            {
              path: "pacienti",
              name: "doctor-patients",
              components: {
                default: () => import("@/views/doctor/PatientsView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Pacienti",
              }
            },
            {
              path: "pacienti/:id",
              name: "doctor-patient-profile",
              components: {
                default: () => import("@/views/doctor/PatientProfileView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Profil pacienta",
              }
            },
            {
              path: "edukacni-materialy",
              name: "doctor-education-resources",
              components: {
                default: () => import("@/views/doctor/EducationResourcesView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Vzdělávací materiály",
              }
            },
            {
              path: "edukacni-materialy/vytvorit",
              name: "doctor-education-resource-new",
              components: {
                default: () => import("@/views/doctor/EducationResourceNewView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Nový vzdělávací materiál",
              }
            },
            {
              path: "edukacni-materialy/editovat/:id",
              name: "doctor-education-resource-edit",
              components: {
                default: () => import("@/views/doctor/EducationResourceEditView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavky",
              name: "doctor-requests",
              components: {
                default: () => import("@/views/doctor/RequestsView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Požadavky",
              }
            }
          ]
        },

        // Patient routes
        /* {
          path: 'pacient',
          component: () => import("@/layouts/MainLayout.vue"), // Assuming the same layout for patient
          children: [
            {
              path: "edukacni-materialy",
              name: "patient-education-resources",
              component: () => import("../views/patient/EducationResourcesView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "edukacni-materialy/:id",
              name: "patient-education-resource-viewer",
              component: () => import("../views/patient/EducationResourceViewer.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "",
              name: "patient-home",
              component: () => import("../views/patient/HomeView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "lekarske-zaznamy",
              name: "patient-reports",
              component: () => import("../views/patient/ReportsView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "lekarske-zaznamy/:id",
              name: "patient-report-detail",
              component: () => import("../views/patient/ReportDetailView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavek-schuzka",
              name: "patient-request-appointment",
              component: () => import("../views/patient/RequestAppointmentView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavek-predpis",
              name: "patient-request-prescription",
              component: () => import("../views/patient/RequestPrescriptionView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavky",
              name: "patient-requests",
              component: () => import("../views/patient/RequestsView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavek-dokumentace",
              name: "patient-request-upload",
              component: () => import("../views/patient/RequestUpload.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "checkin",
              name: "patient-task-checkin",
              component: () => import("../views/patient/TaskCheckinView.vue"),
              meta: {
                headline: "",
              }
            },
            {
              path: "ulohy",
              name: "patient-tasks",
              component: () => import("../views/patient/TasksView.vue"),
              meta: {
                headline: "",
              }
            },
          ]
        } */]
    },

  ],
})

export default router
