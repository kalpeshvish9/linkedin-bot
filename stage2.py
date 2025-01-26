from dependencies import *
from login import driver

wait = WebDriverWait(driver, 10)
df = pd.read_csv("names_and_positions.csv")

headers = ["Name", "Company_Name", "Duration", "Information"]
with open("roles_of_person_in_pervious_list.csv", 'a') as File:
   writer_object = writer(File)
   writer_object.writerow(headers)
   
   count = 0
   for j, row in df.iterrows():
       if count > 999:
           break
           
       name = row['Name']
       link = str(row['ProfileLinks']).strip()
       
       if not link or pd.isna(link):
           continue
           
       try:
           print(f"Processing: {link}")
           driver.get(link)
           
           try:
               see_more = wait.until(EC.element_to_be_clickable((By.XPATH, 
                   "//button[contains(@class, 'pv-profile-section__see-more-inline')]")))
               see_more.click()
           except:
               pass
               
           src = driver.page_source
           parser = soup(src, "html.parser")
           profiles = parser.find_all("li", {"class": "pv-entity__position-group-pager"})
           
           for profile in profiles:
               count += 1
               try:
                   company_name = (profile.find("p", {"class": "pv-entity__secondary-title"}) or \
                                 profile.find("h3", {"class": "t-14"})).text.strip()
               except:
                   company_name = ""
                   
               try:
                   duration = (profile.find("span", {"class": "pv-entity__bullet-item-v2"}) or \
                             profile.find("h4", {"class": "t-14"})).text.strip()
               except:
                   duration = ""
                   
               try:
                   info = profile.find("div", {"class": "pv-entity__extra-details"}).text.strip()
               except:
                   info = ""
                   
               data = [name, company_name, duration, info]
               writer_object.writerow(data)
               
       except Exception as e:
           print(f"Error processing {link}: {str(e)}")
           continue