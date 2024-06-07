from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Machine, ProductionLog
from datetime import datetime, timedelta
from django.urls import reverse

class ProductionLogTestCase(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            machine_name="Test Machine",
            machine_serial_no="12345"
        )
        self.production_log = ProductionLog.objects.create(cycle_no="CN002",unique_id="unique-123",
            material_name="Material-1",
            machine=self.machine,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=8),
            duration=8.0,
            shift="Shift-1",
            produced_product=100,
            bad_product=10,
            unplanned_downtime=0.5,
            operating_time=7.5,
            ideal_cycle_time=60,
            date=datetime.now().date()
        )

    def test_calculate_availability(self):
        availability = self.production_log.calculate_availability()
        self.assertEqual(availability, 93.75) 

    def test_calculate_performance(self):
        performance = self.production_log.calculate_performance()
        self.assertEqual(performance, 22.22) 

    def test_calculate_quality(self):
        quality = self.production_log.calculate_quality()
        self.assertEqual(quality, 90.0)  

    def test_calculate_oee(self):
        oee = self.production_log.calculate_oee()
        self.assertEqual(oee, 18.75) 


class MachineAPITestCase(APITestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            machine_name="Test Machine",
            machine_serial_no="12345"
        )

    def test_get_machines(self):
        url = reverse('machine')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['machine_name'], "Test Machine")

class OEECalculationAPITestCase(APITestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            machine_name="Test Machine",
            machine_serial_no="12345"
        )
        self.production_log = ProductionLog.objects.create(
            cycle_no="CN001",
            unique_id="unique-123",
            material_name="Material-1",
            machine=self.machine,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=8),
            duration=8.0,
            shift="Shift-1",
            produced_product=100,
            bad_product=10,
            unplanned_downtime=0.5,
            operating_time=7.5,
            ideal_cycle_time=60,
            date=datetime.now().date()
        )

    def test_get_oee_calculation(self):
        url = reverse('oee_calculation')
        response = self.client.get(url, {
            'machine_id': self.machine.id,
            'from_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'to_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cycle_no'], "CN001")
