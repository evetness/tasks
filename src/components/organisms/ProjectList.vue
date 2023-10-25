<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { useGlobalStore } from '@/stores/global'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectSkeleton from '@/components/molecules/project/ProjectSkeleton.vue';
import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import ProjectRemove from '@/components/molecules/project/ProjectRemove.vue';
import ProjectAdd from '@/components/molecules/project/ProjectAdd.vue';
import ProjectPay from '../molecules/project/ProjectPay.vue';

export default {
  name: "ProjectList",
  components: { FontAwesomeIcon, ProjectItem, ProjectAdd, ProjectForm, ProjectRemove, ProjectSkeleton, ProjectPay },
  data() {
    return {
      create: false,
      edit: 0,
      remove: 0,
      pay: 0
    }
  },
  computed: {
    skeletonSize() {
      return Math.floor(Math.random() * 5) + 1
    },
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
    },
    pay(newValue) {
      this.setAction(newValue !== 0)
    }
  }
}
</script>

<template>
  <div class="flex items-center gap-6 snap-x overflow-x-auto pb-4">
    
    <template v-if="isProjectLoading" v-for="n in skeletonSize">
      <ProjectSkeleton class="shrink-0 w-56 sm:w-72 snap-center" />
    </template>

    <template v-else v-for="project in projects" :key="project.id">
      <ProjectItem v-if="edit !== project.id && remove !== project.id && pay !== project.id" :project="project"
        @project:pay="pay = project.id" @project:edit="edit = project.id" @project:remove="remove = project.id"
        class="shrink-0 snap-center" />
      <ProjectForm v-if="edit === project.id" :id="project.id" :name="project.name" @form:close="edit = 0"
        class="shrink-0 snap-center" />
      <ProjectRemove v-if="remove === project.id" :id="project.id" :name="project.name" @form:close="remove = 0"
        class="shrink-0 snap-center" />
      <ProjectPay v-if="pay === project.id" :id="project.id" @form:close="pay = 0" class="shrink-0 snap-center" />
    </template>

    <ProjectAdd v-if="!isProjectLoading && !create" class="shrink-0 snap-end" @form:add="create = true" />
    <ProjectForm v-if="create" @form:close="create = false" class="shrink-0 snap-end" />

  </div>
</template>