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
    name: "home",
    component: Home,
  },
  {
    path: "/create",
    name: "create",
    component: Create,
  },
  {
    path: "/verify",
    name: "verify",
    component: Verify,
  },
  {
    path: "/checkout",
    name: "checkout",
    component: Checkout,
  },
  {
    path: "/summary",
    name: "summary",
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
