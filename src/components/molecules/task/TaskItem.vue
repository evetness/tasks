<script setup>
import moment from 'moment/min/moment-with-locales';
import { formatCurrency } from '@/utils';

import { FontAwesomeIcon, FontAwesomeLayers } from "@fortawesome/vue-fontawesome";

import { computed, defineProps, defineEmits } from 'vue';
import { storeToRefs } from 'pinia';
import { useGlobalStore } from '@/stores/global';

const globalStore = useGlobalStore();
const { inAction } = storeToRefs(globalStore);

const props = defineProps(['task']);
const emits = defineEmits(['task:edit', 'task:remove', 'task:complete']);

const time = computed(() => {
  const start = moment(props.task.start);

  if (props.task.end) {
    const end = moment(props.task.end);
    if (start.format("YYYY-MM-DD") === end.format("YYYY-MM-DD")) {
      return `${start.format("YYYY. MM. DD. HH:mm")} - ${end.format("HH:mm")}`;
    }
    return `${start.format("YYYY. MM. DD. HH:mm")} - ${end.format("DD. HH:mm")}`;
  }
  return `${start.format("YYYY. MM. DD. HH:mm")}`;
})
</script>

<template>
  <div class="group/task relative text-brand/80">
    <div class="w-full p-3.5 rounded-xl bg-brand/5" :class="{ 'hover:bg-brand/10 focus:bg-brand/10': !inAction }">
      <div class="flex items-center justify-between gap-2">
        <div class="text-left">
          <div class="flex items-center gap-2 text-xs">
            <font-awesome-icon icon="calendar-day" />
            <div>{{ time }} <i>({{ task.elapsed }})</i></div>
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
      </div>
    </div>

    <button type="button" class="group/complete absolute top-0 left-0 -translate-x-1/3 -translate-y-1/4 px-1"
      @click="emits('task:complete')" :disabled="inAction">
      <span class="sr-only">
        {{ task.completed ? 'Incomplete' : 'Complete' }}
      </span>
      <font-awesome-layers class="text-xl">
        <font-awesome-icon icon="circle" class="text-stone-900" />
        <font-awesome-icon v-if="task.completed" icon="check-circle"
          class="text-brand/80 enabled:group-hover/complete:text-brand" transform="shrink-5" />
        <font-awesome-icon v-else icon="circle-half-stroke" class="text-brand/80 enabled:group-hover/complete:text-brand"
          transform="shrink-5" />
      </font-awesome-layers>
    </button>

    <button v-if="!inAction" type="button" class="group/edit absolute -top-1.5 right-5 px-1" @click="emits('task:edit')">
      <span class="sr-only">Edit</span>
      <font-awesome-layers class="text-xl">
        <font-awesome-icon icon="circle" class="text-stone-900" />
        <font-awesome-icon icon="circle" class="text-brand/80 group-hover/edit:text-brand" transform="shrink-5" />
        <font-awesome-icon icon="pen" class="text-stone-900" transform="shrink-10" />
      </font-awesome-layers>
    </button>

    <button v-if="!inAction" type="button" class="group/remove absolute -top-1.5 -right-2.5 px-1"
      @click="emits('task:remove')">
      <span class="sr-only">Delete</span>
      <font-awesome-layers class="text-xl">
        <font-awesome-icon icon="circle" class="text-stone-900" />
        <font-awesome-icon icon="circle" class="text-brand/80 group-hover/remove:text-brand" transform="shrink-5" />
        <font-awesome-icon icon="trash" class="text-stone-900" transform="shrink-10" />
      </font-awesome-layers>
    </button>

  </div>
</template>