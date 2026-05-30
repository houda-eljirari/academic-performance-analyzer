# students/serializers.py
from rest_framework import serializers
from .models import Student, Module, Assessment, VLEActivity


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'


class VLEActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VLEActivity
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentDetailSerializer(serializers.ModelSerializer):
    assessments    = AssessmentSerializer(many=True, read_only=True)
    vle_activities = VLEActivitySerializer(many=True, read_only=True)
    module         = ModuleSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'