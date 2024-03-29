<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue';

import { storeToRefs } from 'pinia';
import { ref, computed, inject } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, helpers } from "@vuelidate/validators";

import { useProjectStore } from '@/stores/project'
import { useTaskStore } from "@/stores/task.js";
import moment from 'moment';
import { useToastStore } from '@/stores/toast';

const axios = inject('axios');
const props = defineProps(['id', 'name', 'start', 'end']);
const emits = defineEmits(['form:close']);

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const taskStore = useTaskStore();
const { updateTasks } = taskStore;

const toastStore = useToastStore();
const { addToast } = toastStore;

const form = ref({
  name: props.name || "",
  start: props.start || moment().format().slice(0, 16),
  end: props.end || null,
  project_id: selected.value
});

const minValue = (value) => {
  return !helpers.req(value) || value >= form.value.start
};

const rules = computed(() => ({
  name: { $autoDirty: true },
  start: { required, $autoDirty: true },
  end: { minValue, $autoDirty: true }
}));
const $externalResults = ref({});
const v$ = useVuelidate(rules, form, { $externalResults });

const submitForm = async () => {
  if (v$.value.$invalid === false) {
    let response = null
    if (props.id) {
      response = await axios.put(
        `/api/tasks/${props.id}`,
        {
          name: form.value.name,
          start: form.value.start,
          end: form.value.end || null
        }
      ).catch((error) => {
        addToast('exclamation-triangle', 'Task modification failed!', true, 5000);
        return null;
      })
    } else {
      response = await axios.post(
        `/api/tasks`,
        {
          name: form.value.name,
          start: form.value.start,
          end: form.value.end || null,
          project_id: selected.value
        }
      ).catch((error) => {
        addToast('exclamation-triangle', 'Task creation failed!', true, 5000);
        return null;
      })
    }
    if (!response) return;

    const data = await response.data;
    updateTasks(data);
    addToast('check-circle', 'Task successfully saved!', false, 2500);
    emits('form:close');
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" class="text-brand text-sm">
    <div class="rounded-xl bg-brand/5 p-3 flex flex-wrap lg:flex-nowrap items-center gap-1">

      <Input name="name" type="text" autofocus="true" v-model="v$.name.$model" :errors="v$.name.$errors">
      <template #prefix>
        <font-awesome-icon icon="clipboard" class="ml-2" />
      </template>
      </Input>

      <div class="flex-auto self-stretch basis-52 sm:basis-auto md:self-center min-w-[13rem] sm:grow-0">
        <Input name="start" type="datetime-local" v-model="v$.start.$model" :errors="v$.start.$errors"
          class="flex-auto py-[5px]">
        <template #prefix>
          <font-awesome-icon icon="calendar-day" class="ml-2 py-2" />
        </template>
        </Input>
      </div>

      <div class="flex-auto self-stretch basis-52 sm:basis-auto md:self-center min-w-[13rem] sm:grow-0">
        <Input name="end" type="datetime-local" v-model="v$.end.$model" :errors="v$.end.$errors"
          class="flex-auto py-[5px]" :min="v$.start.$model">
        <template #prefix>
          <font-awesome-icon icon="calendar-week" class="ml-2 py-2" />
        </template>
        </Input>
      </div>

      <div class="flex self-end md:items-center gap-1 ml-auto">
        <button type="submit" class="btn btn-text uppercase text-xs" :disabled="v$.$invalid">
          <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
          {{ props.id ? 'Edit' : 'Add' }}
        </button>
        <button type="button" class="btn btn-text uppercase text-xs" @click="emits('form:close')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
          Cancel
        </button>
      </div>

    </div>
  </form>
</template>