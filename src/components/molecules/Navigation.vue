<script setup>
import { useProjectStore } from '@/stores/project'

</script>

<template>
  <ul class="flex flex-wrap text-sm font-medium text-center border-b border-brand/60 space-x-1 -mt-3 -ml-3 mb-3">
    
    <li>
      <button type="button" class="inline-block p-4 uppercase" :class="{
        'text-brand/80 bg-brand/20': page === 'tasks',
        'text-brand/80 hover:bg-brand/10': page !== 'tasks'
      }" @click="page = 'tasks'">
        Tasks
      </button>
    </li>
    
    <li>
      <button type="button" class="inline-block p-4 uppercase" :class="{
        'text-brand/80 bg-brand/20': page === 'wages',
        'text-brand/80 hover:bg-brand/10': page !== 'wages'
      }" @click="page = 'wages'">
        Wages
      </button>
    </li>
    
    <li class="grow"></li>

    <li class="self-center">
      <Input label="Search" name="search" type="search" v-model="search" :disabled="!selected"/>
    </li>
  </ul>
</template>