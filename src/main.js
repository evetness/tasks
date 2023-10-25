import { createApp } from "vue";
import { createPinia } from "pinia";
import axios from "axios";
import VueAxios from "vue-axios";

import App from "@/App.vue";
import "@/style.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";

library.add(fas, far);

const pinia = createPinia();

createApp(App)
  .use(pinia)
  .use(VueAxios, axios)
  .component("font-awesome-icon", FontAwesomeIcon)
  .mount("#app");
