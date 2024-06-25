<template>
    <div class="m-auto w-[60%] bg-sky-300/25 px-2 py-3">
        <div class="flex">
            <p class="text-3xl">{{ branch.headOffice }}</p>
            <p class="text-3xl">{{ branch.headOfficeCode }}</p>
            <p class="text-3xl">{{ branch.branchOffice }}</p>
        </div>
        <div class="flex items-center">
            <p class="text-lg me-2">分行代碼：{{ branch.branchOfficeCode }}</p>
            <button class="sm-btn">複製代碼</button>
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
        <button class="md-btn-full" @click="copyPageLink">複製此頁面連結</button>
    </div>
</template>

<script>

export default {
  props: {
    branch: {
      type: Object,
      required: true,
      default: () => ({})
    }
  },
  methods: {
    copyCode(code) {
      navigator.clipboard.writeText(code).then(() => {
        alert('分行代碼已複製');
      });
    },
    resetSearch() {
      this.$emit('resetSearch');
    },
    copyPageLink() {
      navigator.clipboard.writeText(window.location.href).then(() => {
        alert('頁面連結已複製');
      });
    }
  }
};
</script>