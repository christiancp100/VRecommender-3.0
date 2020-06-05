<template>
    <div class="toolbox mx-auto fluid">
        <b-row>
            <b-col cols="12 fields-to-display-txt">
                <h4 v-if="options.length > 0">Which columns do you want to display?</h4>
                <h4 v-else style="text-align:center">Select the fields on which you want to see some insights :)</h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="10">
                <b-form-group>
                        <b-form-checkbox
                            v-for="(option, i) in options"
                            v-model="chartSelection"
                            :key="option.name"
                            :value="i"
                            name="chart-selection"
                            class="checkbox-group my-auto"
                            inline
                        >
                            {{option.name}}
                        </b-form-checkbox>
                </b-form-group>
            </b-col>
            <b-col cols="2" v-if="options.length > 0">
                <b-button class="create-button" v-if="loading" disabled>
                    <b-spinner small></b-spinner>
                    <span class="sr-only">Loading...</span>
                </b-button>
                <button v-else-if="chartSelection.length > 0" v-on:click="createCharts" class="create-button create-button-hover">CREATE</button>
            </b-col>
        </b-row>
        <b-alert v-if="created" show dismissible fade variant="success">
            Chart created. Look in the "Analysis tab"
        </b-alert>
    </div>

</template>

<script>
import { Chart } from "@/api/Chart"
import { DistributionCharts } from '../api/DistributionCharts'
    export default {
        name: "Toolbox",
        props: ["options", "columns"],
        data() {
            return {
                chartSelection: [],
                created: false,
                loading: false,
            }
        },
        methods: {
            createCharts: async function () {
                try {
                    this.loading = true
                    let charts = []
                    for (let i of this.chartSelection) {
                        let chart = {}
                        chart["type"] = this.options[i]["type"]
                        chart["x"] = this.options[i]["x"]
                        chart["name"] = this.options[i]["name"]
                        if (this.options[i]["y"]) {
                            chart["y"] = this.options[i]["y"]
                            if (this.options[i]["z"]) {
                                // Three dimensions chart
                                chart["z"] = this.options[i]["z"]
                                const data = await Chart.threeColumnsChart(chart["x"], chart["y"], chart["z"], chart["type"])
                                const values = this.prepareChartOptions(data)
                                
                                let encoding = {
                                    x: { field: data["x_label"], type: (typeof data["x_axis"][0] == "number") ? 'quantitative' : "nominal" },
                                    y: { field: data["y_label"], type: (typeof data["y_axis"][0] == "number") ? 'quantitative' : "nominal" },
                                }
                                if (encoding.x.type === "nominal") {
                                    encoding.color = {"aggregate": chart["name"].split(" ")[0], "field": data["z_label"], "type": "quantitative"}
                                    encoding.text = { field: data["z_label"], type: "quantitative"}
                                } else {
                                    encoding.size = { field: data["z_label"], type: "quantitative"}
                                }
                                if (encoding.x.field === "DAY_OF_WEEK") {
                                    encoding.x.sort = null
                                }
                                if (encoding.y.field === "DAY_OF_WEEK") {
                                    encoding.y.sort = null
                                }
                                charts.push({
                                    name: chart["name"],
                                    encoding: encoding,
                                    values: values,
                                    mark: { type: (typeof data["x_axis"][0] == "number") ? "circle" : "rect", tooltip:true },
                                    id: chart["name"],
                                })
                            } else {
                                // Two dimension chart
                                const data = await Chart.twoColumnsType(chart["x"], chart["y"], chart["type"])
                                const values = this.prepareChartOptions(data)

    
                                let encoding = {
                                    x: { field: data["x_label"], type: (typeof data["x_axis"][0] == "number") ? 'quantitative' : "nominal" },
                                    y: { field: data["y_label"], type: (typeof data["y_axis"][0] == "number") ? 'quantitative' : "nominal" }
                                }
                                if (encoding.x.field === "DAY_OF_WEEK") {
                                    encoding.x.sort = null
                                }
                                if (encoding.y.field === "DAY_OF_WEEK") {
                                    encoding.y.sort = null
                                }
                                if (data["z_axis"]) {
                                    encoding.color = {"field": data["z_label"], "type": "quantitative"}
                                    encoding.text = { field: data["z_label"], type: "quantitative"}
                                    
                                } else {
                                    if (encoding.x.field === "DAY_OF_WEEK") {
                                        encoding.x.sort = null
                                    } else if (encoding.x.type === "nominal") {
                                        encoding.x.sort = "-y"
                                    }
                                }
                                charts.push({
                                    name: chart["name"],
                                    encoding: encoding,
                                    values: values,
                                    mark: { type: (chart["type"] === "scatter") ? "point" : (chart["type"] === "time") ? "line" : (chart["type"] === "heatmap") ? "rect" : "bar", "tooltip": true },
                                    id: chart["name"],
                                })
                            }
                        } else {
                            // Distribution chart
                            const column = this.columns.find((item) => {
                                return chart["x"] === item["value"] 
                            })
                            const data = await DistributionCharts.get(column)
                            if (column.type === "categorical") {
                                data.encoding.x.sort = "-y"
                            }
                            charts.push({
                                ...data,
                                name: chart["name"],
                                id: chart["name"]
                            })
                        }
                    }
    
                    let oldCharts = JSON.parse(localStorage.getItem("widgets"))
                    if (!oldCharts) {
                        oldCharts = []
                    }
                    // avoid repetition of charts
                    for (let chart of charts) {
                        let exist = false
                        for (let old of oldCharts) {
                            if (chart.id === old.id) {
                                exist = true
                            }
                        }
                        if (!exist) {
                            oldCharts.push(chart)
                        }
                    }
                    localStorage.setItem("widgets", JSON.stringify(oldCharts))
                    this.chartSelection = Object.assign([], [])
                    this.created = true
                    this.$emit("select_tab", 1);
                } catch {
                    this.loading = false
                }
                this.loading = false
            },
            prepareChartOptions(data) {
                if (data["x_label"].includes(".")) {
                    data["x_label"] = data["x_label"].split(".")[0]
                }
                if (data["y_label"].includes(".")) {
                    data["y_label"] = data["y_label"].split(".")[0]
                }
                if (data["z_label"] && data["z_label"].includes(".")) {
                    data["z_label"] = data["z_label"].split(".")[0]
                }
                let values = []
                for (let i = 0; i < data["x_axis"].length; i++) {
                    let value = {}
                    value[data["x_label"]] = data["x_axis"][i]
                    value[data["y_label"]] = data["y_axis"][i]
                    if (data["z_label"]) {
                        value[data["z_label"]] = data["z_axis"][i]
                    }
                    values.push(value)
                }
                // Sort if someone contains days of week
                let day_axis = null
                if (data["x_label"] && data["x_label"] === "DAY_OF_WEEK") {
                    day_axis = true
                } else if (data["y_label"] && data["y_label"] === "DAY_OF_WEEK") {
                    day_axis = true
                } else if (data["z_label"] && data["z_label"] === "DAY_OF_WEEK") {
                    day_axis = true
                }
                if (day_axis) {
                    values = this.sortDayOfWeek(values)
                }
                return values
            },
            sortDayOfWeek(values) {
                const dayToNumber = {
                    "Sunday": 0,
                    "Monday": 1,
                    "Tuesday": 2,
                    "Wednesday": 3,
                    "Thursday": 4,
                    "Friday": 5,
                    "Saturday": 6
                }
                values = values.sort((a, b) => {
                    if (dayToNumber[a["DAY_OF_WEEK"]] <= dayToNumber[b["DAY_OF_WEEK"]]) {
                        return -1
                    } else {
                        return 1
                    }
                })

                return values
            }

        }
    }
</script>

<style scoped>

    div.row {
        margin: 0;
        text-align: left;
    }
    h2 {
        text-align: left;
        display: inline;
        font-size: 1.2rem;
        color: #ff1e56;
    }

    .toolbox {
        border:3px solid black;
        border-radius: 5px;
        padding: 1rem 0rem;
        background-color: white;
        width: 100%;
        margin: 0;
        height: auto;
        box-shadow: 1px 1px 12px rgba(0, 0, 0, 0.73);
    }

    .checkbox-group {
        margin-left: 1rem;
        color: #1c1c1c;
        font-size: 1rem;
        padding: 0.3rem;
        font-weight: 500;
    }

    .create-button {
        background-color: #ff1e56;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 1rem;
        color: white;
        outline: none;
        border: 3px solid black;
        box-shadow: 1px 1px 12px rgba(0, 0, 0, 0.4);
        margin-top: 20%;
        transition: all .3s ease-in-out;
        transform: translateY(-50%);
    }

    .create-button-hover:hover {
        background-color: black;
        transform: translateY(-60%);
        color: white;
    }
    .fields-to-display-txt{
        text-align:center;
    }
</style>