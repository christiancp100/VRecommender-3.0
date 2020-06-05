import { Api } from "./Api";

class ChartClass {
   constructor() {
      this.baseUrl = Api.baseUrl + "create-chart"
   }

   async suggestedCharts(columns){
      if (columns.length > 3) {
         throw new Error("You must select maximum 3 columns")
      }

      let parameters = ""
      for (let [i, column] of columns.entries()) {
         let parameter = (i > 0) ? "&" : ""
         parameter += `c${i+1}=${column}`
         parameters += parameter
      }

      return Api.get(`${Api.baseUrl}type-of-chart/?${parameters}`)
   }

   async twoColumnsType(x, y, type) {
      return Api.get(`${this.baseUrl}/?x=${x}&y=${y}&type=${type}`)
   }

   async threeColumnsChart(x, y, z, type) {
      return Api.get(`${this.baseUrl}/?x=${x}&y=${y}&z=${z}&type=${type}`)
   }
}

export const Chart = new ChartClass()