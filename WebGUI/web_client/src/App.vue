<script setup lang="ts">
import { NMessageProvider, NDialogProvider } from "naive-ui";
import WebHeader from './components/WebHeader.vue';
import WebBody from './components/WebBody.vue';
import WebTail from './components/WebTail.vue';
</script>

<template>
    <div id="building">
        <n-message-provider>
            <n-dialog-provider>
                <WebHeader />
                <WebBody />
                <WebTail />
            </n-dialog-provider>
        </n-message-provider>
    </div>
</template>

<style>
#app {
    display: flex;
    flex-flow: column nowrap;
    margin-top: 0;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 0;
}

body {
    margin: 0;
    padding: 0;
    border: 0;
}

#building {
    background: url("./bkg_server.jpg");
    width: 100%;
    height: 100%;
    position: fixed;
    background-size: 100% 100%;
}
</style>
