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
            headline: "Demo - výběr role",
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
              name: "doctor-edu-resources",
              components: {
                default: () => import("@/views/doctor/EduResourcesView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Edukační materiály",
              }
            },
            {
              path: "edukacni-materialy/:id",
              name: "doctor-edu-resource-reader",
              components: {
                default: () => import("@/views/doctor/EduResourceReaderView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Náhled edukačního materiálu",
              }
            },
            {
              path: "edukacni-materialy/editovat/:id",
              name: "doctor-edu-resource-edit",
              components: {
                default: () => import("@/views/doctor/EduResourceEditView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Editace edukačního materiálu",
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
                headline: "Žádosti",
              }
            }
          ]
        },

        // Patient routes
        {
          path: 'pacient',
          children: [
            {
              path: "",
              name: "patient-home",
              components: {
                default: () => import("@/views/patient/HomeView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Rozcestník",
              }
            },
            {
              path: "lekarske-zaznamy",
              name: "patient-reports",
              components: {
                default: () => import("@/views/patient/ReportsView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Lékařské zprávy",
              }
            },
            {
              path: "edukacni-materialy",
              name: "patient-edu-resources",
              components: {
                default: () => import("@/views/patient/EducationResourcesView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Edukační materiály",
              }
            },
            {
              path: "edukacni-materialy/:id",
              name: "patient-edu-resource-reader",
              components: {
                default: () => import("@/views/patient/EducationResourceReaderView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              }
            },
            {
              path: "lekarske-zaznamy/:id",
              name: "patient-report-detail",
              components: {
                default: () => import("@/views/patient/ReportDetailView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Zpráva",
              }
            },
            {
              path: "pozadavek-schuzka",
              name: "patient-request-appointment",
              components: {
                default: () => import("@/views/patient/RequestAppointmentView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavek-predpis",
              name: "patient-request-prescription",
              components: {
                default: () => import("@/views/patient/RequestPrescriptionView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "",
              }
            },
            {
              path: "pozadavky",
              name: "patient-requests",
              components: {
                default: () => import("@/views/patient/RequestsView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Žádosti",
              }
            },
            {
              path: "pozadavek-dokumentace",
              name: "patient-request-upload",
              components: {
                default: () => import("@/views/patient/RequestUpload.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Upload dokumentace",
              }
            },
            {
              path: "checkin",
              name: "patient-task-checkin",
              components: {
                default: () => import("@/views/patient/TaskCheckinView.vue"),
                LeftSidebar: () => import("@/components/NavLeftPrimary.vue"),
              },
              meta: {
                headline: "Self-checkin",
              }
            }
          ]
        }]
    },

  ],
})

export default router
