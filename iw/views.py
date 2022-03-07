from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from iw.models import Facility, AdditionalPicture, HistoricData, SystemDiagram, MainSys, SubSys
import json
import requests
from collections import OrderedDict
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from django.conf import settings
import os
import pytz


# Create your views here.
def homepage(request):
    context = {}
    context['images'] = Facility.objects.filter(category="homepageImage")
    context['greeting'] = ""
    return render(request, 'homepage.html', context=context)

# make sure that h,v,ac,lighting is 1,2,3,4.
def systemPage(request, id):
    context = {}

    if id == 4:
        context['plans'] = Facility.objects.filter(category="floorplan_lighting")
        context['percent'] = 80
        context['pix'] = 900
    else:
        context['plans'] = Facility.objects.filter(category="floorplan")
        context['percent'] = 50
        context['pix'] = 800
    mainSys = MainSys.objects.get(id=id)
    subSyss = mainSys.subsys_set.all()
    dic = {}
    for subSys in subSyss:
        dic[subSys] = subSys.facility_set.all()
    context['legends'] = dic
    context['numOfCols'] = subSyss.count()
    context['his_items'] = HistoricData.objects.filter(category=mainSys.name)
    context['diagrams'] = SystemDiagram.objects.filter(category=mainSys.name)
    template = os.path.join(settings.TEMPLATE_ROOT, mainSys.name + ".html")
    return render(request, template, context=context)


def getPlanImage(request, id):
    image = get_object_or_404(Facility, id = id)
    if not image.picture:
        raise Http404
    return HttpResponse(image.picture, content_type=image.content_type)

def getAdditionalImage(request, id):
    image = get_object_or_404(AdditionalPicture, id = id)
    if not image.content:
        raise Http404
    return HttpResponse(image.content, content_type=image.content_type)


def getSystemDiagram(request, id):
    image = get_object_or_404(SystemDiagram, id=id)
    if not image.content:
        raise Http404
    return HttpResponse(image.content, content_type=image.content_type)


def getSpecification(request, id):
    response_data = []
    facility = Facility.objects.get(id=id)
    picList = []
    for pic in facility.additionalpicture_set.all():
        picList.append(pic.id)

    response_data.append({
        "id": facility.id,
        "manufacturer": facility.manufacturer,
        "dateInstalled": facility.dateInstalled.isoformat(),
        "count": facility.count,
        "description": facility.description,
        "pictureIds": picList
    })

    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


# temperature acquisition

