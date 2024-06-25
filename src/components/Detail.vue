<template>
    <div class="m-auto w-[60%] bg-sky-300/25 px-2 py-3">
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

export default {
  props: {
    branch: {
      type: Object,
      required: true,
      default: () => ({})
    }
  },
  data() {
    return {
        codeButton: '複製代碼',
        linkButton: '複製此頁面連結',
    };
  },
  methods: {
    copyCode() {
      const code = this.branch.branchOfficeCode;
      navigator.clipboard.writeText(code)
      .then(() => {
        this.codeButton = '已複製';
        setTimeout(()=>{
            this.codeButton = '複製代碼'
        },500)
      });
    },
    
    resetSearch() {
      this.$emit('resetSearch');
    },
    copyLink() {
      navigator.clipboard.writeText(window.location.href)
      .then(() => {
        this.linkButton = '已複製';
        console.log(this.isCopied);
        setTimeout(()=>{
            this.linkButton = '複製此頁面連結';
        },500)
        console.log(window.location.href);
      });
    }
  }
};
</script>