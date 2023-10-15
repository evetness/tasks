<script>
import {mapActions, mapState} from 'pinia';
import {useProjectStore} from '@/stores/project';
import {useGlobalStore} from "@/stores/global";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import WageForm from '@/components/molecules/wage/WageForm.vue';
import WageItem from "@/components/molecules/wage/WageItem.vue";
import WageRemove from "@/components/molecules/wage/WageRemove.vue";
import WageSkeleton from "@/components/molecules/wage/WageSkeleton.vue";
import {useWageStore} from "@/stores/wage.js";

export default {
  name: "WageCard",
  data() {
    return {
      create: false,
      edit: 0,
      remove: 0,
    };
  },
  computed: {
    ...mapState(useProjectStore, ["selected"]),
    ...mapState(useWageStore, ["wages"]),
    ...mapState(useGlobalStore, ["inAction", "isWagesLoading"])
  },
  methods: {
    async loadWages() {
      await this.getWages();
    },
    ...mapActions(useWageStore, ["getWages"]),
    ...mapActions(useGlobalStore, ["setAction"])
  },
  mounted() {
    this.loadWages()
  },
  watch: {
    search() {
      this.loadWages()
    },
    selected() {
      this.create = false;
      this.edit = 0;
      this.remove = 0;
      this.loadWages()
    },
    edit(newValue) {
      this.setAction(newValue !== 0);
    },
    create(newValue) {
      this.setAction(newValue)
    },
    remove(newValue) {
      this.setAction(newValue !== 0);
    }
  },
  components: {WageRemove, WageSkeleton, WageItem, WageForm, FontAwesomeIcon}
}
</script>

<template>
  <div class="flex flex-col overflow-hidden gap-2">
    <div class="grid grid-cols-12 items-center gap-1 text-xs text-brand/70 font-bold pl-1">
      <div class="col-span-6 text-left">Since</div>
      <div class="col-span-4 text-right">Amount</div>
      <div class="col-span-2 text-right">Actions</div>
    </div>

    <div class="h-fit overflow-y-scroll text-brand/80 space-y-1 text-sm">
      <WageSkeleton v-if="isWagesLoading"/>
      <template v-else v-for="wage in wages" :key="wage.id">
        <WageItem v-if="edit !== wage.id && remove !== wage.id" :wage="wage"
                  @wage:edit="edit = wage.id" @wage:remove="remove = wage.id" :disabled="inAction"/>

        <WageForm v-if="edit === wage.id"
                  :id="wage.id" :date="wage.date" :amount="wage.amount" :currency="wage.currency"
                  @form:close="edit = 0"/>

        <WageRemove v-if="remove === wage.id"
                    :id="wage.id" :amount="wage.amount" :currency="wage.currency" :start="wage.start"
                    @form:close="remove = 0"/>
      </template>
    </div>

    <div class="w-full">
      <WageForm v-if="create" @form:close="create = false"/>
      <button v-else type="button" class="btn btn-text text-sm uppercase w-full justify-center"
              :disabled="inAction || !selected" @click="create = true">
        <font-awesome-icon icon="fa-solid fa-plus"/>
      </button>
    </div>
  </div>
</template>