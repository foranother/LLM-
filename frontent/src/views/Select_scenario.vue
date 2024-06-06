<script setup>
    import { useSimulationStore } from '@/stores/simulations'
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const simulationStore = useSimulationStore()
    const router = useRouter()
    const generating = ref(false)
    const showGenerating = ref(false)
    const isLoading = ref(false)
    console.log(router)

    const item = ref([])
    const client = ref(['이름', '성별', '나이', '종교', '키', '몸무게', '주호소', '입원경로', '사회력', '과거력', '과거수술력', '가족력', '알러지', '면역상태', '약물', '1차 진단명'])
    const title = ref('')
    const disease = ref('')
    const etc = ref('')

    function selectAll() {
    item.value = client.value.slice();
    }
    function deselectAll() {
    item.value = [];
    }
    function generateClicked(){
        generating.value = true
        isLoading.value = true
        console.log(isLoading.value)
        setTimeout(() => {
        showGenerating.value = true
        console.log(title.value, disease.value, item.value.join(", "), etc.value)
        simulationStore.generate(title.value, disease.value, item.value.join(", "), etc.value).then(() => {
            router.push('/list').catch(err => {
            console.error(err);
            console.log('finish')
        });
        });
        }, 500);
    }

</script>

<template>
    <div class="spinner-div" v-if="isLoading">
        <q-spinner-cube color="primary" size="5em" />
    </div>
    <v-container>
        <v-layout class="head" text-center>
            <v-flex><h2>간호 시뮬레이션 시나리오 제목을 입력하세요</h2></v-flex>
        </v-layout>
        <v-layout class="Title" text-center>
            <v-text-field v-model="title" label="간호 시뮬레이션 시나리오 제목"></v-text-field>
        </v-layout>
        <v-layout class="head" text-center>
            <v-flex><h2>메인 질병명을 입력하세요</h2></v-flex>
        </v-layout>
        <v-layout class="Title" text-center>
            <v-text-field v-model="disease" label="질병명"></v-text-field>
        </v-layout>
        <v-layout class="head" text-center>
            <v-flex><h2>가상환자의 원하는 속성을 클릭하세요</h2></v-flex>
        </v-layout>
        <v-layout class="checkbox-container" text-center>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="이름">이름(Name)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="성별">성별(Gender)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="나이">나이(Age)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="종교">종교(Religion)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="키">키(Height)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="몸무게">몸무게(Weight)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="주호소">주호소(Chief complaint)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="입원경로">입원경로(History of present illness)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="사회력">사회력(Social history)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="과거력">과거력(Past medical history)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="과거수술력">과거수술력(Past Surgical history & data)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="가족력">가족력(Family medical history)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="알러지">알러지(Allergies)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="면역상태">면역상태(Immunization)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="약물">약물(Medicaion)</div>
            <div class="checkbox_one"><input type="checkbox" class="checkbox-item" v-model="item" value="1차 진단명">1차 진단명(Primary diagnosis)</div>
        </v-layout>
        <v-btn rounded="sm" variant="outlined" class="all_button" @click="selectAll">전체 선택</v-btn>
        <v-btn rounded="sm" variant="outlined" class="all_button" @click="deselectAll">전체 해제</v-btn>
        <v-layout class="head" text-center>
            <v-flex><h2>그외 기타 정보를 입력하세요</h2></v-flex>
        </v-layout>
        <v-layout class="etc">
            <v-textarea v-model="etc" label = "여기에 입력하세요"></v-textarea>
        </v-layout>
        
        <v-btn rounded="sm" @click="generateClicked" variant="outlined" class="generate_button">Generate</v-btn>
    </v-container>
    <div class="spinner-div" v-if="isLoading"><q-spinner-cube color="primary" size="5em"/></div>

</template>

  
<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}
.head{
    margin-top: 30px;
    margin-bottom: 40px;
    font-family: 'noto'
}

.checkbox_one{
    margin-right: 10px;
    margin-bottom: 10px;
    font-family: 'noto'
}

.checkbox-item {
    margin-right: 10px;
    margin-left: 10px;
    white-space: nowrap;
    align-items: center;
    font-family: 'noto'
}


.checkbox-container {
    margin-bottom: 30px;
    display: flex;
    flex-wrap: wrap; /* 항목들이 컨테이너 너비를 초과하면 다음 줄로 내려감 */
    align-items: center;
    font-family: 'noto'
}

.all_button{
    margin-right: 20px;
    margin-bottom: 30px;
    font-family: 'noto'
}

.generate_button{
    margin-top: 20px;
    font-family: 'noto'
}
</style>