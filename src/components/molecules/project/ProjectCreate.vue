<template>
  <form @submit.prevent="submitForm" class="flex items-center hover:bg-brand/20 focus:bg-brand/20 border-x border-transparent">
    <Input name="name" type="text" v-model="form.name"/>
    <button type="submit" class="btn hover:bg-brand/30">
      <font-awesome-icon icon="fa-regular fa-floppy-disk" />
    </button>
  </form>
</template>

<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";
import Input from '@/components/molecules/Input.vue'

export default {
  name: "ProjectCreate",
  components: {Input},
  setup () {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      form: {
        name: ""
      }
    }
  },
  validators() {
    return {
      form: {
        name: {required, $autoDirty: true}
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        const result = await this.axios.post(
          `/api/projects`,
          { name: this.form.name }
        )
      }
    }
  }
}
</script>