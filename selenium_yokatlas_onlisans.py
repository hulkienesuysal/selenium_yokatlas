from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from peewee import Proxy,Model,CharField,SqliteDatabase

db_proxy=Proxy()
class BaseModel(Model):
    class Meta:
        database=db_proxy

class Liseler(BaseModel):
    veriler=CharField(null=True)

db = SqliteDatabase("yokatlas_onlisans.db")
db_proxy.initialize(db)

db_proxy.connect()
db_proxy.create_tables([Liseler], safe=True)


driver = webdriver.Chrome(ChromeDriverManager().install())

site="https://yokatlas.yok.gov.tr/onlisans-univ.php?u=1004"
saniye=1

driver.get(site)
sleep(saniye)

def scrolltarget(xpath):
    target = driver.find_element_by_xpath(xpath)
    desired_y = (target.size['height'] / 2) + target.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


bolumsayisi=len(driver.find_elements_by_class_name("panel-heading"))
kolon1bolumsayisi=len(driver.find_elements_by_xpath('//*[@id="bs-collapse"]/div'))
print(bolumsayisi)
sleep(saniye)
i=1
k=1
collopse=""
while i<=bolumsayisi: 
    try:
        scrolltarget('//*[@id="bs-collapse{}"]/div[{}]/div/h4/a/button'.format(collopse,k))
        bolum=driver.find_element_by_xpath('//*[@id="bs-collapse{}"]/div[{}]/div/h4/a/div'.format(collopse,k)).text
        print(bolum)
        save=Liseler.create(veriler="----------{}----------({})".format(bolum,i))
        save.save()
        driver.find_element_by_xpath('//*[@id="bs-collapse{}"]/div[{}]/div/h4/a/button'.format(collopse,k)).click()
        #sleep(saniye)
        #driver.find_element_by_xpath('/html/body/div/div[1]/div[6]/div[2]/h2/strong/a[2]').click()
        sleep(saniye)
        scrolltarget('//*[@id="h3060"]/a') 
        driver.find_element_by_xpath('//*[@id="h3060"]/a').click()
        sleep(saniye)
        lisesayisi=len(driver.find_elements_by_xpath('//*[@id="icerik_3060"]/table/tbody/tr'))
        print(lisesayisi)
        o=2
        while o<lisesayisi+1:
            scrolltarget('//*[@id="icerik_3060"]/table/tbody/tr[{}]/td[1]'.format(o))
            liseler=driver.find_element_by_xpath('//*[@id="icerik_3060"]/table/tbody/tr[{}]/td[1]'.format(o)).text
            print(liseler)
            save=Liseler.create(veriler=liseler)
            save.save()
            o+=1
        save=Liseler.create(veriler="")
        save.save()
    except:
        pass
    k+=1
    if i==kolon1bolumsayisi:
        k=1
        collopse="2"
    i+=1
    #driver.back()
    driver.back()
    sleep(saniye)
    
    
