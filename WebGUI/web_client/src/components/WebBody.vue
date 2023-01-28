<script setup lang="ts">
import { h, ref, Ref, watchEffect } from 'vue'
import { useMessage } from 'naive-ui'
import { NAlert, NButton, NIcon, NInput, NScrollbar } from 'naive-ui'
import type { MessageRenderMessage } from 'naive-ui'
import axios from 'axios'

window.$message = useMessage()
function pad(num: number, cover: number) {
    return String("0".repeat(cover) + num).slice(-cover);
}
function getTime() {
    let dt = new Date();
    let y = dt.getFullYear();
    let mt = dt.getMonth() + 1;
    let day = dt.getDate();
    let h = dt.getHours();
    let m = dt.getMinutes();
    let s = dt.getSeconds();
    return y + '.' + mt + '.' + day + ' -  ' + pad(h, 2) + ' : ' + pad(m, 2) + ' : ' + pad(s, 2);
}


const renderMessage: MessageRenderMessage = (props) => {
    const { content, type } = props
    console.log(props);
    return h(
        // NAlert,
        {
            type: type === 'loading' ? 'default' : type,
            title: content,
            style: {
                boxShadow: 'var(--n-box-shadow)',
                maxWidth: 'calc(100vw - 32px)',
                width: '480px'
            }
        },{
            default:() => props.content 
        }
    )
}
let textValue = ref('');
let getResult = ref(false)
let result: Ref<any>
result = ref([])

function search() {
    if (textValue.value == '')
        window.$message.error('请输入数据');
    else {
        let url = 'http://127.0.0.1:5000/api'
        axios.post(url, {
            text: textValue.value
        }).then(res => {
            result.value = []
            let ret = res.data.data
            result.value = ret
            getResult.value = true
        }).catch(err => {
            console.log(err);
        })
    }
}

</script>

<template>
    <div id='mainbox'>
        <div id='controlboard'>
            <div style="margin:10px 0 10px 0">
                <h2>文档搜索：</h2>
            </div>
            <n-input v-model:value="textValue" type="text" placeholder="请输入搜索信息" />
            <n-button style="margin:10px 0 10px 0" type='primary' @click='search'>
                搜索
            </n-button>
            <div class="leftbox" v-show='getResult'>
                <n-scrollbar style='margin:10px 0 0 0'>
                    <span>当前搜索结果数(最大5条): {{ result.length }}</span>
                </n-scrollbar>
            </div>
        </div>



        
        <div id='printboard'>
            <div style="margin: 10px 0 0 20px; text-align:left">
                <h3>
                    搜索结果如下：
                </h3>
            </div>
            <div class="myscrollbarbox">
                <n-scrollbar>
                    <div v-for="(item, index) in result">
                        <h4>标题：{{ item.title }}</h4>
                        <span>原文链接：<a :href='item.url' target='_blank'>{{ item.url }}</a></span><br>
                        <span>相关性：{{ item.correlation }}</span><br>
                    </div>
                    <!-- <span v-for="(item, index) in result" style = 'font-weight: bolder;'>
                        标题：{{ item.title }}<br>
                        原文链接：{{ item.url }}<br>
                        相关性：{{ item.correlation }}<br>
                        <br>
                    </span> -->
                </n-scrollbar>
            </div>
        </div>
    </div>
</template>

<style>
#mainbox {
    display: flex;
    flex-flow: row nowrap;
    margin: 0 auto;
    width: 90%;
    height: 600px;
}

#printboard {
    flex: 3;
    margin: 20px 60px 20px 100px;
    background-color: white;
    padding: 20px 20px 20px 20px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
}

#controlboard {
    flex: 2;
    margin: 20px 20px 20px 20px;
    padding: 40px 40px 40px 40px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    text-align: left;
}

#div1 {
    margin: 20px 20px 20px 20px;
}

#div2 {
    margin: 20px 20px 20px 20px;
}

.myscrollbarbox {
    margin: 10px 10px 20px 20px;
    padding: 10px 10px 20px 20px;
    background-color: rgba(198, 198, 198, 0.6);
    text-align: left;
    width: 90%;
    height: 80%;
    border-radius: 10px;
}

.mybtn {
    width: 100%;
    height: 100%;
}

.statediv {
    margin: 10px 0 10px 0;
}

.leftbox {
    width: 90%;
    height: 60%;
    margin: 10px 0 0 0;
    padding: 10px 10px 20px 20px;
    background-color: rgba(198, 198, 198, 0.666);
    border-radius: 10px;
}
</style>