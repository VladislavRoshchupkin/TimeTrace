from this import d
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
from django.contrib.auth.models import User
from ..models import *
from collections import Counter

class ProjectList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request):
        projects = Project.objects.all()
        queryset = ProjectSerializer(projects, many=True)
        context = {
            'projects' : queryset.data
        }
        return Response(context)


class TimeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSerializer

    def get(self, request):
        employee = Employee.objects.get(user_key=request.user)
        times = Time.objects.filter(time_key=employee)
        queryset = TimeSerializer(times, many=True)
        context = {
            'times' : queryset.data
        }
        return Response(context)


class TaskList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request):
        employee = Employee.objects.get(user_key=request.user)
        tasks = Task.objects.filter(employee_key=employee)
        queryset = TaskSerializer(tasks, many=True)
        context = {
            'tasks' : queryset.data
        }
        return Response(context)

class DepartmentList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer


    def get(self, request):
        department = Department.objects.all()

        dep_array = []
        for e in Employee.objects.all():
            dep_array.append(e.department_key.department_name)
        counts_of_employee = Counter(dep_array).most_common()
        for (k, v) in enumerate(counts_of_employee):
            department_current = Department.objects.get(department_name=v[0])
            department_current.count_employee=v[1]
            department_current.save()
        queryset = DepartmentSerializer(department, many=True)
        context = {
            'department' : queryset.data
        }
        return Response(context)

class RaitingList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RaitingSerializer

    def get(self, request):
        departments = Department.objects.all()
        raiting = Raiting.objects.filter(raiting_key__in=departments)
        queryset = RaitingSerializer(raiting, many=True)
        context = {
            'raiting' : queryset.data
        }
        return Response(context)