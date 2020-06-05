from djangoapi.models import *
from django.http import HttpResponse
import json
import itertools
from .helpers import _formatDate, _reformatKey


def describe(request):
    parameters = request.GET
    if "column" not in parameters:
        return response_missing_parameter("column")
    column = parameters["column"]
    col_type =  columnType(column)
    
    if col_type == "numerical":
        return numerical(request)
    elif col_type == "categorical":
        return categorical(request)
    elif col_type == "timestamp":
        return timestamp(request)
    else:
        return response_incorrect_parameter("column")


#Hassan
def numerical(request): 
    res = request.GET['column'].upper()
    objects = ObjectDocument.search()
    objects.aggs.bucket('Numeric', 'extended_stats', field=res)
# MDA
# don't you check that the results are what you expected before returning them? (?)
    result = objects.execute()
    return HttpResponse(json.dumps(result.aggregations.Numeric.to_dict()),content_type="application/json")


def categorical(request):
# MDA
# I guess that you have ".keyword" here because you're indexing the field as both text and keyword
# why do you need to index as text? (The data is indexed in elasticsearch before django starts, so we don't influence it's mapping)
    res = request.GET['column'].upper() +'.keyword'
    objects = ObjectDocument.search()
    total = ObjectDocument.search().count()
    objects.aggs.bucket('categorical', 'terms',size=500, field=res)
    result = objects.execute()
    max = 0
    sum = 0
    for bucket in result.aggregations.categorical.buckets:
        sum += bucket.doc_count
        if max < bucket.doc_count:
            max = bucket.doc_count 
# MDA
# are the last 3 buckets the largest ones (because you're saying the are most frequent values)? if you're not sorting no (fixed)
# also, you're not setting the shard_size and not checking the error upper bound that the elastic aggregation endpoints returns
# so, the results you are returning can be wrong (Fixed: There is no shard problem, and the size is now set to 500)
    buckets = result.aggregations.categorical.buckets
    buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = True)
    topFreq =[]
    if len(buckets) >= 3:
         topFreq = buckets[:3]
    else:
        topFreq = buckets[:len(buckets)]
        
    topFreqstr = {}
    for index,item in enumerate(topFreq):
        currentstr = {index: item.key }
        topFreqstr.update(currentstr)
    response ={"Count":total,"Sum":sum,"Max":max,"Most Freq":topFreqstr
    }
    return HttpResponse(json.dumps(response),content_type="application/json")


def timestamp(request): 
    res = request.GET['column'].upper()
    res_in = request.GET['interval'].lower()
    objects = ObjectDocument.search().sort(res)
    objects.aggs.bucket('by_date', 'date_histogram', field=res, interval=res_in)
    count = ObjectDocument.search().count()
    result = objects.execute()
    first = result.aggregations.by_date.buckets[0].key_as_string
    last = result.aggregations.by_date.buckets[-1].key_as_string
    unique = 0
    dcNb = 0
    indexfortop = 0

    for index,bucket in enumerate(result.aggregations.by_date.buckets):
        if dcNb <= bucket.doc_count:
            indexfortop = index
            dcNb = bucket.doc_count
    top = result.aggregations.by_date.buckets[indexfortop].key_as_string
    unique = len(result.aggregations.by_date.buckets)
    x ={"Count":count,"Unique":unique,"Top":top,"Freq":dcNb,"First":first,"Last":last}
    return HttpResponse(json.dumps(x),content_type="application/json")


def distribution(request):
    parameters = request.GET
    if "column" not in parameters:
        return response_missing_parameter("column")
    column = parameters["column"]
    col_type = columnType(column)
    
    if col_type == "numerical":
        return ranges(request)
    elif col_type == "categorical":
        return cantrange(request)
    elif col_type == "timestamp":
        return daterange(request)
    else:
        return response_incorrect_parameter("column")
    pass


