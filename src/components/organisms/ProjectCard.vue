<script>
import {mapState, mapActions} from 'pinia'
import {useProjectStore} from '@/stores/project'

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import {sortByString} from "@/utils";

export default {
  name: "ProjectCard",
  components: {FontAwesomeIcon, ProjectItem, ProjectForm},
  data() {
    return {
      projects: [],
      edit: 0,
      create: false,
      group: 0
    }
  },
  computed: {
    ...mapState(useProjectStore, {selected: "id"})
  },
  methods: {
    async loadProjects() {
      const response = await axios.get('/api/projects', {
        params: {order: "ASC", order_by: "name"}
      })
      const data = await response.data
      this.projects = data.items
    },
    async removeProject(id) {
      const response = await axios.delete(`/api/projects/${id}`)
      if (response.status !== 204) return;

      this.projects = this.projects.filter((obj => obj.id !== id));
      if (id === this.selected) this.selectProject(0);
    },
    formCreateSubmitted(project) {
      this.create = false
      this.projects.push(project)
      this.projects.sort((a, b) => sortByString(a, b, "name"))
      this.selectProject(project.id)
    },
    formEditSubmitted(project) {
      const index = this.projects.findIndex((obj => obj.id === project.id))
      this.projects[index] = project
      this.projects.sort((a, b) => sortByString(a, b, "name"))
      if (this.edit !== this.selected) {
        this.selectProject(project.id)
      } else {
        this.edit = 0
      }
    },
    formEditCancelled(id) {
      if (id !== this.selected) {
        this.selectProject(id)
      } else {
        this.edit = 0
      }
    },
    ...mapActions(useProjectStore, {selectProject: "selectProject"})
  },
  async mounted() {
    await this.loadProjects()
  },
  watch: {
    selected() {
      this.edit = 0;
      this.create = false;
    }
  }
}
</script>

<template>
  <div class="h-full flex flex-col gap-3 card">
    <div class="flex items-center justify-between">
      <h1 class="font-medium text-lg md:text-xl leading-none text-brand/80 uppercase">
        Projects
      </h1>
    </div>

    <div class="space-y-1 overflow-y-scroll">
      <template v-for="project in projects" :key="project.id">
        <ProjectItem v-if="edit !== project.id" :project="project" :selected="selected === project.id && !edit"
                     @project:select="selectProject(project.id)"
                     @project:edit="edit = project.id" :can-edit="!create && !edit"
                     @project:remove="removeProject" :can-remove="!create && !edit"/>

        <ProjectForm v-else :id="project.id" :name="project.name"
                     @form:submitted="formEditSubmitted" @form:cancel="formEditCancelled(project.id)"/>
      </template>
      <ProjectForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="this.create = false"/>
      <button v-if="!create" type="button" class="btn btn-text text-sm uppercase w-full justify-center"
              @click="create = !create" :disabled="edit">
        <font-awesome-icon icon="fa-solid fa-plus" />
      </button>
    </div>
  </div>
</template>