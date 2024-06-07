from rest_framework import serializers
from .models import Machine,ProductionLog


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machine
        fields='__all__'

class ProductionLogSerializer(serializers.ModelSerializer):
    machine=MachineSerializer()
    availability = serializers.SerializerMethodField()
    performance = serializers.SerializerMethodField()
    quality = serializers.SerializerMethodField()
    oee = serializers.SerializerMethodField()

    def get_availability(self, obj):
        return obj.calculate_availability()

    def get_performance(self, obj):
        return obj.calculate_performance()

    def get_quality(self, obj):
        return obj.calculate_quality()

    def get_oee(self, obj):
        return obj.calculate_oee()


    class Meta:
        model=ProductionLog
        fields=['cycle_no','unique_id','machine','shift','date','availability','performance','quality','oee']