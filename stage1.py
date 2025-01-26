# stage1.py
from dependencies import *
from login import driver
import config

wait = WebDriverWait(driver, 10)

headers = ["Name", "ProfileLinks", "current_designation", "current_location"]
with open("names_and_positions.csv", 'a') as File:
   writer_object = writer(File)
   writer_object.writerow(headers)

   for company in config.companies_list:
       driver.get(f"https://www.linkedin.com/search/results/people/?keywords={company}&origin=SWITCH_SEARCH_VERTICAL")
       wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-container")))
       
       src = driver.page_source
       parser = soup(src, "html.parser")
       profiles = parser.find_all("li", {"class": "reusable-search__result-container"})
       
       for profile in profiles:
           try:
               try:
                   name = profile.find("div", {"class": "display-flex align-items-center"}).img['alt']
               except:
                   name = profile.find("span", {"class": "entity-result__title-text t-16"}).a.text
               
               name = name.replace("\n","").replace(",","|").strip()
               link = profile.find("div", {"class": "display-flex align-items-center"}).a['href']
               designation = profile.find("div", {"class": "entity-result__primary-subtitle t-14 t-black"}).text.strip()
               location = profile.find("div", {"class": "entity-result__secondary-subtitle t-14"}).text.strip()
               
               data = [name, link, designation, location]
               writer_object.writerow(data)
           except Exception as e:
               print(f"Error processing profile: {str(e)}")
               continue