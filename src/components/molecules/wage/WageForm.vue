<script>
import {mapState, mapActions} from 'pinia'
import {useProjectStore} from '@/stores/project'
import {useWageStore} from "@/stores/wage.js";

import useVuelidate from '@vuelidate/core';
import {required, decimal} from "@vuelidate/validators";

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue'

export default {
  name: "WageForm",
  components: {FontAwesomeIcon, Input},
  props: ["id", "date", "amount", "currency"],
  setup() {
    return {v$: useVuelidate()}
  },
  data() {
    return {
      form: {
        date: this.date || null,
        amount: this.amount || 0,
        currency: this.currency || ""
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
        amount: {required, decimal, $autoDirty: true},
        currency: {required, $autoDirty: true}
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = null
        if (this.id) {
          response = await this.axios.put(
              `/api/wages/${this.id}`,
              {
                date: this.form.date,
                amount: this.form.amount,
                currency: this.form.currency
              }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, {form: {date: [error.response.data.message]}})
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        } else {
          response = await this.axios.post(
              `/api/wages`,
              {
                date: this.form.date,
                amount: this.form.amount,
                currency: this.form.currency,
                project_id: this.selected
              }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, {form: {date: [error.response.data.message]}})
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        }
        if (!response) return;

        const data = await response.data;
        this.updateWages(data);
        this.$emit('form:close');
      }
    },
    ...mapActions(useWageStore, ["updateWages"]),
  },
  emits: ["form:close"]
}
</script>

<template>
  <div class="overflow-y-scroll">
    <div class="flex items-center">
      <div class="basis-60">
        <Input label="Since" name="date" type="date" v-model="form.date" :autofocus="true" form="wage-form"
               :errors="v$.form.date.$errors"/>
      </div>
      <div class="basis-98">
        <Input label="Amount" name="amount" type="number" v-model="form.amount" min="0" class="text-right"
               form="wage-form" :errors="v$.form.amount.$errors"/>
      </div>
      <div class="basis-48">
        <Input label="Currency" name="currency" type="text" v-model="form.currency" maxlength="3" form="wage-form"
               :errors="v$.form.currency.$errors"/>
      </div>

      <form id="wage-form" @submit.prevent="submitForm" class="ml-auto flex items-center justify-end">
        <button type="submit" class="btn btn-text" :disabled="v$.$invalid">
          <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth/>
        </button>
        <button type="button" class="btn btn-text" @click="$emit('form:close')">
          <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth/>
        </button>
      </form>
    </div>
  </div>
  <div v-for="error in errors" class="text-2xs text-brand/75 px-3">{{ error }}</div>
</template>