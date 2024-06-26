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
    <section v-if="selectedBranchDetails">
        <Detail :branch="selectedBranchDetails" @resetSearch="resetSearch"/>
    </section>
</template>


<script>
import axios from 'axios';
import Detail from './Detail.vue';

export default {
  components: {
    Detail  
  },
  data() {
    return {
      openHeadOffice: false,
      openBranch: false,
      headOffices: [],
      branches: [],
      selectedHeadOffice: null,
      selectedBranch: null,
      selectedBranchDetails: null,
      filteredHeadOffices: [],
      search: '',
    }
  },
  methods: {
    toggleHeadOffice() {
      this.openHeadOffice = !this.openHeadOffice;
    },
    toggleBranch() {
      this.openBranch = !this.openBranch;
    },
    fetchHeadOffices() {
      const apiUrl = import.meta.env.VITE_API_URL;
      axios.get(`${apiUrl}api/v1/banks/head_offices/`)
        .then(response => {
          this.headOffices = response.data;
          this.filteredHeadOffices = response.data;
        })
        .catch(error => {
          console.error("沒有抓到總行", error);
        });
    },
    filterHeadOffices() {
      this.filteredHeadOffices = this.headOffices.filter((h) => {
        return (
          h.headOffice.includes(this.search) ||
          h.headOfficeCode.includes(this.search)
        );
      });
      if(this.filteredHeadOffices.length === 0){
        return this.message = "無相關資料"
      }
    },
    selectHeadOffice(headOffice, headOfficeCode) {
      this.selectedHeadOffice = headOffice;
      this.selectedHeadOfficeCode = headOfficeCode;
      this.search = `${headOffice.headOfficeCode} ${headOffice.headOffice}`;
      this.openHeadOffice = false;
      this.fetchBranches();
    },
    fetchBranches() {
      const apiUrl = import.meta.env.VITE_API_URL;
      axios.get(`${apiUrl}api/v1/banks/branches/`, {
        params: {
          head_office: this.selectedHeadOffice.headOffice
        }
      })
        .then(response => {
          this.branches = response.data;
        })
        .catch(error => {
          console.error("沒有抓到分行", error);
        });
    },
    selectBranch(branch) {
      this.selectedBranch = branch;
      this.openBranch = false;
      this.fetchBranchDetails(branch.id);
    },
    fetchBranchDetails(branchId) {
      const apiUrl = import.meta.env.VITE_API_URL;
      axios.get(`${apiUrl}api/v1/banks/detail/${branchId}/`)
        .then(response => {
          this.selectedBranchDetails = response.data;
          this.$router.push({
            name: 'Detail',
            params: {
              headOfficeCode: this.selectedBranchDetails.headOfficeCode,
              branchOfficeCode: this.selectedBranchDetails.branchOfficeCode,
              headOffice: this.selectedBranchDetails.headOffice,
              branchOffice: this.selectedBranchDetails.branchOffice,
            }
          });
        })
        .catch(error => {
          console.error("沒有抓到詳細資料", error);
        });
    },
    resetSearch() {
      this.selectedHeadOffice = null;
      this.selectedBranch = null;
      this.selectedBranchDetails = null;
      this.headOffices = [];
      this.branches = [];
      this.fetchHeadOffices();
      this.filterHeadOffices();
      this.search ="";
      this.$router.push({ path: '/' });
    }
  },
  mounted() {
    this.fetchHeadOffices();
  }
};
</script>