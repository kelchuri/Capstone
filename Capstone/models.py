from django.db import models


class MachineType(models.Model):
    MachineTypeID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=200)
    IdealTemperature = models.DecimalField(max_digits=5, decimal_places=2)
    IdealNoise = models.DecimalField(max_digits=5, decimal_places=2)

class Machine(models.Model):
    MachineID =models.IntegerField(primary_key=True)
    MachineTypeID = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    LastService = models.DateTimeField()

class Temp_Sensor_Data(models.Model):
    RecordID = models.AutoField(primary_key=True)
    MachineID = models.ForeignKey(Machine, on_delete=models.CASCADE)
    TempLogged = models.DecimalField(max_digits=5, decimal_places=2)
    DateLogged = models.DateTimeField()

class Noise_Sensor_Data(models.Model):
    RecordID = models.AutoField(primary_key=True)
    MachineID = models.ForeignKey(Machine, on_delete=models.CASCADE)
    NoiseLogged = models.DecimalField(max_digits=5, decimal_places=2)
    DateLogged = models.DateTimeField()