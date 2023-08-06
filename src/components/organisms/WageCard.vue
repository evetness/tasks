<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import { formatCurrency } from '@/utils';
import WageForm from '@/components/molecules/wage/WageForm.vue';

export default {
  name: "WageCard",
  data() {
    return {
      wage: null,
      amount: "-",
      unpaid: "-",
      edit: false,
      create: false
    };
  },
  computed: {
    ...mapState(useProjectStore, {
      project: "id"
    })
  },
  methods: {
    loadAmounts() {
      this.loadProjectWage(this.project);
      this.loadProjectUnpaidTasksAmount(this.project);
    },
    async loadProjectWage(project_id) {
      const response = await axios.get(`/api/projects/${project_id}/current-salary`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.wage = null;
        this.amount = "-";
      }
      else {
        this.wage = data;
        this.amount = formatCurrency(data.amount, data.currency);
      }
    },
    async loadProjectUnpaidTasksAmount(project_id) {
      const response = await axios.get(`/api/projects/${project_id}/unpaid-tasks`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.unpaid = "-";
      }
      else {
        this.unpaid = formatCurrency(data.amount, data.currency);
      }
    },
    addWage() {
      this.create = false
      this.loadAmounts()
    },
    editWage() {
      this.loadAmounts()
      this.edit = 0
    },
    async removeWage() {
      const response = await axios.delete(`/api/wages/${this.wage.id}`)
      this.loadAmounts()
    },
  },
  mounted() {
    this.loadAmounts()
  },
  watch: {
    project() {
      this.loadAmounts()
    }
  },
  components: { WageForm }
}
</script>

<template>
  <div class="h-full card flex flex-col">
    <div class="flex items-center justify-between mb-3">
      <h1 class="font-medium text-lg md:text-xl leading-none text-brand/80 uppercase">
        Wage
      </h1>

      <button :disabled="this.edit" type="button" class="btn btn-brand text-xs uppercase" @click="this.create = !this.create">
        {{ create ? 'Cancel' : 'New' }}
      </button>
    </div>

    <WageForm v-if="create" @form:submitted="addWage" @form:cancel="this.create = false"/>
    <WageForm v-if="edit" :id="wage.id" :date="wage.date" :amount="wage.amount" :currency="wage.currency" 
      @form:submitted="editWage" @form:cancel="this.edit = false"/>

    <div class="leading-none" v-if="!create && !edit">
      <div class="text-sm text-brand/90 mb-1">Current Wage</div>
      <div class="flex item-center justify-between">

        <div>
          <div class="text-brand/80 font-medium">{{ amount }}</div>
          <div v-if="this.wage" class="text-brand/80 text-xs">{{ this.wage.date }}</div>
        </div>

        <div v-if="this.wage" class="text-brand/80">
          <button type="button" class="btn btn-text" @click="this.edit = this.wage?.id">
            <font-awesome-icon icon="fa-regular fa-pen-to-square" />
          </button>
          
          <button type="button" class="btn btn-text" @click="removeWage">
            <font-awesome-icon icon="fa-regular fa-trash-can" />
          </button>
        </div>

      </div>
    </div>

    <div class="mt-auto" v-if="!create && !edit">
      <div class="text-sm text-brand/90">Unpaid</div>
      <div class="text-brand text-xl font-bold">{{ unpaid }}</div>
    </div>

  </div>
</template>