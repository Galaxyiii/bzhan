<template>
  <div class="common-layout">
    <el-container>

      <el-aside width="200px">
        <el-row class="" style="width:200px;position: fixed;">
          <el-col>

            <el-menu default-active="1">
              <el-menu-item index="1" @click='click1'>
                <el-icon>
                  <icon-menu />
                </el-icon>
                <span>整体情况</span>
              </el-menu-item>

              <el-menu-item index="2" @click='click2'>
                <el-icon>
                  <icon-menu />
                </el-icon>
                <span>个体情况</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-aside>

      <el-main style="width:100%">
        <div v-show="page.which === '1'">
          <div>
            <h2 style="width: 100%; text-align: center;">2023年12月1日-10日各个分区视频发布量占比</h2>
            <div id="pie-chart" class="chart" v-loading="loading_1"></div>
          </div>
          <el-divider></el-divider>
          <div>
            <h2 style="width: 100%; text-align: center;">2023年12月1日-10日视频标题词云图</h2>
            <div id="wordcloud-chart" class="chart" v-loading="loading_1"></div>
          </div>
          <el-divider></el-divider>
          <div>
            <h2 style="width: 100%; text-align: center;">tags关联度热力图</h2>
            <div class="choose-container">
              <div style="display: flex; align-items: center; justify-content: center;">
                <div style="width: auto;">请输入标签：</div>
                <el-select v-model="value" multiple filterable remote reserve-keyword placeholder="Please enter a tag"
                  remote-show-suffix :remote-method="remoteMethod" :loading="loading"
                  style="width:80%; margin-left: 10px; margin-right: 10px;">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
                <el-button type="primary" @click="clickQuery">查询</el-button>
              </div>
            </div>
            <div id="heat-chart" class="chart" v-loading="loading_3"></div>
          </div>
          <el-divider></el-divider>
          <div>
            <h2 style="width: 100%; text-align: center;" @click="displayBar(bar_data)">2023年12月1日-10日 日热门tags变化柱状图</h2>
            <div id="bar-chart" class="chart" v-loading="loading_2"></div>
          </div>
          <el-divider></el-divider>
          <div>
            <h2 style="width: 100%; text-align: center;" @click="displayLine(line_data)">2023年12月1日-10日 日tags动态折线图</h2>
            <div id="line-chart" class="chart" v-loading="loading_1"></div>
          </div>
        </div>

        <div v-if="page.which === '2'">
          <el-row>
            <el-col :span="12">
              <el-form label-width="120px">
                <el-form-item label="视频bv或av号">
                  <el-input v-model="sing.id" style="width:300px" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="onSubmit">查询</el-button>
                  <el-button @click="() => { sing.id = '' }">清空</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
          <!-- <div v-loading="page.loading_info"> -->
          <vedio :msg="sing" v-show="page.info_show"></vedio>
          <!-- </div> -->
          <el-row style="margin-top:0px;">
            <el-col :span="8">
              <div id="rank-chart" style="height:400px; width:400px;"></div>
              <span v-if="page.rank_chart_show"
                style="position:absolute;top:22px;left: 5px;font-size: 16px;">(超过其他视频百分比)</span>
            </el-col>
            <el-col :span="8">
              <div id="wordcloud-chart2" style="height:400px; width:400px;"></div>
            </el-col>

            <el-col :span="8">
              <div id="pie-chart2" style="height:400px; width:400px;"></div>
            </el-col>
          </el-row>
        </div>
      </el-main>

    </el-container>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const bar_data = ref([])
const line_data = ref([])

