<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useGlobalStore } from '@/stores/global';
import { useProjectStore } from '@/stores/project';

const emits = defineEmits(['form:add'])

const globalStore = useGlobalStore();
const { inAction } = storeToRefs(globalStore);

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const disabled = computed(() => inAction.value || !selected.value);
</script>

<template>
  <button type="button" class="relative rounded-xl border-2 border-dashed" :class="{
    'border-brand/60 hover:bg-brand/10 focus:bg-brand/10': !disabled,
    'border-brand/40': disabled
  }" @click="emits('form:add')" :disabled="disabled">

    <div class="flex-auto p-4" :class="{
      'text-brand': !disabled,
      'text-brand/80': disabled
    }">
      <div class="flex items-center justify-center gap-1">
        <font-awesome-icon icon="plus" />
      </div>
    </div>
  </button>
</template>