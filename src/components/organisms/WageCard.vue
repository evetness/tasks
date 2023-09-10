<script>
import {mapState, mapActions} from 'pinia';
import {useProjectStore} from '@/stores/project';
import {useGlobalStore} from "@/stores/global";

import axios from "axios";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

import WageForm from '@/components/molecules/wage/WageForm.vue';
import WageItem from "@/components/molecules/wage/WageItem.vue";
import WageRemove from "@/components/molecules/wage/WageRemove.vue";
import WageSkeleton from "@/components/molecules/wage/WageSkeleton.vue";
import {sortByDate} from "@/utils";

export default {
  name: "WageCard",
  data() {
    return {
      isLoading: true,
      wages: [],
      edit: 0,
      create: false,
      remove: 0,
    };
  },
  computed: {
    ...mapState(useProjectStore, {project: "id"}),
    ...mapState(useGlobalStore, {inAction: "inAction"})
  },
  methods: {
    async reload() {
      await this.getCurrentWage()
      await this.getUnpaidSalary()
    },
    async loadWages() {
      if (!this.project) {
        this.isLoading = false;
        return;
      }
      const response = await axios.get(`/api/wages`, {
        params: {order: "DESC", order_by: "date", project_id: this.project}
      });
      const data = await response.data;
      this.wages = data.items
      this.isLoading = false;
    },
    async formCreateSubmitted(wage) {
      this.create = false
      this.wages.push(wage)
      this.wages.sort((a, b) => sortByDate(a, b, "date"))
      await this.reload()
    },
    async formEditSubmitted(wage) {
      this.edit = 0
      const index = this.wages.findIndex((obj => obj.id === wage.id))
      this.wages[index] = wage
      this.wages.sort((a, b) => sortByDate(a, b, "date"))
      await this.reload()
    },
    async formRemoveSubmitted(id) {
      this.remove = 0
      this.wages = this.wages.filter((obj => obj.id !== id));
      await this.reload()
    },
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"]),
    ...mapActions(useGlobalStore, {toggleAction: "toggleAction"})
  },
  mounted() {
    this.loadWages()
  },
  watch: {
    project() {
      this.create = false;
      this.edit = 0;
      this.remove = 0;
      this.isLoading = true;
      this.loadWages()
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
  },
  components: {WageRemove, WageSkeleton, WageItem, WageForm, FontAwesomeIcon}
}
</script>

<template>
  <div class="flex flex-col overflow-hidden">
    <div class="overflow-y-scroll">
      <table class="w-full text-sm border-separate border-spacing-y-1">

        <thead class="text-brand/70">
        <tr>
          <th class="w-[40%] text-left">Since</th>
          <th class="w-[30%] text-right">Amount</th>
          <th class="w-[20%] text-right">Actions</th>
        </tr>
        </thead>

        <tbody class="text-brand/80">
        <WageSkeleton v-if="isLoading"/>
        <template v-else v-for="wage in wages" :key="wage.id">
          <WageItem v-if="edit !== wage.id && remove !== wage.id" :wage="wage"
                    @wage:edit="edit = wage.id" :can-edit="!inAction"
                    @wage:remove="remove = wage.id" :can-remove="!inAction"/>
          <WageForm v-if="edit === wage.id" :id="wage.id" :date="wage.date" :amount="wage.amount" :currency="wage.currency"
                    @form:submitted="formEditSubmitted" @form:cancel="edit = 0"/>
          <WageRemove v-if="remove === wage.id" :id="wage.id" :amount="wage.amount" :currency="wage.currency" :start="wage.start"
                      @form:submitted="formRemoveSubmitted" @form:cancel="remove = 0"/>
        </template>
        </tbody>

        <tfoot class="sticky bottom-0 bg-[#3e3121]">
        <WageForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="create = false"/>
        <tr v-else>
          <td colspan="3">
            <button type="button" class="btn btn-text text-sm uppercase w-full justify-center"
                    :disabled="inAction || !project" @click="create = !create">
              <font-awesome-icon icon="fa-solid fa-plus"/>
            </button>
          </td>
        </tr>
        </tfoot>

      </table>
    </div>
  </div>
</template>