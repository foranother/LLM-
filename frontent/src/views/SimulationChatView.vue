<script setup>
import ChatBoxItem from '@/components/ChatBoxItem.vue';
import { useSimulationStore } from '@/stores/simulations';
import { onMounted } from 'vue';
import { routerKey, useRoute, useRouter } from 'vue-router';
import { ref, computed } from 'vue';

const simulationStore = useSimulationStore()
const route = useRoute()
const router = useRouter()
const showAddMemberDialog = ref(false)
const showAlert = ref(false)
const regenerating = ref(false)
const scenarioing = ref(false)
const isLoading = ref(false)

const emailInput = ref('')

const alert = ref({
  type: 'success',
  icon: '$success',
  title: 'Success',
  message: 'Successfully adding a member to this simulation.'
})

onMounted(() => {
  simulationStore.get(route.params.id)

})

function setAlert(type, icon, title, message) {
  alert.value = {
    type, icon, title, message
  }
  showAlert.value = true
}
const contentCompute = computed(() => {
  var bold = /\*\*(.*?)\*\*/gm;
  return simulationStore.detail?.content?.replace(/\n/g, "<br>").replace(bold, '<strong>$1</strong>')

})

function addMemberClicked() {

  simulationStore.addMember(emailInput.value, route.params.id).then(res => {
    setAlert('success', '$success', 'Success', 'Successfully adding a member to this simulation.')
    emailInput.value = ''
  }).catch(err => {
    setAlert('error', '$error', 'Error', err.response.data.email[0])
  })
}

function regenerateClicked(){
            isLoading.value = true
            regenerating.value = true
            setTimeout(() => {
            console.log(route.params.id)
            const sim_id = route.params.id
            simulationStore.regenerate(sim_id).then(() => {
              router.go(0).catch(err => {
                console.error(err);
                console.log('finish')
            });
            });
            }, 500);
        }

function scenarioClicked(){
            scenarioing.value = true
            setTimeout(() => {
            console.log(route.params.id)
            const sim_id = route.params.id
            simulationStore.scenario(sim_id).then(() => {
              router.push({path:'/open-list/', force: true}).catch(err => {
                console.error(err);
                console.log('finish')
            });
            });
            }, 500);
        }

</script>

<template>
  <div class="spinner-div" v-if="isLoading">
    <q-spinner-cube
    color="primary"
    size="5em"
  /></div>
  <v-container class="px-12">
    <v-row>
      <v-col cols="12" md="7" lg="8">
        <v-card>
          <v-card-title style="font-family: 'noto';">
            {{ simulationStore.detail.title }}
            <v-btn icon="mdi-account-plus" variant="outlined" class="float-right"
              @click="showAddMemberDialog = true"></v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="overflow-auto">

            <p class="overflow-auto" v-html="contentCompute" style="max-height: 700px; min-height: 400px; font-family: 'noto';"></p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="5" lg="4">
        <ChatBoxItem></ChatBoxItem>
        <v-btn @click="regenerateClicked" variant="outline-primary" elevation="4" rounded="lg" size="large" class="btn">ReGenerate</v-btn>
        <v-btn @click="scenarioClicked" variant="light" elevation="4" rounded="lg" size="large" class="btn">시나리오 생성</v-btn>
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

<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}

.btn{
  margin-top: 30px;
  margin-left: 10px;
  margin-right: 10px;
  font-family: 'noto';
}
</style>