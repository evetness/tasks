<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";
import Input from '@/components/molecules/Input.vue';
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
        let response = null
        if (this.id) {
          response = await this.axios.put(
            `/api/projects/${this.id}`,
            { name: this.form.name }
          )
        } else {
          response = await this.axios.post(
            `/api/projects`,
            { name: this.form.name }
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
  <form @submit.prevent="submitForm" class="flex items-center text-brand/80 text-sm hover:bg-brand/20 focus:bg-brand/20 border-x border-transparent">
    <Input label="Name" name="name" type="text" v-model="form.name" :autofocus="true"/>
    <button type="submit" class="btn hover:bg-brand/30">
      <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
    </button>
    <button type="button" class="btn hover:bg-brand/30" @click="$emit('form:cancel')">
      <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
    </button>
  </form>
</template>