<template>
    <div class="flex justify-center my-3">
        <section class="mx-2">
            <label>銀行名稱</label>
            <div class="relative w-[16rem]">
                <button @click="toggle" :class="(open) && 'ring-blue-600'" class="flex w-full items-center justify-between rounded bg-white p-2 ring-1 ring-gray-300">
                    <span class="text-gray-300">請輸入關鍵字或銀行代碼...</span>
                    <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </button>

                <ul v-if="open" class="z-2 absolute mt-1 w-full rounded bg-gray-50 ring-1 ring-gray-300" x-show="open">
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('Python')">Python</li>
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('PHP')">PHP</li>
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('C#')">C#</li>
                </ul>
            </div>
            <div class="text-gray-500 text-sm">可使用下拉選單或直接輸入關鍵字查詢</div>
        </section>
        <section>
            <label>分行名稱</label>
            <div class="relative w-[10rem]">
                <button @click="toggle" :class="(open) && 'ring-blue-600'" class="flex w-full items-center justify-between rounded bg-white p-2 ring-1 ring-gray-300">
                    <span class="text-gray-300">請選擇分行名稱</span>
                    <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </button>
                <ul v-if="open" class="z-2 absolute mt-1 w-full rounded bg-gray-50 ring-1 ring-gray-300" x-show="open">
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('Python')">Python</li>
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('PHP')">PHP</li>
                    <li class="cursor-pointer select-none p-2 hover:bg-gray-200" @click="setLanguage('C#')">C#</li>
                </ul>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    data() {
      return {
        open: false,
        language: ''
      }
    },
    methods: {
        toggle() {
            this.open = !this.open;
        },
        setLanguage(val) {
            this.language = val;
            this.open = false;
        }
    }
}; 
</script>