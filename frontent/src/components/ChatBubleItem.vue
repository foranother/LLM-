<template>
    <v-row v-if="user?.current_user">
        <v-spacer></v-spacer>
        <v-col cols="8">
            <span class="text-subtitle-2 text-right">{{ user?.display_name }}</span>
            <v-sheet rounded="lg" class="mx-auto pa-2 text-body-2" color="primary">
                {{ message }}
            </v-sheet>
        </v-col>
        <v-col cols="auto"> <v-avatar size="32">

                <v-img alt="John" :src="user?.photo_url"></v-img>
            </v-avatar></v-col>
    </v-row>

    <v-row v-else>
        <v-col cols="auto"> <v-avatar size="32">

                <v-img alt="John" :src="user?.photo_url"></v-img>
            </v-avatar></v-col>
        <v-col cols="8">
            <span class="text-subtitle-2">{{ user?.display_name }}</span>
            <v-sheet rounded="lg" class="mx-auto pa-2 text-body-2" color="secondary">
                {{ message }}
            </v-sheet>
        </v-col>
        <v-spacer></v-spacer>
    </v-row>

</template>

<script>
import { reactive, toRefs } from 'vue'

export default {
    props: ['message', 'user'],
    setup() {
        const state = reactive({
            count: 0,
        })

        return {
            ...toRefs(state),
        }
    }
}
</script>

<style lang="scss" scoped></style>