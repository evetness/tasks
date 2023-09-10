<script>
import {mapState, mapActions, mapWritableState} from "pinia";
import {useProjectStore} from '@/stores/project'
import moment from "moment/min/moment-with-locales";

export default {
  name: "ProjectWage",
  data() {
    return {
      wageLoading: true,
      salaryLoading: true
    }
  },
  methods: {
    moment,
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"])
  },
  computed: {
    ...mapState(useProjectStore, {selectedProject: "id", amount: "amount", unpaid: "unpaid"}),
    ...mapWritableState(useProjectStore, {wage: "wage", salary: "salary"})
  },
  watch: {
    selectedProject() {
      this.wage = null;
      this.salary = null;
    }
  },
  async mounted() {
    await this.getCurrentWage()
    if (this.wage) this.wageLoading = false
    await this.getUnpaidSalary()
    if (this.salary) this.salaryLoading = false
  }
}
</script>

<template>
  <div class="flex justify-between gap-1 flex-wrap">
    <div class="leading-none">
      <div class="text-xs text-brand/60 mb-1">Current Wage</div>
      <div v-if="wageLoading" class="animate-pulse">
        <div class="h-6 w-full bg-brand/20"></div>
        <div class="h-4 w-2/3 bg-brand/10"></div>
      </div>
      <div v-else>
        <div class="text-brand/80 font-medium">{{ amount }}</div>
        <div v-if="wage" class="text-brand/70 text-xs">{{ moment(wage.date).fromNow() }}</div>
      </div>
    </div>

    <div class="leading-none text-right ml-auto">
      <div class="text-xs text-brand/60 mb-1">Unpaid</div>
      <div v-if="salaryLoading" class="animate-pulse">
        <div class="h-8 w-24 bg-brand/30"></div>
      </div>
      <div v-else>
        <div class="text-brand text-xl font-bold">{{ unpaid }}</div>
      </div>
    </div>
  </div>
</template>
