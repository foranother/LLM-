<script setup>
import { useSimulationStore } from '@/stores/simulations';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { ref, computed } from 'vue';
import mainIMG  from '@/assets/patient.jpg'

const simulationStore = useSimulationStore()
const route = useRoute()
const showAddMemberDialog = ref(false)
const showAlert = ref(false)

const emailInput = ref('')

const alert = ref({
  icon: '$success',
  title: 'Success',
  message: 'Successfully adding a member to this simulation.'
})
console.log(route.params.id)
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

</script>

<template>
  <v-container class="px-12">
    <img :src="mainIMG" width="600" height="500" alt="Main Image" />
  </v-container>
  <v-container class="px-12">
    <v-row>
      <v-col cols="12" md="7" lg="12">
        <v-card>
          <v-card-title style="font-family: 'noto';">
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
