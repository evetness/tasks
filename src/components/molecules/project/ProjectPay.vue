<script setup>
import { ref, computed, inject } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";

import { storeToRefs } from 'pinia';
import { useProjectStore } from "@/stores/project.js";
import { useTaskStore } from "@/stores/task.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";
import { useToastStore } from '@/stores/toast';

const emits = defineEmits(['form:close']);
const axios = inject('axios');

const projectStore = useProjectStore();
const { project } = storeToRefs(projectStore);
const { getCurrentWage, getUnpaidSalary } = projectStore;

const taskStore = useTaskStore();
const { getTasks } = taskStore;

const toastStore = useToastStore();
const { addToast }= toastStore;


const form = ref({
  date: null
});
const rules = computed(() => ({
  date: { required, $autodirty: true }
}));
const v$ = useVuelidate(rules, form);

const submitForm = async () => {
  if (v$.value.$invalid === false) {
    let response = await axios.put(
      `/api/tasks/complete`,
      {
        date: form.value.date,
        project_id: project.value.id,
      }
    ).catch((error) => {
      addToast('exclamation-triangle', 'Payment failed!', true, 5000);
      return null;
    })
    if (!response) return

    getCurrentWage();
    getUnpaidSalary();
    getTasks();
    addToast('check-circle', 'Payment successful!', true, 2500);
    emits('form:close')
  }
}
</script>

<template>
  <div class="group relative w-64 sm:w-72">
    <div class="text-brand text-sm text-center">
      <div class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="dollar" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="text-sm">
            <Input type="date" v-model="v$.date.$model" :autofocus="true" :errors="v$.date.$errors"
              class="flex-auto py-[5px]">
            <template #prefix>
              <font-awesome-icon icon="calendar" class="ml-2 py-2" />
            </template>
            </Input>
          </div>
          <div class="text-2xs text-brand/70 text-left">
            {{ v$.$errors.map(error => error.$message).join(', ') || '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end mt-1.5">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="dollar" fixedWidth />
              Pay
            </button>
            <button type="button" class="btn btn-text text-xs uppercase" @click="emits('form:close')">
              <font-awesome-icon icon="xmark" fixedWidth />
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