const sever = 'http://localhost:8000'
const page = reactive({
  which: '1',
  rank_chart_show: 0,
  info_show: false,
  loading_info: false,
  loading1: false,
  loading2: false,
  loading3: false,
})
const click1 = () => {
  page.which = '1'
}
const click2 = () => {
  page.which = '2'
}
const sing = reactive({
  id: '',
  pic: 'https://i0.hdslb.com/bfs/archive/4f48196287dc053d92b07eb0411260368444e20a.jpg',
  title: "苹果M4性能分析：尽力了，但芯片工艺快到头了！",
  bv: '',
  up: '极客湾Geekerwan',
  view: 0,
  danmu: 0,
  reply: 0,
  favorite: 0,
  coin: 0,
  share: 0,
  like: 0,
  like_rate: 0,
  coin_rate: 0,
  favorite_rate: 0,
  share_rate: 0,
  reply_rate: 0,
  danmu_rate: 0,
  interact_rate: 0,
  honor: "",
  word_data: [{ "value": "42", "name": "存活", }, { value: '30', name: 'VIVO' }],
  pie: []
})

const onSubmit = () => {
  page.loading_info = true;

  let formData = new FormData();
  formData.append('video_id', sing.id);
  axios.post(sever + '/single-video/basic-info', formData)
    .then((res) => {
      let data = res.data.data;
      sing.pic = data.pic || '';
      sing.title = data.title || '';
      sing.bv = data.bvid || '';
      let owner = data.owner || {};
      sing.up = owner.name || '';
      let stat = data.stat || {};
      sing.view = stat.view || 0;
      sing.danmu = stat.danmaku || 0;
      sing.reply = stat.reply || 0;
      sing.favorite = stat.favorite || 0;
      sing.coin = stat.coin || 0;
      sing.share = stat.share || 0;
      sing.like = stat.like || 0;
      sing.like_rate = stat.like_rate || 0;
      sing.coin_rate = stat.coin_rate || 0;
      sing.favorite_rate = stat.favorite_rate || 0;
      sing.danmu_rate = stat.danmaku_rate || 0;
      sing.share_rate = stat.share_rate || 0;
      sing.reply_rate = stat.reply_rate || 0;
      sing.interact_rate = stat.interact_rate || 0;
      sing.honor = '';
      if (data.honor) {
        for (let h of data.honor) {
          sing.honor += h.desc;
          sing.honor += '，';
        }
      }
      if (data.honor) sing.honor = sing.honor.substring(0, sing.honor.length - 1);
      page.loading_info = false;
      page.info_show = true;

      let rank_data = data.rank_data || {};
      var rank = [
        rank_data.view || 0,
        rank_data.like_rate || 0,
        rank_data.interact_rate || 0,
        rank_data.coin_rate || 0,
        rank_data.share_rate || 0,
        rank_data.favorite_rate || 0
      ];
      var chartDom = document.getElementById('rank-chart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '排名雷达图'
        },
        legend: {
          data: ['']
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        radar: {
          indicator: [
            { name: '播放量', max: 1 },
            { name: '点赞率', max: 1 },
            { name: '互动率', max: 1 },
            { name: '投币率', max: 1 },
            { name: '分享率', max: 1 },
            { name: '收藏率', max: 1 }
          ]
        },
        series: [
          {
            name: 'Budget vs spending',
            type: 'radar',
            data: [
              {
                value: rank,
                name: 'Allocated Budget'
              }
            ]
          }
        ]
      };
      option && myChart.setOption(option);
      page.rank_chart_show = 1;
    })
    .catch((error) => {
      console.error("Error fetching basic info:", error);
      page.loading_info = false;
    })
    .then(() => {
      axios.post(sever + '/single-video/replies-word-data', formData)
        .then((res) => {
          let data = res.data.data.word_data || [];
          sing.word_data = [];
          const color = () => {
            let colors = ['#fe9a8bb3', '#fe9a8bb3', '#fe9a8b03', '#9E87FFb3', '#9E87FFb3', '#9E87FFb3', '#fe9a8bb3', '#fe9a8bb3', '#fe9a8bb3', '#73DDFF', '#58D5FF'];
            return colors[parseInt(Math.random() * 10)];
          };
          for (let i of data) {
            let tmp = {};
            tmp['value'] = String(i[1]);
            tmp['name'] = i[0];
            tmp['textStyle'] = {};
            tmp['textStyle']['color'] = color();
            sing.word_data.push(tmp);
            if (sing.word_data.length >= 25) break;
          }

          let myChart = echarts.init(document.getElementById("wordcloud-chart2"));
          myChart.setOption({
            backgroundColor: '#fff',
            toolbox: {
              show: true,
              feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                restore: { show: true },
                saveAsImage: { show: true }
              }
            },
            title: {
              text: '评论云图',
              left: '-1%',
              textStyle: {
                color: '#3B3E41',
              }
            },
            series: [
              {
                type: 'wordCloud',
                left: '10%',
                top: '0%',
                width: '100%',
                height: '100%',
                sizeRange: [12, 50],
                rotationRange: [0, 0],
                gridSize: 25,
                layoutAnimation: true,
                textStyle: {
                  normal: {
                    color() {
                      let colors = ['#fe9a8bb3', '#fe9a8bb3', '#fe9a8b03', '#9E87FFb3', '#9E87FFb3', '#9E87FFb3', '#fe9a8bb3', '#fe9a8bb3', '#fe9a8bb3', '#73DDFF', '#58D5FF'];
                      return colors[parseInt(Math.random() * 10)];
                    }
                  }
                },
                data: sing.word_data
              }
            ]
          });
        })
        .then(() => {
          axios.post(sever + '/single-video/replies-sentiment', formData)
            .then((res) => {
              let data = res.data.data || {};
              sing.pie = [
                { value: (data.pos_rate || 0) + 0.001, name: '好评' },
                { value: (data.neg_rate || 0) + 0.001, name: '差评' }
              ];

              var chartDom = document.getElementById('pie-chart2');
              var myChart = echarts.init(chartDom);
              var option = {
                color: ['#ee6666', '#5470c6'],
                title: {
                  text: '评论情感',
                  subtext: '',
                  left: 'left'
                },
                tooltip: {
                  trigger: 'item'
                },
                legend: {
                  orient: 'vertical',
                  left: 'right'
                },
                series: [
                  {
                    type: 'pie',
                    radius: '50%',
                    data: sing.pie,
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
              option && myChart.setOption(option);
            });
        });
    });
}


// const clear = () => { sing.id = '' }

const list = ref([])
const options = ref([])
const value = ref([])
const loading = ref(false)

const remoteMethod = (query) => {
  let formData = new FormData()
  formData.append("word", query)
  loading.value = true
  axios.post(sever + '/all-video/tags-count-by-word', formData)
    .then((res) => {
      let data = res.data.data["tags_count_by_word"]
      list.value = data.map((item) => {
        return { value: `${item[0]}`, label: `${item[0]}` }
      })
      loading.value = false
      options.value = list.value.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase())
      })
    })
}

