<template>
    <div class="padding-0">
        <b-container class="container">
            <h2 class="my-5">{{data_type}} Data</h2>
            <b-table stacked="stickyHeader" borderless striped hover :items="items"></b-table>
        </b-container>

    </div>

</template>

<script>
    export default {
        name: "Table",
        props: ['items', 'data_type'],
        data() {
            return {}
        }
    }
</script>

<style scoped>
    .container {
        width: 90%;
        justify-content: center;
    }

    .padding-0 {
        padding: 0;
        max-width: 100%;
    }
</style>