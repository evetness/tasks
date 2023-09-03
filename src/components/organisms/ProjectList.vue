<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { useGlobalStore } from '@/stores/global'

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import ProjectRemove from '@/components/molecules/project/ProjectRemove.vue';
import ProjectSkeleton from '@/components/molecules/project/ProjectSkeleton.vue';
import {sortByString} from "@/utils";

export default {
  name: "ProjectList",
  components: { FontAwesomeIcon, ProjectItem, ProjectForm, ProjectRemove, ProjectSkeleton },
  data() {
    return {
      projects: [],
      create: false,
      edit: 0,
      remove: 0
    }
  },
  computed: {
    ...mapState(useProjectStore, { selected: "id" }),
    ...mapState(useGlobalStore, { inAction: "inAction" })
  },
  methods: {
    async loadProjects() {
      const response = await axios.get('/api/projects', {
        params: { page: 1, per_page: 0, order: "ASC", order_by: "name" }
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
      this.toggleAction(false)
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
    formRemoveSubmitted(id) {
      this.projects = this.projects.filter((obj => obj.id !== id));
      if (id === this.selected) this.selectProject(0);
    },
    ...mapActions(useProjectStore, { selectProject: "selectProject" }),
    ...mapActions(useGlobalStore, { toggleAction: "toggleAction" })
  },
  async mounted() {
    await this.loadProjects()
  },
  watch: {
    selected() {
      this.edit = 0;
      this.create = false;
      this.remove = 0;
    }
  }
}
</script>

<template>
  <div class="space-y-1 overflow-y-scroll">
    <template v-for="project in projects" :key="project.id">
      <ProjectItem v-if="edit !== project.id && remove !== project.id" :project="project"
        :selected="selected === project.id && !edit" @project:select="selectProject(project.id)"
        @project:edit="edit = project.id" :can-edit="!inAction" @project:remove="remove = project.id"
        :can-remove="!inAction" />

      <ProjectForm v-if="edit === project.id" :id="project.id" :name="project.name" @form:submitted="formEditSubmitted"
        @form:cancel="formEditCancelled(project.id)" />

      <ProjectRemove v-if="remove === project.id" :id="project.id" :name="project.name"
        @form:submitted="formRemoveSubmitted" @form:cancel="remove = 0" />
    </template>
    <ProjectForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="this.create = false" />
    <button v-if="!create" type="button" class="btn btn-text text-sm uppercase w-full justify-center"
      @click="create = !create; toggleAction(!inAction)" :disabled="inAction">
      <font-awesome-icon icon="fa-solid fa-plus" />
    </button>
  </div>
</template>