const clickQuery = () => {
  // console.log(value)
  let tagData = new FormData()
  let tags = value.value.join(",")
  tagData.append("tags", tags)
  loading_3.value = true
  axios.post(sever + '/all-video/tags-relation', tagData)
    .then((res) => {
      let data = res.data.data
      displayHeat(tags, data["tags_relation"])
      loading_3.value = false
    })
}

const loading_1 = ref(true)
const loading_2 = ref(true)
const loading_3 = ref(true)

const displayWordcloud = (data) => {
  let chart = echarts.init(document.getElementById('wordcloud-chart'))
  let new_data = []
  for (let k in data) {
    new_data.push({ "name": k, "value": data[k] })
  }
  chart.setOption({
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '80%', // 调整词云容器的宽度
      height: '80%', // 调整词云容器的高度
      sizeRange: [20, 80], // 调整词的大小范围
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 2,
      drawOutOfBound: false,
      shrinkToFit: false,
      layoutAnimation: true,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160)
          ].join(',') + ')'
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          textShadowBlur: 10,
          textShadowColor: '#333'
        }
      },
      data: new_data
    }]
  })
}


const displayPie = (data) => {
  let chartDom = document.getElementById('pie-chart')
  let myChart = echarts.init(chartDom)
  let option
  let new_data = []
  for (let k in data) {
    new_data.push({ "name": k, "value": data[k] })
  }
  option = {
    legend: {
      top: 'bottom'
    },
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    series: [
      {
        name: 'Nightingale Chart',
        type: 'pie',
        radius: [50, 250],
        center: ['50%', '50%'],
        roseType: 'area',
        itemStyle: {
          borderRadius: 8
        },
        data: new_data
      }
    ]
  }
  option && myChart.setOption(option)
}

