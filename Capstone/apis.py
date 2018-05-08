from django.http import HttpResponse
from .models import MachineType, Machine, Temp_Sensor_Data, Noise_Sensor_Data
import numpy as np
import datetime
import json
import random
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def getMachines(request):
    machines = Machine.objects.all()
    final_response = []
    for machine in machines:
        response = {}
        machine_str = machine.__dict__
        response["id"] = machine_str["MachineID"]
        response["type_id"] = machine.MachineTypeID.__dict__["MachineTypeID"]
        response["name"] = machine.MachineTypeID.__dict__["Name"]
        response["last_service"] = get_date_str(machine_str["LastService"])
        # response["AvgTemperature"] = getTempData(machine.temp_sensor_data_set)
        # response["AvgNoise"] = getNoiseData(machine.noise_sensor_data_set)
        final_response.append(response)
    return HttpResponse(final_response)

def getMachineInfo(request):
    machine = int(request.GET.get("machineid"))
    machines = Machine.objects.filter(MachineID=machine)
    machineObj = machines[0]
    machine_str = machineObj.__dict__
    final = []
    response = {}
    response["id"] = machine_str["MachineID"]
    response["type_id"] = machineObj.MachineTypeID.__dict__["MachineTypeID"]
    response["name"] = machineObj.MachineTypeID.__dict__["Name"]
    response["Ideal_temp"] = machineObj.MachineTypeID.__dict__["IdealTemperature"]
    response["Ideal_noise"] = machineObj.MachineTypeID.__dict__["IdealNoise"]
    response["desc"] = machineObj.MachineTypeID.__dict__["Description"]
    response["last_service"] = get_date_str(machine_str["LastService"])
    response["noise_data"] = getNoiseData(machine)
    response["temp_data"] = getTempData(machine)
    final.append(response)
    return HttpResponse(final)

@csrf_exempt
def addTempData(request):
    body = json.loads(request.body)
    device  = body["machineId"]
    machines = Machine.objects.filter(MachineID=device)
    machineObj = machines[0]
    temp = body["temp"]
    date = body["date"]
    noise = getNoise(temp)
    tempdata = Temp_Sensor_Data(MachineID=machineObj, TempLogged=temp, DateLogged=date)
    noisedata = Noise_Sensor_Data(MachineID=machineObj, NoiseLogged=noise, DateLogged=date)
    tempdata.save()
    noisedata.save()
    return HttpResponse("Data Saved")

def getMachineData(request):
    machine = int(request.GET.get("machineid"))
    start = datetime.datetime.strptime(request.GET.get("start"), '%m-%d-%Y %H:%M:%S')
    end = datetime.datetime.strptime(request.GET.get("end"), '%m-%d-%Y %H:%M:%S')
    response = {}
    noise_data, avg_noise, max_noise, min_noise = getNoiseDataDate(machine, start, end)
    temp_data, avg_temp, max_temp, min_temp = getTempDataDate(machine, start, end)
    machines = Machine.objects.filter(MachineID=machine)
    machineObj = machines[0]
    response["name"] = machineObj.MachineTypeID.__dict__["Name"]
    response["Ideal_temp"] = machineObj.MachineTypeID.__dict__["IdealTemperature"]
    response["Ideal_noise"] = machineObj.MachineTypeID.__dict__["IdealNoise"]
    response["desc"] = machineObj.MachineTypeID.__dict__["Description"]
    response["noise_data"] = noise_data
    response["temp_data"] = temp_data
    response["noise_attr"] = {"avg":avg_noise, "min": min_noise, "max": max_noise}
    response["temp_attr"] = {"avg": avg_temp, "min": min_temp, "max": max_temp}
    final = []
    final.append(response)
    return HttpResponse(final)


def getNoise(temp):
    return random.uniform(temp-10, temp+10)


def getTempDataDate(id, start, end):
    objs = {"Date":[], "Temp":[]}
    data = Temp_Sensor_Data.objects.filter(MachineID=id)
    for record in data:
        date = record.__dict__["DateLogged"]
        date = date.replace(tzinfo=None)
        if(start<=date<=end):
            date_str = get_date_str(date)
            objs["Date"].append(date_str)
            objs["Temp"].append(record.__dict__["TempLogged"])
    return objs, np.mean(objs["Temp"]), max(objs["Temp"]), min(objs["Temp"])
    #return np.mean(objs)

def getNoiseDataDate(id, start, end):
    objs = {"Date": [], "Noise": []}
    data = Noise_Sensor_Data.objects.filter(MachineID=id)
    for record in data:
        date = record.__dict__["DateLogged"]
        date = date.replace(tzinfo=None)
        if (start <= date <= end):
            date_str = get_date_str(date)
            objs["Date"].append(date_str)
            objs["Noise"].append(record.__dict__["NoiseLogged"])
    return objs, np.mean(objs["Noise"]), max(objs["Noise"]), min(objs["Noise"])
    #return np.mean(objs)

def getTempData(id):
    objs = {"Date":[], "Temp":[]}
    data = Temp_Sensor_Data.objects.filter(MachineID=id)
    for record in data:
        date = record.__dict__["DateLogged"]
        date_str = get_date_str(date)
        objs["Date"].append(date_str)
        objs["Temp"].append(record.__dict__["TempLogged"])
    return objs
    #return np.mean(objs)

def getNoiseData(id):
    objs = {"Date": [], "Noise": []}
    data = Noise_Sensor_Data.objects.filter(MachineID=id)
    for record in data:
        date = record.__dict__["DateLogged"]
        date_str = get_date_str(date)
        objs["Date"].append(date_str)
        objs["Noise"].append(record.__dict__["NoiseLogged"])
    return objs
    #return np.mean(objs)

def get_date_str(date):
    return date.strftime('%m/%d/%Y %H:%M:%S')