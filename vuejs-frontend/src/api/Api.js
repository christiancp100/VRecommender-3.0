import Vue from "vue"

class ApiClass {
   constructor() {
      this.baseUrl = "http://localhost:8000/"
   }

   async get(endpoint) {
      return Vue.axios.get(endpoint).then((response) => {
         return Promise.resolve(response.data)
      })
   }
}

export const Api = new ApiClass()

