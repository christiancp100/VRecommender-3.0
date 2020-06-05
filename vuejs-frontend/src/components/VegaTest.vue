<template>
    <div class='dashboard'>
        <vega-lite :data="values" mark="bar" autoResize="true" :encoding="encoding"/>
    </div>
</template>

<script>

    export default {
        name: "VegaTest",

        data() {
            return {
                values: [
                    {count: 'AAAAAAAA', b: 28}, {count: 'B', b: 55}, {count: 'C', b: 43},
                    {count: 'AAAAAAAA', b: 28}, {count: 'B', b: 55}, {count: 'C', b: 43},
                    {count: 'DDDDDDD', b: 91}, {count: 'E', b: 81}, {count: 'F', b: 53},
                    {count: 'G', b: 19}, {count: 'H', b: 87}, {count: 'I', b: 52}
                ],
                encoding: {
                    x: {field: 'count', type: 'ordinal'},
                    y: {field: 'b', type: 'quantitative'}
                }
            }
        }

    }
</script>

<style scoped>

</style>