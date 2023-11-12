<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { computed, defineProps, defineEmits } from 'vue';

import { storeToRefs } from 'pinia';
import { useGlobalStore } from "@/stores/global.js";
import { useProjectStore } from "@/stores/project.js";

const globalStore = useGlobalStore();
const projectStore = useProjectStore();

const emits = defineEmits(['project:edit', 'project:remove', 'project:salary', 'project:pay']);
const props = defineProps(['project']);
const { inAction, isSalaryLoading } = storeToRefs(globalStore);
const { selected, unpaid, elapsed, amount } = storeToRefs(projectStore);
const { selectProject } = projectStore;

const isSelected = computed(() => props.project.id === selected.value);
const canPaySalary = computed(() => isSelected.value && !isSalaryLoading.value && unpaid.value !== '-');
</script>

<template>
  <div class="group relative w-56 sm:w-72">
    <div class="flex gap-0.5 text-brand text-sm text-center">

      <button v-if="!isSelected" type="button" @click="selectProject(project.id)" :disabled="inAction"
        class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/10" :class="{
          'group-hover:bg-brand/30 group-focus-within:bg-brand/30': !inAction
        }">
        <font-awesome-icon icon="clipboard" />
      </button>

      <button v-if="isSelected" type="button" @click="emits('project:edit', project.id)" :disabled="inAction"
        class="h-7 w-11 sm:w-12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/50" :class="{
          'hover:bg-brand/60 focus:bg-brand/60': !inAction
        }">
        <font-awesome-icon icon="pen-to-square" />
      </button>

      <button v-if="isSelected" type="button" @click="emits('project:remove', project.id)" :disabled="inAction"
        class="h-7 w-11 sm:w-12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/50" :class="{
          'hover:bg-brand/60 focus:bg-brand/60': !inAction
        }">
        <font-awesome-icon icon="trash-can" />
      </button>

      <button v-if="isSelected" type="button" @click="emits('project:salary', project.id)" :disabled="inAction"
        class="h-7 w-11 sm:w-12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/50" :class="{
          'hover:bg-brand/60 focus:bg-brand/60': !inAction
        }">
        <font-awesome-icon icon="file-invoice-dollar" />
      </button>

      <button v-if="canPaySalary" type="button" @click="emits('project:pay', project.id)" :disabled="inAction"
        class="h-7 w-11 sm:w-12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/50" :class="{
          'hover:bg-brand/60 focus:bg-brand/60': !inAction
        }">
        <font-awesome-icon icon="dollar" />
      </button>

    </div>

    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent" :class="{
      'bg-brand/10': !isSelected && inAction,
      'bg-brand/10 group-hover:bg-brand/20 group-focus-within:bg-brand/20': !isSelected && !inAction,
      'bg-brand/40': isSelected
    }">
      <button type="button" @click="selectProject(project.id)" :disabled="isSelected || inAction" class="flex-auto p-4">

        <div class="flex items-center justify-between gap-1 sm:text-xl break-all text-brand" :class="{
          'pb-14 sm:pb-16': !isSelected,
          'font-bold': isSelected
        }">
          {{ project.name }}
        </div>

        <div v-if="isSelected" class="leading-none text-right ml-auto mt-1">
          <div v-if="isSalaryLoading" class="animate-pulse">
            <div class="text-sm sm:text-lg w-32 bg-brand/30 ml-auto rounded">&nbsp;</div>
            <div class="text-2xs sm:text-xs w-24 bg-brand/20 ml-auto rounded">&nbsp;</div>
            <div class="text-2xs sm:text-xs w-10 bg-brand/20 ml-auto rounded">&nbsp;</div>
          </div>
          <div v-else class="leading-none">
            <div class="text-brand text-sm sm:text-lg font-bold">{{ unpaid }}</div>
            <div class="text-brand/80 text-2xs sm:text-xs font-medium">{{ amount }}/h</div>
            <div class="text-brand/80 text-2xs sm:text-xs font-medium">{{ elapsed }}</div>
          </div>
        </div>

      </button>
    </div>
  </div>
</template>