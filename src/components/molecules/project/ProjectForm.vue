<script>
import useVuelidate from '@vuelidate/core';
import { required } from "@vuelidate/validators";
import Input from '@/components/atoms/Input.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { mapActions, mapState } from "pinia";
import { useProjectStore } from "@/stores/project.js";

export default {
  name: "ProjectForm",
  props: ["isEdit"],
  components: { FontAwesomeIcon, Input },
  setup() {
    return { v$: useVuelidate() }
  },
  computed: {
    ...mapState(useProjectStore, ["selected", "project"])
  },
  data() {
    return {
      form: {
        name: this.isEdit ? this.project : ""
      },
      vuelidateExternalResults: {
        form: {
          name: []
        }
      },
      errors: new Set()
    }
  },
  validations() {
    return {
      form: {
        name: { required, $autoDirty: true }
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.v$.$invalid === false) {
        let response = null
        if (this.isEdit) {
          response = await this.axios.put(
            `/api/projects/${this.selected}`,
            { name: this.form.name }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, { form: { name: [error.response.data.message] } })
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        } else {
          response = await this.axios.post(
            `/api/projects`,
            { name: this.form.name }
          ).catch((error) => {
            if (error.response.status === 409) {
              Object.assign(this.vuelidateExternalResults, { form: { name: [error.response.data.message] } })
              this.errors.add(error.response.data.message)
            }
            return null;
          })
        }
        if (!response) return

        const project = await response.data
        this.updateProjects(project)
        this.$emit('form:close')
      }
    },
    ...mapActions(useProjectStore, ["updateProjects"]),
  },
  mounted() {
    console.log(this.project)
  },
  emits: ["form:close"]
}
</script>

<template>
  <div class="group relative w-64 sm:w-72">
    <div class="text-brand text-sm text-center">
      <div class="h-6 w-5/12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="plus" v-if="!isEdit" />
        <font-awesome-icon icon="pen-to-square" v-if="isEdit" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="text-sm">
            <Input name="name" type="text" v-model="form.name" :autofocus="true" :errors="v$.form.name.$errors">
            <template #prefix>
              <font-awesome-icon icon="clipboard" class="ml-2" />
            </template>
            </Input>
          </div>
          <div class="text-2xs text-brand/70 text-left">
            {{ errors.size !== 0 ? Array.from(errors).join(', ') : '&nbsp;' }}
          </div>
          <div class="flex items-center gap-1 justify-end mt-2">
            <button type="submit" class="btn btn-text text-xs uppercase" :disabled="v$.$invalid">
              <font-awesome-icon icon="fa-regular fa-floppy-disk" fixedWidth />
              {{ isEdit ? 'Edit' : 'Add' }}
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