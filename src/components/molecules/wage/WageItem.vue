<script>
import moment from 'moment/min/moment-with-locales'
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import { formatCurrency } from "@/utils.js";

export default {
  name: "WageItem",
  props: ["wage"],
  computed: {
    ...mapState(useProjectStore, { project: "id" })
  },
  methods: {
    formatCurrency,
    moment
  },
  emits: ["wage:edit", "wage:remove"]
}
</script>

<template>
  <tr class="group hover:bg-brand/20">
    <td class="text-xs text-left pl-2">{{ this.moment(wage.date).format("LL") }}</td>
    <td class="text-xs text-right">{{ this.formatCurrency(wage.amount, wage.currency) }}</td>
    <td>
      <div class="flex items-center justify-end">
        <button type="button" class="btn btn-text" @click="$emit('wage:edit', wage.id)">
          <font-awesome-icon icon="fa-regular fa-pen-to-square" fixedWidth />
        </button>
  
        <button type="button" class="btn btn-text" @click="$emit('wage:remove', wage.id)">
          <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
        </button>
      </div>
    </td>
  </tr>
</template>