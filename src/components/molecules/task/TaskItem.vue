<script>
import moment from 'moment/min/moment-with-locales'

import { formatCurrency } from '@/utils'
import { FontAwesomeIcon, FontAwesomeLayers } from "@fortawesome/vue-fontawesome";

export default {
  name: "TaskItem",
  components: { FontAwesomeIcon, FontAwesomeLayers },
  props: ["task", "disabled"],
  computed: {
    elapsed() { return moment.duration(this.task.elapsed).humanize() }
  },
  methods: {
    formatCurrency,
    moment,
    time() {
      const start = this.moment(this.task.start);
      const end = this.moment(this.task.end);
      if (start.format("YYYY-MM-DD") === end.format("YYYY-MM-DD")) {
        return `${start.format("YYYY. MM. DD. HH:mm")} - ${end.format("HH:mm")}`;
      }
      return `${start.format("YYYY. MM. DD. HH:mm")} - ${end.format("DD. HH:mm")}`;
    }
  },
  emits: ["task:edit", "task:remove"]
}
</script>

<template>
  <div class="group relative rounded-xl bg-brand/5 hover:bg-brand/10 text-brand/80">
    <button type="button" class="w-full p-3 flex items-center justify-between gap-2">
      <div class="text-left">
        <div class="flex items-center gap-2 text-xs">
          <font-awesome-icon icon="calendar-day" />
          {{ this.time() }}
          <div class="font-italic text-2xs">(kb. {{ elapsed }})</div>
        </div>
        <div class="font-medium tracking-wider text-brand/90">
          {{ task.name }}
        </div>
      </div>

      <div class="flex justify-between gap-2">
        <div class="text-right font-extrabold tracking-thighter">
          {{ formatCurrency(task.amount, task.currency) }}
        </div>
      </div>
    </button>
    <font-awesome-layers class="absolute top-0 left-0 -translate-x-1/3 -translate-y-1/3">
      <font-awesome-icon icon="circle" class="text-stone-900" />
      <font-awesome-icon v-if="task.completed" icon="check-circle" class="text-brand/80" transform="shrink-5" />
      <font-awesome-icon v-else icon="circle-half-stroke" class="text-brand/80" transform="shrink-5" />
    </font-awesome-layers>
  </div>
  <!-- <div class="group hover:bg-brand/20 pl-1">
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
  </div> -->
</template>