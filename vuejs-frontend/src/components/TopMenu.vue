<template>
    <b-tabs content-class="mt-3" fill align="center" bg-variant="dark" class="tabs">
        <b-tab active v-on:click="selectTab(0)">
            <template v-slot:title>
                <b-icon-table style="font-size: 1rem"/>
                <span>Describe</span>
            </template>
        </b-tab>
        <b-tab v-on:click="selectTab(1)">
            <template v-slot:title>
                <b-icon-bar-chart style="font-size: 1rem"/>
                <span>Analyse</span>
            </template>
        </b-tab>
        <b-tab v-on:click="selectTab(2)">
            <template v-slot:title>
                <b-icon-map style="font-size: 1rem"/>
                <span>Map</span>
            </template>
        </b-tab>
    </b-tabs>
</template>

<script>
  export default {
    name: "TopMenu",
    methods: {
      selectTab: function (selectedTab) {
        this.$emit("select_tab", selectedTab)
      }
    }
  }
</script>

<style scoped>
    div {
        position: relative;
        z-index: 3;
        padding: 0;
        margin: 0;
        width: 100%;
    }

    span {
        font-size: 1rem;
        margin-left: 2rem;
    }

    .tabs {
        box-shadow: 1px 3px 12px black;
        border: 0;
    }


</style>