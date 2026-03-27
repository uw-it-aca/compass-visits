import { createWebHistory, createRouter } from "vue-router";

// vue-gtag-next track routing
// import { trackRouter } from "vue-gtag-next";

// page components
import Home from "@/pages/home.vue";
import Verify from "@/pages/verify.vue";
import Checkout from "@/pages/checkout.vue";
import Create from "@/pages/create.vue";
import Summary from "@/pages/summary.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/create",
    name: "Create",
    component: Create,
  },
  {
    path: "/verify",
    name: "Verify",
    component: Verify,
  },
  {
    path: "/checkout",
    name: "Checkout",
    component: Checkout,
  },
  {
    path: "/summary",
    name: "Visit Summary",
    component: Summary,
  },


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// add router tracking to vue-gtag-next
// trackRouter(router);

export default router;
