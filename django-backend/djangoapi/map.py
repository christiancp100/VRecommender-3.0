from djangoapi.helpers import _reformatKey
from djangoapi.models import *
from django.http import HttpResponse
import json

import csv

from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def airports(request):
    parameters = request.GET
    if "value" in parameters:
        value = parameters["value"]
    else: 
        value=10
    value2 = int(value)
    # LAX,Los Angeles International,Los Angeles,CA,USA,33.94253611,-118.4080744
    # name, city, state, country, latitude, longitude
    # ORIGIN_AIRPORT_NAME,ORIGIN_AIRPORT_CITY, ORIGIN_AIRPORT_STATE,ORIGIN_AIRPORT_COUNTRY, ORIGIN_AIRPORT_COORDINATES
    code="AIRLINE_CODE"
    name="ORIGIN_AIRPORT_NAME"
    city="ORIGIN_AIRPORT_CITY"
    state ="ORIGIN_AIRPORT_STATE"
    country ="ORIGIN_AIRPORT_COUNTRY"
    coordinate ="ORIGIN_AIRPORT_COORDINATES"
    result = []

    objects = ObjectDocument.search().source([code, name, city, state, country, coordinate])
    object2 = objects[0:value2]
    result.append(["iata","name","city","state","country","latitude","longitude"])
    for hit in object2:
        result.append([
            hit[code],
            hit[name],
            hit[city],
            hit[state],
            hit[country],
            (hit[coordinate])[1],
            (hit[coordinate])[0]
        ])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in result), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="airports.csv"'



    #response = {"iata": codes, "name":names, "city":cities, "state": states, "country":countries, "latitude": latitudes, "longitude":longitudes}
    return response #HttpResponse(json.dumps({'result':result}), content_type="application/json")
    #http://localhost:8000/map/airports/?value=5  

def flights(request):
    #this funtion returns the count of flights from origin to destination. i.e:
    # origin,destination,count
    # ABE,ATL,853
    # value is used for the size of the aggregation
    # { "origin": "ABE", "destination": "ATL", "count": 853},
    parameters = request.GET
    if "value" in parameters:
        value = parameters["value"]
    else: 
        value=10
    objects = ObjectDocument.search().source(["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"])
    
    objects.aggs.bucket('origin', 'terms', size=value, field="ORIGIN_AIRPORT.keyword").bucket('destination', 'terms', size=value, field="DESTINATION_AIRPORT.keyword")
    results = objects.execute()

    result =[]
    result.append(["origin", "destination", "count"])
    for bucket in results.aggregations.origin.buckets:
        for innerBucket in bucket.destination.buckets:
            result.append([bucket.key, innerBucket.key, innerBucket.doc_count])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in result), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="flights-airport.csv"'

    return response#HttpResponse(json.dumps(result),content_type="application/json")
    #http://localhost:8000/map/flights/?value=5  
    