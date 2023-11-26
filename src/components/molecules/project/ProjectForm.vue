<script setup>
import { ref, computed, inject } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, maxLength } from "@vuelidate/validators";

import { storeToRefs } from 'pinia';
import { useProjectStore } from "@/stores/project.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";
import { useToastStore } from '@/stores/toast';

const axios = inject('axios');
const props = defineProps(['isEdit']);
const emits = defineEmits(['form:close']);

const projectStore = useProjectStore();
const { project } = storeToRefs(projectStore);

const toastStore = useToastStore();
const { addToast }= toastStore;

const form = ref({
  name: props.isEdit ? project.value.name : "",
});
const rules = computed(() => ({
  name: { required, maxLength: maxLength(20), $autodirty: true }
}));
const $externalResults = ref({});
const v$ = useVuelidate(rules, form, { $externalResults });

const submitForm = async () => {
  if (v$.value.$invalid === false) {
    let response = null;
    if (props.isEdit) {
      response = await axios.put(
        `/api/projects/${project.value.id}`,
        { name: form.value.name }
      ).catch((error) => {
        if (error.response.status === 409) {
          $externalResults.value = { name: [error.response.data.message] };
        }
        addToast('exclamation-triangle', 'Project modification failed!', true, 5000);
        return null;
      })
    } else {
      response = await axios.post(
        `/api/projects`,
        { name: form.value.name }
      ).catch((error) => {
        if (error.response.status === 409) {
          $externalResults.value = { name: [error.response.data.message] };
        }
        addToast('exclamation-triangle', 'Project creation failed!', true, 5000);
        return null;
      })
    }
    if (!response) return

    const result = await response.data
    projectStore.updateProjects(result)
    addToast('check-circle', 'Project successfully saved!', true, 2500);
    emits('form:close')
  }
}
</script>

<template>
  <div class="group relative w-64 sm:w-72">
    <div class="text-brand text-sm text-center">
      <div class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="plus" v-if="!isEdit" />
        <font-awesome-icon icon="pen-to-square" v-if="isEdit" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="text-sm">
            <Input name="name" maxlength="20" v-model="v$.name.$model" :autofocus="true" :errors="v$.name.$errors">
            <template #prefix>
              <font-awesome-icon icon="clipboard" class="ml-2" />
            </template>
            </Input>
          </div>
          <div class="text-2xs text-brand/70 text-left">
            {{ v$.$errors.map(error => error.$message).join(', ') || '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end mt-2">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
              {{ isEdit ? 'Edit' : 'Add' }}
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