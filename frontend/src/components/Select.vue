<template>
    <div class="flex justify-center my-3">
        <section class="mx-2">
            <label>銀行名稱</label>
            <div class="relative w-[16rem]">
              <div class="flex w-full items-center justify-between rounded bg-white p-2 ring-1 ring-gray-300">
                <input v-model="search" @click="toggleHeadOffice" @focus="openHeadOffice" 
                @input="filterHeadOffices" 
                class="w-full outline-none" 
                placeholder="請輸入關鍵字或銀行代碼..." />
                <font-awesome-icon :icon="['fas', 'chevron-down']" @click="toggleHeadOffice"/>
              </div>
                <ul v-if="openHeadOffice" v-show="filteredHeadOffices" class="z-2 absolute mt-1 w-full rounded bg-gray-50 ring-1 ring-gray-300 max-h-60 overflow-y-auto">
                    <li v-if="filteredHeadOffices.length === 0" class="w-full rounded bg-gray-50 text-center py-2">
                      {{ message }}
                    </li>
                    <li v-for="headOffice in filteredHeadOffices" :key="headOffice.id" @click="selectHeadOffice(headOffice, headOffice.headOfficeCode)" class="cursor-pointer p-2 hover:bg-gray-200">{{ headOffice.headOfficeCode }} {{ headOffice.headOffice }}</li>
                </ul>
            </div>
            <div class="text-gray-500 text-sm">可使用下拉選單或直接輸入關鍵字查詢</div>
        </section>
        <section>
            <label>分行名稱</label>
            <div class="relative w-[10rem]">
                <button @click="toggleBranch" :disabled="!selectedHeadOffice" :class="(openBranch) && 'ring-blue-600'" class="flex w-full items-center justify-between rounded bg-white p-2 ring-1 ring-gray-300">
                    <span :class="{'text-gray-300': !selectedBranch, 'text-gray-700': selectedBranch}">{{ selectedBranch ? selectedBranch.branchOffice : '請選擇分行名稱' }}</span>
                    <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </button>
                <ul v-if="openBranch" class="z-2 absolute mt-1 w-full rounded bg-gray-50 ring-1 ring-gray-300 max-h-60 overflow-y-auto" >
                    <li v-for="branch in branches" :key="branch.id" @click="selectBranch(branch)" class="cursor-pointer p-2 hover:bg-gray-200">{{ branch.branchOffice }}</li>
                </ul>
            </div>
        </section>
    </div>
    <router-view :branch="selectedBranchDetails" @resetSearch="resetSearch"></router-view>
</template>


<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import axios from 'axios';
import Detail from './Detail.vue';

export default {
  components: {
    Detail  
  },
  setup(){
    const route = useRoute();
    const router = useRouter();
    const search = ref('');
    const openHeadOffice = ref(false);
    const openBranch = ref(false);
    const headOffices = ref([]);
    const branches = ref([]);
    const selectedHeadOffice = ref(null);
    const selectedHeadOfficeCode = ref(null);
    const selectedBranch = ref(null);
    const selectedBranchDetails = ref(null);
    const filteredHeadOffices = ref([]);
    const message = ref('');


    const toggleHeadOffice = () => {
      openHeadOffice.value = !openHeadOffice.value;
    };

    const toggleBranch = () => {
      openBranch.value = !openBranch.value;
    };

    const fetchHeadOffices = async () => {
      const apiUrl = import.meta.env.VITE_API_URL;
      try {
        const response = await axios.get(`${apiUrl}api/v1/banks/head_offices/`);
        headOffices.value = response.data;
        filteredHeadOffices.value = response.data;
        if (route.params.headOfficeCode) {
          getCodeOfficesFromRoute();
        }
      } catch (error) {
        console.error("沒有抓到總行", error);
      }
    };

    const filterHeadOffices = () => {
      filteredHeadOffices.value = headOffices.value.filter((h) => {
        return (
          h.headOffice.includes(search.value) ||
          h.headOfficeCode.includes(search.value)
        );
      });
      if(filteredHeadOffices.value.length === 0){
        return message.value = "無相關資料"
      }
    };
    const selectHeadOffice = (headOffice, headOfficeCode) => {
      selectedHeadOffice.value = headOffice;
      selectedHeadOfficeCode.value = headOfficeCode;
      search.value = `${headOffice.headOfficeCode} ${headOffice.headOffice}`;
      openHeadOffice.value = false;
      fetchBranches(headOffice.headOfficeCode);
    };

    const fetchBranches = async () => {
      const apiUrl = import.meta.env.VITE_API_URL;
      if (selectedHeadOffice.value) {
        try {
          const response = await axios.get(`${apiUrl}api/v1/banks/branches/`, {
            params: {
              head_office: selectedHeadOffice.value.headOffice
            }
          });
          branches.value = response.data;
          if (route.params.branchOfficeCode) {
            getBranchFromRoute();
          }
        } catch (error) {
          console.error("沒有抓到分行", error);
        }
      }
    };

    const selectBranch = (branch) => {
      selectedBranch.value = branch;
      openBranch.value = false;
      fetchBranchDetails(branch.branchOfficeCode);
    };

    const fetchBranchDetails = async (branchOfficeCode) => {
      const apiUrl = import.meta.env.VITE_API_URL;
      try {
        const response = await axios.get(`${apiUrl}api/v1/banks/detail/${branchOfficeCode}/`);
        selectedBranchDetails.value = response.data;
        router.push({
          name: 'Detail',
          params: {
            headOfficeCode: selectedBranchDetails.value.headOfficeCode,
            branchOfficeCode: selectedBranchDetails.value.branchOfficeCode,
            headOffice: selectedBranchDetails.value.headOffice,
            branchOffice: selectedBranchDetails.value.branchOffice,
          }
        });
      } catch (error) {
        console.error("沒有抓到詳細資料", error);
      }
    };

    const resetSearch = () => {
      selectedHeadOffice.value = null;
      selectedBranch.value = null;
      selectedBranchDetails.value = null;
      headOffices.value = [];
      branches.value = [];
      search.value = "";
      router.push({ path: '/' });

    };

    const getCodeOfficesFromRoute = () => {
      const { headOfficeCode, branchOfficeCode, headOffice } = route.params;
      if (headOfficeCode) {
        selectedHeadOffice.value = headOffices.value.find(h => 
        h.headOfficeCode === headOfficeCode);
        if (selectedHeadOffice.value && branchOfficeCode) {
          fetchBranches(headOfficeCode);
          search.value = `${selectedHeadOffice.value.headOffice} ${selectedHeadOffice.value.headOfficeCode}`;
        }
      }
    };
    
    const getBranchFromRoute = () => {
      const { branchOfficeCode } = route.params;
      if (branchOfficeCode) {
        selectedBranch.value = branches.value.find(b => b.branchOfficeCode === branchOfficeCode);
      }
    };

    onMounted(() => {
      fetchHeadOffices();
    });

    return {
      search,
      openHeadOffice,
      openBranch,
      headOffices,
      branches,
      selectedHeadOffice,
      selectedBranch,
      selectedBranchDetails,
      filterHeadOffices,
      toggleHeadOffice,
      filteredHeadOffices,
      selectHeadOffice,
      toggleBranch,
      selectBranch,
      resetSearch,
      message,
    };
  },
};
</script>
