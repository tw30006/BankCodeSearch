<template>
    <div class="flex-col">
            <header class="text-5xl bg-sky-700/25 text-center p-5">台灣銀行代碼查詢</header>
        <Select/>
        <Detail/>
        <footer class="text-center text-sm">powered by <a href="https://5xcampus.com/">5xCampus</a></footer>
    </div>
    
</template>

<script setup>
    import Select from './components/Select.vue';
</script>

