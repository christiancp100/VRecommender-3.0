<template>
    <div id="app">
        <!--<div id="nav"><router-link to="/">Home</router-link></div>-->
        <router-view />
    </div>
</template>

<style>
#app {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    font-family: 'Lato', Helvetica, sans-serif;
    font-size: 14px;

}

#vg-tooltip-element {
    z-index: 9999;
}
</style>
