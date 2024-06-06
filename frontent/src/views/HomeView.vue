<script setup>
import { useDiseaseStore } from '@/stores/disease'
import { useSimulationStore } from '@/stores/simulations'
import mainIMG  from '@/assets/main.jpg'
import { computed, ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';


const diseaseStore = useDiseaseStore()
const router = useRouter()

const tableLoading = ref(false)


const searchLoading = ref(false)


onMounted(() => {
  tableLoading.value = true
  diseaseStore.list().finally(() => {
    tableLoading.value = false
  })
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

function moveOpenList() {
  if (!searchLoading.value) {
    router.push({path:'/open-list/', force: true})
  }
}

</script>

<template>
    <div style="float: left; margin-top: 150px; margin-left: 150px">
      <div style="display:flex; justify-content: left;" class="NursingText">간호 시뮬레이션 시나리오를</div>
      <div style="display:flex; justify-content: left;" class="NursingText2">생성하세요</div>
      <div style="display:flex; justify-content: left;">
      <v-btn variant="tonal" @click="moveOpenList" size="x-large" rounded="lg" style="font-family: 'noto'; margin-right: 30px;" >시나리오 보기</v-btn>
      <v-btn variant="tonal" @click="moveGenerate" size="x-large" rounded="lg" style="font-family: 'noto';" >시나리오 생성</v-btn>
      </div>

    </div>

    <div style="float: right; margin-top: 120px; margin-left: 150px;">
      <v-img :src="mainIMG" cover width="600" aspect-ratio="1/1"></v-img>
    </div>
    
    <v-row justify="center">
      
    </v-row>





</template>

<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}
.NursingText{
  font-family: 'noto';
  font-weight: bold;
  font-size: 40px;

}
.NursingText2{
  font-family: 'noto';
  font-weight: bold;
  font-size: 65px;
  margin-bottom: 50px;
  color: blueviolet;
}
.text-left{
  font-family: noto;
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  margin:auto
}
</style>