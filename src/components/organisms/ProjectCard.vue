<script>
import {mapState, mapActions} from 'pinia'
import {useProjectStore} from '@/stores/project'
import {useGlobalStore} from '@/stores/global'

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import ProjectSkeleton from '@/components/molecules/project/ProjectSkeleton.vue';
import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import ProjectRemove from '@/components/molecules/project/ProjectRemove.vue';

export default {
  name: "ProjectCard",
  components: {FontAwesomeIcon, ProjectItem, ProjectForm, ProjectRemove, ProjectSkeleton},
  data() {
    return {
      create: false,
      edit: 0,
      remove: 0
    }
  },
  computed: {
    ...mapState(useProjectStore, ["projects"]),
    ...mapState(useGlobalStore, ["inAction", "isProjectLoading"])
  },
  methods: {
    ...mapActions(useProjectStore, ["getProjects"]),
    ...mapActions(useGlobalStore, ["setAction"])
  },
  async mounted() {
    await this.getProjects();
  },
  watch: {
    edit(newValue) {
      this.setAction(newValue !== 0)
    },
    create(newValue) {
      this.setAction(newValue)
    },
    remove(newValue) {
      this.setAction(newValue !== 0)
    }
  }
}
</script>

<template>
  <div class="h-full flex flex-col gap-3 card">
    <div class="flex items-center justify-between">
      <h1 class="font-extrabold text-lg md:text-xl leading-none text-brand/80 uppercase">
        <font-awesome-icon icon="rocket" />
        Projects
      </h1>
    </div>
    <ProjectSkeleton v-if="isProjectLoading"/>
    <div v-else class="space-y-1 overflow-y-scroll">
      <template v-for="project in projects" :key="project.id">
        <ProjectItem v-if="edit !== project.id && remove !== project.id" :project="project"
                     @project:edit="edit = project.id" @project:remove="remove = project.id"/>

        <ProjectForm v-if="edit === project.id" :id="project.id" :name="project.name" @form:close="edit = 0"/>

        <ProjectRemove v-if="remove === project.id" :id="project.id" :name="project.name" @form:close="remove = 0"/>
      </template>

      <ProjectForm v-if="create" @form:close="create = false"/>
      <button v-else type="button"
              class="btn btn-text text-sm uppercase w-full justify-center" @click="create = true" :disabled="inAction">
        <font-awesome-icon icon="fa-solid fa-plus"/>
      </button>

    </div>
  </div>
</template>