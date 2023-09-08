<script>
import moment from 'moment/min/moment-with-locales'

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import { formatCurrency } from "@/utils.js";

export default {
  name: "WageRemove",
  props: ["id", "amount", "currency", "start"],
  methods: {
    async submitForm() {
      const response = await axios.delete(`/api/wages/${this.id}`)
      if (response.status !== 204) return;
      this.$emit('form:submitted', this.id)
    },
    formatCurrency,
    moment
  },
  components: {FontAwesomeIcon}
}
</script>

<template>
  <tr>
    <td colspan="2" class="border-l border-dashed border-brand/80">
      <div class="flex items-center mr-auto">
        <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 px-2" shake fixedWidth style="--fa-animation-duration: 2s;" />
        <div class="text-xs">
          Remove <span class="font-bold">{{ this.formatCurrency(amount, currency) }}</span> wage started at <span class="font-bold">{{ this.moment(start).format("LL") }}</span>?
        </div>
      </div>
    </td>
    <td class="border-r border-dashed border-brand/80">
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