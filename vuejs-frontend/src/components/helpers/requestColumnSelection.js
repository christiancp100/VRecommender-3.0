import {Describe} from "../../api/Describe";

const convertToReadableDate = (dateT) => {
    var date = new Date(dateT);
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = date.getFullYear();

    return mm + '/' + dd + '/' + yyyy;
}

const columnsRequest = async () => {
    return await Describe.getColumns();
}

const _formatData = (data) => {
    Object.entries(data).forEach(([item, value]) => {
        if (typeof value === "number") data[item] = Math.trunc(value);
    })
    delete data["std_deviation_bounds"]
    delete data["sum_of_squares"]
    delete data["sum_of_squares"]
    delete data["std_deviation"];
    delete data["variance"];
    delete data["count"];
    delete data["Count"];

    //Reshaping names
    if(data["standard deviation"]) data["standard deviation"] = data["std_deviation"];

    //formatting date
    if(data["Top"]){
        data["Top"]= convertToReadableDate(data["Top"]);
        data["First"]= convertToReadableDate(data["First"]);
        data["Last"]= convertToReadableDate(data["Last"]);
    }

    return data;
}


export default async function (selection) {
    this.selection = selection;
    const selection_info = [];
    const columns = await columnsRequest();
    // If the item is no more selected we remove it but without re-rendering the rest of components
    for (const c of columns) {
        if (this.rendered.includes(c.value) && !selection.includes(c.value)) {
            this.rendered = this.rendered.filter(r => r !== c.value);
            this.serverData = this.serverData.filter(n => n.name !== c.text);
        }
    }
    for (const c of columns) {
        for (const s of selection) {
            // if the column is not rendered and the value is selected, render the item
            if (c.value === s && !this.rendered.includes(c.value)) {
                selection_info.push(c);
                this.rendered.push(c.value);
            }
        }
    }

    try {
        for (const s of selection_info) {
            // No more longer distinction between column types (it's done in the backend)
            const data = await Describe.request(s);
            const cleaned_data = {
                name: s.text,
                value: s.value,
                type: s.type,
                description: _formatData(data)
            }
            this.serverData.push(cleaned_data);
        }
    } catch (e) {
        console.log(e);
        return false;
    }
    return true;
}


export const checkColumn = (column) => {
    switch (column.value) {
        case "DESTINATION_AIRPORT_COORDINATES":
        case "ORIGIN_AIRPORT_COORDINATES":
        case "CANCELLATION_REASON":
        case "CANCELLED":
        case "DIVERTED":
        case "FLIGHT_NUMBER":
            return false;
        default:
            return true;

    }
}
