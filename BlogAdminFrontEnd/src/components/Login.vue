<template>
  <div class="login_container">
      <div class="login_box">
          
        <!-- 头像区域 -->
        <div class="avatar">
            <img src="@/assets/img/avatar.png" alt="">
        </div>

        <!-- 登陆表单区域 -->
        <el-form label-width="0px" class="login_form" :model="loginForm" :rules="loginFormRules" ref="loginFormRef">
            <!-- 用户名 -->
            <el-form-item prop="username">
                <el-input prefix-icon="iconfont icon-icon_user" v-model="loginForm.username"></el-input>
            </el-form-item>

            <!-- 密码 -->
            <el-form-item prop="password">
                <el-input prefix-icon="iconfont icon-3702mima" v-model="loginForm.password" type="password"></el-input>
            </el-form-item>

            <!-- 按钮区域 -->
            <el-form-item class="btns">
                <el-button type="primary" @click="login">登录</el-button>
                <el-button type="info" @click="resetLoginForm">重置</el-button>
            </el-form-item>

        </el-form>

      </div>
  </div>
</template>

<script>
    import {encrypted, } from '@/assets/js/passWordEncrypt.js'
    export default {
        data(){
            return {

                // 这是表单对象绑定的数据
                loginForm: {
                    username: "chendacheng",
                    password: "cdc19951216"
                },

                // 表单验证对象
                loginFormRules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                    ]
                }
            }
        },

        methods: {
            resetLoginForm(){
                this.$refs.loginFormRef.resetFields()
            },

            login(){
                this.$refs.loginFormRef.validate((valid)=>{
                    if (!valid) return;

                    const userInfo = {
                        userName: this.loginForm.username,
                        passWord: encrypted('#5rym@0$r^ma*8#@', this.loginForm.password)
                    }

                    this.$http.post("admin/user/login", userInfo). then(response => {
                        const res = response.data;
                        if (res.status_code === 1000){
                            this.$message.success("登录成功");
                            window.sessionStorage.setItem("AUTHORIZATION", res.data.token);
                            this.$router.push('/config');
                        }else {
                            this.$message.error("登录失败，" + res.message)
                        }
                    })
                })
            },
        }

    };
</script>

<style scoped>
    .login_container {
        background-color: #2b4b6b;
        height: 100%;
        width: 100%;

    }

    .login_box {
        width: 450px;
        height: 300px;
        background-color: #fff;
        border-radius: 3px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .avatar {
        height: 130px;
        width: 130px;
        border: 1px solid #eee;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 0 10px;
        position: absolute;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #fff;
    }

    .avatar > img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
        background-color: #eee;
    }

    .btns {
        display: flex;
        justify-content: flex-end;
    }

    .login_form {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 10px 30px;
        box-sizing: border-box;
    }

</style>