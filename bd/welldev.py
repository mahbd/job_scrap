import requests

from bd.gemini import convert_using_gemini
from bd.models import Job

def scrap_welldev():
    url = 'https://api.recruitment.welldev.io/api/publics/job_posts'  # res json
    response = requests.get(url)
    jobs = response.json()
    if not jobs:
        print("No job links found matching the specified structure.")
        return
    for job in jobs:
        try:
            Job.objects.get(url=job['job_post_url'])
        except Job.DoesNotExist:
            details = convert_using_gemini(job)
            if details:
                new_job = Job()
                new_job.title = details.get('title')
                new_job.subtitle = details.get('subtitle')
                new_job.description = details.get('description')
                new_job.content_hash = job['job_post_url']
                new_job.requirements = details.get('requirements')
                new_job.beneficiaries = details.get('beneficiaries')
                new_job.company = 'WellDev'
                new_job.location = details.get('location')
                new_job.salary = details.get('salary')
                new_job.date_posted = details.get('date_posted')
                new_job.url = job['job_post_url']
                new_job.category = details.get('category')
                new_job.is_suitable = details.get('is_suitable') or False
                new_job.job_type = details.get('job_type')
                new_job.save()
        except KeyError:
            print(f"KeyError for job: {job}")
            return

    # delete old jobs
    Job.objects.filter(company='WellDev').exclude(url__in=[job['job_post_url'] for job in jobs]).delete()
