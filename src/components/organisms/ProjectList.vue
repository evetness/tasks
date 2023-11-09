<script setup>
import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";
import ProjectRemove from '@/components/molecules/project/ProjectRemove.vue';
import ProjectAdd from '@/components/molecules/project/ProjectAdd.vue';
import ProjectPay from '@/components/molecules/project/ProjectPay.vue';
import ProjectWageForm from '@/components/molecules/project/ProjectWageForm.vue';

import { ref, computed, watch, onMounted } from 'vue';

import { storeToRefs } from 'pinia';
import { useProjectStore } from '@/stores/project';
import { useGlobalStore } from '@/stores/global';
import ProjectWageRemove from '../molecules/project/ProjectWageRemove.vue';

const projectStore = useProjectStore();
const { projects } = storeToRefs(projectStore);
const { getProjects } = projectStore;

const globalStore = useGlobalStore();
const { isProjectLoading } = storeToRefs(globalStore);
const { setAction } = globalStore;

const create = ref(false);
const edit = ref(0);
const remove = ref(0);
const pay = ref(0);
const wage = ref(0);
const removeWage = ref(false);

const skeletonSize = computed(() => Math.floor(Math.random() * 5) + 1);

const hideItem = (projectId) => {
  if (
    edit.value !== projectId &&
    remove.value !== projectId &&
    pay.value !== projectId &&
    wage.value !== projectId
  ) {
    return true
  } else {
    return false
  }
}

watch(create, (newValue) => setAction(newValue));
watch(edit, (newValue) => setAction(newValue !== 0));
watch(remove, (newValue) => setAction(newValue !== 0));
watch(pay, (newValue) => setAction(newValue !== 0));
watch(wage, (newValue) => setAction(newValue !== 0));

onMounted(async () => {
  await getProjects();
})
</script>

<template>
  <div class="flex items-center gap-6 snap-x overflow-x-auto pb-4">

    <template v-if="isProjectLoading" v-for="n in skeletonSize">
      <div class="group relative animate-pulse shrink-0 w-56 sm:w-72 snap-center">
        <div class="flex gap-0.5">
          <div class="h-6 w-5/12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/10"></div>
          <div class="h-6 w-2/12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/5"></div>
          <div class="h-6 w-2/12 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/5"></div>
        </div>
        <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/10">
          <div class="flex-auto p-4">
            <div class="flex items-center justify-center gap-1 py-5 sm:py-8 sm:text-2xl break-all">&nbsp;</div>
          </div>
        </div>
      </div>
    </template>

    <template v-else v-for="project in projects" :key="project.id">
      <ProjectItem v-if="hideItem(project.id)" :project="project" @project:pay="pay = project.id"
        @project:edit="edit = project.id" @project:remove="remove = project.id" @project:salary="wage = project.id"
        class="shrink-0 snap-center" />
      <ProjectForm v-if="edit === project.id" :isEdit="true" @form:close="edit = 0" class="shrink-0 snap-center" />
      <ProjectRemove v-if="remove === project.id" @form:close="remove = 0" class="shrink-0 snap-center" />
      <ProjectPay v-if="pay === project.id" @form:close="pay = 0" class="shrink-0 snap-center" />
      <ProjectWageForm v-if="wage === project.id && !removeWage" @form:close="wage = 0" @form:remove="removeWage = true"
        class="shrink-0 snap-center" />
      <ProjectWageRemove v-if="wage === project.id && removeWage" @form:close="wage = 0; removeWage = false"
        class="shrink-0 snap-center" />
    </template>

    <ProjectAdd v-if="!isProjectLoading && !create" class="shrink-0 snap-end" @form:add="create = true" />
    <ProjectForm v-if="create" :isEdit="false" @form:close="create = false" class="shrink-0 snap-end" />

  </div>
</template>