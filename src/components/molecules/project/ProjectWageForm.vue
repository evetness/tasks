<script setup>
import { ref, computed, inject } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, decimal } from "@vuelidate/validators";

import { useProjectStore } from "@/stores/project.js";
import { useTaskStore } from "@/stores/task.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";
import { storeToRefs } from 'pinia';

const axios = inject('axios');
const emits = defineEmits(['form:close', 'form:remove']);

const projectStore = useProjectStore();
const { project, wage } = storeToRefs(projectStore);
const { getCurrentWage, getUnpaidSalary } = projectStore;
const taskStore = useTaskStore();
const { getTasks } = taskStore;

const form = ref({
  date: wage.value ? wage.value.date : null,
  amount: wage.value ? wage.value.amount : 0,
  currency: wage.value ? wage.value.currency : ""
});
const rules = computed(() => ({
  date: { required, $autoDirty: true },
  amount: { required, decimal, $autoDirty: true },
  currency: { required, $autoDirty: true }
}));
const $externalResults = ref({});
const v$ = useVuelidate(rules, form, { $externalResults });

const submitForm = async () => {
  if (v$.value.$invalid === false) {
    let response = await axios.put(
      `/api/projects/${project.value.id}/wage`,
      {
        date: form.value.date,
        amount: form.value.amount,
        currency: form.value.currency
      }
    )
    if (!response) return;

    getCurrentWage();
    getUnpaidSalary();
    getTasks();
    emits('form:close');
  }
}
</script>

<template>
  <div class="group relative w-64 sm:w-72">
    <div class="flex gap-0.5 text-brand text-sm text-center">
      <div class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="file-invoice-dollar" />
      </div>
      <button v-if="wage" type="button" @click="emits('form:remove', true)"
        class="h-7 w-11 sm:w-12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20 hover:bg-brand/40 focus:bg-brand/40">
        <font-awesome-icon icon="trash-can" />
      </button>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="space-y-1 text-xs">
            <Input name="date" type="date" v-model="v$.date.$model" :autofocus="true" :errors="v$.date.$errors"
              class="flex-auto py-[5px]">
            <template #prefix>
              <font-awesome-icon icon="calendar" class="ml-2 py-2" />
            </template>
            </Input>
            <div class="flex items-center gap-1">
              <Input name="amount" type="number" v-model="v$.amount.$model" min="0" :errors="v$.amount.$errors">
              <template #prefix>
                <font-awesome-icon icon="wallet" class="ml-2" />
              </template>
              </Input>
              <Input name="currency" type="text" v-model="v$.currency.$model" maxlength="3" :errors="v$.currency.$errors">
              <template #prefix>
                <font-awesome-icon icon="dollar" class="ml-2" />
              </template>
              </Input>
            </div>
          </div>
          <div class="text-2xs text-brand/70 text-left">
            {{ v$.$errors.map(error => error.$message).join(', ') || '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
              Save
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
