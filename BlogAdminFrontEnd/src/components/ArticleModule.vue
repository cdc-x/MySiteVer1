<template>
    <div style="height:100%;">
        <el-scrollbar style="height:100%;">
            <el-row :gutter='20'>
                <el-col :span='13' style="margin-top: 70px; margin-bottom: 15px" v-if="!isArticleContent">

                    <div class="article-list">
                        <el-card style="width: 100%; margin-bottom: 12px;" v-for="item in articleList" :key="item.id"   @click.native="getArticleInfo(item.id)">
                            <el-row :gutter="20" style="height: 100%">
                                <el-col :span="8" style="height: 100%">
                                    <img src="/static/img/afo.jpg" width="100%" height="100%">
                                </el-col>
                                <el-col :span="16" style="height: 100%">
                                    <h4>{{item.title}}</h4>
                                    <p class="article-desc">{{item.desc}}</p>
                                    <div class="article-attr" style="">
                                        <i class="iconfont icon-shijian"> {{item.publish_time}}</i>
                                        <i class="iconfont icon-yuedu"> {{item.browse}}</i>
                                        <i class="iconfont icon-dianzan"> {{item.thumb}}</i>
                                        <i class="iconfont icon-yingyong"> {{item.category}}</i>                                        
                                    </div>

                                </el-col>
                            </el-row>
                            
                        </el-card>
                    </div>

                    <div :class="{'article-load-outer': articleList.length === total}">
                        <div class="article-load" @click="handleCurrentChange()" :class="{'dis-click': articleList.length === total}">
                            <span class="left">
                                <div class="page-num">
                                    {{articleList.length}} / {{total}}
                                </div>
                            </span>
                            <span class="right">
                                <div class="page-more">
                                    More
                                    <span class="iconfont icon-et-more"></span>
                                </div>
                            </span>
                        </div>
                    </div>    
                </el-col>

                <el-col :span='13' style="margin-top: 70px; margin-bottom: 15px" v-if="isArticleContent">
                    <!-- 文章列表及内容显示区域 -->
                    <mavon-editor 
                        v-model="articleContent"
                        :external-link="externalLink" 
                        :subfield="false"
                        :defaultOpen="'preview'"
                        :editable="false"
                        :toolbarsFlag="false"
                        :scrollStyle="true"
                        :ishljs="true">
                    </mavon-editor>

                    <div class="content-footer">
                        <button @click="thumbArticle()" class="thumb-btn" :class="{'thumbed': articleThumbed}">
                            <span class="iconfont icon-dianzan"></span>
                            <span>{{articleThumbed?"已赞":"真棒！"}} {{articleThumbNum}}</span>
                        </button>
                        <div>
                            本文于 {{articlePubTime}} 发布在 {{articleCate}} 专题
                        </div>
                        <div>
                            &copy;自由转载 - 署名 - 非商业性使用
                        </div>
                    </div>

                    <!-- 快速返回顶部 -->
                    <el-button icon="el-icon-caret-top" circle class="back-top" v-if="topLeft < -50" @click="backTop()"></el-button>

                </el-col>

                <el-col :span='7'>
                    <!-- 搜索卡片 -->
                    <el-card class="box-card" style="margin-top: 70px;">
                        <el-input placeholder="搜点什么..." v-model="queryInfo.searchContent" style="width: 300px" clearable>
                            <el-button slot="append" icon="el-icon-search" @click="getArticleListBySearch()"></el-button>
                        </el-input>
                    </el-card>
                    <!-- 总热门文章 -->
                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <i class="iconfont icon-huo" style="color:red"></i>
                            <span>Hottest</span>
                        </div>
                        <div v-for="(item, index) in hotArticle" :key="index" class="hot-article-item" @click="getArticleInfo(item.id)">
                            <span class="hot-index" :class="{'hot-index-1':index === 0, 'hot-index-2':index === 1, 'hot-index-3':index === 2}">
                                {{index + 1}}
                            </span>
                            <span style="font-size:13.58px">{{item.title}}</span>
                        </div>
                    </el-card>
                    <!-- 日历区域 -->
                    <div ref="scrollJudgeRef">
                        <el-card class="box-card">
                            <Calendar @choseDay="clickDate" :markDate="markDate">
                            </Calendar>
                        </el-card>
                    </div>
                    
                    <!-- 其他固件区域 -->
                    <div v-if="topLeft >= -250">
                        <!-- 文章类别区域 -->
                        <el-card class="box-card tag-list" v-if="!isArticleContent" style="overflow-y:auto; height: 350px">
                            <el-tag 
                                v-for="tag in tagNum" 
                                :key="tag.tag" 
                                type="info" 
                                style="margin: 5px" 
                                :class="tag.icon" class="tag-item"
                                @click="queryArticleByTag(tag.tag)">
                                    {{tag.tag}} ({{tag.count}})
                            </el-tag>
                        </el-card>

                        <!-- 文章菜单展示区 -->
                        <el-card class="box-card" v-if="isArticleContent">
                            <div class="article-title border-style" @click="topMao(articleInfo.href)">
                                <div style="font-size: 14px;font-weight: bold;padding-left: 12px">{{ articleInfo.title }}</div>
                                <div style="font-size: 12px; color: gray;padding-left: 12px">共{{ articleInfo.count }}字</div>
                            </div>
                            
                            <div class="article-menu border-style">
                                <el-scrollbar style="height:100%;">
                                <ul style="margin: 0; padding: 6px">
                                    <li v-for="(item, index) in menuList" :key="index" class="article-menu-item" :class="item.level" @click="topMao(item.href)">{{ item.title }}</li>
                                </ul>
                                </el-scrollbar>
                            </div>

                            <div class="article-footer border-style" style="color: gray">
                                <i class="iconfont icon-heart" style="font-size: 14px; padding: 0 12px; margin: 0; border-right: 2px solid gray;">
                                    <span style="margin-left: 5px">按赞</span>
                                </i>
                                <i class="iconfont icon-yuedu" style="font-size: 14px; padding:0 12px; margin: 0; border-right: 2px solid gray;">
                                    <span style="margin-left: 5px">{{articleBrowseNum}}</span>
                                </i>
                                <i class="iconfont icon-dianzan" style="font-size: 14px; padding:0 12px;">
                                    <span style="margin-left: 5px">{{articleThumbNum}}</span>
                                </i>
                            </div>
                        </el-card>

                        <!-- 友链 -->
                        <el-card class="box-card">
                            <div slot="header" class="clearfix">
                                <i class="iconfont icon-lianjie"></i>
                                <span>友链</span>
                            </div>
                            <el-link 
                            v-for="item in ExtLink" :key="item.value" 
                            :href="item.value" 
                            target="_blank"
                            >{{item.label}}</el-link>
                        </el-card>
                    </div>
                    
                    <!-- 其他固件展示固定区域 -->
                    <div  v-if="topLeft < -250" style="position: fixed; width: 22.5%; top: 70px;" >
                         <!-- 文章类别固定区域 -->
                        <el-card class="box-card tag-list" v-if="!isArticleContent" style="overflow-y:auto; height: 350px">
                            <el-tag 
                                v-for="tag in tagNum" 
                                :key="tag.tag" 
                                type="info" 
                                style="margin: 5px" 
                                :class="tag.icon" 
                                class="tag-item"
                                @click="queryArticleByTag(tag.tag)">
                                    {{tag.tag}} ({{tag.count}})
                            </el-tag>
                        </el-card>
                        
                         <!-- 文章菜单展示固定区域 -->
                        <el-card class="box-card" v-if="isArticleContent">
                            <div class="article-title border-style" @click="topMao(articleInfo.href)">
                                <div style="font-size: 14px;font-weight: bold;padding-left: 12px">{{ articleInfo.title }}</div>
                                <div style="font-size: 12px; color: gray;padding-left: 12px">共{{ articleInfo.count }}字</div>
                            </div>
                            
                            <div class="article-menu border-style">
                                <el-scrollbar style="height:100%;">
                                <ul style="margin: 0; padding: 6px">
                                    <li v-for="(item, index) in menuList" :key="index" class="article-menu-item" :class="item.level" @click="topMao(item.href)">{{ item.title }}</li>
                                </ul>
                                </el-scrollbar>
                            </div>

                            <div class="article-footer border-style" style="color: gray">
                                <i class="iconfont icon-heart" style="font-size: 14px; padding: 0 12px; margin: 0; border-right: 2px solid gray;">
                                    <span style="margin-left: 5px">按赞</span>
                                </i>
                                <i class="iconfont icon-yuedu" style="font-size: 14px; padding:0 12px; margin: 0; border-right: 2px solid gray;">
                                    <span style="margin-left: 5px">{{articleBrowseNum}}</span>
                                </i>
                                <i class="iconfont icon-dianzan" style="font-size: 14px; padding:0 12px;">
                                    <span style="margin-left: 5px">{{articleThumbNum}}</span>
                                </i>
                            </div>
                        </el-card>

                        <!-- 友链 -->
                        <el-card class="box-card">
                            <div slot="header" class="clearfix">
                                <i class="iconfont icon-lianjie"></i>
                                <span>友链</span>
                            </div>
                            <el-link 
                            v-for="item in ExtLink" :key="item.value" 
                            :href="item.value" 
                            target="_blank"
                            >{{item.label}}</el-link>
                        </el-card>
                    </div>
                </el-col>
            </el-row>
        </el-scrollbar>
    </div>
    
