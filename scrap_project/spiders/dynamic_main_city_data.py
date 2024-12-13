import scrapy
import json
import re
import random

class ScraperSpider(scrapy.Spider):
    name = "dynamic_main_city_data"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract script containing data
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log("Found script containing `window.IBU_HOTEL` data.")

            # Extract JSON-like data using regex
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)
            if match:
                try:
                    json_string = match.group(1)  # Extract JSON-like string
                    data = json.loads(json_string)  # Parse JSON string into Python dictionary

                    
                    # Extract `htlsData` information
                    htls_data = data.get("initData", {}).get("htlsData", {})
                    if htls_data:
                        # Extract inboundCities from `htlsData`
                        inside_outside = ['inboundCities','outboundCities']
                        inbound_cities = htls_data.get(random.choice(inside_outside), [])
                        if inbound_cities:
                            self.logger.info(f'Found {len(inbound_cities)} inbound cities.')
                            # Process the first city for now
                            city = random.choice(inbound_cities)  # Select the first city
                            city_id = city.get("id")
                            city_url = f"https://uk.trip.com/hotels/list?city={city_id}"

                            # Log selected city
                            self.logger.info(f"Fetching data for city: {city.get('name')} (ID: {city_id})")
                            
                            # Make a request to fetch city data
                            yield scrapy.Request(city_url, callback=self.parse_city_data, meta={'city': city})
                        else:
                            self.logger.error("No 'inboundCities' found in 'htlsData'.")
                    else:
                        self.logger.error("No 'htlsData' found in 'initData'.")
                except Exception as e:
                    self.log(f"Error parsing JSON data: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found.")

    def parse_city_data(self, response):
        # Extract the city object from meta
        city = response.meta['city']

        # Extract script containing hotel list data
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log(f"Found script containing hotel list data for city {city.get('name')}.")

            # Use regex to extract JSON-like data
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)
            if match:
                try:
                    json_string = match.group(1)  # Extract matched JSON string
                    data = json.loads(json_string)  # Parse JSON string into Python dictionary

                    # Extract `hotelList` information
                    hotel_list = data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])
                    if hotel_list:
                        self.logger.info(f'Found {len(hotel_list)} hotels for city {city.get("name")}.')

                        # Iterate through the hotel list to extract and yield required data
                    for hotel in hotel_list:
                        hotel_basic_info = hotel.get("hotelBasicInfo", {})
                        comment_info = hotel.get("commentInfo", {})
                        room_info = hotel.get("roomInfo", {})
                        position_info = hotel.get("positionInfo", {})
                        

                        yield {
                            "city_id": city.get("id"),
                            "hotel_id": hotel_basic_info.get("hotelId"),
                            "city_name": city.get("name"),
                            "hotel_name": hotel_basic_info.get("hotelName"),
                            "price": hotel_basic_info.get("price"),
                            "comment_score": comment_info.get("commentScore"),
                            "room_name": room_info.get("physicalRoomName"),
                            "position_name": position_info.get("positionName"),
                            "lat": position_info.get("coordinate", {}).get("lat"),
                            "lng": position_info.get("coordinate", {}).get("lng"),
                            "image": hotel_basic_info.get("hotelImg"),
                        }
                    else:
                        self.logger.error("No 'hotelList' found in 'firstPageList'.")
                except Exception as e:
                    self.log(f"Error parsing JSON data from city page: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data on city page.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found on city page.")
