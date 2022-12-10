<template>
  <v-tabs
    fixed-tabs
    background-color="indigo"
    dark
  >
    <v-tab>
      Map Overview
    </v-tab>
    <v-tab>
      Correlational Study
    </v-tab>
    <v-tab>
      CHD Prediction
    </v-tab>
    <v-tab-item>
      <v-main>
        <MapPlot/>
      </v-main>
    </v-tab-item>
    <v-tab-item>
      <div>
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="20">
            <WordCloudPlot/>
          </v-col>
          <v-col cols="12" md="10">
            <ScatterPlot/>
          </v-col>
        </v-row>
      </v-container>
      </div>
    </v-tab-item>
    <v-tab-item>
      prediction here
    </v-tab-item>
</v-tabs>
</template>
<script>
import ScatterPlot from './ScatterPlot';
import WordCloudPlot from './WordCloudPlot';
import MapPlot from './MapPlot';
export default {
  components: {MapPlot, ScatterPlot, WordCloudPlot},
  data: () => ({
  }),
}
</script>