class weatherAcquirer:
    # constants
    ORIGIN = "https://api.weather.com/v1/location/{city}{suffix}/observations/historical.json?apiKey={key}&units=e&startDate={start}&endDate={end}"
    KEY = "e1f10a1e78da46f5b10a1e78da96f525"
    COUNTRY_SUFFIX = ":9:US"
    DATES = {}

    # cache
    log = {}
    temperatures = {}

    def __init__(self):
        ## dates
        mo31 = ["01", "03", "05", "07", "08", "10", "12"]
        mo30 = ["04", "06", "09", "11"]
        mo28 = ["02"]
        for mo in mo31:
            self.DATES[mo] = "31"
        for mo in mo30:
            self.DATES[mo] = "30"
        for mo in mo28:
            self.DATES[mo] = "28"

    ## helper method: convert oF to oC
    def f2c(self, temp_f):
        return "%.1f" % ((temp_f - 32) / 1.8)

    # helper method: sort map
    def sortByTimestamp(self):
        self.temperatures = OrderedDict(sorted(self.temperatures.items()))

    ## helper method: merge two dictionaries.
    def merge(self, dict1, dict2):
        res = {**dict1, **dict2}
        return res

    ## Clean cache.
    def flush(self):
        self.log = {}
        self.temperatures = {}

    def acquireDailyTemp(self, city: str, year: str, month: str, day: str):
        errorlog = {}
        temperatures = {}
        start = year + month + day
        end = start
        url = self.ORIGIN.format(city=city, suffix=self.COUNTRY_SUFFIX, key=self.KEY, start=start, end=end)
        r = requests.get(url)
        content = json.loads(r.content)
        if content['metadata']['status_code'] != 200:
            errorlog[month] = "status code 400"
        # log temperatures
        for observation in content['observations']:
            temperatures[observation['expire_time_gmt']] = self.f2c(observation['temp'])
        print("{year}/{month}/{day} temperature for {city} complete".format(year=year, month=month, day=day, city=city))

        # cache.
        self.log = self.merge(self.log, errorlog)
        self.temperatures = self.merge(self.temperatures, temperatures)
        return errorlog, temperatures

    def acquireMonthlyTemp(self, city: str, year: str, month: str):
        errorlog = {}
        temperatures = {}
        start = year + month + "01"
        end = year + month + self.DATES[month]
        url = self.ORIGIN.format(city=city, suffix=self.COUNTRY_SUFFIX, key=self.KEY, start=start, end=end)
        r = requests.get(url)
        content = json.loads(r.content)
        if content['metadata']['status_code'] != 200:
            errorlog[month] = "status code 400"
        # log temperatures
        for observation in content['observations']:
            temperatures[observation['expire_time_gmt']] = self.f2c(observation['temp'])
        print("{year}/{month} temperature for {city} complete".format(year=year, month=month, city=city))

        # cache.
        self.log = self.merge(self.log, errorlog)
        self.temperatures = self.merge(self.temperatures, temperatures)
        return errorlog, temperatures

    def acquireAnnualTemp(self, city: str, year: str):
        errorlog = {}
        temperatures = {}
        for mo in self.DATES:
            prevErrorlog, prevTemps = self.acquireMonthlyTemp(city, year, mo)
            # merge errorlog and temperature map.
            errorlog = self.merge(errorlog, prevErrorlog)
            temperatures = self.merge(temperatures, prevTemps)
        print("{year} temperature for {city} complete".format(year=year, city=city))

        # cache.
        self.log = self.merge(self.log, errorlog)
        self.temperatures = self.merge(self.temperatures, temperatures)
        return errorlog, temperatures

def convertToMyFormat(year:int, month:int, day:int):
    month_out = str(month)
    if month < 10:
        month_out = "0" + month_out
    day_out = str(day)
    if day < 10:
        day_out = "0" + day_out
    return str(year), month_out, day_out

def realtime(request):
    context = {}
    ac = weatherAcquirer()
    current_time = datetime.now(tz = pytz.timezone('America/New_York'))
    year, month, day = convertToMyFormat(current_time.year, current_time.month, current_time.day)
    # ac.acquireDailyTemp("KPIT", year, month, day)
    ac.acquireMonthlyTemp("KPIT", year, month)
    ac.sortByTimestamp()

    dates = []
    for unix_ts in ac.temperatures.keys():
        dates.append((datetime.fromtimestamp(unix_ts) - timedelta(hours=7)).strftime('%m/%d-%H:%M'))

    monthMap = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }

    context['dates'] = dates
    context['temps'] = list(ac.temperatures.values())
    context['title'] = "temperature of Pittsburgh for {month}/{year}".format(month=monthMap[month], year=year)
    return render(request, 'realtime.html', context=context)


def getHistoricData(request, id):
    hData = get_object_or_404(HistoricData, id=id)
    path = os.path.join(settings.CSV_ROOT, hData.filename)
    df = pd.read_csv(path, parse_dates=True, index_col='dt')
    selectedPeriod = df[(df.index > "2018-1-1") & (df.index < "2018-12-31")]
    dts = selectedPeriod.index
    dts = dts.strftime("%m-%d/%H:%M")
    # dts = dts.strftime("%H:%M")
    dts = dts.to_numpy().tolist()
    # values = selectedPeriod.value.to_numpy().tolist()
    values = selectedPeriod.value.to_numpy()
    values = np.where(values == "/", 0, values)
    values = values.tolist()


    response_data = {
        "timestamps": dts,
        "values": values,
        "id": id,
        "title": hData.title
    }
    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def getSubsys(request, id):
    subsys = SubSys.objects.get(id=id)
    sysDiagrams = subsys.systemdiagram_set.all()
    diagramIDs = []
    for sysDiagram in sysDiagrams:
        diagramIDs.append(sysDiagram.id)

    response_data = {
        "id" : id,
        "picIDs": diagramIDs,
        "description": subsys.description
    }

    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def getStatic(request, filename):
    file = os.path.join(settings.STATIC_IW, filename)
    return HttpResponse(file)