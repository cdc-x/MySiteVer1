<template>
    <div>
        <el-card class="box-card" style="width: 100%; margin: 0 auto">
            <!-- 头部搜索区域 -->
            <el-row :gutter="20" style="margin-bottom: 20px">
                <el-col :span="12">
                    <el-input placeholder="请输入文章标题" clearable @clear="getArticleList" v-model="queryInfo.article" style="width: 320px">
                        <el-button slot="append" icon="el-icon-search" @click="getArticleList"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="12">
                    <el-button type="primary" @click="handleAddClick" style="float: right">新增文章</el-button>
                </el-col>
            </el-row>

            <!-- 表单展示区域 -->
            <el-table :data="articleList" border stripe :header-cell-style="{background:'#eef1f6',color:'#606266'}" :row-style="{height: '0'}" :cell-style="{padding: '5px'}">
                <el-table-column label="标题" prop="title" resizable show-overflow-tooltip></el-table-column>
                <el-table-column label="简介" prop="article_desc" resizable show-overflow-tooltip></el-table-column>
                <el-table-column label="分类" prop="category_name" resizable show-overflow-tooltip></el-table-column>
                <el-table-column label="标签" prop="tags_name" resizable show-overflow-tooltip></el-table-column>
                <el-table-column label="发布时间" prop="publish_time" ></el-table-column>
                <el-table-column label="阅读量" prop="browse"></el-table-column>
                <el-table-column label="点赞量" prop="thumb"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button @click="handleEditClick(scope.row)" type="text" size="small">编辑</el-button>
                        <el-button @click="handleDeleteClick(scope.row)" type="text" size="small">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="queryInfo.page" :page-sizes="[10, 20, 30, 40, 50, 100]"
            :page-size="queryInfo.pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total" style="margin-top: 20px">
            </el-pagination>
        </el-card>

        <el-dialog title="新增文章" :visible.sync="addDialogVisible" width="90%" @close="handleAddClose" :close-on-click-modal="false">
            <el-form :model="addArticleForm" :rules="addArticleRules" ref="addArticleRef" label-width="100px">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="addArticleForm.title" style="width: 450px" clearable  placeholder="请输入文章标题"></el-input>
                </el-form-item>
                <el-form-item label="简介" prop="desc">
                    <el-input v-model="addArticleForm.desc" style="width: 450px" clearable placeholder="请输入文章简介"></el-input>
                </el-form-item>
                <el-form-item label="分类" prop="category">
                    <el-select v-model="addArticleForm.category" placeholder="请选择分类" clearable style="width: 450px" filterable>
                        <el-option v-for="item in CategoryOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="标签" prop="tag">
                    <el-select v-model="addArticleForm.tag" multiple collapse-tags placeholder="请选择标签" style="width: 450px" clearable filterable>
                        <el-option v-for="item in TagOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="日期" prop="publish_time">
                    <el-date-picker v-model="addArticleForm.publish_time" type="date" placeholder="选择发布时间" style="width: 450px" clearable
                    value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <mavon-editor v-model="addArticleForm.content" style="height: 600px" :external-link="externalLink" ishljs></mavon-editor>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addArticle">发 布</el-button>
            </span>
        </el-dialog>

        <el-dialog title="编辑文章" :visible.sync="editDialogVisible" width="90%" :close-on-click-modal="false">

            <el-form :model="editArticleForm" :rules="editArticleRules" ref="editArticleRef" label-width="100px">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="editArticleForm.title" style="width: 450px" clearable></el-input>
                </el-form-item>
                <el-form-item label="简介" prop="article_desc">
                    <el-input v-model="editArticleForm.article_desc" style="width: 450px" clearable></el-input>
                </el-form-item>
                <el-form-item label="分类" prop="category">
                    <el-select v-model="editArticleForm.category" placeholder="请选择分类" clearable style="width: 450px">
                        <el-option v-for="item in CategoryOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="标签" prop="tag">
                    <el-select v-model="editArticleForm.tag" multiple collapse-tags placeholder="请选择标签" style="width: 450px" clearable>
                        <el-option v-for="item in TagOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="日期" prop="publish_time">
                    <el-date-picker v-model="editArticleForm.publish_time" type="date" placeholder="选择发布时间" style="width: 450px" clearable
                    value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <mavon-editor v-model="editArticleForm.content" style="height: 600px" ishljs :external-link="externalLink"></mavon-editor>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editArticle">发 布</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data(){
        return {

            externalLink: {
                markdown_css: () => '../static/md/markdown/github-markdown.min.css',
                hljs_js: () => '../static/md/highlightjs/highlight.min.js',
                hljs_css: (css) => '../static/md/highlightjs/styles/' + css + '.min.css',
                hljs_lang: (lang) => '../static/md/highlightjs/languages/' + lang + '.min.js',
                katex_css: () => '../static/md/katex/katex.min.css',
                katex_js: () => '../static/md/katex/katex.min.js',
            },

            queryInfo: {
                article: "",
                page: 1,
                pageSize: 10
            },
            articleList: [],
            total: 0,

            // 发布文章
            addDialogVisible: false,
            addArticleForm: {
                title: "",
                desc: "",
                category: "",
                tag: [],
                content: "",
                publish_time: null
            },

            addArticleRules: {
                title: [{ required: true, message: '请输入文章标题', trigger: 'blur' },],
                desc: [{ required: true, message: '请输入文章简介', trigger: 'blur' },],
                // category: [{ required: true, message: '请选择选择分类', trigger: 'blur' },],
                // tag: [{ required: true, message: '请选择选择标签', trigger: 'blur' },],
                publish_time: [{ required: true, message: '请选择发布时间', trigger: 'blur' },]
            },

            CategoryOptions: [],
            TagOptions: [],
            ModuleOptions: [
                {label: "温故知新", value: "code"},
                {label: "三省吾身", value: "think"}
            ],

            // 编辑文章
            editDialogVisible: false,
            editArticleForm: {
                aid: "",
                title: "",
                article_desc: "",
                category: "",
                tag: [],
                content: "",
                publish_time: null
            },

            editArticleRules: {
                title: [{ required: true, message: '请输入文章标题', trigger: 'blur' },],
                desc: [{ required: true, message: '请输入文章简介', trigger: 'blur' },],
                // category: [{ required: true, message: '请选择选择分类', trigger: 'blur' },],
                // tag: [{ required: true, message: '请选择选择标签', trigger: 'blur' },],
                publish_time: [{ required: true, message: '请选择发布时间', trigger: 'blur' },],
            },


        }
    },

    created(){
        this.getArticleList()
        this.queryCategoryTag()
    },

    methods: {
        // 查询文章
        getArticleList(){
            this.$http.post('admin/article/list', this.queryInfo).then(response => {
                if (response.status === 200){
                    const res = response.data;
                    if (res.status_code === 1000){
                        this.total = res.total;
                        this.articleList = res.data;
                    }else {
                        this.$message.error(res.message)
                    }
                }else {
                    this.$message.error("获取文章列表失败")
                }
            })
        },

        handleSizeChange(newSize){
            this.queryInfo.pageSize = newSize;
            this.getArticleList()
        },

        handleCurrentChange(newPage){
            this.queryInfo.page = newPage;
            this.getArticleList()
        },

        // 新增文章
        handleAddClick(){
            this.addDialogVisible = true
        },

        queryCategoryTag(){
            this.$http.get('admin/article/category_tag').then(response => {
                if (response.status === 200){
                    const res = response.data;
                    if (res.status_code === 1000){
                        this.CategoryOptions = res.category;
                        this.TagOptions = res.tag;
                    }else {
                        this.$message.error(res.message)
                    }
                }else {
                    this.$message.error("请求分类和标签数据失败")
                }
            })
        },

        addArticle(){
            this.$refs.addArticleRef.validate(valid => {
                if (!valid){
                    this.$message.error("请完善信息")
                }else {
                    this.$http.post('admin/article/add', this.addArticleForm).then(response => {
                        if (response.status === 200){
                            const res = response.data;
                            if (res.status_code === 1000){
                                this.$message.success(res.message);
                                this.getArticleList()
                                this.addDialogVisible = false
                            }else {
                                this.$message.error(res.message)
                            }
                        }else {
                            this.$message.error("新增文章失败")
                        }
                    })
                }
            })
        },

        handleAddClose(){
            this.addArticleForm.title = ""
            this.addArticleForm.desc = ""
            this.addArticleForm.category = ""
            this.addArticleForm.tag = []
            this.addArticleForm.content = ""
            this.addArticleForm.module = ""
            this.addArticleForm.publish_time = null
        },
        

        // 删除文章
        handleDeleteClick(row){
            this.$confirm('此操作将永久删除该文章, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$http.get('admin/article/delete', {params: {id: row.aid}}).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.getArticleList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("删除文章失败")
                    }
                });
            }).catch(() => {
                    this.$message({
                    type: 'info',
                    message: '已取消删除'
                });          
            });
        },

        // 编辑文章
        handleEditClick(row){
            this.editDialogVisible = true
            this.editArticleForm.aid = row.aid
            this.editArticleForm.title = row.title
            this.editArticleForm.article_desc = row.article_desc
            this.editArticleForm.category = row.category
            this.editArticleForm.tag = row.tag
            this.editArticleForm.content = row.content
            this.editArticleForm.publish_time = row.publish_time
            this.editArticleForm.module = row.module
        },

        editArticle(){
            this.$refs.editArticleRef.validate(valid => {
                if (!valid){
                    this.$message.error("请完善信息")
                }else {
                    this.$http.post('admin/article/edit', this.editArticleForm).then(response => {
                        if (response.status === 200){
                            const res = response.data;
                            if (res.status_code === 1000){
                                this.$message.success(res.message);
                                this.getArticleList()
                                this.editDialogVisible = false
                            }else {
                                this.$message.error(res.message)
                            }
                        }else {
                            this.$message.error("编辑文章失败")
                        }
                    })
                }
            })
        },
    },
   
}
</script>

<style scoped>
    /deep/ pre {
        border-radius: 3px;
        padding: 5px !important;
        
    }

    /deep/ .markdown-body .hljs {
        padding: 5px;
    }

</style>