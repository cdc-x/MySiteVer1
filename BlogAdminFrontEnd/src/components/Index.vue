<template>
    <div class="home-container">
        <el-container>
            <!-- 导航栏头部  -->
            <el-header>
                <el-row>
                    <!-- 网站标题 -->
                    <el-col :span='4'>
                        <span class="site-name" @click="changePath('1')">&lt;/&gt; CDC</span>
                    </el-col>
                    <!-- 网站描述 -->
                    <el-col :span='16'>
                        <span class="site-desc" @click="changePath('1')">万事开头难, 然后中间难, 然后一直难...</span>
                    </el-col>
                    <!-- 网站头像 -->
                    <el-col :span='4'>
                        <div class="avatar" @click="changePath('4')">
                            <img src="@/assets/img/avatar.png">
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <el-scrollbar style="height:100%;">
                        <!-- 分类导航栏 -->
                        <el-menu :default-active="activePath" background-color="#e6e6e6" text-color="#848484" active-text-color="#0289F5">
                            <el-menu-item index="1"  @click="changePath('1')">
                                <i class="iconfont iconfont icon-code"></i>
                                <span slot="title">温故知新</span>
                            </el-menu-item>
                            <el-menu-item index="2" @click="changePath('2')">
                                <i class="iconfont icon-yingyong"></i>
                                <span slot="title">应用集市</span>
                            </el-menu-item>
                             <el-menu-item index="3" @click="changePath('3')">
                                <i class="iconfont icon-pengyouquan"></i>
                                <span slot="title">生活碎片</span>
                            </el-menu-item>
                            <el-menu-item index="4" @click="changePath('4')">
                                <i class="iconfont icon-wowowo"></i>
                                <span slot="title">关于我</span>
                            </el-menu-item>
                        </el-menu>
                    </el-scrollbar>
                </el-aside>

                <!-- 内容区域 -->
                <el-main>
                    <article-module v-if="activePath === '1'" :key="'1'" ref="articleRef"></article-module>
                    <application v-if="activePath === '2'" :key="'2'"></application>
                    <life-module v-if="activePath === '3'" :key="'3'"></life-module>
                    <about-me v-if="activePath === '4'" :key="'4'"></about-me>
                </el-main>
            </el-container>
        </el-container>

        <!-- 社交工具固定区域 -->
        <div class="contact">
            <button class="contact-btn wechat iconfont icon-weixin" @click="showContact('wechat')"></button>
            <button class="contact-btn qq iconfont icon-QQ" @click="showContact('qq')"></button>
            <button class="contact-btn gzh iconfont icon-daohang-gongzhonghaotixing" @click="showContact('gzh')"></button>
            <button class="contact-btn git iconfont icon-github-fill" @click="showContact('git')"></button>
        </div>

        <!-- 社交码显示区域 -->
        <div class="show-contact" v-if="isShowContact">
            <div class="contact-content">
                <el-card>
                    <div slot="header" class="clearfix" style="font-size: 20px; font-weight: bold;">
                        <span>{{contactTite}}</span>
                    </div>
                    <div style="height: 300px; width: 300px; margin: 0 auto;">
                        <img :src="contactImg" style="width: 100%; height: 100%">
                    </div>
                </el-card>
            </div>

            <!-- 二维码关闭按钮 -->
            <el-button icon="el-icon-close" circle class="contact-close" @click="closeContact()"></el-button>
        </div>

        

    </div>
    
</template>

<script>

import ArticleModule from "./ArticleModule.vue"
import Application from './Application.vue'
import LifeModule from './LifeModule.vue'
import AboutMe from './AboutMe.vue'

