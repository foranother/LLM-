<script setup>

import LoginIMG from '@/assets/login-img.jpg'
import { useAuthStore } from '@/stores/auth';
import { useRouter, useRoute } from 'vue-router';


const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()


function logoutClick() {
    authStore.login().then(() => {
        router.push({ path: route.query.redirect || '/' })
    })
}
</script>

<template>
    <v-layout class="rounded rounded-md">

        <v-main class="d-flex align-center justify-center" style="height: 100vh;">

            <v-container>
                <v-row align="center" justify="space-around">
                    <v-col class="text-center" cols="0" sm="0" md="6" lg="6">
                        <v-img :src="LoginIMG" cover class="mx-auto" aspect-ratio="1/1"></v-img>
                    </v-col>
                    <v-col class="text-center" cols="6" sm="12" md="6" lg="4">
                        <h1 class="mb-6">SimNurse</h1>
                        <div class="mb-6">로그인 또는 회원가입을 완료한 후
                            멋진 시뮬레이션 시나리오를 생성 해보세요!</div>

                        <v-btn variant="outlined" size="large" block prepend-icon="mdi-google" class="overflow-hidden"
                            @click="logoutClick">Google
                            계정으로 로그인
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-layout>
</template>