const displayLine = (data) => {
  let chartDom = document.getElementById('line-chart');
  if (!chartDom) {
    console.error('Element with id "line-chart" not found');
    return;
  }

  // 如果已经有图表实例，清理它
  if (echarts.getInstanceByDom(chartDom)) {
    echarts.getInstanceByDom(chartDom).dispose();
  }

  let myChart = echarts.init(chartDom);
  let option;

  // 提取所有区域
  let areas = new Set();
  for (let day in data) {
    for (let area in data[day]) {
      areas.add(area);
    }
  }
  areas = Array.from(areas);

  // 构建原始数据数组
  let raw_data = [];
  raw_data.push(["Day", "Area", "Count"]);
  for (let day in data) {
    for (let area in data[day]) {
      raw_data.push([Number(day), area, data[day][area]]);
    }
  }

  function run(_rawData) {
    const datasetWithFilters = [];
    const seriesList = [];

    echarts.util.each(areas, function (area) {
      var datasetId = 'dataset_' + area;
      datasetWithFilters.push({
        id: datasetId,
        fromDatasetId: 'dataset_raw',
        transform: {
          type: 'filter',
          config: {
            and: [
              { dimension: 'Day', gte: 20231201 },
              { dimension: 'Area', '=': area }
            ]
          }
        }
      });

      seriesList.push({
        type: 'line',
        datasetId: datasetId,
        showSymbol: false,
        name: area,
        endLabel: {
          show: true,
          formatter: function (params) {
            return params.value[2] + ': ' + params.value[0];
          }
        },
        labelLayout: {
          moveOverlap: 'shiftY'
        },
        emphasis: {
          focus: 'series'
        },
        encode: {
          x: 'Day',
          y: 'Count',
          label: ['Area', 'Count'],
          itemName: 'Day',
          tooltip: ['Count']
        }
      });
    });

    option = {
      toolbox: {
        show: true,
        feature: {
          mark: { show: true },
          dataView: { show: true, readOnly: false },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      animationDuration: 5000,
      dataset: [
        {
          id: 'dataset_raw',
          source: _rawData
        },
        ...datasetWithFilters
      ],
      tooltip: {
        order: 'valueDesc',
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        nameLocation: 'middle'
      },
      yAxis: {
        name: 'Count'
      },
      grid: {
        right: 140
      },
      series: seriesList
    };

    // 使用 setTimeout 确保在下一次事件循环中调用 setOption
    setTimeout(() => {
      myChart.setOption(option);
    }, 0);
  }

  run(raw_data);
  option && myChart.setOption(option);
}

const displayBar = (data) => {
  // console.log(data)
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.getElementById('bar-chart'))
  var updateFrequency = 1000	// 数据更新速度
  var new_data = []
  var startIndex = 0

  for (let day in data) {
    let tags = []
    let counts = []

    data[day].forEach(element => {
      tags.push(element.tag);
      counts.push(element.count);
    });
    new_data.push({ "day": day, "tag": tags, "count": counts });
  }

  // console.log(new_data)
  // 获取第一个数据
  var startDay = new_data[startIndex].day
  var startTag = new_data[startIndex].tag
  var startCount = new_data[startIndex].count

  var option = {
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    // 图标的上下左右边界
    grid: {
      top: 10,
      bottom: 30,
      left: 120,
      right: 120
    },
    // x 轴相关
    xAxis: {
      max: 'dataMax',
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(100,100,100, 0.4)',
          type: 'dashed'
        }
      },

      axisLabel: {
        // 圆整 X 轴 参数
        formatter: function (n) {
          return Math.round(n) + ''
        }
      }
    },
    dataset: {
      source: new_data
    },
    // y 轴数据
    yAxis: {
      type: 'category',
      inverse: true, 	// 大在上面，小在下面排序
      max: 5,			// 最多显示个数
      data: startTag,
      axisLabel: {
        show: true,
        textStyle: {
          fontSize: 14
        },
        rich: {
          flag: {
            fontSize: 25,
            padding: 5
          }
        }
      },
      animationDuration: 400,
      animationDurationUpdate: 300
    },
    series: [{
      realtimeSort: true,
      seriesLayoutBy: 'column',
      type: 'bar',
      itemStyle: {
        /* color: 'rgb(13,208,229)' */
        color: function (param) {

          return 'rgb(84,111,198)'//countryColors[param.name];
        }
      },
      encode: {
        x: 0,
        y: 3
      },
      label: {
        show: true,
        precision: 1,
        position: 'right',
        valueAnimation: true,
      },
      data: startCount
    }],

    animationDuration: 0,
    animationDurationUpdate: 500,
    animationEasing: 'linear',
    animationEasingUpdate: 'linear',
    graphic: {
      // 年代的文字 Text
      elements: [{
        type: 'text',
        right: 120,
        bottom: 60,
        style: {
          text: "" + startDay,
          font: 'bolder 30px Times New Roman',
          fill: 'rgba(100, 100, 100, 0.25)'
        },
        z: 100
      }]
    }
  }

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option)
  for (var i = startIndex; i < new_data.length - 1; ++i) {
    (function (i) {
      setTimeout(function () {
        updateDay(new_data[i + 1])
      }, (i + 1) * updateFrequency)
    })(i)
  }

  // 更新数据
  function updateDay(dt) {
    option.yAxis.data = dt.tag
    option.series[0].data = dt.count
    option.graphic.elements[0].style.text = "" + dt.day
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option)
  }
}

