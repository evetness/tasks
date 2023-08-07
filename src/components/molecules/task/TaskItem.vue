<script>
import moment from 'moment/min/moment-with-locales'
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import { formatCurrency } from '@/utils'

export default {
  name: "TaskItem",
  props: ["task"],
  computed: {
    elapsed() { return moment.duration(this.task.elapsed).humanize() },
    ...mapState(useProjectStore, { project: "id" })
  },
  methods: {
    formatCurrency,
    moment
  },
  emits: ["task:edit", "task:remove"]
}
</script>

<template>
  <tr class="group hover:bg-brand/20">
    <td class="text-xs text-left pl-2">
      <div class="flex items-center gap-1">
        <font-awesome-icon v-if="task.completed" icon="fa-regular fa-check-circle" size="xs" />
        <font-awesome-icon v-else icon="fa-regular fa-hourglass-half" size="xs" />
        {{ task.name }}
      </div>
    </td>
    <td class="text-xs text-right">{{ this.moment(task.start).format("lll") }}</td>
    <td class="text-xs text-right">{{ this.moment(task.end).format("lll") }}</td>
    <td class="text-xs text-right text-brand">{{ elapsed }}</td>
    <td class="text-xs text-right text-brand tracking-thighter font-extrabold group-hover:text-sm pr-1">
      {{ formatCurrency(task.amount, task.currency) }}
    </td>
    <td class="text-right">
      <button type="button" class="btn btn-text" @click="$emit('task:edit', this.task.id)">
        <font-awesome-icon icon="fa-regular fa-pen-to-square" />
      </button>

      <button type="button" class="btn btn-text" @click="$emit('task:remove', this.task.id)">
        <font-awesome-icon icon="fa-regular fa-trash-can" />
      </button>
    </td>
  </tr>
</template>