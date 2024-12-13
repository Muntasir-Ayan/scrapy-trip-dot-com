import scrapy
import json
import re

class ScraperSpider(scrapy.Spider):
    name = "dynamic_cities"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract script containing data
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log("Found script containing `window.IBU_HOTEL` data.")

            # Fractional searching using regex to extract JSON-like data
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)

            if match:
                try:
                    json_string = match.group(1)  # Extract matched JSON-like data
                    data = json.loads(json_string)  # Parse JSON string into a Python dictionary
                    
                    # Extract `htlsData` information
                    htls_data = data.get("initData", {}).get("htlsData", {})
                    if htls_data:
                        # Extract the inboundCities data from htlsData
                        inbound_cities = htls_data.get('inboundCities', [])
                        
                        if inbound_cities:
                            self.logger.info(f'Found {len(inbound_cities)} inbound cities.')
                            # Only fetch data for the first city in the list
                            city = inbound_cities[0]  # Select the first city
                            city_id = city.get("id")
                            city_url = f"https://uk.trip.com/hotels/list?city={city_id}"

                            # Make a request for the first city's page
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
        # Extract the city data from the response (e.g., title, hotels, etc.)
        city = response.meta['city']  # Get the city object from meta

        # You can then extract other details about the city, such as hotel listings, etc.
        # Example: Extracting city name from the page title (adjust as per actual page structure)
        city_name = response.xpath("//title/text()").get()
        
        # Example: You could extract hotel information here (modify with correct selectors)
        hotels = response.xpath("//div[contains(@class, 'hotel-list-item')]").getall()

        self.logger.info(f"Data for city: {city_name}")

        # Yield city data, along with hotels or any other information
        yield {
            'city_id': city.get('id'),
            'city_name': city.get('name'),
            'hotels': hotels
        }
