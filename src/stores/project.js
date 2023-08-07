import axios from 'axios'
import { defineStore } from 'pinia'

import {formatCurrency} from "@/utils"

// useLocalStorage from vueuse for storing project id
export const useProjectStore = defineStore('project', {
  state: () => ({ id: 0, wage: null, salary: null }),
  getters: {
    amount() {
      return this.wage ? formatCurrency(this.wage.amount, this.wage.currency) : "-"
    },
    unpaid() {
      return this.salary ? formatCurrency(this.salary.amount, this.salary.currency) : "-"
    }
  },
  actions: {
    selectProject(id) { this.id = id },
    async getCurrentWage() {
      const response = await axios.get(`/api/projects/${this.id}/current-salary`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.wage = null;
      } else {
        this.wage = data;
      }
    },
    async getUnpaidSalary() {
      const response = await axios.get(`/api/projects/${this.id}/unpaid-tasks`);
      const data = await response.data;
      if (Object.keys(data).length === 0) {
        this.salary = null;
      } else {
        this.salary = data;
      }
    }
  }
})
