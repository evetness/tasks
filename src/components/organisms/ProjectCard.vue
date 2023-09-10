<script>
import {mapState, mapActions} from 'pinia'
import {useProjectStore} from '@/stores/project'
import {useGlobalStore} from '@/stores/global'

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import ProjectSkeleton from '@/components/molecules/project/ProjectSkeleton.vue';
import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import ProjectRemove from '@/components/molecules/project/ProjectRemove.vue';
import {sortByString} from "@/utils";

export default {
  name: "ProjectCard",
  components: {FontAwesomeIcon, ProjectItem, ProjectForm, ProjectRemove, ProjectSkeleton},
    data() {
    return {
      isLoading: true,
      projects: [],
      create: false,
      edit: 0,
      remove: 0
    }
  },
  computed: {
    ...mapState(useProjectStore, {selected: "id"}),
    ...mapState(useGlobalStore, {inAction: "inAction"})
  },
  methods: {
    async loadProjects() {
      const response = await axios.get('/api/projects', {
        params: {page: 1, per_page: 0, order: "ASC", order_by: "name"}
      })
      const data = await response.data
      this.projects = data.items
      this.isLoading = false
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
    formRemoveSubmitted(id) {
      this.projects = this.projects.filter((obj => obj.id !== id));
      if (id === this.selected) this.selectProject(0);
    },
    ...mapActions(useProjectStore, {selectProject: "selectProject"}),
    ...mapActions(useGlobalStore, {toggleAction: "toggleAction"})
  },
  async mounted() {
    await this.loadProjects();
  },
  watch: {
    selected() {
      this.edit = 0;
      this.create = false;
      this.remove = 0;
    },
    edit(newValue) {
      if (newValue === 0) {
        this.toggleAction(false)
      } else {
        this.toggleAction(true)
      }
    },
    create(newValue) {
      this.toggleAction(newValue)
    },
    remove(newValue) {
      if (newValue === 0) {
        this.toggleAction(false)
      } else {
        this.toggleAction(true)
      }
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
    <ProjectSkeleton v-if="isLoading"/>
    <div v-else class="space-y-1 overflow-y-scroll">
      <template v-for="project in projects" :key="project.id">
        <ProjectItem v-if="edit !== project.id && remove !== project.id" :project="project"
                     :selected="selected === project.id && !edit" @project:select="selectProject(project.id)"
                     @project:edit="edit = project.id" :can-edit="!inAction" @project:remove="remove = project.id"
                     :can-remove="!inAction"/>

        <ProjectForm v-if="edit === project.id" :id="project.id" :name="project.name"
                     @form:submitted="formEditSubmitted"
                     @form:cancel="formEditCancelled(project.id)"/>

        <ProjectRemove v-if="remove === project.id" :id="project.id" :name="project.name"
                       @form:submitted="formRemoveSubmitted" @form:cancel="remove = 0"/>
      </template>
      <ProjectForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="create = false"/>
      <button v-if="!create" type="button" class="btn btn-text text-sm uppercase w-full justify-center"
              @click="create = !create" :disabled="inAction">
        <font-awesome-icon icon="fa-solid fa-plus"/>
      </button>
    </div>
  </div>
</template>