def ranges(request): 
    parameters = request.GET
    res = parameters["column"].upper()
    if "range" not in parameters:
        ranges = 6
    else:
        ranges = int(parameters["range"])

    if "order" not in parameters:
        order  = "asc"
    else:
         order = parameters["order"].lower()

    if order == "asc":
        rev = False
    else:
        rev = True
    objects = ObjectDocument.search()
    objects.aggs.bucket('Numeric', 'extended_stats', field=res)
    result = objects.execute()
    max = int(result.aggregations.Numeric.max)
    min = int(result.aggregations.Numeric.min)
    scaler = (max - min)//ranges
    obj = []
    for x in range(min,max,scaler):
        current_obj = {"from": x , "to": x+scaler}
        obj.append(current_obj)
    objects = ObjectDocument.search()
    objects.aggs.bucket('by_ranges', 'range', field=res, ranges=obj)
    result = objects.execute()
    buckets = result.aggregations.by_ranges.buckets
    buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = rev)
    finalstr = {}
    for index,bucket in enumerate(buckets):
        currentstr = {index: {"Key": bucket.key, "Doc_count": bucket.doc_count}}
        finalstr.update(currentstr)
    return HttpResponse(json.dumps(finalstr),content_type="application/json")
    
    
#Hassan
def cantrange(request): 
    parameters = request.GET
    res = parameters["column"].upper() +'.keyword'

    if "range" not in parameters:
        n = 10
    else:
        n = int(parameters["range"])

    if "order" not in parameters:
        order  = "asc"
    else:
         order = parameters["order"].lower()

    if order == "asc":
        rev = False
    else:
        rev = True
    objects = ObjectDocument.search()
    objects.aggs.bucket('categorical', 'terms', field=res)
    result = objects.execute()
# MDA
# are the last 10 the largest? same comment as before about sorting and also shard_size & error upper bound  (fixed, not shard issue)
    buckets = result.aggregations.categorical.buckets
    if (len(buckets) >= n):
        buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = rev)[:n]
    else:
        buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = rev)[:len(buckets)]
    finalstr = {}
    for index,bucket in enumerate(buckets):
        currentstr = {index: {"Key": bucket.key, "Doc_count": bucket.doc_count}}
        finalstr.update(currentstr)

    return HttpResponse(json.dumps(finalstr),content_type="application/json")


#Hassan
def daterange(request): 
    parameters = request.GET
    res = parameters["column"].upper()

    if "interval" not in parameters:
        res_in = "day"
    else:
        res_in = parameters["interval"].lower()

    if "order" not in parameters:
        order  = "asc"
    else:
         order = parameters["order"].lower()

    if order == "asc":
        rev = False
    else:
        rev = True
    objects = ObjectDocument.search().sort(res)
    objects.aggs.bucket('by_date', 'date_histogram', field=res, interval=res_in)
    result = objects.execute()
    buckets = result.aggregations.by_date.buckets
    if (len(buckets) >= 10):
        buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = rev)[:10]
        # buckets = sorted(buckets, key = lambda i: i['key'], reverse = False)
    else:
        buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = rev)
        # buckets = sorted(buckets, key = lambda i: i['key'], reverse = False)

    finalstr = {}
    for index,bucket in enumerate(buckets):
        currentstr = {index: {"Key": _formatDate(bucket.key_as_string), "Doc_count": bucket.doc_count}}
        finalstr.update(currentstr)
    
    return HttpResponse(json.dumps(finalstr),content_type="application/json")


def allColumnType(request):
    fields = ObjectDocument._index.get_mapping()['objects']["mappings"]["properties"]
    keyword = ["Delay","Time"]
    finalstr = {}
    for index,field in enumerate(fields):
        text = field.replace("_"," ").title()
        for word in keyword:
            if word in text:
                text += " (Min)"
        fieldType = columnType(field)
        currentstr = {index: {"text": text, "type": fieldType, "value":field }}
        finalstr.update(currentstr)
    finalstr = sorted(finalstr.values(), key = lambda i: i['type'], reverse = False)
    return HttpResponse(json.dumps(finalstr),content_type="application/json")


