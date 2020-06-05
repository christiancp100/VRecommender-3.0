<template>
    <b-container fluid>
        <div v-if="serverData.length > 0">

            <b-alert v-if="error" show dismissible fade variant="danger">
                {{ error }}
            </b-alert>

            <b-row cols="my-auto mx-auto">
                <b-container>
                    <Toolbox v-on:select_tab="onSelectTab"  v-bind:options="options" v-bind:columns="serverData"/>
                </b-container>
            </b-row>


            <b-container fluid>
                <b-row cols-lg="3" cols-sm="1" class="mt-3 mx-auto">
                    <b-col v-for="column in serverData" :key="column.name" class="mb-4">
                        <DescriptionItem
                                v-on:onRemove="onChartRemove"
                                v-on:onSelection="onChartSelection"
                                v-bind:column="column"/>
                    </b-col>
                </b-row>
            </b-container>
        </div>
        <div v-else>
            <h1 class="center" style="margin-top: 20%; color: #1c1c1c">Select a column on the left panel to start 🔥</h1>
        </div>
    </b-container>

</template>

<script>
    import Toolbox from "./Toolbox";
    import DescriptionItem from "./DescriptionItem";
    import {Chart} from "../api/Chart";

    export default {
        name: "DescribeView",
        components: {Toolbox, DescriptionItem},
        props: ["selection", "serverData"],
        data() {
            let selectedForChart = [];
            this.serverData.forEach(c => selectedForChart.push(c.name));
            return {
                selectedForChart: selectedForChart,
                options: [],
                chartSelected: [],
                error: null
            }
        },
        methods: {
            onChartSelection: async function (selection) {
                this.chartSelected.push(selection);
                this.getSuggestedCharts()
            },
            onSelectTab: function (){
                this.$emit("select_tab", 1);
            },
            onChartRemove: async function (remove) {
                this.chartSelected = this.chartSelected.filter(i => i !== remove);
                this.getSuggestedCharts()
            },
            async getSuggestedCharts() {
                if (this.chartSelected.length === 0) {
                    this.options = []
                    return
                }
                try {
                    let response = await Chart.suggestedCharts(this.chartSelected);
                    this.options = []
                    if (response["options"]) {
                        const charts = response["options"]
                        for (let chart of charts) {
                            this.addCheckbox(chart)
                        }
                    } else {
                        this.addCheckbox(response)
                    }
                    this.error = null
                } catch (e) {
                    this.options = []
                    this.error = e.message
                }
            },
            addCheckbox(chart) {
                let option = {
                    "name": chart["name"],
                    "type": chart["chart_type"],
                    "x": chart["x"],
                }
                if (chart["x"] === "ROWS") {
                    return
                }
                if (chart["y"]) {
                    option["y"] = chart["y"]
                    if (!chart["z"]) {
                        if (!chart["aggregation"]) {
                            this.options.push(option)
                        } else {
                            for (let agg of chart["aggregation"]) {
                                if (agg === "count") {
                                    continue
                                }
                                let newOption = {...option}
                                newOption["name"] = `${agg} of ${option["y"]} grouped by ${option["x"]}`
                                newOption["y"] = `${agg}.${option["y"]}`
                                this.options.push({...newOption})
                            }
                        }
                    } else {
                        option["z"] = chart["z"]
                        if (!chart["aggregation"] || option["z"] === "ROWS") {
                            if (option["z"] === "ROWS") {
                                option["name"] = `Count of ${option["z"]} grouped by ${option["x"]} and ${option["y"]}`
                                delete option["z"]
                            }
                            this.options.push({...option})
                        } else {
                            for (let agg of chart["aggregation"]) {
                                let newOption = {...option}
                                newOption["name"] = `${agg} of ${option["z"]} grouped by ${option["x"]} and ${option["y"]}`
                                newOption["y"] = option["y"]
                                newOption["z"] = `${agg}.${option["z"]}`
                                this.options.push({...newOption})
                            }
                        }
                    }
                } else {
                    this.options.push({...option})
                }
            }
        }
    }
</script>

<style scoped>

</style>
