import { defineStore } from 'pinia'

export const useDBStore = defineStore('firestore-store', {
  actions: {
    getDb() {
      return this.$db
    },
  }
})
