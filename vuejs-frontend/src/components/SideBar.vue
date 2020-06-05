<template>
    <div id="side-bar">
        <b-row class="mx-auto">
            <b-col>
                <span class="title mt-5"><span class="v3">V3</span>Recommender</span>
            </b-col>
        </b-row>
        <!--<b-row class="px-3 mx-auto">
            <b-form-input
                    size="sm"
                    class="mt-5"
                    v-model="airport_name"
                    v-on:input="searchByAirport"
                    placeholder="Filter by airport"/>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-5 mb-0"><span class="pick-year">Pick date range</span></b-col>
            <b-row class="mx-auto">
                <b-col cols="12" class="mt-2">
                    <b-form-datepicker
                            reset-button
                            placeholder="From"
                            size="sm"
                            v-model="date_from"
                            v-on:input="changeDateRange"
                            class="mb-2 date-picker mx-auto"/>
                </b-col>
                <b-col cols="12" class="mt-1">
                    <b-form-datepicker
                            reset-button
                            placeholder="To"
                            size="sm"
                            v-model="date_to"
                            v-on:input="changeDateRange"
                            class="mb-2 date-picker mx-auto"/>
                </b-col>
            </b-row>
        </b-row>-->
        <b-row>
            <b-col class="mb-0 col-m-0-2" cols="12">
                <h3 class="col-m-0">Columns</h3>
                <b-col class="mb-2 mx-auto"  cols="12">
                    <b-form-input
                            size="sm"
                            class="card-input mx-auto"
                            v-model="column_text"
                            v-on:input="searchColumn"
                            style="color: white"
                            placeholder="Search..."/>
                </b-col>
            </b-col>
            <b-card
                    class="mb-4 mx-auto card-col"
            >
                <b-col>
                    <b-form-group id="column-list" class="form-text">
                        <b-form-checkbox-group
                                class=""
                                stacked
                                id="checkbox-group-1"
                                :options="selectedFiltered"
                                v-model="selected"
                                v-on:input="changeColumn"
                                name="selected-columns"
                        ></b-form-checkbox-group>
                    </b-form-group>
                </b-col>
            </b-card>
        </b-row>
    </div>
</template>

<script>
    export default {
        name: "SideBar",
        props: ['columns'],
        data() {

            return {
                selected: [],
                selectedFiltered : this.columns,
                column_text : '',
                airport_name: '',
                date_from: '',
                date_to: '',
            }
        },
        methods: {
            changeColumn: function () {
                this.$emit("selectedColumns", this.selected);
            },
            changeDateRange: function () {
                this.$emit("newDateRange", {from: this.date_from, to: this.date_to});
            },
            searchByAirport : function () {
                this.$emit("newAirportName", this.airport_name);
            },
            searchColumn : function (value){
                this.selectedFiltered = this.columns.filter(c => c.text.toLowerCase().includes(value.toLowerCase()));
            }

        },
    }
</script>

<style scoped>
    .col-m-0{
        margin-top: 0;
        padding-top: 0;
        color: #ff1e56;
        font-size: 1.5rem;
    }

    .col-m-0-2{
        margin-top: 2rem;
        padding-bottom: 0;
        margin-bottom: 0;
    }

    .card-col{
        width: 90%;
        height: 78vh;
        margin-bottom: 0;
        overflow-y: scroll;
        background-color: #1c1c1c;
        color: white;
        font-size: 1rem;
    }
    #side-bar {
        position: relative;
        margin-top: 0;
        height: 100%;
        background-color: #1c1c1c;
        box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.48);
        padding-right: 0;
        margin-right: 0;
        z-index: 100;
    }

    .pick-year {
        font-size: 1rem;
        color: #ff1e56;
    }

    .title {
        display: block;
        color: #ff1e56;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 1.5rem;
    }

    input[type=text] {
        border-radius: 2px;
        border: 0;
        box-shadow: inset 0 -1px 0 #ddd;

    }

    .date-picker {
        font-size: 0.8rem;
        max-width: 12rem;
    }


    #column-list {
        text-align: left;
    }

    .card-input, .card-input:focus{
        border: 0;
        background: transparent;
        border-radius: 0;
        border-bottom: 1px solid white;
        outline: 0;
        width: 80%;
    }


    .v3{
        font-family: 'Lato', Helvetica, sans-serif;
        border-radius: 50px;
        padding: 0.6rem;
        background-color: #ff1e56;
        color: white;
        margin-right: 0.25rem;
        font-size: 1.7rem;
        font-weight: bolder;
    }

</style>