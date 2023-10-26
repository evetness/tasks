<script>
import useVuelidate from '@vuelidate/core';
import { required, decimal } from "@vuelidate/validators";

import { mapActions, mapState } from "pinia";
import { useProjectStore } from "@/stores/project.js";
import { useTaskStore } from "@/stores/task.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Input from "@/components/atoms/Input.vue";

export default {
  name: "ProjectWage",
  components: { FontAwesomeIcon, Input },
  computed: {
    ...mapState(useProjectStore, ["selected", "wage"])
  },
  setup() {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        date: this.wage ? this.wage.date : null,
        amount: this.wage ? this.wage.amount : 0,
        currency: this.wage ? this.wage.currency : ""
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
        amount: { required, decimal, $autoDirty: true },
        currency: { required, $autoDirty: true }
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = await this.axios.put(
          `/api/projects/${this.selected}/wage`,
          {
            date: this.form.date,
            amount: this.form.amount,
            currency: this.form.currency
          }
        )
        if (!response) return

        this.getCurrentWage();
        this.getUnpaidSalary();
        this.getTasks();
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
        <font-awesome-icon icon="file-invoice-dollar" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="space-y-1 text-xs">
            <Input name="date" type="date" v-model="form.date" :autofocus="true" :errors="v$.form.date.$errors">
            <template #prefix>
              <font-awesome-icon icon="calendar" class="ml-2" />
            </template>
            </Input>
            <div class="flex items-center gap-1">
              <Input name="amount" type="number" v-model="form.amount" min="0" :errors="v$.form.amount.$errors">
              <template #prefix>
                <font-awesome-icon icon="wallet" class="ml-2" />
              </template>
              </Input>
              <Input name="currency" type="text" v-model="form.currency" maxlength="3" :errors="v$.form.currency.$errors">
              <template #prefix>
                <font-awesome-icon icon="dollar" class="ml-2" />
              </template>
              </Input>
            </div>
          </div>
          <div class="text-2xs text-brand/70 text-left">
            {{ errors.size !== 0 ? Array.from(errors).join(', ') : '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
              Save
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
