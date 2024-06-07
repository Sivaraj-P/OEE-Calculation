from django.db import models
from uuid import uuid4

SHIFTS=(
    ('Shift-1','Shift-1'),
    ('Shift-2','Shift-2'),
    ('Shift-3','Shift-3')
)

class Machine(models.Model):
    machine_name = models.CharField(max_length=255)
    machine_serial_no = models.CharField(max_length=255, unique=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_name

class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, unique=True,default=uuid4)
    material_name = models.CharField(max_length=255)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(default=8.0,help_text='Duration in hours')  
    shift = models.CharField(max_length=255,choices=SHIFTS)
    produced_product = models.IntegerField()
    bad_product = models.IntegerField()
    unplanned_downtime = models.FloatField(default=0.0,help_text='Unplanned downtime in hours') 
    operating_time = models.FloatField(help_text='Available Operating time in hours')  
    ideal_cycle_time= models.FloatField(help_text='Ideal cycle time in seconds')  
    date=models.DateField()
    def calculate_availability(self):
        operating_time = self.operating_time
        return round((operating_time / self.duration)*100,2)

    def calculate_performance(self):
        total_production_time = self.operating_time
        total_units_produced = self.produced_product
        return round(((total_units_produced * self.ideal_cycle_time) / (total_production_time*60*60))*100,2)

    def calculate_quality(self):
        total_produced = self.produced_product
        total_good = self.produced_product - self.bad_product
        return round((total_good / total_produced)*100,2) if total_produced > 0 else 0

    def calculate_oee(self):
        availability = self.calculate_availability()
        performance = self.calculate_performance()
        quality = self.calculate_quality()
        return round(((availability/100) * (performance/100) * (quality/100))*100,2)

   

    def __str__(self):
        return f"{self.cycle_no} - {self.material_name}"
    

    class Meta:
        unique_together=('machine','shift','date')
