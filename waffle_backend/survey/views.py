from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from survey.serializers import OperatingSystemSerializer, SurveyResultSerializer
from survey.models import OperatingSystem, SurveyResult


class SurveyResultViewSet(viewsets.GenericViewSet):
    queryset = SurveyResult.objects.all()
    serializer_class = SurveyResultSerializer

    def list(self, request):
        surveys = self.get_queryset().select_related('os')
        return Response(self.get_serializer(surveys, many=True).data)

    def retrieve(self, request, pk=None):
        survey = get_object_or_404(SurveyResult, pk=pk)
        return Response(self.get_serializer(survey).data)

    # POST /api/v1/survey/
    def create(self, request, *args, **kwargs):
        python = request.data.get('python')
        rdb = request.data.get('rdb')
        programming = request.data.get('programming')
        os = request.data.get('os')

        if not python or not rdb or not programming or not os:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            python_int = int(python)
            rdb_int = int(rdb)
            programming_int = int(programming)
            myList= [python_int, rdb_int, programming_int]

            if not all(1 <= num <= 5 for num in myList):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if OperatingSystem.objects.filter(name=os).exists():
            new_survey = SurveyResult.objects.create(os=OperatingSystem.objects.get(name=os), user=request.user, python=python_int, rdb=rdb_int, programming=programming_int)
        else:
            new_os = OperatingSystem.objects.create(name=os)
            new_survey = SurveyResult.objects.create(os=new_os, user=request.user, python=python_int, rdb=rdb_int, programming=programming_int)

        return Response(self.get_serializer(new_survey).data, status=status.HTTP_201_CREATED)


class OperatingSystemViewSet(viewsets.GenericViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer

    def list(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, pk=None):
        try:
            os = OperatingSystem.objects.get(id=pk)
        except OperatingSystem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(os).data)
