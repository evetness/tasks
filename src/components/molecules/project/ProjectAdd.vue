<script setup>
import { storeToRefs } from 'pinia';
import { useGlobalStore } from '@/stores/global';

const emits = defineEmits(['form:add'])
const globalStore = useGlobalStore();
const { inAction } = storeToRefs(globalStore);
</script>

<template>
  <button type="button" class="group relative w-56 sm:w-72" @click="emits('form:add')" :disabled="inAction">
    <div class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-dashed" :class="{
      'border-brand/60 group-hover:bg-brand/20 group-focus:bg-brand/20': !inAction,
      'border-brand/40': inAction
    }">
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-dashed" :class="{
      'border-brand/60 group-hover:bg-brand/20 group-focus:bg-brand/20': !inAction,
      'border-brand/40': inAction
    }">
      <div class="flex-auto p-4" :class="{
        'text-brand': !inAction,
        'text-brand/80': inAction
      }">
        <div class="flex items-center justify-center gap-1 py-7 sm:py-8 sm:text-xl break-all">
          <font-awesome-icon icon="plus" />
          &nbsp;
        </div>
      </div>
    </div>
  </button>
</template>