<template>
    <div class="content">
        <el-card class="box-card" style="width: 100%; margin: 0 auto">
            <!-- 头部搜索区域 -->
            <el-row :gutter="20" style="margin-bottom: 20px">
                <el-col :span="12">
                    <el-input placeholder="请输入标签名" clearable @clear="getTagList" v-model="queryInfo.tag" style="width: 320px">
                        <el-button slot="append" icon="el-icon-search" @click="getTagList"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="12">
                    <el-button type="primary" @click="addDialogVisible = true" style="float: right">新增标签</el-button>
                </el-col>
            </el-row>

            <!-- 表单展示区域 -->
            <el-table :data="tagList" border stripe :row-style="{height: '0'}" :cell-style="{padding: '5px'}">
                <el-table-column label="标签名" prop="tag"></el-table-column>
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

            <!-- 新增标签弹窗区域 -->
            <el-dialog title="新增标签" :visible.sync="addDialogVisible" width="30%" @close="handleAddClose">
                <el-form :model="addTagForm" :rules="addTagRules" ref="addTagRef" label-width="100px">
                    <el-form-item label="标签名称" prop="tag">
                        <el-input v-model="addTagForm.tag" clearable></el-input>
                    </el-form-item>
                </el-form>
  
                <span slot="footer" class="dialog-footer">
                    <el-button @click="addDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addTag">确 定</el-button>
                </span>
            </el-dialog>

            <!-- 编辑标签弹窗 -->
            <el-dialog title="编辑标签" :visible.sync="editDialogVisible" width="30%">
                <el-form :model="editTagForm" :rules="addTagRules" ref="editTagRef" label-width="100px">
                    <el-form-item label="标签名称" prop="tag">
                        <el-input v-model="editTagForm.tag" clearable></el-input>
                    </el-form-item>
                </el-form>
  
                <span slot="footer" class="dialog-footer">
                    <el-button @click="editDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="editTag">确 定</el-button>
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
            tagList: [],
            queryInfo: {
                tag: "",
                page: 1,
                pageSize: 10
            },
            total: 0,
            addTagForm: {
                tag: ""
            },
            addTagRules:{
                tag: [
                    { required: true, message: '请输入标签名称', trigger: 'blur' },
                ]
            },

            editTagForm: {
                tid: "",
                tag: ""
            },
        }
    },

    created(){
        this.getTagList()
    },

    methods: {
        getTagList(){
            this.$http.post('admin/tag/list', this.queryInfo).then(response => {
                if (response.status === 200){
                    const res = response.data;
                    if (res.status_code === 1000){
                        this.tagList = res.data;
                        this.total = res.total;
                    }else {
                        this.$message.error(res.message)
                    }
                }else {
                    this.$message.error("查询标签信息失败")
                }
            })
        },

        handleSizeChange(newSize){
            this.queryInfo.pageSize = newSize;
            this.getTagList()
        },

        handleCurrentChange(newPage){
            this.queryInfo.page = newPage;
            this.getTagList()
        },

        handleAddClose(){
            this.$refs.addTagRef.resetFields()
        },

        addTag(){
            this.$refs.addTagRef.validate(valid => {
                if (!valid) return;
                this.$http.post('admin/tag/add', this.addTagForm).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.addDialogVisible = false;
                            this.getTagList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("新增标签失败")
                    }
                })
            })
        },

        editTag(){
            this.$refs.editTagRef.validate(valid => {
                if (!valid) return;
                this.$http.post('admin/tag/edit', this.editTagForm).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.editDialogVisible = false;
                            this.getTagList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("修改标签失败")
                    }
                })
            })
        },

        handleEditClick(row){
            this.editDialogVisible = true;
            this.editTagForm.tid = row.tid;
            this.editTagForm.tag = row.tag;
        },

        handleDeleteClick(row){
            this.$confirm('此操作将永久删除该标签, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$http.get('admin/tag/delete', {params: {id: row.tid}}).then(response => {
                    if (response.status === 200){
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success(res.message);
                            this.getTagList();
                        }else {
                            this.$message.error(res.message)
                        }
                    }else {
                        this.$message.error("删除标签失败")
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