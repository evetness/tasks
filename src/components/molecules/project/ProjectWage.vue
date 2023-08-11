<script>
import { mapState, mapActions } from "pinia";
import {useProjectStore} from '@/stores/project'
import moment from "moment/min/moment-with-locales";

export default {
  name: "ProjectWage",
  methods: {
    moment,
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"])
  },
  computed: {
    ...mapState(useProjectStore, ["wage", "amount", "unpaid"])
  },
  async created() {
    await this.getCurrentWage()
    await this.getUnpaidSalary()
  }
}
</script>

<template>
  <div class="flex justify-between gap-1">
    <div class="leading-none">
      <div class="text-xs text-brand/60 mb-1">Current Wage</div>
      <div class="text-brand/80 font-medium">{{ amount }}</div>
      <div v-if="wage" class="text-brand/70 text-xs">{{ moment(wage.date).fromNow() }}</div>
    </div>

    <div class="leading-none text-right">
      <div class="text-xs text-brand/60 mb-1">Unpaid</div>
      <div class="text-brand text-xl font-bold">{{ unpaid }}</div>
    </div>
  </div>
</template>
