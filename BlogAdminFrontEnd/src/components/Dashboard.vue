<template>
    <div class="content">
        <el-row>
            <el-col :span="12" class="dash-head">
                <div style="line-height: 60px; margin-left: 16px; margin-bottom: 16px; font-size: 24px; font-weight: bold;">后台数据统计</div>
            </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-bottom: 24px;">
            <el-col :span="6">                     
                <el-card class="box-card" style="background-color: #17A2B8; width: 300px">
                    <div style="display: flex; justify-content: space-between;"> 
                        <div>
                            <i class="iconfont icon-wangluo" style="font-size: 64px; color: white"></i>
                        </div>
                        <ul>
                            <li style="color: white; font-size: 24px; font-weight: blod">访问量</li>
                            <li style="color: white; font-size: 30px; font-weight: blod">50, 000</li>
                        </ul>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card class="box-card" style="background-color: #6F42C1; width: 300px">
                    <div style="display: flex; justify-content: space-between;"> 
                        <div>
                            <i class="iconfont icon-bianjiwenzhang_huaban" style="font-size: 64px; color: white"></i>
                        </div>
                        <ul>
                            <li style="color: white; font-size: 24px; font-weight: blod">文章数</li>
                            <li style="color: white; font-size: 30px; font-weight: blod">50, 000</li>
                        </ul>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card class="box-card" style="background-color: #1CAF9A; width: 300px">
                    <div style="display: flex; justify-content: space-between;"> 
                        <div>
                            <i class="iconfont icon-yuedu" style="font-size: 64px; color: white"></i>
                        </div>
                        <ul>
                            <li style="color: white; font-size: 24px; font-weight: blod">阅读量</li>
                            <li style="color: white; font-size: 30px; font-weight: blod">50, 000</li>
                        </ul>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card class="box-card" style="background-color: #0866C6; width: 300px">
                    <div style="display: flex; justify-content: space-between;"> 
                        <div>
                            <i class="iconfont icon-dianzan" style="font-size: 64px; color: white"></i>
                        </div>
                        <ul>
                            <li style="color: white; font-size: 24px; font-weight: blod">点赞数</li>
                            <li style="color: white; font-size: 30px; font-weight: blod">50, 000</li>
                        </ul>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="10">
            <el-col :span="16">
                <el-card class="box-card" style="margin-bottom: 16px;">
                    <div id="daliy" style="width: 100%; height: 400px"></div>
                </el-card>
                 <el-card class="box-card">
                     <div id="thumb" style="width: 100%; height: 400px"></div>
                 </el-card>
            </el-col>
            <el-col :span="8">
                 <el-card class="box-card">
                     <div id="category" style="width: 100%; height: 300px"></div>
                 </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
   data(){
       return {
          
       }
   },

   mounted(){
      this.dailyBrowse();
      this.thumbCount();
      this.categoryDetail();
   },

   methods: {
      dailyBrowse(){
          var myChart = this.$echarts.init(document.getElementById('daliy'));

          var option = {
            title: {
                text: '日访问量',
                x: 'center'
            },

            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Sun', 'Sun', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                data: [150, 230, 224, 218, 135, 147, 260, 260, 260, 260],
                type: 'line'
                }
            ]
        };
        myChart.setOption(option);

      },

      thumbCount(){
          var myChart = this.$echarts.init(document.getElementById('thumb'));

          var option = {
            title: {
                text: '点赞数排名',
                x: 'center'
            },

            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Sun', 'Sun', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [150, 230, 224, 218, 135, 147, 260, 260, 260, 260],
                    type: 'bar'
                }
            ]
        };
        myChart.setOption(option);
      },

      categoryDetail(){
          var myChart = this.$echarts.init(document.getElementById('category'));

          var option = {
            title: {
                text: 'Referer of a Website',
                subtext: 'Fake Data',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [
                {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: 1048, name: 'Search Engine' },
                    { value: 735, name: 'Direct' },
                    { value: 580, name: 'Email' },
                    { value: 484, name: 'Union Ads' },
                    { value: 300, name: 'Video Ads' }
                ],
                emphasis: {
                    itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
                }
            ]
        };
        myChart.setOption(option);
      }
   },
}
</script>

<style scoped>
    .content {
        width: 90%;
        margin: 0 auto;
    }

    .dash-head {
        display: flex;   
    }

    /deep/ .el-card__header {
        border-bottom: none;
        
    }

</style>