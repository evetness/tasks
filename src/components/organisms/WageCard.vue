<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import WageForm from '@/components/molecules/wage/WageForm.vue';
import WageItem from "@/components/molecules/wage/WageItem.vue";

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
    sortByDate(a, b) {
      let da = new Date(a.date), db = new Date(b.date);
      return db - da;
    },
    async loadWages() {
      if (!this.project) return;
      const response = await axios.get(`/api/wages`, {
        params: {order: "DESC", order_by: "date", project_id: this.project}
      });
      const data = await response.data;
      this.wages = data.items
    },
    formCreateSubmitted(wage) {
      this.create = false
      this.wages.push(wage)
      this.wages.sort(this.sortByDate)
    },
    formEditSubmitted(wage) {
      this.edit = 0
    },
    async removeWage(id) {
      const response = await axios.delete(`/api/wages/${id}`)
      if (response.status !== 204) return;

      this.wages = this.wages.filter((obj => obj.id !== id));
    },
  },
  mounted() {
    this.loadWages()
  },
  watch: {
    project() {
      this.loadWages()
    }
  },
  components: {WageItem, WageForm }
}
</script>

<template>
  <div class="flex flex-col h-full">
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
                    @wage:edit="edit = wage.id"
                    @wage:remove="removeWage"/>
          <WageForm v-else :id="wage.id" :date="wage.date" :amount="wage.amount" :currency="wage.currency"
                    @form:submitted="formEditSubmitted" @form:cancel="this.edit = 0"/>
        </template>
        <WageForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="this.create = false"/>
        <tr>
          <td colspan="3">
            <button v-if="!create && !edit" type="button" class="btn btn-text text-sm uppercase w-full justify-center"
                    :disabled="this.edit || !this.project" @click="this.create = !this.create">
              <font-awesome-icon icon="fa-solid fa-plus" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="mt-auto">
    </div>
  </div>
</template>