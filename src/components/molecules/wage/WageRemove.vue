<script>
import moment from 'moment/min/moment-with-locales'

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import { formatCurrency } from "@/utils.js";
import {mapActions} from "pinia";
import {useWageStore} from "@/stores/wage.js";

export default {
  name: "WageRemove",
  props: ["id", "amount", "currency", "start"],
  methods: {
    async submitForm() {
      const response = await axios.delete(`/api/wages/${this.id}`)
      if (response.status !== 204) return;
      this.removeWage(this.id)
      this.$emit("form:close")
    },
    formatCurrency,
    moment,
    ...mapActions(useWageStore, ["removeWage"])
  },
  components: {FontAwesomeIcon},
  emits: ["form:close"]
}
</script>

<template>
  <div class="border-x border-dashed border-brand/80 grid grid-cols-12 gap-1">
    <div class="col-span-10 flex items-center mr-auto">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 px-2" shake fixedWidth style="--fa-animation-duration: 2s;" />
      <div class="text-xs">
        Remove <span class="font-bold">{{ this.formatCurrency(amount, currency) }}</span> wage started at <span class="font-bold">{{ this.moment(start).format("LL") }}</span>?
      </div>
    </div>
    <form id="task-remove-form" @submit.prevent="submitForm" class="col-span-2 flex items-center justify-end">
      <button type="submit" class="btn btn-text">
        <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
      </button>
      <button type="button" class="btn btn-text" @click="$emit('form:close')">
        <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
      </button>
    </form>
  </div>
</template>