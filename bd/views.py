from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .cefalo import scrap_cefalo
from .models import Job
from .serializers import JobSerializer
from .therap import scrap_therap
from .welldev import scrap_welldev


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

@api_view(['GET'])
def scrap_cefalo_req(request):
    scrap_cefalo()
    return Response({"status": "scraping done cefalo"})


@api_view(['GET'])
def scrap_therap_req(request):
    scrap_therap()
    return Response({"status": "scraping done therap"})

@api_view(['GET'])
def scrap_welldev_req(request):
    scrap_welldev()
    return Response({"status": "scraping done welldev"})


def get_job_list_html(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs,
    }
    return render(request, 'bd/jobs.html', context)

def get_job_detail_html(request, pk):
    job = Job.objects.get(pk=pk)
    context = {
        'job': job,
    }
    return render(request, 'bd/job.html', context)
