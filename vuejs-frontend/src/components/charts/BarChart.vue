<template>
    <div class="container">
        <div :id="chartData.id"></div>
    </div>
</template>

<script>
import embed from 'vega-embed'

export default {
    name: "BarChart",
    props: ["chartData"],
    computed: {
        vegaLiteSpec: function() {
            if (!this.chartData.encoding.x) {
                return null
            }
            return {
                ...this.chartData,
                "data": {
                    "values": this.chartData.values
                },
                "encoding": {
                    ...this.chartData.encoding,
                    "x": {
                        ...this.chartData.encoding.x,
                        "sort": null,
                        "axis": {
                            ...this.chartData.encoding.x.axis,
                            "labelOverlap": false,
                            "labelAlign": "right",
                            "labelAngle": -45
                        }
                    }
                }
            }
        }
    },
    watch: {
        vegaLiteSpec: async function(new_val) {
            if (!new_val)
                return

            await embed(`#${this.chartData.id}`, new_val)
        }
    },
    async mounted() {
        if (this.vegaLiteSpec) {
            await embed(`#${this.chartData.id}`, this.vegaLiteSpec)
        }
    }
}
</script>

<style scoped>
    .container{
        width: 309px;
    }
</style>