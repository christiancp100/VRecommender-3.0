<template>
    <div class="container mt-5">
        <b-row >
            <b-col cols="12" class="mb-5">
                <h3>How many airports do you want to display? (default 100)</h3>
                <b-form-input
                        id="selection"
                        type="number"
                        style="text-align: center"
                        v-model="selection"
                        placeholder="How many airports do you want to display? (default 100)"
                        v-on:input="reloadMap"
                />
            </b-col>
            <b-col v-if="loading === true"  cols="12">
                <Loading/>
            </b-col>
            <b-col cols="12">
                <div id="map"></div>
            </b-col>
        </b-row>
    </div>
</template>

<script>
  import embed from 'vega-embed';
  import Loading from "./Loading";
  //const airportsEndpoint = "http://localhost:8000/map/airports/?value=10000";
  //const flightsEndpoint = "https://vega.github.io/vega/data/flights-airport.csv";
  export default {
    name: "MapView",
    components: {Loading},
    props: ["chartData"],
    data(){
      return{
        selection : 100,
        loading : true,
      }
    },
    computed: {
      vegaLiteSpec: function () {
        const airportsEndpoint = "https://vega.github.io/vega/data/airports.csv";
        const flightsEndpoint = `http://localhost:8000/map/flights/?value=${this.selection}`;
        return{
          "$schema": "https://vega.github.io/schema/vega/v5.json",
          "width": 1000,
          "height": 660,
          "padding": {
            "top": 25,
            "left": 0,
            "right": 0,
            "bottom": 0
          },
          "autosize": "none",
          "data": [
            {
              "name": "states",
              "url": "https://vega.github.io/vega/data/us-10m.json",
              "format": {
                "type": "topojson",
                "feature": "states"
              },
              "transform": [
                {
                  "type": "geopath",
                  "projection": "projection"
                }
              ]
            },
            {
              "name": "traffic",
              "url": flightsEndpoint,
              "format": {"type": "csv", "parse": "auto"},
              "transform": [
                {
                  "type": "aggregate",
                  "groupby": ["origin"],
                  "fields": ["count"], "ops": ["sum"], "as": ["flights"]
                },
              ]
            },
            {
              "name": "incoming",
              "url": flightsEndpoint,
              "format": {"type": "csv", "parse": "auto"},
              "transform": [
                {
                  "type": "aggregate",
                  "groupby": ["destination"],
                  "fields": ["count"], "ops": ["sum"], "as": ["incoming"]
                },
              ]
            },
            {
              "name": "airports",
              "url": airportsEndpoint,
              "format": {
                "type": "csv",
                "parse": "auto"
              },
              "transform": [
                {
                  "type": "lookup",
                  "from": "traffic", "key": "origin",
                  "fields": ["iata"], "as": ["traffic"]
                },
                {
                  "type": "lookup",
                  "from": "incoming", "key": "destination",
                  "fields": ["iata"], "as": ["incoming"]
                },
                {
                  "type": "filter",
                  "expr": "datum.traffic != null"
                },
                {
                  "type": "geopoint",
                  "projection": "projection",
                  "fields": ["longitude", "latitude"]
                },
                {
                  "type": "filter",
                  "expr": "datum.x != null && datum.y != null"
                },
                {
                  "type": "collect", "sort": {
                    "field": "traffic.flights",
                    "order": "descending"
                  }
                },
                {
                  "type": "voronoi", "x": "x", "y": "y"
                },
                {
                  "type": "collect", "sort": {
                    "field": "traffic.flights",
                    "order": "descending"
                  }
                }
              ]
            },
            {
              "name": "routes",
              "url": flightsEndpoint,
              "format": {"type": "csv", "parse": "auto"},
              "transform": [
                {
                  "type": "filter",
                  "expr": "hover && hover.iata == datum.origin"
                },
                {
                  "type": "lookup",
                  "from": "airports", "key": "iata",
                  "fields": ["origin", "destination"], "as": ["source", "target"]
                },
                {
                  "type": "filter",
                  "expr": "datum.source && datum.target"
                },
                {
                  "type": "linkpath",
                  "shape": "line"
                }
              ]
            }
          ],
          "projections": [
            {
              "name": "projection",
              "type": "albersUsa",
              "scale": 1200,
              "translate": [
                {
                  "signal": "width / 2"
                },
                {
                  "signal": "height / 2"
                }
              ]
            }
          ],
          "scales": [
            {
              "name": "size",
              "type": "linear",
              "domain": {"data": "traffic", "field": "flights"},
              "range": [16, 1000]
            },
          ],
          "signals": [
            {
              "name": "hover",
              "value": null,
              "on": [
                {"events": "@cell:mouseover", "update": "datum"},
                {"events": "@cell:mouseout", "update": "null"}
              ]
            },
            {
              "name": "title",
              "value": "U.S. Airports, 2008",
              "update": "hover && hover.incoming ? hover.name + ' (' + hover.iata + ') - ' + hover.state + ' | Outgoing flights: ' + hover.traffic.flights + ' | Incoming flights: ' + hover.incoming.incoming: 'U.S. Airports, 2015'"
            }
          ],
          "marks": [
            {
              "type": "path",
              "from": {
                "data": "states"
              },
              "encode": {
                "enter": {
                  "fill": {
                    "value": "#1c1c1c"
                  },
                  "stroke": {
                    "value": "white"
                  }
                },
                "update": {
                  "path": {
                    "field": "path"
                  }
                }
              }
            },
            {
              "type": "symbol",
              "from": {"data": "airports"},
              "encode": {
                "enter": {
                  "size": {"scale": "size", "field": "traffic.flights"},
                  "fill": {"value": "#ff1e56"},
                  "fillOpacity": {"value": 0.8},
                  "stroke": {"value": "white"},
                  "strokeWidth": {"value": 1.5}
                },
                "update": {
                  "x": {"field": "x"},
                  "y": {"field": "y"}
                }
              }
            },
            {
              "type": "path",
              "name": "cell",
              "from": {"data": "airports"},
              "encode": {
                "enter": {
                  "fill": {"value": "transparent"}
                },
                "update": {
                  "path": {"field": "path"}
                }
              }
            },
            {
              "type": "text",
              "interactive": true,
              "encode": {
                "enter": {
                  "x": {"signal": "width", "offset": -5},
                  "y": {"value": 0},
                  "fill": {"value": "#ff1e56"},
                  "fontSize": {"value": 20},
                  "align": {"value": "right"}
                },
                "update": {
                  "text": {"signal": "title"}
                }
              }
            },
            {
              "type": "path",
              "interactive": false,
              "from": {"data": "routes"},
              "encode": {
                "enter": {
                  "path": {"field": "path"},
                  "stroke": {"value": "#ff1e56"},
                  "strokeOpacity": {"value": 0.45}
                }
              }
            }
          ],
        }
      }
    },
    watch: {
      vegaLiteSpec: async function (new_val) {
        this.loading = true;
        if (!new_val)
          return
        const res = await embed(`#map`, new_val)
        if(res) {
          this.loading = false;
        }
      }
    },
    async mounted() {
      this.loading = true;
      if (this.vegaLiteSpec) {
        const res = await embed(`#map`, this.vegaLiteSpec)
        if(res){
          this.loading = false;
        }
      }
    },
    methods : {
      reloadMap : async function(){
        this.loading = true;
        if(!this.selection) this.selection = 100
        const res = await embed(`#map`, this.vegaLiteSpec);
        if(res){
          this.loading = false;
        }

      }
    }
  }
</script>

<style scoped>
    .container {
        display: flex;
        flex-direction: row;
        align-content: center;
        justify-content: center;
    }
</style>