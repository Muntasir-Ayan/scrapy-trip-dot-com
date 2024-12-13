import scrapy
import json
import re

class ScraperSpider(scrapy.Spider):
    name = "dynamic_url_cities"
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
                        inbound_cities = htls_data.get('inboundCities', [])
                        if inbound_cities:
                            self.logger.info(f'Found {len(inbound_cities)} inbound cities.')
                            # Process the first city for now
                            city = inbound_cities[0]  # Select the first city
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
                        # self.logger.info(f'Found {len(hotel_list)} hotels for city {city.get("name")}.')
                        print("-------*****------")
                        print(len(hotel_list))
                        print("-------*****------")
                        # Yield data for the city and its hotels
                        yield {
                            'city_id': city.get('id'),
                            'city_name': city.get('name'),
                            'hotel_list': hotel_list
                        }
                    else:
                        self.logger.error("No 'hotelList' found in 'firstPageList'.")
                except Exception as e:
                    self.log(f"Error parsing JSON data from city page: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data on city page.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found on city page.")
