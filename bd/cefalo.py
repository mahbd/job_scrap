import requests
from bs4 import BeautifulSoup

from bd.gemini import convert_using_gemini
from bd.models import Job

def get_available_job_links():
    base_url = "https://ats.cefalo.com/api/v1/public/jobs"
    res = requests.get(base_url)
    jobs = res.json()
    job_links = []
    for job in jobs:
        slug = job['slug']
        job_url = f"https://career.cefalo.com/job/{slug}"
        job_links.append(job_url)
    return job_links

def get_job_details(job_url):
    res = requests.get(job_url)
    soup = BeautifulSoup(res.text, "html.parser")
    section = soup.find("section", id="singleJob")
    if not section:
        return None
    return convert_using_gemini(section)

def scrap_cefalo():
    job_links: list[str] = get_available_job_links()
    for link in job_links:
        try:
            Job.objects.get(url=link)
        except Job.DoesNotExist:
            details = get_job_details(link)
            if details:
                new_job = Job()
                new_job.title = details.get('title')
                new_job.subtitle = details.get('subtitle')
                new_job.description = details.get('description')
                new_job.content_hash = link
                new_job.requirements = details.get('requirements')
                new_job.beneficiaries = details.get('beneficiaries')
                new_job.company = 'Cefalo'
                new_job.location = details.get('location')
                new_job.salary = details.get('salary')
                new_job.date_posted = details.get('date_posted')
                new_job.url = link
                new_job.category = details.get('category')
                new_job.is_suitable = details.get('is_suitable') or False
                new_job.job_type = details.get('job_type')
                new_job.save()
    if not job_links:
        print("No job links found matching the specified structure.")
    # delete old jobs
    Job.objects.filter(company='Cefalo').exclude(url__in=job_links).delete()