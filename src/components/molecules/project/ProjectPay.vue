<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";

import {mapActions, mapState} from "pinia";
import {useProjectStore} from "@/stores/project.js";

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";
import {useTaskStore} from "@/stores/task.js";

export default {
  name: "ProjectPay",
  components: {FontAwesomeIcon, Input},
  setup() {
    return {v$: useVuelidate()}
  },
  data() {
    return {
      form: {
        date: null,
        project_id: this.project
      },
      vuelidateExternalResults: {
        form: {
          date: [],
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
        date: {required, $autoDirty: true},
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = await this.axios.put(
            `/api/tasks/complete`,
            {
              date: this.form.date,
              project_id: this.selected
            }
        )
        if (!response) return

        // TODO update tasks
        await this.getCurrentWage();
        await this.getUnpaidSalary();
        await this.getTasks();
        this.$emit('form:close')
      }
    },
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"]),
    ...mapActions(useTaskStore, ["getTasks"])
  },
  emits: ["form:close"]
}
</script>

<template>
  <form @submit.prevent="submitForm" class="flex items-center text-brand/80 text-sm hover:bg-brand/20 focus:bg-brand/20 border-x border-transparent">
    <Input label="Date" name="date" type="date" v-model="form.date" :autofocus="true" :errors="v$.form.date.$errors"/>
    <button type="submit" class="btn btn-text" :disabled="v$.$invalid" title="Submit">
      <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
    </button>
    <button type="button" class="btn btn-text" @click="$emit('form:close')" title="Cancel">
      <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
    </button>
  </form>
  <div v-for="error in errors" class="text-2xs text-brand/75 px-3">{{error}}</div>
</template>