# SUSANNA
def response_missing_parameter(parameter):
    res = HttpResponse(json.dumps({'error': "parameter " + parameter +  " not found"}),content_type="application/json")
    res.status_code = 404
    return res


def response_incorrect_parameter(parameter):
    res = HttpResponse(json.dumps({'error': "wrong parameter for " + parameter}),content_type="application/json")
    res.status_code = 404
    return res


def chartType(request): 
    parameters = request.GET
    if "c1" in parameters:
        c1 = parameters["c1"]
    else: 
        return response_missing_parameter("c1")

    if "c2" in parameters:
        c2 = parameters["c2"]
        if "c3" in parameters:
            return threeColumnsChart(c1, c2, parameters["c3"])
        else:
            return twoColumnsChart(c1, parameters["c2"])
    else: 
        return oneColumnChart(c1)


def createChart(request):
    parameters = request.GET

    if "type" in parameters:
        chart_type = parameters["type"]
    else: 
        return response_missing_parameter("type")

    if "x" in parameters:
        x = parameters["x"]
    else: 
        return response_missing_parameter("x")

    if "y" in parameters:
        y = parameters["y"]
        if "z" in parameters:
            return createChartXYZ(x, y, parameters["z"], chart_type)
        else:
            return createChartXY(x, parameters["y"], chart_type)
    else: 
        return createChartX(x, chart_type)


def createChartX(x, chart_type):
    if "." not in x:
        return response_missing_parameter("type of x")
    x_type, x = x.split(".")
    return createJsonChartX(x, x_type)


def createChartXY(x, y, chart_type): 
    if chart_type == 'scatter':
        return createScatterPlot(x, y, chart_type)
    elif chart_type == 'heatmap':
        return createHeatmapPlot(x, y, chart_type)
    
    if "." not in y:
        return response_missing_parameter("type of y")
    y_type, y = y.split(".")  
    
    if chart_type == 'bar':
        return createBarChart(x, y, y_type, chart_type)
    elif chart_type == 'line':
        return createLineChart(x, y, y_type, chart_type)
    else:
        return response_incorrect_parameter("chart type")


def createChartXYZ(x, y, z, chart_type):
    if chart_type == 'scatter':
        return create3dScatterPlot(x, y, z, chart_type)
    if "." not in z:
        return response_missing_parameter("type of z")
    z_type, z = z.split(".")
    if chart_type == 'heatmap':
        return create3dHeatmapPlot(x, y, z, z_type, chart_type)
    else:
        return response_incorrect_parameter("chart type")


def createJsonChartX(x, chart_type):
    return {"name": "distribution of "+ x, "chart_type" : chart_type, "x" : x}


def create_json_chart_XY(x, x_type, y, y_type, chart_type):
    chart_info = {
        "name": "correlation of "+ x +" and "+y ,
        "chart_type" : chart_type,
        "x" : x,
        "y": y,
        "aggregation": ["sum", "avg"] if chart_type != "scatter" else None
    }
    if chart_type != "scatter":
        chart_info["aggregation"] =  ["sum", "avg"]
    if chart_type == "line":
        chart_info["aggregation"].append("time")
    response = {"options" : [singleColumnChart(x, x_type), singleColumnChart(y, y_type), chart_info]}
    return HttpResponse(json.dumps(response), content_type="application/json")


def create_json_chart_XYZ(x, x_type, y, y_type, z, z_type, chart_type):
    chart_info = {
        "name": chart_type + " of " + x + " and " + y + " and " + z,
        "chart_type" : chart_type,
        "x" : x,
        "y": y,
        "z": z
    }
    if chart_type == "heatmap":
        chart_info["aggregation"] = ["count"] if z == "ROWS"  else ["sum", "avg"]
    if z != "ROWS":
        options = [singleColumnChart(x, x_type), singleColumnChart(y, y_type), singleColumnChart(z, z_type), chart_info]
    else:
        options = [singleColumnChart(x, x_type), singleColumnChart(y, y_type), chart_info]
    response = {"options" : options}
    return HttpResponse(json.dumps(response), content_type="application/json")


