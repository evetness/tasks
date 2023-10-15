<script>
import moment from 'moment/min/moment-with-locales'

import { formatCurrency } from '@/utils'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default {
  name: "TaskItem",
  components: {FontAwesomeIcon},
  props: ["task", "disabled"],
  computed: {
    elapsed() { return moment.duration(this.task.elapsed).humanize() }
  },
  methods: {
    formatCurrency,
    moment
  },
  emits: ["task:edit", "task:remove"]
}
</script>

<template>
  <div class="group hover:bg-brand/20 pl-1">
    <div class="grid grid-cols-12 items-center gap-1 text-xs">
      <div class="col-span-4 flex items-center gap-1">
        <font-awesome-icon v-if="task.completed" icon="fa-regular fa-check-circle" size="xs" />
        <font-awesome-icon v-else icon="fa-regular fa-hourglass-half" size="xs" />
        {{ task.name }}
      </div>

      <div class="col-span-4 text-right">
        <div>{{ this.moment(task.start).format("lll") }} - {{ this.moment(task.end).format("lll") }}</div>
        <div class="font-bold">{{ elapsed }}</div>
      </div>

      <div class="col-span-2 text-right tracking-thighter" :class="{
        'group-hover:font-extrabold group-hover:text-sm transition-all': task.amount
      }">
        {{ formatCurrency(task.amount, task.currency) }}
      </div>

      <div class="col-span-2 flex items-center justify-end">
        <button type="button" class="btn btn-text" :disabled="disabled"
                @click="$emit('task:edit', this.task.id)">
          <font-awesome-icon icon="fa-regular fa-pen-to-square" fixedWidth />
        </button>

        <button type="button" class="btn btn-text" :disabled="disabled"
                @click="$emit('task:remove', this.task.id)">
          <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
        </button>
      </div>
    </div>
  </div>
</template>