</template>

<script>
import Calendar from '@/components/Calendar/calendar.vue'
export default {

    components: {
        Calendar
    },

    mounted(){
        window.addEventListener('scroll', this.handleScrollx, true)
    },

    created(){
        this.$http.all([this.getArticleList(), this.getHotArticleList(), this.getArticleTagNum()]).then(
            this.$http.spread((res1, res2, res3) => {
                let _articleList = res1.data
                this.articleList = _articleList.data
                this.total = _articleList.total
                this.markDate = _articleList.date_mark

                let _hotArticleList = res2.data
                this.hotArticle = _hotArticleList.data

                let _articleTag = res3.data
                for (let i = 0; i < this.tagNum.length; i++) {
                        this.tagNum[i].count = _articleTag.data[this.tagNum[i].tag];
                    }
            })
        )
    },

    data(){
        return {
            // mavon-editor 本地加载设置
            externalLink: {
                markdown_css: () => '../static/md/markdown/github-markdown.min.css',
                hljs_js: () => '../static/md/highlightjs/highlight.min.js',
                hljs_css: (css) => '../static/md/highlightjs/styles/' + css + '.min.css',
                hljs_lang: (lang) => '../static/md/highlightjs/languages/' + lang + '.min.js',
                katex_css: () => '../static/md/katex/katex.min.css',
                katex_js: () => '../static/md/katex/katex.min.js',
            },

            // 查询数据
            queryInfo: {
                searchContent: '',
                searchTag: '',
                page: 1
            },

            // 文章总数
            total: 0,

            // 文章列表
            articleList: [],

            // 文章分类数
            tagNum: [
                {tag: "Python", icon: "iconfont icon-python", count: 0},
                {tag: "Django", icon: "iconfont icon-django", count: 0},
                {tag: "Vue", icon: "iconfont icon-vuejs", count: 0},
                {tag: "GoLang", icon: "iconfont icon-Goyuyan", count: 0},
                {tag: "JavaScript", icon: "iconfont icon-java-script", count: 0},
                {tag: "HTML", icon: "iconfont icon-html5", count: 0},
                {tag: "CSS", icon: "iconfont icon-css", count: 0},
                {tag: "Flask", icon: "iconfont icon-flask", count: 0},
                {tag: "ElasticSearch", icon: "iconfont icon-ElasticSearch", count: 0},
                {tag: "RabbitMQ", icon: "iconfont icon-rabbitmq", count: 0},
                {tag: "Redis", icon: "iconfont icon-redis", count: 0},
                {tag: "MySQL", icon: "iconfont icon-mysql", count: 0},
                {tag: "后端", icon: "iconfont icon-houduankaifa", count: 0},
                {tag: "前端", icon: "iconfont icon-qianduankaifa", count: 0},
                {tag: "算法", icon: "iconfont icon-zhinengsuanfa", count: 0},
                {tag: "数据结构", icon: "iconfont icon-relation-analysis-full", count: 0},
                {tag: "编码", icon: "iconfont icon-code", count: 0},
                {tag: "消息队列", icon: "iconfont icon-xiaoxiduilie", count: 0},
                {tag: "生活", icon: "iconfont icon-kafei", count: 0},
                {tag: "工作", icon: "iconfont icon-a-gongzuotaigongzuozhuo-06", count: 0},
                {tag: "学习", icon: "iconfont icon-xuexi", count: 0},
                {tag: "三省吾身", icon: "iconfont icon-dengpao", count: 0}
            ],

            // 友链
            ExtLink: [
                {label: "Hui_Tong", "value": "https://www.cnblogs.com/tongh/"}
            ],

            // 总热门文章列表
            hotArticle: [],

            // 归档日期
            markDate: [],

            // 文章内容
            articleContent: "",

            // 文章点赞数
            articleThumbNum: 0,

            // 文章浏览数
            articleBrowseNum: 0,

            // 文章发布时间
            articlePubTime: "",

            // 当前文章ID
            articleId: "",

            // 文章分类
            articleCate: "",

            // 文章是否已点赞
            articleThumbed: false,

            // 文章菜单
            menuList: [],

            // 显示内容距离窗口顶部的距离
            topLeft: 0,

            // 当前是否显示文章内容
            isArticleContent: false,

            // 文章标题及字数统计
            articleInfo: {
                title: "",
                count: 0
            }
        }
    },

    methods: {
        // 查询所有文章列表
        getArticleList(){
            this.queryInfo.searchContent = ""
            this.queryInfo.searchTag = ""
            this.queryInfo.page = 1
            const url = "/article/all?page=" + this.queryInfo.page
            return this.$http.get(url)
        },

        // 根据搜索内容查询文章列表
        getArticleListBySearch(){
            this.queryInfo.searchTag = ""
            this.queryInfo.page = 1
            const url = "/article/all?page=" + this.queryInfo.page + "&searchContent=" + this.queryInfo.searchContent
            this.$http.get(url).then(response => {
                if (response.status == 200){
                    const res = response.data
                    this.articleList = res.data
                    this.total = res.total
                    this.markDate = res.date_mark
                }
            })
        },

        // 根据文章分类查询文章列表
        getArticleListByTag(){
            this.queryInfo.searchContent = ""
            this.queryInfo.page = 1
            const url = "/article/all?page=" + this.queryInfo.page + "&searchTag=" + this.queryInfo.searchTag
            this.$http.get(url).then(response => {
                if (response.status == 200){
                    const res = response.data
                    this.articleList = res.data
                    this.total = res.total
                    this.markDate = res.date_mark
                }
            })
        },

        // 分页
        handleCurrentChange(newPage){
            this.queryInfo.page ++;
            let url = ""
            if (this.queryInfo.searchContent.length !== 0) {
                url = "/article/all?page=" + this.queryInfo.page + "&searchContent=" + this.queryInfo.searchContent
            }else if (this.queryInfo.searchTag.length !== 0) {
                url = "/article/all?page=" + this.queryInfo.page + "&searchTag=" + this.queryInfo.searchTag
            }else {
                url = "/article/all?page=" + this.queryInfo.page
            }

            this.$http.get(url).then(response => {
                if (response.status == 200){
                    const res = response.data
                    this.total = res.total
                    this.markDate = res.date_mark

                    if (res.page === 1){
                        this.articleList = res.data
                    }else {
                        this.articleList = this.articleList.concat(res.data)
                    } 
                }
            })
        },

        // 查询热门文章
        getHotArticleList(){
            return this.$http.get("/article/hot")
        },

        // 查询所有文章分类的数量
        getArticleTagNum(){
            return this.$http.get("/article/tags")
        },

        // 根据分类标签查询所有文章
        queryArticleByTag(tagName){
            this.queryInfo.searchTag = tagName
            this.getArticleListByTag()
        },

        // 查询文章点赞数
        getArticleThumbNum2(aid){
            this.$http.get("/article/count/thumb?p=" + aid).then(response => {
                const res = response.data
                this.articleThumbNum = res.data
            })
        },

        // 查询文章内容
        getArticleContent(aid){
            return this.$http.get("/article/content?p=" + aid)
        },

        // 查询文章点赞数
        getArticleThumbNum(aid){
            return this.$http.get("/article/count/thumb?p=" + aid)
        },

        // 查询文章浏览数
        getArticleBrowseNum(aid){
            return this.$http.get("/article/count/browse?p=" + aid)
        },

        // 查询当前用户是否已点赞当前文章
        getArticleThumbed(aid){
            return this.$http.get("/article/check/thumb?p=" + aid)
        },

        // 查询文章详细信息
        getArticleInfo(aid){
            this.$http.all([this.getArticleContent(aid), this.getArticleThumbNum(aid), this.getArticleBrowseNum(aid), this.getArticleThumbed(aid)]).then(
                this.$http.spread((res1, res2, res3, res4) => {
                    let _articleInfo = res1.data;
                    let _thumbInfo = res2.data;
                    let _browseInfo = res3.data;
                    let _thumbed = res4.data;
                    this.articleContent = _articleInfo.data
                    this.articlePubTime = _articleInfo.pub_time
                    this.articleCate = _articleInfo.category
                    this.articleId = aid
                    this.isArticleContent = true
                    this.getArticleMenu()
                    this.articleThumbNum = _thumbInfo.data
                    this.articleBrowseNum = _browseInfo.data
                    this.articleThumbed = _thumbed.flag
                })
            )
        },
        
        // 点击返回顶部
        backTop(){
            this.topMao(this.articleInfo.href)
        },

        // 文章点赞
        thumbArticle(){
            if (this.articleThumbed === false){
                this.$http.get("/article/thumb?p=" + this.articleId).then(response => {
                    this.getArticleThumbNum2(this.articleId)
                    this.articleThumbed = true
                })
            }
        },

        // 日历日期点击事件
        clickDate(date){
            console.log(date);
        },

        getArticleMenu(){
            let menuList = []
            let articleInfo = {
                title: "",
                count: 0,
                href: ""
            }

            this.$nextTick(() => {
                let _aList = document.querySelectorAll(".v-show-content a");
                articleInfo.count = document.getElementsByClassName("v-show-content")[0].innerText.length;
                for (let i = 0; i < _aList.length; i++){
                    parent = _aList[i].parentNode;
                    if (_aList[i].id && parent.tagName !== "H1"){
                        let _data = {
                            title: parent.innerText, 
                            href: _aList[i].id,
                            level: "level1"
                        };

                        if (parent.tagName === "H3"){
                            _data.level = "level2"
                        }else if (parent.tagName === "H4"){
                            _data.level = "level3"
                        }else if (parent.tagName === "H5"){
                            _data.level = "level4"
                        }
                        menuList.push(_data)
                    }else {
                        if (_aList[i].id && parent.tagName === "H1"){
                            articleInfo.title = parent.innerText;
                            articleInfo.href = _aList[i].id;
                        }
                    }

                };
            })
            this.menuList = menuList;
            this.articleInfo = articleInfo;
        },

        topMao(id){
            let dHeight = document.documentElement.clientHeight;
            let elem = document.getElementById(id).parentNode;
            let oldHeight = elem.style.height;
            elem.style.height = dHeight - 70 + "px";
            elem.scrollIntoView(false);
            elem.style.height = oldHeight;
        },

        handleScrollx(){
            this.$nextTick(() => {
                if (this.$refs.scrollJudgeRef){
                    this.topLeft = this.$refs.scrollJudgeRef.getBoundingClientRect().top;
                }
            })
        },

    }
    
}
</script>

