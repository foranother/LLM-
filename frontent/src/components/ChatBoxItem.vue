<script setup>

import { useSimulationStore } from '@/stores/simulations';
import ChatBubleItem from './ChatBubleItem.vue'
import { nextTick, onBeforeUnmount, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { doc, query, where, onSnapshot, limit } from "firebase/firestore";
import { useDBStore } from '@/stores/db';



const simulationStore = useSimulationStore()
const dbStore = useDBStore()
const route = useRoute()
const firstInit = ref(true)

const message = ref('')
var unsub = null
const fetched = ref(false)
const maxScroll = ref(0)
const scrollTop = ref(0)

async function load({ done }) {
    // Perform API call
    if (fetched.value) {

        done('empty')
        return
    }
    const res = await simulationStore.getChat(route.params.id)
    setTimeout(() => {
        if (res.data) {
            if (res.data.length > 0) {
                done('ok')
            } else {
                done('empty')
            }


        } else {
            done('error')
        }
    }, 300)
    fetched.value = true
}

onMounted(() => {
    if (unsub == null) {

        const q = query(doc(dbStore.getDb(), "chats", route.params.id))
        unsub = onSnapshot(q, (doc) => {
            if (firstInit.value) {
                firstInit.value = false
            } else {
                simulationStore.fetchRealtimeChat(doc.data())
                nextTick(() => {
                    if (maxScroll.value - scrollTop.value <= 50) {
                        document.getElementById('chat-box').scrollTo(0, 999999999)
                    }
                })
            }
        });
    }
})

onBeforeUnmount(() => {
    if (unsub != null) {
        unsub()
    }
})

function sendChatClick() {
    simulationStore.sendChat(message.value, route.params.id)

    message.value = ''
}

function onScroll(e) {
    scrollTop.value = e.target.scrollTop
    maxScroll.value = Math.max(scrollTop.value, maxScroll.value)
}
</script>

<template>
    <v-card>
        <v-card-title primary-title>
            
            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn icon="mdi-account-multiple" v-bind="props" variant="text" class="float-right"
                        @click="showAddMemberDialog = true"></v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="(item, index) in simulationStore.detail?.members" :key="index" :value="index"
                        :prepend-avatar="item.photo_url" :subtitle="item.email" :title="item.display_name">

                    </v-list-item>
                </v-list>
            </v-menu>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
            <v-infinite-scroll id="chat-box" v-scroll.self="onScroll" :onLoad="load" :height="550" :items="items"
                side="start" style="scrollbar-width: thin;">

                <template v-for="(item, index) in simulationStore.chats" :key="item">
                    <!-- <div :class="['pa-2', index % 2 === 0 ? 'bg-grey-lighten-2' : '']">
                        Item #{{ item }}
                    </div> -->

                    <v-col>
                        <ChatBubleItem :message="item.content" :user="simulationStore.memberHashMap[item.sender]" />
                    </v-col>
                </template>

                <template v-slot:empty></template>
            </v-infinite-scroll>

        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="px-6">
            <v-text-field v-model="message" placeholder="Chat.." variant="outlined" id="chat" rounded="xl"
                v-on:keyup.enter="sendChatClick" density="compact" hide-details style="font-family: 'noto';"></v-text-field>
            <v-btn icon="mdi-send" @click="sendChatClick"></v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>

export default {
    data: () => ({
        items: [0],
    }),
    methods: {
        async api() {
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve(Array.from({ length: 10 }, (k, v) => v + this.items.at(-1) + 1));
                }, 1000);
            });
        },

    },
    components: { ChatBubleItem }
}
</script>

<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}
</style>