from dependencies import *
from login import *
import config

wait = WebDriverWait(driver, 20)

df = pd.read_csv("roles_of_person_in_pervious_list.csv")
df.drop_duplicates(keep=False, inplace=True)
arr = list(df['Company_Name'])
names = list(df['Name'])

hitWords = ['full-time', 'part-time', 'internship', 'contract', 'crio.Do', 'girlscript foundation', 
           'girlscript summer of code', 'google summer of code', 'major league hacking', 'placementunit|bitspilani',
           'highcommissionofcanadainindia', 'australiandepartmentofhomeaffairs', 'googlesummerofcode', 
           'majorleaguehacking', 'australiandepartmentofhomeaffairs', 'highcommissionofcanadainindia', 
           'britishrirways', 'resumevogue']

blockWords = ['placement', 'university', 'bachleors', 'college', 'institute', 'jecrc', 'daiict', 
             'student', 'ieee', 'dtu', 'self-employed', 'self', 'iit', 'da-iict', 'army', 
             'school', 'corona', 'mit', 'harvard', 'freelancing', 'freelancer', 'freelance', 'youtuber']

people = set()
for j in range(len(arr)):
   designation = " ".join(arr[j].split())
   flag = False
   if len(designation) > 12:
       if designation[0:12].lower() == "company name":
           flag = True 
           designation = designation.replace(designation[0:12], "")
   if flag == False and len(designation) > 7:
       if (designation[0:7].lower() == "company"):
           designation = designation.replace(designation[:7], "")
   designation = designation.lower().split()
   checker = False
   for i in range(len(designation)):
       if designation[i] in blockWords:
           checker = True
           break
   if checker == False:
       if (designation[-1] in hitWords):
           designation = designation[:-1]
       if " ".join(designation) not in hitWords:
           people.add(" ".join(designation))

people = list(people)
count = 0

for j in range(len(people)):
   if count > 99:
       break
       
   driver.get("https://www.linkedin.com/search/results/companies/?keywords=" + 
              str(people[j])+"&origin=GLOBAL_SEARCH_HEADER")
   
   wait.until(EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__result-container")))
   
   src = driver.page_source
   parser = soup(src, "html.parser")
   userList = parser.find_all("li", {"class": "reusable-search__result-container"})
   
   if len(userList) != 0:
       links = userList[0].a['href']+"/people/"
       driver.get(links)
       
       wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid grid__col--lg-8 pt5 pr4 m0")))
       time.sleep(20)
       
       src = driver.page_source
       parser = soup(src, "html.parser")
       user = parser.find_all("li", {"class": "grid grid__col--lg-8 pt5 pr4 m0"})
       
       count = 0
       for i in range(len(user)):
           count += 1
           time.sleep(5)
           
           src = driver.page_source
           parser = soup(src, "html.parser")
           
           try:
               connectRequest = wait.until(EC.element_to_be_clickable((By.XPATH, 
                   "//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view full-width']")))
               
               if connectRequest:
                   connectRequest.click()
                   
                   addNote = wait.until(EC.element_to_be_clickable((By.XPATH,
                       "//button[@class='mr1 artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--secondary ember-view']")))
                   addNote.click()
                   
                   message = wait.until(EC.presence_of_element_located((By.XPATH,
                       "//textarea[@class='ember-text-area ember-view connect-button-send-invite__custom-message mb3']")))
                       
                   name = wait.until(EC.presence_of_element_located((By.XPATH,
                       "//div[@class='org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view']"))).text
                   print(name)
                   
                   message.send_keys(config.message)
                   
                   send = wait.until(EC.element_to_be_clickable((By.XPATH,
                       "//button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")))
                   send.click()
                   
           except Exception as e:
               print(f"Error: {str(e)}")
               continue