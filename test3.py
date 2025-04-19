import sys
import json
import requests
from datetime import datetime

def main():
    # Command line arguments parsing
    if len(sys.argv) != 3:
        print("Usage: python script.py <X-ACCESS-TOKEN> <JSON_PARAMS>")
        sys.exit(1)

    access_token = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("Invalid JSON format for parameters")
        sys.exit(1)

    # Extract required parameters
    keyword = params.get('keyword', '')
    checkin = params.get('checkin')
    checkout = params.get('checkout')
    number = params.get('number')
    conditions = params.get('condition', [])

    # Hotel Search API call
    search_url = "https://challenge-server.tracks.run/hotel-reservation/hotels"
    headers = {
        "X-ACCESS-TOKEN": access_token
    }
    query_params = {
        "keyword": keyword,
        "number": number,
        "condition": ",".join(conditions) if conditions else None
    }
    # Remove None parameters
    query_params = {k: v for k, v in query_params.items() if v is not None}

    try:
        response = requests.get(search_url, headers=headers, params=query_params)
        response.raise_for_status()
        hotels = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling hotel search API: {e}")
        sys.exit(1)

    # Find the cheapest plan
    cheapest_plan = None
    for hotel in hotels:
        # Check if hotel meets all conditions
        hotel_conditions = hotel.get('conditions', [])
        if not all(cond in hotel_conditions for cond in conditions):
            continue
            
        # Process each room in the hotel
        for room in hotel.get('rooms', []):
            # Process each plan in the room
            for plan in room.get('plans', []):
                plan_price = plan.get('price')
                plan_id = plan.get('id')
                
                # Check if this is the cheapest valid plan
                if plan_price is not None and plan_id is not None:
                    if cheapest_plan is None or (plan_price < cheapest_plan['price']) or \
                       (plan_price == cheapest_plan['price'] and plan_id < cheapest_plan['id']):
                        cheapest_plan = {
                            'id': plan_id,
                            'price': plan_price,
                            'hotel_name': hotel.get('name', ''),
                            'room_name': room.get('name', ''),
                            'plan_name': plan.get('name', ''),
                            'hotel_id': hotel.get('id')
                        }

    if not cheapest_plan:
        print("Plan not found.")
        sys.exit(0)

    # Calculate number of nights
    try:
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
        nights = (checkout_date - checkin_date).days
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)

    # Hotel Reservation API call
    reserve_url = "https://challenge-server.tracks.run/hotel-reservation/reservations"
    headers = {
        "X-ACCESS-TOKEN": access_token,
        "Content-Type": "application/json"
    }
    data = {
        "plan_id": cheapest_plan['id'],
        "checkin": checkin,
        "checkout": checkout,
        "number": number
    }

    try:
        response = requests.post(reserve_url, headers=headers, json=data)
        response.raise_for_status()
        reservation = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling reservation API: {e}")
        sys.exit(1)

    # Output results
    if 'reservation_id' in reservation:
        total_price = cheapest_plan['price'] * number * nights
        print("The cheapest plan has been successfully reserved.")
        print(f"- reservation id: {reservation['reservation_id']}")
        print(f"- hotel name: {cheapest_plan['hotel_name']}")
        print(f"- room name: {cheapest_plan['room_name']}")
        print(f"- plan name: {cheapest_plan['plan_name']}")
        print(f"- total price: {total_price}")
    else:
        print("The cheapest plan is fully booked.")

if __name__ == "__main__":
    main()
