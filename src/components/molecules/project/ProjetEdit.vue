<script>
import Input from '@/components/molecules/Input.vue'
export default {
  name: "ProjectEdit",
  components: {Input},
  props: ["id", "name"],
  data() {
    return {
      v$: useVuelidate(),
      form: {
        name: this.name
      }
    }
  },
  validators() {
    return {
      form: {
        name: {required: true, $autoDirty: true}
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        const result = await this.axios.post(
          `/api/projects/${this.id}`,
          { name: this.form.name }
        )
      }
    }
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" class="flex items-center hover:bg-brand/20 focus:bg-brand/20 border-x border-transparent">
    <Input name="name" type="text" v-model="v$.form.name.$model"/>
    <button type="submit" class="btn btn-brand">
      <font-awesome-icon icon="fa-regular fa-floppy-disk" />
    </button>
  </form>
</template>