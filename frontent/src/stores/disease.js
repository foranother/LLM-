import { defineStore } from 'pinia'

const endpoint = 'Opensimulation/'
export const useDiseaseStore = defineStore('diseases-store', {
  state: () => ({
    data: []
  }),
  getters: {
    // doubleCount: (state) => state.count * 2
  },
  actions: {
    list() {
      return this.$axios.get(endpoint).then((res) => {
        this.data = res.data
        return res
      }).catch(err=> console.log(err))
    },
  }
})
