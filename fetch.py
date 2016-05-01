import datetime
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

def schedule(pod=None, neighborhood=None):
    """Work around website inconsistencies"""
    if pod:
        site = 'http://www.seattlefoodtruck.com/schedule/' + pod + '-food-truck-pod'
        date_format = '%A, %d %B %Y '
    elif neighborhood:
        site = 'http://www.seattlefoodtruck.com/' + neighborhood
        date_format = '%A, %B %d %Y '
    else:
        site = 'http://www.seattlefoodtruck.com/schedule/occidental-park-food-truck-pod'
        date_format = '%A, %d %B %Y '

    """Grab page"""
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, site)
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
        truck_date = datetime.datetime.strptime(day[0].text, date_format).date().isoformat()
        daydict = {"date": truck_date, "trucks":[item.text for item in day[1]]}
        jsonschedule.append(daydict)
    
    return(jsonschedule)

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description='List food trucks available in an area')
    parser.add_argument('-p', '--pod', nargs='?',
                        help='Location to check for truck schedule')
    parser.add_argument('-n', '--neighborhood', nargs='?',
                        help='Location to check for truck schedule')
    args = parser.parse_args()
    if args.pod:
        print(json.dumps(schedule(pod=args.pod)))
    elif args.neighborhood:
        print(json.dumps(schedule(neighborhood=args.neighborhood)))
    else:
        print(json.dumps(schedule()))
