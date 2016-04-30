import datetime
import json
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

def schedule():
    """Grab page"""
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://www.seattlefoodtruck.com/schedule/occidental-park-food-truck-pod/')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    
    """Strip line breaks because Beautiful Soup is dumb"""
    body = buffer.getvalue()
    body = str(body).replace("<br>", "").replace("</br>", "")

    """Parse schedule into lists"""
    soup = BeautifulSoup(body, 'html.parser')
    days = soup.find_all('dt')
    schedule = [truck.ul.find_all('strong') for truck in soup.find_all('dd')]
    
    """Convert separate lists into a sensible object"""
    jsonschedule = []
    for day in zip(days, schedule):
        truck_date = datetime.datetime.strptime(day[0].text, '%A, %d %B %Y ').date().isoformat()
        daydict = {"date": truck_date, "trucks":[item.text for item in day[1]]}
        jsonschedule.append(daydict)
    
    return(jsonschedule)

if __name__ == "__main__":
    print(schedule())
