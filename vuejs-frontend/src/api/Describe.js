import { Api } from "./Api";

class DescribeClass {
   constructor() {
      this.baseUrl = Api.baseUrl + "describe";
   }

   async numeric(column) {
      return Api.get(`${this.baseUrl}/numeric/?column=${column}`);
   }
   
   async categoric(column) {
      return Api.get(`${this.baseUrl}/category/?column=${column}`);
   }

   async timestamp(column) {
      return Api.get(`${this.baseUrl}/timestamp/?column=${column}&interval=month`);
   }

   async getColumns(){
      let res = []
      let data = await Api.get(Api.baseUrl + "columns/");
      Object.values(data).forEach(c => res.push(c))
      return res;
   }

   async request({value, type}, interval = "month"){
      let additionalParams = '';
      if(type === "timestamp"){
         additionalParams = `&interval=${interval}`;
      }
      return Api.get(`${this.baseUrl}/?column=${value}${additionalParams}`);
   }
}

export const Describe = new DescribeClass()