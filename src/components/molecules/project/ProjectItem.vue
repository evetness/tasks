<script>
import ProjectWage from "@/components/molecules/project/ProjectWage.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ProjectUnpaidComplete from "@/components/molecules/project/ProjectPay.vue";
import {mapState, mapActions} from "pinia";
import {useGlobalStore} from "@/stores/global.js";
import {useProjectStore} from "@/stores/project.js";

export default {
  name: "ProjectItem",
  components: {ProjectUnpaidComplete, FontAwesomeIcon, ProjectWage},
  props: ["project"],
  data() {
    return {
      complete: false
    }
  },
  computed: {
    isSelected() { return this.selected === this.project.id },
    canPaySalary() { return this.isSelected && this.unpaid !== '-'},
    ...mapState(useProjectStore, ["selected", "unpaid"]),
    ...mapState(useGlobalStore, ["inAction"])
  },
  methods: {
    ...mapActions(useProjectStore, ["selectProject"]),
    ...mapActions(useGlobalStore, ["setAction"])
  },
  emits: ["project:edit", "project:remove"],
  watch: {
    complete(newValue) {
      this.setAction(newValue)
    },
  }
}
</script>

<template>
  <div class="group">
    <div class="flex items-center text-sm group-hover:bg-brand/20 group-focus-within:bg-brand/20 border-x"
         :class="{
            'border-transparent': !isSelected,
            'border-brand/60 bg-brand/10': isSelected
         }">
      <button type="button" class="w-full py-2 px-3 text-left text-brand break-all" @click="selectProject(project.id)">
        {{ project.name }}
      </button>

      <button v-if="canPaySalary" type="button" class="btn btn-text" :disabled="inAction" @click="complete = true">
        <font-awesome-icon icon="dollar" fixedWidth />
      </button>

      <button type="button" class="btn btn-text" :disabled="inAction" @click="$emit('project:edit', project.id)">
        <font-awesome-icon icon="fa-regular fa-pen-to-square" fixedWidth />
      </button>

      <button type="button" class="btn btn-text" :disabled="inAction" @click="$emit('project:remove', project.id)">
        <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
      </button>
    </div>
    <div v-if="isSelected">
      <ProjectWage :complete="complete" @form:close="this.complete = false"/>
    </div>
  </div>
</template>