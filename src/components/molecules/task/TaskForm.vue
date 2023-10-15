<script>
import {mapActions, mapState} from 'pinia'
import {useProjectStore} from '@/stores/project'

import useVuelidate from '@vuelidate/core';
import {required} from "@vuelidate/validators";

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

import Input from '@/components/atoms/Input.vue';
import Checkbox from '@/components/atoms/Checkbox.vue';
import {useTaskStore} from "@/stores/task.js";

export default {
  name: "TaskForm",
  components: {FontAwesomeIcon, Input, Checkbox},
  props: ["id", "name", "start", "end", "completed"],
  setup() {
    return {v$: useVuelidate()}
  },
  data() {
    return {
      form: {
        name: this.name || "",
        start: this.start || null,
        end: this.end || null,
        completed: this.completed || false,
        project_id: this.selected
      },
      vuelidateExternalResults: {
        form: {
          start: [],
          end: [],
        }
      },
      errors: new Set()
    }
  },
  computed: {
    ...mapState(useProjectStore, ["selected"])
  },
  validations() {
    return {
      form: {
        completed: {required, $autoDirty: true},
        name: {required, $autoDirty: true},
        start: {required, $autoDirty: true},
        end: {required, $autoDirty: true}
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
                completed: this.form.completed,
                name: this.form.name,
                start: this.form.start,
                end: this.form.end
              }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, {
                form: {
                  start: [error.response.data.message],
                  end: [error.response.data.message]
                }
              })
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        } else {
          response = await this.axios.post(
              `/api/tasks`,
              {
                completed: this.form.completed,
                name: this.form.name,
                start: this.form.start,
                end: this.form.end,
                project_id: this.selected
              }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, {
                form: {
                  start: [error.response.data.message],
                  end: [error.response.data.message]
                }
              })
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        }
        if (!response) return;

        const data = await response.data;
        this.updateTasks(data);
        this.$emit('form:close');
      }
    },
    ...mapActions(useTaskStore, ["updateTasks"]),
  },
  emits: ["form:close"]
}
</script>

<template>
  <div class="overflow-y-scroll">
    <div class="flex items-center text-xs">

      <div class="grow flex items-stretch self-stretch">
        <Checkbox name="completed" v-model="form.completed" :errors="v$.form.completed.$errors"/>
        <div class="flex-1 [&>*]:h-full">
          <Input name="name" type="text" :autofocus="true" v-model="form.name" form="task-form"
                 :errors="v$.form.name.$errors"/>
        </div>
      </div>

      <div class="flex items-stretch">
        <Input name="start" type="datetime-local" v-model="form.start" form="task-form"
               :errors="v$.form.start.$errors"/>
        <Input name="end" type="datetime-local" v-model="form.end" form="task-form" :errors="v$.form.end.$errors"/>
      </div>

      <form id="task-form" @submit.prevent="submitForm" class="flex items-center justify-end">
        <button type="submit" class="btn btn-text" :disabled="v$.$invalid">
          <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth/>
        </button>
        <button type="button" class="btn btn-text" @click="$emit('form:close')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth/>
        </button>
      </form>

    </div>
  </div>

  <div v-for="error in errors" class="text-2xs text-brand/75 px-3">
    {{ error }}
  </div>
</template>