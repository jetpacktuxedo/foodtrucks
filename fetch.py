import datetime
import json
import requests

def schedule(pod_name=None, location_id='39'):
    if pod_name is not None:
        pod = pod_lookup(pod_name)
        location_id = pod.get('location').get('id')

    # Build url
    page = 1
    wtrucks = 'true'
    wbookings = 'true'
    wstatus = 'approved'
    url = ('https://www.seattlefoodtruck.com/api/events'
           '?page={}&for_locations={}&with_active_trucks={}'
           '&include_bookings={}&with_booking_status={}').format(
                   page, location_id, wtrucks, wbookings, wstatus)

    # Reformat output
    events = requests.get(url).json().get('events')
    eventlist = []
    for event in events:
        next_trucks = {'start': event.get('start_time'),
                       'end': event.get('end_time'),
                       'trucks': []}
        for truck in event.get('bookings'):
            truck = truck.get('truck')
            single_truck = {'truck_name': truck.get('name'),
                            'truck_id': truck.get('id')}
            next_trucks.get('trucks').append(single_truck)
        eventlist.append(next_trucks)
    return eventlist

def pod_lookup(searchpod):
    url = 'https://www.seattlefoodtruck.com/api/pods'
    podlist = requests.get(url).json().get('pods')
    for pod in podlist:
        if pod.get('id') == searchpod:
            return pod
    #print(json.dumps(podlist))

def get_menu(truck_id):
    url = 'https://www.seattlefoodtruck.com/api/trucks/{}'.format(truck_id)
    menu = requests.get(url)
    if menu:
        return menu.json().get('menu_items')

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
        print(json.dumps(schedule(pod_name=args.pod)))
    else:
        print(json.dumps(schedule()))
