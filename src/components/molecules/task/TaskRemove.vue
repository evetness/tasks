<script>
import moment from 'moment/min/moment-with-locales'
import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default {
  name: "TaskRemove",
  props: ["id", "name", "start"],
  methods: {
    async removeTask() {
      const response = await axios.delete(`/api/tasks/${this.id}`)
      if (response.status !== 204) return;
      this.$emit('form:submitted', this.id)
    },
    moment
  }
}
</script>

<template>
  <tr class="border-x border-dashed border-brand/80">
    <td colspan="5">
      <div class="flex items-center mr-auto">
        <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 px-2" shake fixedWidth style="--fa-animation-duration: 2s;" />
        <div class="text-xs">
          Remove <span class="font-bold">{{ name }}</span> task started at <span class="font-bold">{{ this.moment(start).format("lll") }}</span>?
        </div>
      </div>
    </td>
    <td>
      <form id="task-remove-form" @submit.prevent="submitForm" class="flex items-center justify-end">
        <button type="submit" class="btn btn-text">
          <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
        </button>
        <button type="button" class="btn btn-text" @click="$emit('form:cancel')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
        </button>
      </form>
    </td>
  </tr>  
</template>