export default {
    components: {
        ArticleModule,
        Application,
        LifeModule,
        AboutMe
    },

    data(){
        return {
            // 当前的页面
            activePath: "1",
            // 点击展示社交二维码
            isShowContact: false,
            // 展示的平台
            contactTite: "",
            // 展示的二维码
            contactImg: "",
        }
    },

    methods: {
        // 改变当前路径
        changePath(path){
            if (this.$refs.articleRef) {
                this.$refs.articleRef.isArticleContent = false
                this.$refs.articleRef.queryInfo.searchContent = ''
                this.$refs.articleRef.queryInfo.searchTag = ''
                this.$refs.articleRef.getArticleList()
            }
            
            this.activePath = path
        },

        // 点击展示社交工具
        showContact(contactType){
            if (contactType == 'qq'){
                this.isShowContact = true
                this.contactImg = "/static/img/contact/qq.png"
                this.contactTite = "QQ号搜索: 1275500642"
            }else if (contactType == 'wechat'){
                this.isShowContact = true
                this.contactImg = "/static/img/contact/wechat.png"
                this.contactTite = "微信号搜索: CDC1275500642"
            }else if (contactType == 'gzh'){
                this.isShowContact = true
                this.contactImg = "/static/img/contact/gzh.png"
                this.contactTite = "公众号"
            }else if (contactType == 'git'){
                window.open("https://github.com/cdc-x" ,"_blank")
            }
        },

        // 关闭社交平台二维码
        closeContact(){
            this.isShowContact = false
            this.contactTite = ''
            this.contactImg = ''
        }
    },

    created() {
       
    },

    
}
</script>

<style scoped>
    .home-container {
        height: 100%;
        background-color: #e6e6e6;
    }

    .el-header {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 999;
        background-color: rgba(255, 255, 255, .7);
        backdrop-filter: blur(5px);
    }

    .el-aside {
        position: fixed;
        top: 70px;
        left: 10%;
        height: 100%;
    } 

    .el-main {
        position: fixed;
        right: 0;
        width: 80%;
        height: 100%;
        padding: 0;
    }

    .site-name {
        float: right;
        line-height: 60px;
        font-size: 24px;
        color: rgb(0, 136, 245);
        cursor: pointer;
        margin-right: 10%;
    }

    .site-desc {
        line-height: 60px;
        font-size: 14px;
        color: #0088f5;
        cursor: pointer;
        margin-left: 60px;
    }

     .avatar {
        height: 50px;
        width: 50px;
        border-radius: 50%;
        margin-top: 5px;
        margin-left: 20px;
        cursor: pointer;
    }

    .avatar > img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
    }
   
    .el-icon-s-data:hover {
        color: #0088F5 !important;
    }

    .el-menu-item {
        font-weight: bold;
        font-size: 14px;
        width: 145px;
    }

    .el-menu-item:hover {
        background-color: rgba(255, 255, 255, .5) !important;
    }

    .el-menu-item:focus {
        background-color: rgba(255, 255, 255, .5) !important;
    }

    .contact {
        position: fixed;
        top: 50%;
        left: 0;
        height: auto;
        max-width: 4rem;
        display: flex;
        flex-direction: column;
        opacity: .4;
    }

    .contact-btn {
        width: 36px;
        height: 34px;
        border: none;
        font-size: 20px;
    }

    .wechat:hover {
        width: 110%;
        color: white;
        background-color: green;
        transition: width .1s;
    }

    .qq:hover {
        width: 110%;
        color: white;
        background-color: blue;
        transition: width .1s;
    }

    .gzh:hover {
        width: 110%;
        color: white;
        background-color: rgb(16, 186, 16);
        transition: width .1s;
    }

    .git:hover {
        width: 110%;
        color: white;
        background-color: red;
        transition: width .1s;
    }

    .show-contact {
        width: 100%;
        height: 100%;
        background: hsla(0, 0%, 75%, 0.6);
        position: relative;
        left: 0;
        top: 0;
        justify-content: center;
        align-items: center;
        z-index: 999;
    }

    .contact-content {
        height: 450px;
        width: 450px;
        position: absolute;
        margin: auto;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
    }

    .contact-close {
        position: absolute;
        left: calc(50% - 25px);
        top: calc(50% + 200px);
    }
    

</style>