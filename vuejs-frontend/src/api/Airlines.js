import Api from "./Api"

class AirlinesClass {
   constructor() {
      this.baseUrl = Api.baseUrl + "airlines"
   }

   count() {
      return Api.get(`${this.baseUrl}/count`)
   }
}

export const Airlines = new AirlinesClass()