<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue';

import { storeToRefs } from 'pinia';
import { ref, computed, inject, defineProps, defineEmits } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";

import { useProjectStore } from '@/stores/project'
import { useTaskStore } from "@/stores/task.js";

const axios = inject('axios');
const props = defineProps(['id', 'name', 'start', 'end', 'completed']);
const emits = defineEmits(['form:close']);

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const taskStore = useTaskStore();
const { updateTasks } = taskStore;

const form = ref({
  name: props.name || "",
  start: props.start || null,
  end: props.end || null,
  completed: props.completed || false,
  project_id: selected.value
});
const rules = computed(() => ({
  completed: { required, $autoDirty: true },
  name: { required, $autoDirty: true },
  start: { required, $autoDirty: true },
  end: { required, $autoDirty: true }
}));
const $externalResults = ref({});
const v$ = useVuelidate(rules, form, { $externalResults });

const submitForm = async () => {
  if (v$.$invalid === false) {
    let response = null
    if (props.id) {
      response = await axios.put(
        `/api/tasks/${props.id}`,
        {
          completed: form.value.completed,
          name: form.value.name,
          start: form.value.start,
          end: form.value.end
        }
      ).catch((error) => {
        if (error.response.status === 409) {
          const message = error.response.data.message;
          $externalResults.value = { start: [message], end: [message] };
        }
        return null;
      })
    } else {
      response = await axios.post(
        `/api/tasks`,
        {
          completed: form.value,
          name: form.value.name,
          start: form.value.start,
          end: form.value.end,
          project_id: selected.value
        }
      ).catch((error) => {
        if (error.response.status === 409) {
          const message = error.response.data.message;
          $externalResults.value = { start: [message], end: [message] };
        }
        return null;
      })
    }
    if (!response) return;

    const data = await response.data;
    updateTasks(data);
    emits('form:close');
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" class="text-brand">
    <div class="rounded-xl bg-brand/5 p-3 flex flex-col md:flex-row items-center gap-1 text-sm">

      <Input name="name" type="text" v-model="v$.name.$model" :autofocus="true" :errors="v$.name.$errors">
      <template #prefix>
        <font-awesome-icon icon="clipboard" class="ml-2" />
      </template>
      </Input>

      <div class="flex-auto self-stretch md:self-auto md:basis-32">
        <Input name="start" type="datetime-local" v-model="v$.start.$model" :errors="v$.start.$errors" class="py-[5px]">
        <template #prefix>
          <font-awesome-icon icon="calendar-day" class="ml-2" />
        </template>
        </Input>
      </div>

      <div class="flex-auto self-stretch md:self-auto md:basis-32">
        <Input name="end" type="datetime-local" v-model="v$.end.$model" :errors="v$.end.$errors" class="py-[5px]">
        <template #prefix>
          <font-awesome-icon icon="calendar-week" class="ml-2" />
        </template>
        </Input>
      </div>


      <div class="flex self-end md:items-center gap-1">
        <button type="submit" class="btn btn-text" :disabled="v$.$invalid">
          <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
          {{ props.id ? 'Edit' : 'Add' }}
        </button>
        <button type="button" class="btn btn-text" @click="emits('form:close')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
          Cancel
        </button>
      </div>

    </div>
  </form>

  <div class="text-2xs text-brand/70 text-left">
    {{ v$.$errors.map(error => error.$message).join(', ') || '&nbsp;' }}
  </div>
</template>