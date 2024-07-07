<template>
    <div class="m-auto w-[60%] bg-sky-300/25 px-2 py-3" v-if="branch">
        <div class="flex">
            <p class="text-3xl">{{ branch.headOffice }}</p>
            <p class="text-3xl">{{ branch.headOfficeCode }}</p>
            <p class="text-3xl">{{ branch.branchOffice }}</p>
        </div>
        <div class="flex items-center">
            <p class="text-lg me-2">分行代碼：{{ branch.branchOfficeCode }}</p>
            <button class="sm-btn" @click="copyCode">{{ codeButton }}</button>
        </div>
        <p class="text-lg">地址：{{ branch.address }}</p>
        <div class="flex justify-between">
            <p class="text-lg">電話：{{ branch.tel }}</p>
            <div class="flex items-center">
                <p class="text-sm text-gray-400">資料來源：</p>
                <a href="https://data.gov.tw/dataset/6041" class="text-gray-400 text-sm flex items-end">政府資料開放平台</a>
            </div>
            
        </div>
    </div>
    <div class="flex justify-center my-2">
        <button class="md-btn me-5" @click="resetSearch">重新查詢</button>
        <button class="md-btn-full" @click="copyLink">{{ linkButton }}</button>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  props: {
    branch: {
      type: Object,
      required: true,
    }
  },
  emits: ['resetSearch'],
  setup(props, { emit }) {
    const route = useRoute();
    const branch = ref(null);
    const codeButton = ref('複製代碼');
    const linkButton = ref('複製此頁面連結');

    const fetchBranchDetails = (branchOfficeCode) => {
      const apiUrl = import.meta.env.VITE_API_URL;
      axios.get(`${apiUrl}api/v1/banks/detail/${branchOfficeCode}/`)
        .then(response => {
          branch.value = response.data;
        })
        .catch(error => {
          console.error("沒有抓到詳細資料", error);
        });
    };

    onMounted(() => {
      const branchOfficeCode = route.params.branchOfficeCode;
      if (branchOfficeCode) {
        fetchBranchDetails(branchOfficeCode);
      }
    });

    watch(() => route.params.branchOfficeCode, (newBranchOfficeCode) => {
      if (newBranchOfficeCode) {
        fetchBranchDetails(newBranchOfficeCode);
      }
    });

    const copyCode = () => {
      if (branch.value) {
        const code = branch.value.branchOfficeCode;
      navigator.clipboard.writeText(code)
        .then(() => {
          codeButton.value = '已複製';
          setTimeout(() => {
            codeButton.value = '複製代碼';
          }, 500);
        });
      }
    };

    const copyLink = () => {
      if (branch.value) {
        const baseUrl = import.meta.env.VITE_Base_URL;
      const url = `${baseUrl}${branch.value.headOfficeCode}/${branch.value.branchOfficeCode}/${branch.value.headOffice}-${branch.value.branchOffice}.html`;
      navigator.clipboard.writeText(url)
        .then(() => {
          linkButton.value = '已複製';
          setTimeout(() => {
            linkButton.value = '複製此頁面連結';
          }, 500);
        });
      }
    };

    const resetSearch = () => {
      emit('resetSearch');
    };

    return {
      branch,
      codeButton,
      linkButton,
      copyCode,
      copyLink,
      resetSearch,
    };
  },
};
</script>
