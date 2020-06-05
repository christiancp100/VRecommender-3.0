<template>
    <b-row class="display">
        <b-col :cols="selectedTab === 0 ? 2 : 0">
            <SideBar
                    v-if="selectedTab === 0"
                    v-on:newDateRange="requestNewDateRange"
                    v-on:selectedColumns="requestColumnSelection"
                    v-on:newAirportName="requestAirportSearch"
                    v-bind:columns="columnsInSideBar"
            />
        </b-col>
        <b-col :cols="selectedTab === 0 ? 10 : 12">
            <TopMenu v-on:select_tab="selectedTabEvent($event)"/>
            <template v-if="selectedTab === 0">
                <DescribeView
                        v-on:select_tab="selectedTabEvent($event)"
                        v-bind:serverData="serverData"
                />
            </template>
            <template v-else-if="selectedTab === 1">
                <AnalysisView/>
            </template>
            <template v-else-if="selectedTab === 2">
                <MapView v-bind:serverData="serverData"/>
            </template>
        </b-col>
    </b-row>
</template>

<script>
  import SideBar from "./SideBar";
  import TopMenu from "./TopMenu";
  import DescribeView from "./DescribeView";
  import AnalysisView from "./AnalysisView";
  import _requestColumnSelection, {checkColumn} from "./helpers/requestColumnSelection";
  import {Describe} from "../api/Describe";
  import MapView from "./MapView";

  export default {
    data() {
      return {
        numericalData: [],
        categoricalData: [],
        timestampData: [],
        serverData: [],
        selectedTab: 0,
        columnsInSideBar: [],
        selection: [],
        rendered: [],
        dateRange: null,
        airport_name: null,

        chartSelection: [],
        chartOptions: [],
      };
    },
    async mounted() {
        await this.getColumns();
    },
    components: {MapView, AnalysisView, DescribeView, TopMenu, SideBar},
    methods: {
      selectedTabEvent: function (tab) {
        this.selectedTab = tab;
      },
      requestColumnSelection: _requestColumnSelection,
      requestNewDateRange: function (dateRange) {
        this.dateRange = dateRange;
      },
      requestAirportSearch: function (airportName) {
        this.airport_name = airportName;
      },
      getColumns : async function(){
        let data = await Describe.getColumns();
        data.forEach(col => {
          if(checkColumn(col)){
            this.columnsInSideBar.push(col);
          }
        });
      }
    }
  };
</script>

<style scoped>
    div {
        padding: 0;
    }

    .display {
        width: 100%;
        height: 100vh;
        padding: 0;
        margin: 0;
    }
</style>
