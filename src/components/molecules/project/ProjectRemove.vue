<script>
import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default {
  name: "ProjectRemove",
  props: ["id", "name"],
  methods: {
    async submitForm() {
      const response = await axios.delete(`/api/projects/${this.id}`)
      if (response.status !== 204) return;
      this.$emit('form:submitted', this.id)
    }
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" 
    class="flex items-center text-brand/80 text-sm hover:bg-brand/20 focus:bg-brand/20 border-x border-dashed border-brand/80">
    <div class="flex items-center mr-auto">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 px-2" shake fixedWidth style="--fa-animation-duration: 2s;" />
      <div class="text-xs">
        Remove <span class="font-bold">{{ name }}</span>?
      </div>
    </div>
    <button type="submit" class="btn hover:bg-brand/30">
      <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
    </button>
    <button type="button" class="btn hover:bg-brand/30" @click="$emit('form:cancel')">
      <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
    </button>
  </form>
</template>