def singleColumnChart(x, x_type):
    if (x_type == "numerical"):
        return createJsonChartX(x, "histogram")
    elif (x_type == "categorical"):
        return createJsonChartX(x, "bar")
    elif (x_type == "timestamp"):
        return createJsonChartX(x, "line")
    else:
        return response_incorrect_parameter("x_type")


def oneColumnChart(x):
    return HttpResponse(json.dumps(singleColumnChart(x, columnType(x))), content_type="application/json")


def twoColumnsChart(x, y):
    types = [columnType(x), columnType(y)]
    if list(set(types)) == ["numerical"]:
        return create_json_chart_XY(x, types[0], y, types[1], "scatter")
    elif list(set(types)) == ["categorical"]:
        return create_json_chart_XYZ(x, types[0], y, types[1], "ROWS", "numerical",  "heatmap")
    elif "numerical" in types and "categorical" in types:
        categorical = [x, y]
        numerical = categorical.pop(types.index("numerical"))
        return create_json_chart_XY(categorical[0], "categorical", numerical, "numerical", "bar")
    elif "timestamp" in types and "numerical" in types :
        numerical = [x, y]
        timestamp = numerical.pop(types.index("timestamp"))
        return create_json_chart_XY(timestamp, "timestamp", numerical[0], "numerical", "line")

    return response_incorrect_parameter("chart type")


def threeColumnsChart(x, y, z):
    types = [columnType(x), columnType(y), columnType(z)]
    if (list(set(types)) == ["numerical"]):
        return create_json_chart_XYZ(x, types[0], y, types[0], z, types[0], "scatter")
    elif ("numerical" in types and types.count("categorical") == 2):
        values = [x, y, z]
        numerical = values.pop(types.index("numerical"))
        return create_json_chart_XYZ(values[0], "categorical", values[1], "categorical", numerical, "numerical", "heatmap")
    return response_incorrect_parameter("chart type")


def columnType(column):
    field_type = ObjectDocument._index.get_mapping()['objects']["mappings"]["properties"][column]["type"]  

    if field_type in ["text", "keyword"]:
        return "categorical"
    elif field_type in ["short", "int", "long", "double", "float"]:
        return "numerical"
    elif field_type == "date":
        return "timestamp"
    elif field_type == "geo_point":
        return "map"
    else:
        return response_incorrect_parameter("column type")


def createBarChart(x, y, y_type, chart_type): 
    x_keyword = x+".keyword"
    objects = ObjectDocument.search()
    objects.aggs.bucket('x_category', 'terms', size=500, field=x_keyword).metric('y_numeric', y_type, field=y)
    result = objects.execute()
    x_axis = []
    y_axis = []
    # MDA
    # i -> bucket (fixed)   
    for bucket in result.aggregations.x_category.buckets:
        x_axis.append(bucket.key)
        y_axis.append(bucket.y_numeric.value)
    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "x_axis" : x_axis, "y_axis" : y_axis}
    return HttpResponse(json.dumps(response),content_type="application/json")


def createLineChart(x, y, y_type, chart_type):
     #should return the time series in the x axis and y axis is numerical. plot a line chart
     #aggregate using the time then plot average or sum of numerical 
     #or just time show the values?
    objects = ObjectDocument.search().sort(x)
    objects.aggs.bucket('by_date', 'date_histogram', field=x, interval='day').metric('metric', y_type, field=y)
    result = objects.execute()
    buckets = result.aggregations.by_date.buckets
    buckets = sorted(buckets, key = lambda i: i['doc_count'], reverse = True)
    if (len(buckets) >= 10):
        topBuckets = buckets[:10]
    else:
        topBuckets = buckets

    x_axis =[]
    y_axis= []
    for bucket in topBuckets:
        x_axis.append(_formatDate(bucket.key_as_string))
        y_axis.append(bucket.metric.value)
    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "x_axis" : x_axis, "y_axis" : y_axis}
    return HttpResponse(json.dumps(response),content_type="application/json")


