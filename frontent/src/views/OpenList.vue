<script setup>
import { useDiseaseStore } from '@/stores/disease'
import { useSimulationStore } from '@/stores/simulations'

import { computed, ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';


const diseaseStore = useDiseaseStore()
const router = useRouter()

const tableLoading = ref(false)



const search = ref('')
const searchLoading = ref(false)

onMounted(() => {
  tableLoading.value = true
  diseaseStore.list().finally(() => {
    tableLoading.value = false
  })
})

function filter(value) {

  return value.title.includes(search.value) || value.id.toString().includes(search.value)
}
const filteredDisease = computed(() => {
  return diseaseStore.data?.filter(filter)
})

function searchOnClick() {
  if (!searchLoading.value) {
    router.push({path:'/list/', force: true})
  }
}

function moveGenerate() {
  if (!searchLoading.value) {
    router.push({path:'/generate/', force: true})
  }
}

function toBriefDetail(id) {
    router.push('/brief/' + id)
}

function toScenarioDetail(id) {
  router.push('/scenario/' + id)
}
</script>

<template>
  <v-container class="px-12">
    <v-row class="mt-12" justify="center">
      <v-col cols="9" md="10" lg="6">
        <v-text-field label="검색할 시나리오 제목을 입력하세요" v-model="search" v-on:keyup.enter="searchOnClick" variant="outlined"
          rounded="xl" style="font-family: 'noto';" ></v-text-field>
      </v-col>
      <v-col cols="auto"><v-btn icon="mdi-magnify" variant="flat" @click="searchOnClick" :loading="searchLoading"></v-btn></v-col>
    </v-row>
    <v-row justify="center">
      
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="12" lg="8">
        <v-table fixed-header height="400px">
          <thead>
            <tr>
              <th class="text-left">
                <h4 style="text-align: center;">시나리오명</h4>
              </th>
              <th class="text-left">
                <h4 style="text-align: center;">개요</h4>
              </th>
              <th class="text-left">
                <h4 style="text-align: center;">시나리오</h4>
              </th>

            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredDisease" :key="item.id" style="font-family: 'noto'; font-size: 15px">
              <td style="text-align: center;">{{ item.title }}</td>
              <td style="text-align: center;"><v-icon  icon="mdi-eye" @click="toBriefDetail(item.id)"></v-icon></td>
              <td style="text-align: center;"><v-icon icon="mdi-eye" @click="toScenarioDetail(item.id)"></v-icon></td>
            </tr>
            <tr v-if="tableLoading">
              <td colspan="4" class="text-center">
                <v-progress-circular indeterminate></v-progress-circular>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>

  </v-container>

</template>

<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}
#NursingText{
  font-family: 'noto';
  font-weight: bold;
  font-size: 50px;
  margin-bottom: 100px;
}
.text-left{
  font-family: noto;
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  margin:auto
}
</style>