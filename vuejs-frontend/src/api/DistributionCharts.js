import { Api } from "./Api";

class DistributionChartsClass {
    constructor() {
        this.baseUrl = `${Api.baseUrl}distribution`;
    }

    async get(
        { value, type },
        args = { range: 10, interval: "month", order: "DESC" }
    ) {
        let additionalParams = "";
        let { range, interval, order } = args;
        if (range === null) range = 10;
        if (interval === null) interval = "month";
        if (order === null) order = "DESC";

        if (type !== "timestamp") {
            additionalParams = `&range=${range}`;
        } else {
            additionalParams = `&interval=${interval}`;
        }
        additionalParams += `&order=${order}`;
        let url = `${this.baseUrl}/?column=${value}${additionalParams}`;
        const data = await Api.get(url);

        let values = [];
        Object.values(data).forEach((e) => {
            let obj = { count: e.Doc_count };
            obj[value] = e.Key.trim(15);
            values.push(obj);
        });
        // Separate in bins if numerical
        let encoding = {};
        if (type === "numerical") {
            values = values.map((x) => {
                let i = 0,
                    prepend = "";
                if (x[value].startsWith("-")) {
                    i = 1;
                    prepend = "-";
                }
                x[`${value}_s`] = parseInt(
                    prepend +
                        x[value]
                            .split("-")
                            [i].substring(0, x[value].split("-")[i].length - 2)
                );
                x[`${value}_e`] = parseInt(
                    x[value]
                        .split("-")
                        [i + 1].substring(
                            0,
                            x[value].split("-")[i + 1].length - 2
                        )
                );
                return x;
            });
            encoding = {
                x: {
                    field: `${value}_s`,
                    type: "quantitative",
                    bin: {
                        binned: true,
                        step: values[0][`${value}_e`] - values[0][`${value}_s`],
                    },
                    axis: {
                        title: value,
                    },
                },
                x2: {
                    field: `${value}_e`,
                },
                y: { field: "count", type: "quantitative" },
            };
        } else {
            encoding = {
                x: { field: value, type: "ordinal" },
                y: { field: "count", type: "quantitative" },
            };
        }
        return {
            values: values,
            encoding: encoding,
            mark: { type: "bar", tooltip: true },
            id: value,
        };
    }
}

export const DistributionCharts = new DistributionChartsClass();
