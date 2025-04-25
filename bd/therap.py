import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # To create absolute URLs

from bd.gemini import convert_using_gemini
from bd.models import Job

base_url = "https://therap.hire.trakstar.com/"


def get_available_job_links():
    response = requests.get(base_url)
    job_links = []
    soup = BeautifulSoup(response.content, 'lxml')
    job_items = soup.find_all('div', class_='js-careers-page-job-list-item')

    for item in job_items:
        link_tag = item.find('a')
        if link_tag and link_tag.has_attr('href'):
            relative_link = link_tag['href']
            absolute_link = urljoin(base_url, relative_link)
            job_links.append(absolute_link)
    return job_links

def get_job_details(job_url):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.content, 'lxml')
    contents = soup.find_all('div', class_='main-content')
    if not contents:
        return None
    content = contents[0]
    return convert_using_gemini(content)


def scrap_therap():
    job_links = get_available_job_links()
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
                new_job.company = 'TherapBD'
                new_job.location = details.get('location')
                new_job.salary = details.get('salary')
                new_job.date_posted = details.get('date_posted')
                new_job.url = link
                new_job.category = details.get('category')
                new_job.is_suitable = details.get('is_suitable') or False
                new_job.job_type = details.get('job_type')
                new_job.save()
