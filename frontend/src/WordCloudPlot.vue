<template>
  <div id="WordCloudPlot" style="height: inherit" >
    <div class="item">
      <div id="mzgqc" style="width: 1400px;height:650px;"></div>
      <!--      <div id="line"></div>-->
      <div class="search">
        <el-select @change="changeFun" v-model="sharch" placeholder="Please select:">
          <el-option
              v-for="item in headList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </div>
    </div>
  </div>
</template>

<script>
import {myEcharts} from '../util/wordcloud'
import axios from 'axios'
export default {
  name: "WordCloudPlot",
  data() {
    return {
      address:[
        { label: 'Lack of Health Insurance', value: 'Lack of Health Insurance'},
        { label: 'Arthritis', value: 'Arthritis'},
        { label: 'Binge Drinking', value: 'Binge Drinking'},
        { label: 'High Blood Pressure', value: 'High Blood Pressure'},
        { label: 'Blood Pressure Medication', value: 'Blood Pressure Medication'},
        { label: 'Cancer', value: 'Cancer'},
        { label: 'Asthma', value: 'Asthma'},
        { label: 'Coronary Heart Disease', value: 'Coronary Heart Disease'},
        { label: 'Annual Checkup', value: 'Annual Checkup'},
        { label: 'Cholesterol Screening', value: 'Cholesterol Screening'},
        { label: 'Colonoscopy', value: 'Colonoscopy'},
        { label: 'Chronic obstructive pulmonary disease', value: 'Chronic obstructive pulmonary disease'},
        { label: 'Preventive Services (Older Men)', value: 'Preventive Services (Older Men)'},
        { label: 'Preventive Services (Older Women)', value: 'Preventive Services (Older Women)'},
        { label: 'Smoking', value: 'Smoking'},
        { label: 'Dental Visit', value: 'Dental Visit'},
        { label: 'Diabetes', value: 'Diabetes'},
        { label: 'High Cholesterol', value: 'High Cholesterol'},
        { label: 'Kidney Disease', value: 'Kidney Disease'},
        { label: 'Physical Inactivity', value: 'Physical Inactivity'},
        { label: 'Mammography', value: 'Mammography'},
        { label: 'Poor Mental Health', value: 'Poor Mental Health'},
        { label: 'Obesity', value: 'Obesity'},
        { label: 'Cervical Cancer Screening', value: 'Cervical Cancer Screening'},
        { label: 'Poor Physical Health', value: 'Poor Physical Health'},
        { label: 'Sleep < 7 hrs', value: 'Sleep < 7 hrs'},
        { label: 'Stroke', value: 'Stroke'},
        { label: 'Teethlost', value: 'Teethlost'}
      ],
      list: [],
      headList: [],
      sharch: ''
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    drawWordCloudPlot() {
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/word',
        data: {
          sharch: this.sharch
        }
      }).then(res => {
        myEcharts(res.data,this.sharch)
      })
    },
    changeFun() {
      this.drawWordCloudPlot()
    },
    getList() {
      axios({
        url: 'http://127.0.0.1:5000/list',
        method: 'get'
      }).then(res => {
        res.data.shift()
        //console.log(this.sharch)
        this.headList = []
        res.data.forEach((el,index) => {
          let obj = {
            label: el,
            value: el
          }
          this.headList.push(obj)
          if(index === 0) {
            this.sharch = el
          }
        })
        console.log('test1')
        console.log(this.sharch)
        console.log('test2')
        console.log(typeof(this.sharch))
        this.drawWordCloudPlot()
      })
    },
  }
}
</script>