<style scoped>
    
    /*鼠标悬浮图片放大*/
    .el-carousel img:hover {
        cursor: pointer;
        transition: all 0.8s;
        transform: scale(1.1);
    }

    .title-tip {
        height: 30px;
        line-height: 30px;
        text-align: center;
        padding: 0 10px;
        mix-blend-mode: screen;
        font-weight: bold;
        font-size: 14px;
        background-color: rgba(255, 255, 255, .6);
        position: fixed;
        top: 25px;
        right: 40px;
        z-index: 999;
    }

    .title-tip:hover {
        cursor: pointer;
    }

    /deep/ .article-list .el-card__body {
        padding: 10px;
        height: 130px;
    }

    /deep/ .article-list .el-card {
        background-color: rgba(255, 255, 255, .5);
    }

    /deep/ .article-list .el-card:hover {
        background-color: white;
        cursor: pointer;
    }

    .article-desc {
        width: 220px; 
        overflow: hidden; 
        text-overflow: ellipsis; 
        white-space: nowrap; 
        font-size: 14px;
    }

    .article-attr {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: gray; 
        margin-top: 25px
    }

    .article-attr .iconfont {
        font-size: 13.5px;
    }

    /deep/ .el-pager li {
        background: none;
    }

    .hot-article-item {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        margin-bottom: 6px;
        cursor: pointer;
    }

    .tag-item {
        font-size: 12px;
    }

    .el-tag.el-tag--info:hover {
        cursor: pointer;
        background-color: rgba(128, 128, 128, 0.3);
    }

    .hot-index{
        height: 20px;
        width: 20px;
        margin-right: 5px;
        color: rgba(0, 0, 0, .38);
        display: inline-block;
        text-align: center;
        background-color: #e8e8e8;
    }

    .hot-index-1 {
        background-color: rgba(0, 136, 245, .5);
        color: white;
    }

    .hot-index-2 {
        background-color: #4caf5099;
        color: white;
    }

    .hot-index-3 {
        background-color: #ff572299;
        color: white;
    }

    .border-style {
        width: 100%;
        border: 1px dashed #dedede;
        border-radius: 4px;
        margin-bottom: 1rem;
        text-align: left;
    }
    
    .article-title {
        display: flex;
        flex-direction: column;
        height: 72px;
    }

    .article-title > div {
        margin-top: 12px;
        cursor: pointer;
    }

    .article-title > div:hover {
        color: #0088F5;
    }

    /deep/ pre {
        border-radius: 3px;
        padding: 5px !important;
        
    }

    /deep/ .markdown-body .hljs {
        padding: 5px;
    }

    .articleDetail > img {
        width: 200px;
    }


    .level2 {
        padding-left: 36px !important;
    }

     .level3 {
        padding-left: 48px !important;
    }

     .level4 {
        padding-left: 60px !important;
    }

    .article-menu-item {
        cursor: pointer;
        padding-left: 12px;
        font-size: 14px;
        color: gray;
        margin-top: 6px;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .article-menu-item:hover {
        color: #0088F5
    }

    .article-menu {
        height: 300px;
        overflow-y: scroll;
    }

    .article-menu::-webkit-scrollbar {
        display:none
    }

    .article-footer {
        height: 36px;
        line-height: 36px;
        cursor: default;
    }

    .article-footer:hover > * {
        color: #0088F5;
    }

    /* 设置滚动条 */
    /deep/ .el-scrollbar__wrap {
        overflow-x: hidden;
    }

    /deep/ .el-scrollbar__bar.is-horizontal {
        width: 0;
        height: 0;
    }

    .el-scrollbar__thumb {
        background-color: rgba(0,0,0,.5);
    }

    .is-horizontal {
        width: 0;
    }

    .el-card__body,  .el-card__header{
        padding: 0.618rem;
    }


    .el-card {
        margin-bottom: 10px;
    }

    .back-top {
        position: fixed;
        bottom: 100px;
        right: 100px;
    }

    .content-footer {
        height: 100px;
        background-color: #fff;
        text-align: center;
        border-top: 2px #eee dashed;
        padding: 2rem 0;
    }

    .thumb-btn {
        height: 35px;
        background-color: #fff;
        border: 2px rgba(0, 0, 0, .38) solid;
        border-radius: 5px;
        cursor: pointer;
    }

    .thumb-btn:hover {
        border: 2px #ff5722 solid;
        color: #ff5722;
        
    }

    .thumb-btn span {
        margin-right: 5px;
    }
    
    .content-footer div {
        margin: 15px 0;
        font-size: 14px;
        color: rgba(0, 0, 0, .58);
        font-weight: bold;
    }

    .thumbed {
        background-color: #ff5722;
        border: 2px #ff5722 solid;
        color: white;
    }

    .thumbed:hover {
        color: white;
    }

    .article-load {
        width: 100%;
        height: 3rem;
        position: relative;
        display: block;
        border-radius: 4px;
        overflow: hidden;
    }

    .article-load .left {
        position: absolute;
        display: inline-block;
        width: 80%;
        height: 100%;
        transform: translateZ(0) translateX(-5%) skew(-20deg);
        background-color: rgba(255, 255, 255, .4)
    }

    .article-load .right {
        position: absolute;
        display: inline-block;
        background-color: red;
        width: 35%;
        height: 100%;
        transform: translateZ(0) translateX(220%) skew(-20deg);
        background-color: white
    }

    .page-num {
        line-height: 3rem;
        position: absolute;
        left: 10%;
        transform: translateZ(0) translateX(0%) skew(20deg);
        font-size: 14px;
        color: rgba(0, 0, 0, .5);
    }

    .page-more {
        line-height: 3rem;
        position: absolute;
        left: 20%;
        transform: translateZ(0) translateX(0%) skew(20deg);
        font-size: 15px;
        font-weight: bold;
        color: rgba(0, 0, 0, .5);
    }

    .article-load:hover {
        cursor: pointer;
    }

    .article-load:hover .left {
        background-color: white;
    }

    .article-load:hover .page-num {
        color: #0088F5;
    }

     .article-load:hover .right {
        background-color: #0088F5;
    }

    .article-load:hover .page-more {
        color: white;
    }

    .article-load-outer {
        cursor: not-allowed;
    }

    .dis-click {
        pointer-events: none;
    }

</style>