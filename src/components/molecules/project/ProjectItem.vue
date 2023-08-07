<script>
import axios from "axios";
import ProjectWage from "@/components/molecules/project/ProjectWage.vue";

export default {
  name: "ProjectItem",
  components: {ProjectWage},
  props: ["project", "selected", "canEdit", "canRemove"],
  emits: ["project:select", "project:canEdit", "project:edit", "project:canRemove", "project:remove"],
  data() {
    return {
      wage: null,
      salary: null,
    }
  },
  methods: {
    async getCurrentWage() {
      const response = await axios.get(`/api/projects/${this.project.id}/current-salary`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.wage = null;
      } else {
        this.wage = data;
      }
    },
    async getUnpaidAmount() {
      const response = await axios.get(`/api/projects/${this.project.id}/unpaid-tasks`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.salary = null;
      } else {
        this.salary = data;
      }
    },
  },
  async mounted() {
    await this.getCurrentWage();
    await this.getUnpaidAmount();
  }
}
</script>

<template>
  <div>
    <div class="flex items-center text-sm group hover:bg-brand/20 focus-within:bg-brand/20 border-x"
         :class="{
            'border-transparent': !selected,
            'border-brand/60 bg-brand/10': selected
         }"
    >
      <button type="button" class="w-full py-2 px-3 text-left text-brand"
              @click="$emit('project:select', project.id)">
        {{ project.name }}
      </button>

      <button type="button" class="btn btn-text" :disabled="!canEdit"
              @click="$emit('project:edit', project.id)">
        <font-awesome-icon icon="fa-regular fa-pen-to-square" />
      </button>

      <button type="button" class="btn btn-text" :disabled="!canRemove"
              @click="$emit('project:remove', project.id)">
        <font-awesome-icon icon="fa-regular fa-trash-can" />
      </button>
    </div>
    <div v-if="selected" class="px-3 pt-2 pb-2 text-brand/60 border-x border-brand/60">
      <ProjectWage :wage="wage" :salary="salary" />
    </div>
  </div>
</template>