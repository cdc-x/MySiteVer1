<template>
    <div class="content">
        <el-card class="box-card" style="width: 100%; margin: 0 auto">
            <!-- 头部搜索区域 -->
            <el-row :gutter="20" style="margin-bottom: 20px">
                <el-col :span="12">
                    <el-input placeholder="请输入分类名" clearable @clear="getCategoryList" v-model="queryInfo.category" style="width: 320px">
                        <el-button slot="append" icon="el-icon-search" @click="getCategoryList"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="12">
                    <el-button type="primary" @click="addDialogVisible = true" style="float: right">新增分类</el-button>
                </el-col>
            </el-row>

            <!-- 表单展示区域 -->
            <el-table :data="categoryList" border stripe :row-style="{height: '0'}" :cell-style="{padding: '5px'}">
                <el-table-column label="分类名" prop="category"></el-table-column>
                <el-table-column label="创建时间" prop="create__time"></el-table-column>
                <el-table-column label="修改时间" prop="update__time"></el-table-column>
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

            <!-- 新增分类弹窗区域 -->
            <el-dialog title="新增分类" :visible.sync="addDialogVisible" width="30%" @close="handleAddClose">
                <el-form :model="addCategoryForm" :rules="addCategoryRules" ref="addCategoryRef" label-width="100px">
                    <el-form-item label="分类名称" prop="category">
                        <el-input v-model="addCategoryForm.category" clearable></el-input>
                    </el-form-item>
                </el-form>
  
                <span slot="footer" class="dialog-footer">
                    <el-button @click="addDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addCategory">确 定</el-button>
                </span>
            </el-dialog>

            <!-- 编辑分类弹窗 -->
            <el-dialog title="编辑分类" :visible.sync="editDialogVisible" width="30%">
                <el-form :model="editCategoryForm" :rules="addCategoryRules" ref="editCategoryRef" label-width="100px">
                    <el-form-item label="分类名称" prop="category">
                        <el-input v-model="editCategoryForm.category" clearable></el-input>
                    </el-form-item>
                </el-form>
  
                <span slot="footer" class="dialog-footer">
                    <el-button @click="editDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="editCategory">确 定</el-button>
                </span>
            </el-dialog>
        </el-card>
    </div>
</template>

<script>
export default {
    data(){
        return {
            addDialogVisible: false,
            editDialogVisible: false,
            categoryList: [],
            queryInfo: {
                category: "",
                page: 1,
                pageSize: 10
            },
            total: 0,
            addCategoryForm: {
                category: ""
            },
            addCategoryRules:{
                category: [
                    { required: true, message: '请输入分类名称', trigger: 'blur' },
                ]
            },

            editCategoryForm: {
                cid: "",
                category: ""
            },
        }
    },

    created(){
        this.getCategoryList()
    },

    methods: {
        getCategoryList(){
            this.$http.post('admin/category/list', this.queryInfo).then(response => {
                if (response.status === 200){
                    const res = response.data;
                    if (res.status_code === 1000){
                        this.categoryList = res.data;
                        this.total = res.total;
                    }else {
                        this.$message.error(res.message)
                    }
                }else {
                    this.$message.error("查询分类信息失败")
                }
            })
        },

        handleSizeChange(newSize){
            this.queryInfo.pageSize = newSize;
            this.getCategoryList()
        },

        handleCurrentChange(newPage){
            this.queryInfo.page = newPage;
            this.getCategoryList()
        },

        handleAddClose(){
            this.$refs.addCategoryRef.resetFields()
        },

        addCategory(){
            this.$refs.addCategoryRef.validate(valid => {
                if (!valid) return;
                this.$http.post('admin/category/add', this.addCategoryForm).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.addDialogVisible = false;
                            this.getCategoryList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("新增分类失败")
                    }
                })
            })
        },

        editCategory(){
            this.$refs.editCategoryRef.validate(valid => {
                if (!valid) return;
                this.$http.post('admin/category/edit', this.editCategoryForm).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.editDialogVisible = false;
                            this.getCategoryList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("修改分类失败")
                    }
                })
            })
        },

        handleEditClick(row){
            this.editDialogVisible = true;
            this.editCategoryForm.cid = row.cid;
            this.editCategoryForm.category = row.category;
        },

        handleDeleteClick(row){
            this.$confirm('此操作将永久删除该分类, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$http.get('admin/category/delete', {params: {id: row.cid}}).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.getCategoryList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("删除分类失败")
                    }
                });
            }).catch(() => {
                    this.$message({
                    type: 'info',
                    message: '已取消删除'
                });          
            });
        }

    }
   
}
</script>

<style scoped>
</style>