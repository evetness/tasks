<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import useVuelidate from '@vuelidate/core';
import { required, decimal } from "@vuelidate/validators";

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue'

export default {
  name: "WageForm",
  components: {FontAwesomeIcon, Input},
  props: ["id", "date", "amount", "currency"],
  setup () {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        date: this.date || null,
        amount: this.amount || 0,
        currency: this.currency || ""
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
          )
        } else {
          response = await this.axios.post(
            `/api/wages`,
            {
              date: this.form.date,
              amount: this.form.amount,
              currency: this.form.currency,
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
  <tr>
    <td>
      <Input label="Since" name="date" type="date" v-model="form.date" :autofocus="true" form="wage-form"/>
    </td>
    <td>
      <div class="flex">
        <Input label="Amount" name="amount" type="number" v-model="form.amount" min="0" class="text-right" form="wage-form"/>
        <Input label="Currency" name="currency" type="text" v-model="form.currency" maxlength="3" form="wage-form"/>
      </div>
    </td>
    <td>
      <form id="wage-form" @submit.prevent="submitForm" class="flex items-center justify-end">
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