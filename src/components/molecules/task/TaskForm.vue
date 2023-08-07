<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";

import Input from '@/components/molecules/Input.vue';
import Checkbox from '@/components/molecules/Checkbox.vue';

export default {
  name: "TaskForm",
  components: { Input, Checkbox },
  props: ["id", "name", "start", "end", "completed"],
  setup() {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        name: this.name || "",
        start: this.start || null,
        end: this.end || null,
        completed: this.completed || false,
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
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = null
        if (this.id) {
          response = await this.axios.put(
            `/api/tasks/${this.id}`,
            {
              name: this.form.name,
              start: this.form.start,
              end: this.form.end
            }
          )
        } else {
          response = await this.axios.post(
            `/api/tasks`,
            {
              name: this.form.name,
              start: this.form.start,
              end: this.form.end,
              project_id: this.project
            }
          )
        }
        if (response.status !== 200) {
          return
        }
        const data = await response.data
        this.$emit('form:submitted', data)
      }
    }
  }
}
</script>

<template>
  <tr class="hover:bg-brand/10">
    <td>
      <div class="flex item-center">
        <div class="flex shrink">
          <Checkbox name="completed" :autofocus="true" />
        </div>
        <div class="flex-1">
          <Input name="name" type="text" v-model="form.name" form="task-form"/>
        </div>
      </div>
    </td>
    <td>
      <Input name="start" type="datetime-local" v-model="form.start" form="task-form"/>
    </td>
    <td>
      <Input name="end" type="datetime-local" v-model="form.end" form="task-form"/>
    </td>
    <td></td>
    <td></td>
    <td>
      <form id="task-form" @submit.prevent="submitForm" class="flex items-center justify-end">
        <button type="submit" class="btn btn-text">
          <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
        </button>
        <button type="button" class="btn btn-text" @click="$emit('form:cancel')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
        </button>
      </form>
    </td>
  </tr>
</template>