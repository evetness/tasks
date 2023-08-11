<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import WageForm from '@/components/molecules/wage/WageForm.vue';
import WageItem from "@/components/molecules/wage/WageItem.vue";
import { sortByDate } from "@/utils";

export default {
  name: "WageCard",
  data() {
    return {
      wages: [],
      edit: 0,
      create: false
    };
  },
  computed: {
    ...mapState(useProjectStore, { project: "id" })
  },
  methods: {
    async reload() {
      await this.getCurrentWage()
      await this.getUnpaidSalary()
    },
    async loadWages() {
      if (!this.project) return;
      const response = await axios.get(`/api/wages`, {
        params: {order: "DESC", order_by: "date", project_id: this.project}
      });
      const data = await response.data;
      this.wages = data.items
    },
    async formCreateSubmitted(wage) {
      this.create = false
      this.wages.push(wage)
      this.wages.sort((a, b) => sortByDate(a, b, "date"))
      await this.reload()
    },
    async formEditSubmitted(wage) {
      const index = this.wages.findIndex((obj => obj.id === wage.id))
      this.wages[index] = wage
      this.wages.sort((a, b) => sortByDate(a, b, "date"))
      this.edit = 0
      await this.reload()

    },
    async removeWage(id) {
      const response = await axios.delete(`/api/wages/${id}`)
      if (response.status !== 204) return;

      this.wages = this.wages.filter((obj => obj.id !== id));
      await this.reload()
    },
    ...mapActions(useProjectStore, ["getCurrentWage", "getUnpaidSalary"])
  },
  mounted() {
    this.loadWages()
  },
  watch: {
    project() {
      this.loadWages()
    }
  },
  components: { WageItem, WageForm }
}
</script>

<template>
  <div class="flex flex-col overflow-hidden">
    <div class="overflow-y-scroll">
      <table class="w-full text-sm">
        <thead class="text-brand/70">
          <tr>
            <th class="w-[40%] text-left">Since</th>
            <th class="w-[30%] text-right">Amount</th>
            <th class="w-[20%] text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="text-brand/80">
          <template v-for="wage in wages" :key="wage.id">
            <WageItem v-if="edit !== wage.id" :wage="wage"
                      @wage:edit="edit = wage.id" :can-edit="!create && !edit"
                      @wage:remove="removeWage" :can-remove="!create && !edit"/>
            <WageForm v-else :id="wage.id" :date="wage.date" :amount="wage.amount" :currency="wage.currency"
                      @form:submitted="formEditSubmitted" @form:cancel="edit = 0"/>
          </template>
          <WageForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="create = false"/>
          <tr v-if="!create && !edit">
            <td colspan="3">
              <button type="button" class="btn btn-text text-sm uppercase w-full justify-center"
                      :disabled="edit || !project" @click="create = !create">
                <font-awesome-icon icon="fa-solid fa-plus" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>