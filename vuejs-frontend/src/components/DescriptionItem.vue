<template>
    <div class="custom-card ">
        <b-row>
            <b-col md="12" class="card-style">
                <b-card no-body class="card-style--2" style="height:100%">
                    <b-row style="height:100%" align-v="stretch">
                        <b-col md="12">
                            <b-alert class="alert mb-0"
                                     variant="primary"
                                     show
                                     v-if="column.type === 'categorical'">
                                <b-icon-exclamation-triangle-fill/>
                                You are seeing the top 10 results
                            </b-alert>


                            <b-card-body style="border: none;" :title="column.name">
                                <span class="data-type">Data type: {{column.type}}</span>
                                <b-list-group>

                                    <b-list-group-item
                                            v-for="(data, item) in column.description" :key="item">
                                        <div v-if="item === 'top' && column.type !== 'timestamp'">
                                            <b>top:</b> <br>
                                            <span v-for="(value, order) in item" :key="order">
                                                <b>{{order+1}}) </b> {{data[order+1]}}
                                            </span>
                                        </div>
                                        <div v-else-if="item === 'Most Freq' && column.type === 'categorical'">
                                            <b>top:</b> <br>
                                            <span v-for="(value, order) in item" :key="order">
                                                <b v-if="data[order+1]">{{order+1}}) </b> {{data[order+1]}}
                                            </span>
                                        </div>

                                        <div v-else>
                                            <b>{{item}}:</b>
                                            {{data}}
                                        </div>
                                    </b-list-group-item>
                                </b-list-group>
                                <b-list-group style="margin-top: 1rem">
                                    <b-list-group-item>
                                        <b>Select {{column.type === 'timestamp' ? "a time interval (default is month)" : "the number of bars to display: "  }}</b>
                                        <b-row style="margin-top: 1rem">
                                            <b-col>
                                                <b-form-select
                                                        v-model="argSelected"
                                                        v-on:input="() => getChartData({range: argSelected, interval: argSelected, order: orderSelected})"
                                                        :options="column.type === 'timestamp' ? interval : bars"
                                                />
                                            </b-col>
                                            <b-col>
                                                <b-form-select
                                                        v-model="orderSelected"
                                                        v-on:input="() => getChartData({range: argSelected, interval: argSelected, order: orderSelected})"
                                                        :options="[{ value: null, text: 'Sort' },'ASC', 'DESC']"
                                                />
                                            </b-col>
                                        </b-row>

                                    </b-list-group-item>
                                </b-list-group>
                                <div class="chart-container">
                                    <BarChart v-bind:chartData="chartData"/>
                                </div>
                            </b-card-body>
                        </b-col>
                        <b-col md="12" align-self="baseline">
                            <div class="chart-container">
                                <BarChart v-bind:chartData="chartData"/>
                            </div>
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>

            <b-col md="12">
                <input :v-model="column.name" v-if="chartSelected" type="button" v-on:click="select"
                       class="select-btn select-btn-selected" value="SELECTED"/>
                <input v-else type="button" v-on:click="select" class="select-btn" value="SELECT"/>
            </b-col>
        </b-row>
    </div>
</template>

<script>
  import BarChart from "./charts/BarChart";
  import {DistributionCharts} from "../api/DistributionCharts";


  export default {
    name: "DescriptionItem",
    components: {BarChart},
    props: ["column"],
    data() {
      return {
        bars: [{ value: null, text: 'Number of bars' },1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        interval: [{ value: null, text: 'Date frame' },"year", "month", "day"],
        argSelected : null,
        orderSelected : null,
        chartSelected: false,
        chartData: {
          values: [],
          encoding: {}
        },
      }
    },
    async mounted() {
      await this.getChartData();
    },

    methods: {
      select: function () {
        this.chartSelected = !this.chartSelected;
        if (this.chartSelected === true) {
          this.$emit("onSelection", this.column.value);
        } else {
          this.$emit("onRemove", this.column.value);
        }
      },
      getChartData : async function (args={range : 10, interval : "month", order : "DESC"}){
        let res = await DistributionCharts.get(this.column, args);
        this.chartData = res;
        return res;
      }
    }
  }
</script>

<style scoped>

    .select-btn {
        outline: none;
        background-color: #1c1c1c;
        width: 100%;
        height: 3rem;
        color: white;
        font-size: 1.2rem;
        bottom: 0;
        border: 0;
        border-radius: 0 0 5px 5px;
    }

    .select-btn-selected {
        background-color: #ff1e56;
    }

    .card-style {
        height: 48rem;
    }

    .card-style--2 {
        max-width: 540px;
        border-radius: 5px 5px 0 0;
        border: none;
    }

    .custom-card {
        border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.69);
    }

    .chart-container {
        margin-top: 1.2rem;
        margin-left: -15% !important;
        overflow-y: scroll;
        z-index: 100 !important;
    }

    .alert {
        border-radius: 5px 5px 0 0;
        border: none;
        background-color: #1c1c1c;
        font-weight: 700;
        color: white;
    }

    .data-type {
        font-size: 1rem;
        color: grey;
        text-transform: capitalize;
        margin-bottom: 0.3rem;
        font-style: italic;
        font-weight: 400;
    }


</style>