<script setup>
import { useSimulationStore } from '@/stores/simulations';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ref, computed, useSlots } from 'vue';
import mainIMG  from '@/assets/간호사진.png'


const simulationStore = useSimulationStore()
const route = useRouter()
const showAddMemberDialog = ref(false)
const showAlert = ref(false)
const slots = useSlots()
const slotProps = { message: 'Hello from slot props!' }
const imgurl = ref('')

onMounted(() => {
  simulationStore.get(route.params.id).then(() => {
    // 여기서 console.log를 통해 detail이 올바르게 로드되었는지 확인
    console.log('Detail after fetching:', simulationStore.detail);
    if (simulationStore.detail) {
      imgurl.value = simulationStore.detail.imgurl;
    }
  });
});
console.log(imgurl)

if (slots.default) {
  // 디버깅을 위해 슬롯 호출
  console.log(slots.default(slotProps));
}

const emailInput = ref('')
console.log(simulationStore.detail)
const alert = ref({
  type: 'success',
  icon: '$success',
  title: 'Success',
  message: 'Successfully adding a member to this simulation.'
})

function setAlert(type, icon, title, message) {
  alert.value = {
    type, icon, title, message
  }
  showAlert.value = true
}
const contentCompute = computed(() => {
  var bold = /\*\*(.*?)\*\*/gm;
  return simulationStore.detail?.scenario?.replace(/\n/g, "<br>").replace(bold, '<strong>$1</strong>')

})



</script>

<template>
  <v-container class="px-12">
    <img :src="mainIMG" width="600" height="500" alt="Main Image" />
  </v-container>
  
  <v-container class="px-12">
    <v-row>
      <v-col cols="12" md="7" lg="11">
        <v-card>
          <v-card-title style="font-family: 'noto';" >
            {{ simulationStore.detail.title }}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="overflow-auto">
            <p class="overflow-auto" v-html="contentCompute" style="max-height: 700px; min-height: 400px; font-family: 'noto';"></p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showAddMemberDialog" max-width="400">
      <v-card prepend-icon="mdi-account-plus" title="Add member">
        <v-card-text>
          <v-text-field v-model="emailInput" name="email" label="email" id="id" variant="outlined" density="compact"
            class="mt-2" hide-details></v-text-field>

          <v-alert v-if="showAlert" class="mt-4" :color="alert.type" :icon="alert.icon" :title="alert.title"
            :text="alert.message"></v-alert>
        </v-card-text>


        <template v-slot:actions>
          <v-spacer></v-spacer>

          <v-btn @click="addMemberClicked">
            Save
          </v-btn>
        </template>
      </v-card>
    </v-dialog>

  </v-container>
</template>
