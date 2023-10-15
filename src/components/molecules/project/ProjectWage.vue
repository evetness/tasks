<script>
import {mapState, mapActions, mapWritableState} from "pinia";
import {useProjectStore} from '@/stores/project'
import moment from "moment/min/moment-with-locales";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ProjectPay from "@/components/molecules/project/ProjectPay.vue";
import {useGlobalStore} from "@/stores/global.js";

export default {
  name: "ProjectWage",
  components: {ProjectPay, FontAwesomeIcon},
  props: ["complete"],
  emits: ["form:close"],
  methods: {
    moment,
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"])
  },
  computed: {
    ...mapState(useProjectStore, ["amount", "unpaid", "elapsed", "wage", "salary"]),
    ...mapState(useGlobalStore, ["isCurrentWageLoading", "isSalaryLoading"]),
  },
  async mounted() {
    await this.getCurrentWage()
    await this.getUnpaidSalary()
  }
}
</script>

<template>
  <div class="px-3 pt-2 pb-2 text-brand/60 border-x border-brand/60 bg-brand/5 group-hover:bg-brand/10 group-focus-within:bg-brand/10">
    <div class="flex justify-between gap-1 flex-wrap">
      <div class="leading-none">
        <div class="text-xs text-brand/60 mb-1">Current Wage</div>
        <div v-if="isCurrentWageLoading" class="animate-pulse">
          <div class="h-6 w-full bg-brand/20"></div>
          <div class="h-4 w-2/3 bg-brand/10"></div>
        </div>
        <div v-else>
          <div class="text-brand/80 font-medium">{{ amount }}</div>
          <div v-if="wage" class="text-brand/70 text-xs">{{ moment(wage.date).fromNow() }}</div>
        </div>
      </div>

      <div class="leading-none text-right ml-auto">
        <div class="text-xs mb-1">
          <div class="flex items-center justify-end gap-1">
            <span class="text-brand/60">Unpaid</span>
          </div>
        </div>
        <div v-if="isSalaryLoading" class="animate-pulse">
          <div class="h-8 w-24 bg-brand/30"></div>
        </div>
        <div v-else class="leading-none">
          <div class="text-brand text-xl font-bold">{{ unpaid }}</div>
          <div class="text-brand/70 text-xs">{{ elapsed }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="border-x border-brand/60">
    <ProjectPay v-if="complete" @form:close="$emit('form:close')" />
  </div>
</template>
