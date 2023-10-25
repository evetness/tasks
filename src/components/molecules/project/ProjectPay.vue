<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";

import { mapActions, mapState } from "pinia";
import { useProjectStore } from "@/stores/project.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";
import { useTaskStore } from "@/stores/task.js";

export default {
  name: "ProjectPay",
  props: ["id"],
  components: { FontAwesomeIcon, Input },
  setup() {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        date: null,
        project_id: this.id
      },
      vuelidateExternalResults: {
        form: {
          date: [],
        }
      },
      errors: new Set()
    }
  },
  validations() {
    return {
      form: {
        date: { required, $autoDirty: true },
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
            project_id: this.id
          }
        )
        if (!response) return

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
  <div class="group relative w-64 sm:w-72">
    <div class="text-brand text-sm text-center">
      <div class="h-6 w-5/12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="dollar" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <Input label="Date" name="date" type="date" v-model="form.date" :autofocus="true"
            :errors="v$.form.date.$errors" />
          <div class="text-2xs text-brand/70 text-left">
            {{ errors.size !== 0 ? Array.from(errors).join(', ') : '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end mt-1">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="dollar" fixedWidth />
              Pay
            </button>
            <button type="button" class="btn btn-text text-xs uppercase" @click="$emit('form:close')">
              <font-awesome-icon icon="xmark" fixedWidth />
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
