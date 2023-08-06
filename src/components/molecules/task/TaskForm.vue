<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import useVuelidate from '@vuelidate/core';
import { required, decimal } from "@vuelidate/validators";

import Input from '@/components/molecules/Input.vue';

export default {
  name: "TaskForm",
  components: { Input },
  props: ["id", "name", "start", "end"],
  setup() {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        name: this.date || "",
        start: this.start || null,
        end: this.end || null,
        project_id: this.project
      }
    }
  },
  computed: {
    ...mapState(useProjectStore, {
      project: "id"
    })
  },
  validators() {
    return {
      form: {
        name: { required, $autoDirty: true },
        start: { required, $autoDirty: true },
        end: { required, $autoDirty: true }
      }
    }
  },
}
</script>

<template>
  <tr>
    <td class="text-xs text-left py-1 pl-1 flex items-center gap-1">
      <Input name="name" type="text" v-model="form.name" />
    </td>
    <td class="text-xs text-right">
      <Input name="start" type="date" v-model="form.start" />
    </td>
    <td class="text-xs text-right">
      <Input name="end" type="date" v-model="form.end" />
    </td>
    <td></td>
    <td></td>
    <td class="flex items-center">
      <button type="submit" class="btn hover:bg-brand/30">
        <font-awesome-icon icon="fa-regular fa-floppy-disk" />
      </button>
      <button type="button" class="btn hover:bg-brand/30" @click="$emit('form:cancel')">
        <font-awesome-icon icon="fa-solid fa-xmark" />
      </button>
    </td>
  </tr>
</template>