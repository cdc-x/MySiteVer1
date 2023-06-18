<template>
    <el-container class="content">
        <el-header>
            <div>
                <img src="@/assets/img/avatar.png" alt="" />
                <span>博客后台管理系统</span>
            </div>
            <el-button @click="logout" type="info">退出</el-button>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <el-menu :default-active="activePath" background-color="#333744" text-color="#fff" active-text-color="#409EFF">
                    <el-menu-item index="1" @click="saveNavState('1')">
                        <i class="iconfont icon-tongji"></i>
                        <span slot="title">数据统计</span>
                    </el-menu-item>
                    <el-submenu index="2">
                        <template slot="title">
                            <i class="iconfont icon-a-gongzuotaigongzuozhuo-06"></i>
                            <span>基础配置</span>
                        </template>
                        <el-menu-item index="2-1" @click="saveNavState('2-1')">
                            <i class="iconfont icon-fenlei"></i>
                            <span slot="title">分类设置</span>
                        </el-menu-item>
                        <el-menu-item index="2-2" @click="saveNavState('2-2')">
                            <i class="iconfont icon-24gf-tags4"></i>
                            <span slot="title">标签设置</span>
                        </el-menu-item>
                    </el-submenu>
                    <el-menu-item index="3" @click="saveNavState('3')">
                        <i class="iconfont icon-bianjiwenzhang_huaban"></i>
                        <span slot="title">文章设置</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <dashboard v-if="activePath === '1'"></dashboard>
                <category-set v-if="activePath === '2-1'"></category-set>
                <tag-set v-if="activePath === '2-2'"></tag-set>
                <article-set v-if="activePath === '3'"></article-set>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import Dashboard from './Dashboard.vue'
import ArticleSet from './ArticleSet.vue'
import TagSet from './TagSet.vue'
import CategorySet from './CategorySet.vue'

export default {
    components: {
        Dashboard,
        ArticleSet,
        TagSet,
        CategorySet,
        ArticleSet
    },
    
    data(){
        return {
            activePath: '1'
        }
    },

    created(){
        
    },

    methods: {
        logout(){
            this.$http.get('admin/user/logout').then(response => {
                if (response.status === 200){
                    const res = response.data;
                    if (res.status_code === 1000){
                        // 清楚浏览器缓存
                        window.sessionStorage.clear();
                        // 强制跳转到登录页面
                        this.$router.push("/login");
                        this.$message.success(res.message);
                    }else {
                        this.$message.error(res.message);
                    }
                }else {
                    this.$message.error("退出登录失败");
                }
            })
        },

        saveNavState(path){
            this.activePath = path
        }
    }
}
</script>

<style scoped>
    .el-header {
        background-color: #373d41;
        display: flex;
        justify-content: space-between;
        padding-left: 0;
        align-items: center;
        color: #eee;
        font-size: 20px;
    }

    .el-aside {
        background-color: #333744;
    }

    .el-main {
        background: #eaedf1;
    }

    .content{
        height: 100%;
    }

    .el-header > div > img {
        height: 50px;
        width: 50px;
        border-radius: 50%;
    }

    .el-header > div > span {
        margin-left: 15px;
    }

    .el-header > div {
        display: flex;
        align-items: center;
    }

    /deep/ .el-menu {
        border-right: none
    }
</style>