def createScatterPlot(x, y, chart_type): 
    # performs a full search on elasticsearch and only returns field x and y
    objects = ObjectDocument.search().source([x, y])
    # MDA
    # are you arbitrarily limiting this to the first 10k results? (Fixed: no longer capping the result)
    # I agree that you should not send an uncapped amount of objects to the client, but this is not the way to do it
    # you could for example get the available area for the plot as part of the request, and then as you iterate over the
    # result and calculate the coordinates, you filter out all the points that overlap more than 90% (for example) with 
    # existing points
    # also, if there are too many results, elastic won't return everything and you'll need to paginate
    x_axis = []
    y_axis= []
    # scan is used for pagination and to return all results from the query
    for hit in objects.scan():
        # to limit the result by skipping points that already exist after the first 5000 
        if (len(x_axis) > 1000) and (hit[x] in x_axis or hit[y] in y_axis) :
            continue
        else:
            x_axis.append(hit[x])
            y_axis.append(hit[y])

    # MDA
    # I don't understand this -- would be nice to have a comment describing the objects you're iterating on (Fixed: Removed this code, using the scan instead)
    
    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "x_axis" : x_axis, "y_axis" : y_axis}
    return HttpResponse(json.dumps(response),content_type="application/json")   


def createHeatmapPlot(x, y, chart_type):
    # given 2 categorical columns, create a heatmap where count is used as the z_axis
    x=x+'.keyword'
    y=y+'.keyword'
    objects = ObjectDocument.search().source([x,y])
    objects.aggs.bucket('heatmap', 'terms', size=500,field=x).bucket('inner', 'terms', field=y)
    results = objects.execute()

    x_axis =[]
    y_axis=[]
    count=[]
    for bucket in results.aggregations.heatmap.buckets:
        for innerBucket in bucket.inner.buckets:
            x_axis.append(bucket.key)
            y_axis.append(innerBucket.key)
            count.append(innerBucket.doc_count)

    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "z_label":"Count","x_axis" : x_axis, "y_axis" : y_axis, "z_axis": count}
    return HttpResponse(json.dumps(response),content_type="application/json")


def create3dHeatmapPlot(x, y, z, z_type, chart_type):
    #given 2 categorical columns and 1 numerical, create a heatmap 
    x=x+'.keyword'
    y=y+'.keyword'
    objects = ObjectDocument.search().source([x,y,z])
    objects.aggs.bucket('heatmap', 'terms', size=500,field=x).bucket('inner', 'terms', field=y).metric('metric', z_type, field=z)
    results = objects.execute()

    x_axis =[]
    y_axis=[]
    z_axis=[]
    for bucket in results.aggregations.heatmap.buckets:
        for innerBucket in bucket.inner.buckets:
            x_axis.append(bucket.key)
            y_axis.append(innerBucket.key)
            z_axis.append(innerBucket.metric.value)

    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "z_label":z, "z_type":z_type,"x_axis" : x_axis, "y_axis" : y_axis, "z_axis":z_axis}
    return HttpResponse(json.dumps(response),content_type="application/json")


def create3dScatterPlot(x, y, z, chart_type):
    #given 3 numerical columns as return data to use for a scatterplot. we plot x and y and use z for the size
    objects = ObjectDocument.search().source([x, y, z])
    x_axis = []
    y_axis= []
    z_axis=[]
    objects = objects[:10000]
    for hit in objects:
        # to limit the result by skipping points that already exist after the first 5000 
        if len(x_axis)> 1000 and (hit[x] in x_axis or hit[y] in y_axis):
            continue
        else:
            x_axis.append(hit[x])
            y_axis.append(hit[y])
            z_axis.append(hit[z])
    response = { "type_of_chart" : chart_type, "x_label" : x, "y_label" : y, "z_label" : z, "x_axis" : x_axis, "y_axis" : y_axis, "z_axis":z_axis}
    return HttpResponse(json.dumps(response),content_type="application/json") 