const displayHeat = (tags, items) => {
  // console.log(items)

  var chartDom = document.getElementById('heat-chart')
  var myChart = echarts.init(chartDom)
  var option

  // prettier-ignore
  const hours = tags.split(",")
  // prettier-ignore
  const days = tags.split(",")

  const data = items
    .map(function (item) {
      return [item[1], item[0], item[2] || '-']
    })
  option = {
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: {
        show: true
      }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: 0.5,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%'
    },
    series: [
      {
        name: '关系度',
        type: 'heatmap',
        data: data,
        label: {
          show: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  option && myChart.setOption(option)

}


onMounted(() => {
  let formData = new FormData()
  formData.append("num", 100)

  axios.post(sever + '/all-video/all-video-info', formData)
    .then((res) => {
      let data = res.data.data
      displayPie(data["rate_data"])
      displayWordcloud(data["words_count"])
      // displayLine(data["line_data"])
      line_data.value = data["line_data"]
      loading_1.value = false
    })

  axios.post(sever + '/all-video/tags-count-in-day')
    .then((res) => {
      let data = res.data.data
      // displayBar(data["tags_count_in_day"])
      loading_2.value = false
      bar_data.value = data["tags_count_in_day"]
    })

  loading.value = false
  axios.post(sever + '/all-video/tags-count-by-word')
    .then((res) => {
      let data = res.data.data["tags_count_by_word"]
      list.value = data.map((item) => {
        return { value: `${item[0]}`, label: `${item[0]}` }
      })
      options.value = list.value
      loading.value = false
    })
})

</script>

<style>
.page-all {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 100%;
}

.chart {
  width: 100%;
  height: 70vh;
}
</style>
