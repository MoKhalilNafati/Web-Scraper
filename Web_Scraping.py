import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

BASE_URL = "https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/?hec-degreeProgrammeType=w&hec-teachingLanguage=2&hec-deadlineId=3&hec-studyType=t,v&hec-admissionMode=O,X&hec-subjectGroup=1"

request = requests.get(BASE_URL)
src = request.content
data = BeautifulSoup(src, 'lxml')

program = []
university = []
location = []
period = []
aos = []
focus = []
deadlines = []
semester = []
annotation = []
modus = []
requirements = []
lecture = []
advisory = []
links = []

# Find Programs
programs = data.find_all('span', {'class': 'js-dynamic-content u-display-block u-font-light u-size-24 result__headline-content mb-24 u-size-32@lg'})
# Find Universities
universities = data.find_all('span', {'class': 'js-dynamic-content u-display-block u-font-regular u-size-18 result__headline-content mb-8'})
# Find Locations
locations = []
for strong in data.find_all('strong'):
    if strong.text.strip() == 'Location:':
        locations.append(strong.find_parent().find_next('dd'))
# Find Period Of Study
pos = []
for strong in data.find_all('strong'):
    if strong.text.strip() == 'Standard Period of Study:':
        pos.append(strong.find_parent().find_next('dd'))
# Find links
default_links = data.find_all('a', {'href', 'link link--nowrap u-stretched-link u-position-static result__link qa-more-link u-text-primary u-font-italic'})

for a in default_links:
    links.append("https://www.daad.de" + a['href'])

# Append programs, universities, locations, period
for i in range(len(programs)):
    program.append(programs[i].text.strip())
    university.append(universities[i].text.strip())
    location.append(locations[i].text.strip())
    period.append(pos[i].text.strip())

# Visit each detail page
for link in links:
    request = requests.get(link)
    src = request.content
    data = BeautifulSoup(src, 'lxml')

    # Area of study
    h5_aos = data.find('h5', string="Area of study")
    if h5_aos:
        ul = h5_aos.find_next_sibling('ul')
        if ul:
            aos.append(" | ".join(li.text.strip() for li in ul.find_all("li")))
        else:
            p = h5_aos.find_next_sibling('p')
            aos.append(p.text.strip() if p else "-")
    else:
        aos.append('-')

    # Focus
    h5_focus = data.find('h5', string='Focus')
    if h5_focus:
        p = h5_focus.find_next_sibling('p')
        focus.append(p.text.strip() if p else '-')
    else:
        focus.append('-')

    # Deadlines
    ddln = data.find_all('h6', string='Deadlines for international students from countries that are not members of the European Union')
    if ddln:
        deadlines.append(" | ".join(d.find_next_sibling('p').text.strip() for d in ddln))
    else:
        deadlines.append('-')

    # Admission semester
    h5_semester = data.find('h5', string='Admission semester')
    if h5_semester:
        p = h5_semester.find_next_sibling('p')
        semester.append(p.text.strip() if p else '-')
    else:
        semester.append('-')

    # Annotation
    h5_annotation = data.find('h5', string='Annotation')
    if h5_annotation:
        p = h5_annotation.find_next_sibling('p')
        annotation.append(p.text.strip() if p else '-')
    else:
        annotation.append('-')

    # Admission modus
    h5_modus = data.find('h5', string='Admission modus')
    if h5_modus:
        ps = h5_modus.find_next_siblings('p')
        if ps:
            items = [p.text.strip() for p in ps]
            modus.append(" | ".join(items))
        else:
            modus.append('-')
    else:
        modus.append('-')

    # Admission requirements
    h5_requirements = data.find('h5', string='Admission requirements')
    if h5_requirements:
        p = h5_requirements.find_next_sibling('p')
        requirements.append(p.text.strip() if p else '-')
    else:
        requirements.append('-')

    # Lecture period
    h5_lecture = data.find('h5', string='Lecture period')
    if h5_lecture:
        ul = h5_lecture.find_next_sibling('ul')
        if ul:
            lecture.append(" | ".join(li.text.strip() for li in ul.find_all('li')))
        else:
            p = h5_lecture.find_next_sibling('p')
            lecture.append(p.text.strip() if p else '-')
    else:
        lecture.append('-')

    # Student advisory service
    h4_section = data.find("h4", string="Student advisory service")
    email = "-"
    web = "-"
    if h4_section:
        div_item = h4_section.find_next_sibling("div")
        if div_item:
            dls = div_item.find_all("dl")
            i = 0
            while i < len(dls):
                dl = dls[i]
                dt_email = dl.find("dt", string="E-Mail:")
                if dt_email:
                    dd_email = dt_email.find_next_sibling("dd")
                    if dd_email:
                        span_email = dd_email.find("span", class_="link__text u-decoration-underline")
                        if span_email:
                            raw_email = span_email.get_text(separator="", strip=True)
                            email = raw_email.replace(' at ', '@').replace(' ', '')
                dt_web = dl.find("dt", string="Web:")
                if dt_web:
                    dd_web = dt_web.find_next_sibling("dd")
                    if dd_web:
                        a_web = dd_web.find("a")
                        if a_web and a_web.has_attr("href"):
                            web = a_web["href"]
                if email != "-" and web != "-":
                    break
                i += 1
    advisory.append(email + " | " + web)

# Export to CSV
file_list = [program, university, location, period, aos, focus, deadlines, semester,
             annotation, modus, requirements, lecture, advisory, links]

exported = zip_longest(*file_list, fillvalue='-')

with open("C:/Users/Khalil/Documents/VS/Web Scraping/programs.csv", 'w', newline="") as myFile:
    wr = csv.writer(myFile)
    wr.writerow([
        'Program', 'University/Hochschule', 'Location', 'Period Of Study', 'Area Of Study',
        'Focus', 'Deadlines', 'Admission Semester', 'Annotation', 'Admission Modus',
        'Admission Requirements', 'Lecture Period', 'Student Advisory', 'Link'
    ])
    wr.writerows(exported)

