<script setup lang="ts">
import { ref } from 'vue';
let t = setTimeout(time, 1000);
let nowtime = ref("");
function pad(num: number, cover: number) {
    return String("0".repeat(cover) + num).slice(-cover);
}
function time() {
    clearTimeout(t);
    let dt = new Date();
    let y = dt.getFullYear();
    let mt = dt.getMonth() + 1;
    let day = dt.getDate();
    let h = dt.getHours();
    let m = dt.getMinutes();
    let s = dt.getSeconds();
    nowtime.value = y + '年' + mt + '月' + day + '日' + ' - ' + pad(h,2) + ' : ' + pad(m,2) + ' : ' + pad(s,2);
    // document.querySelector("#clock").innerHTML = y + '年' + mt + '月' + day + '日' + ' - ' + h + ' : ' + m + ' : ' + s;
    t = setTimeout(time, 1000);
}
</script>

<template>
    <div id='webhead'>
        <h1>信息检索系统</h1>
        <span id="clock">{{ nowtime }}</span>
    </div>
</template>

<style>
#webhead {
    position: relative;
    height: 60px;
}

#clock {
    position: absolute;
    top: 20px;
    right: 100px;
    width: 200px;
    height: 60px;
}
</style>