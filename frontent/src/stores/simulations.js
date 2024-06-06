import { defineStore } from 'pinia'

const endpoint = 'simulations/'
const chat_endpoint = 'chats/'
const member_endpoints = 'members/'
export const useSimulationStore = defineStore('simulations-store', {
  state: () => ({
    data: [],
    detail: {},
    chats: [],
    sendingQueue: [],
    memberHashMap: {}
  }),
  getters: {
    // doubleCount: (state) => state.count * 2
  },
  actions: {
    list() {
      return this.$axios.get(endpoint).then((res) => {
        this.data = res.data
        return res
      })
    },
    generate(title, disease, item, etc) {
      return this.$axios.post(endpoint, {title, disease, item, etc})
    },
    regenerate(sim_id) {
      return this.$axios.post('regenerate/', {sim_id})
    },
    scenario(sim_id) {
      return this.$axios.post('Opensimulation/', {sim_id})
    },
    setHashMap(arr) {
      this.memberHashMap = {}
      arr.forEach((e)=>{

        this.addHashMapValue(e)
      })
    },
    addHashMapValue(member){
      this.memberHashMap[member.uid] = member
    },
    get(id) {
      return this.$axios.get(endpoint+id).then((res) => {
        this.setHashMap(res.data.members)
        this.detail = res.data
        return res
      })
    },
    getChat(sim_id) {
      this.chats = []
      return this.$axios.get(chat_endpoint+sim_id).then((res) => {
        this.chats = res.data
        return res
      })

    },
    sendChat(content, sim_id) {
      return this.$axios.post(chat_endpoint+sim_id+"/", {content}).then((res) => {
        this.chats.push(res.data)
        console.log(this.chats)
        return res
      })

    },
    fetchRealtimeChat(chat) {
      this.chats.push(chat)
    },
    addMember(email, sim_id) {
      return this.$axios.post(endpoint+sim_id+"/"+member_endpoints, {email}).then(res=>{
        this.addHashMapValue(res.data)
        this.detail?.members?.push(res.data)
        return res
      })
    }
  }
})
