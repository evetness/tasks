<script>
import moment from 'moment/min/moment-with-locales'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import { formatCurrency } from "@/utils.js";

export default {
  name: "WageItem",
  props: ["wage", "disabled"],
  methods: {
    formatCurrency,
    moment
  },
  emits: ["wage:edit", "wage:remove"],
  components: {FontAwesomeIcon}
}
</script>

<template>
  <div class="group hover:bg-brand/20 pl-1">
    <div class="grid grid-cols-12 items-center gap-1 text-xs">
      <div class="col-span-6 flex items-center gap-1">{{ this.moment(wage.date).format("LL") }}</div>
      <div class="col-span-4 text-right">{{ this.formatCurrency(wage.amount, wage.currency) }}</div>
      <div class="col-span-2 flex items-center justify-end">
        <button type="button" class="btn btn-text" :disabled="disabled"
                @click="$emit('wage:edit', this.wage.id)">
          <font-awesome-icon icon="fa-regular fa-pen-to-square" fixedWidth />
        </button>

        <button type="button" class="btn btn-text" :disabled="disabled"
                @click="$emit('wage:remove', this.wage.id)">
          <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
        </button>
      </div>
    </div>
  </div>
</template>