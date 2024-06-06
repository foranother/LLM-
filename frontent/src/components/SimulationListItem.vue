<script setup>
import { useSimulationStore } from '@/stores/simulations';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router'

const simulationStore = useSimulationStore()
const router = useRouter()

onMounted(() => {
    simulationStore.list()
})

function toSimDetail(id) {
    router.push('/list/' + id)
}
</script>

<template>
    <v-card flat width="100%">
        <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-video-input-component"></v-icon> &nbsp;
            Simulation List

            <v-spacer></v-spacer>

            <v-text-field prepend-inner-icon="mdi-magnify" density="compact" label="Search" single-line flat
                hide-details variant="solo-filled"></v-text-field>
        </v-card-title>

        <v-divider></v-divider>
        <v-data-table :headers="table_header" :items="simulationStore.data">

            <template v-slot:item.id="{ item }">
                <div style="max-width: 100px;" class="d-inline-block text-truncate">{{ item.id }}</div>
            </template>

            <template v-slot:item.created="{ item }">
                <div>{{ new Date(item.created).toLocaleDateString() }}</div>
            </template>

            <template v-slot:item.option="{ item }">
                <v-icon icon="mdi-eye" @click="toSimDetail(item.id)"></v-icon>
            </template>
        </v-data-table>
    </v-card>
</template>

<script>
export default {
    data: () => ({
        table_header: [
            { title: '번호', value: 'id' },
            { title: '시뮬레이션 시나리오 제목', value: 'title' },
            { title: '생성일', value: 'created' },
            { title: '보기', value: 'option' }
        ]
    })
}
</script>