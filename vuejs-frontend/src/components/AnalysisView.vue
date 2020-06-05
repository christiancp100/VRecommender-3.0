<template>
    <div>
        <button v-on:click="resetWidgets" class="my-auto create-button">REMOVE ALL WIDGETS</button>
        <b-row cols-lg="3" class="mt-3 mx-auto">
            <b-col v-for="(widget, i) in customWidgets" :key="widget.id" class="mb-4">
                <div class="custom-card">
                    <div style="height:3rem">
                        <h6 style="height:100%; width:100%; text-align:center">{{ widget.name }}</h6>
                    </div>
                    
                    <div :id="`vega-chart-${i}`"></div>
                    <b-row class="justify-content-center bottom-button">
                        <b-col cols="8">
                            <h5 style="background-color: black; color:white; border-radius: 0.5rem; padding: 0.5rem" @click="showFullscreenChart(i)">
                                Zoom <b-icon-arrows-fullscreen style="margin-left: 0.5rem"></b-icon-arrows-fullscreen>
                            </h5>
                        </b-col>
                    </b-row>
                </div>
            </b-col>
        </b-row>

        <!-- Modal here -->
        <b-modal size="xl" centered ok-only ok-title="Close fullscreen" id="fullscreen-chart-modal">

            <h2 slot="modal-title">{{ chart.name }}</h2>

            <b-row class="justify-content-md-center">
                <div id="vega-chart-modal"></div>
            </b-row>

        </b-modal>
    </div>
</template>

<script>
import embed from 'vega-embed'

export default {
    name: "AnalysisView",
    data() {
        return {
            widgets: [],
            baseSpec: {
                $schema: "https://vega.github.io/schema/vega-lite/v4.json",
                // values : values,
                width: 300,
                height: 300,
                autosize: "pad",
                padding: 10
            },
            chart: {}
        }
    },
    computed: {
        customWidgets: function () {
            let customWidgets = []
            for (let widget of this.widgets) {
                customWidgets.push({
                    ...this.baseSpec,
                    ...widget,
                    "data": {
                        "values": widget.values
                    },
                    "encoding": {
                        ...widget.encoding,
                        "x": {
                            ...widget.encoding.x,
                            "axis": {
                                ...widget.encoding.x.axis,
                                "labelOverlap": true,
                                "labelAlign": "right",
                                "labelAngle": -30
                            },
                        },
                        "y": {
                            ...widget.encoding.y,
                            "axis": {
                                ...widget.encoding.y.axis,
                                "labelOverlap": "parity",
                            }
                        }
                    }
                })
            }
            return customWidgets
        }
    },
    watch: {
        customWidgets: async function (new_val) {
            for (let [i, widget] of Object.entries(new_val)) {
                await embed(`#vega-chart-${i}`, widget)
            }
        }
    },
    async mounted() {
        this.widgets = JSON.parse(localStorage.getItem("widgets"))
        if (!this.widgets) {
            this.widgets = []
        }
    },
    methods: {
        resetWidgets: function () {
            this.widgets = []
            localStorage.setItem("widgets", JSON.stringify([]))
        },
        showFullscreenChart: async function (i) {
            this.chart = this.customWidgets[i]
            this.$bvModal.show("fullscreen-chart-modal")
            this.chart.width = 800
            this.chart.height = 600
            this.chart.encoding.x.axis.labelOverlap = false
            this.chart.encoding.y.axis.labelOverlap = false
            // TODO: put another call to the endpoint to have a very detailed chart, others should be low-res
            await embed("#vega-chart-modal", this.chart)
        }
    }
}
</script>

<style scoped>
.create-button {
    background-color: #ff1e56;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    font-size: 1rem;
    color: white;
    outline: none;
    border: none;
}

.create-button:hover {
    background-color: #cd1746;
}

.custom-card {
    display: flex;
    position: relative;
    flex-direction: column;
    padding: 1rem;
    height: 36rem;
    min-width: 30rem;
    border-radius: 0.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.bottom-button {
    bottom: 0;
    width: 30rem;
    margin-bottom: 1rem;
    margin-left: auto;
    margin-right: auto;
    margin-top: auto;
}
</style>