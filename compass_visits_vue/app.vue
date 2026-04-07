<template>
  <NavMessage
   v-if="persMsg && persMsg.length > 0"
  :messages="persMsg"
  :level="msgLevel"
  />
  <router-view></router-view>
</template>

<script>
import NavMessage from "@/components/nav-message.vue";

export default {
  name: "App",
  components: { NavMessage },
  data() {
    return {
      persMsg: window.persistent_msgs || [],
      msgLevel: window.persistent_msgs_level || "info",
    };
  },
};
</script>
