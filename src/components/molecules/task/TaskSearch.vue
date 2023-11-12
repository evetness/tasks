<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue';

import { storeToRefs } from 'pinia';
import { ref, computed } from 'vue';
import useVuelidate from '@vuelidate/core';

import { useGlobalStore } from '@/stores/global';


const globalStore = useGlobalStore();
const { search } = storeToRefs(globalStore);

const form = ref({
  search: search.value || ""
});
const rules = computed(() => ({
  search: { $autoDirty: true }
}));
const $externalResults = ref({});
const v$ = useVuelidate(rules, form, { $externalResults });

</script>

<template>
  <form class="text-brand text-sm">
    <div class="flex items-center gap-1">
      <Input name="search" type="text" v-model="search" :autofocus="false">
      <template #prefix>
        <font-awesome-icon icon="search" class="ml-2" />
      </template>
      </Input>
    </div>
    <small class="text-brand/80 2text-xs">Search for tasks in name, or type in <b>paid</b> or <b>inprogress</b> for query
      task status.</small>
  </form>
</template>