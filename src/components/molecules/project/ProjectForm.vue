<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";
import Input from '@/components/atoms/Input.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  name: "ProjectCreate",
  props: ["id", "name"],
  components: {FontAwesomeIcon, Input},
  setup () {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        name: this.name || ""
      },
      vuelidateExternalResults: {
        form: {
          name: []
        }
      }
    }
  },
  validations() {
    return {
      form: {
        name: {required, $autoDirty: true}
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = null
        if (this.id) {
          response = await this.axios.put(
            `/api/projects/${this.id}`,
            { name: this.form.name }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, { form: { name: error.response.data.message }})
            }
          })
        } else {
          response = await this.axios.post(
            `/api/projects`,
            { name: this.form.name }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, { form: { name: error.response.data.message }})
            }
          })
        }
        const data = await response.data
        this.$emit('form:submitted', data)
      }
    }
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" class="flex items-center text-brand/80 text-sm hover:bg-brand/20 focus:bg-brand/20 border-x border-transparent">
    <Input label="Name" name="name" type="text" v-model="form.name" :autofocus="true" :errors="v$.form.name.$errors"/>
    <button type="submit" class="btn btn-text" :disabled="v$.$invalid" title="Submit">
      <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
    </button>
    <button type="button" class="btn btn-text" @click="$emit('form:cancel')" title="Cancel">
      <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
    </button>
  </form>
</template>