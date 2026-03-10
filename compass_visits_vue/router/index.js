import { createWebHistory, createRouter } from "vue-router";

// vue-gtag-next track routing
// import { trackRouter } from "vue-gtag-next";

// page components
import Home from "@/pages/home.vue";
import Verify from "@/pages/verify.vue";
import Checkout from "@/pages/checkout.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
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

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// add router tracking to vue-gtag-next
// trackRouter(router);

export default router;
