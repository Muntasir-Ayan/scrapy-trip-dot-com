import scrapy
import json
import re

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract script containing data
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            # Debug: Log found data (optional for large scripts)
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

                        self.logger.info(f'htlsData: {json.dumps(htls_data, indent=2)[:500]}')
                        yield{
                            'data': htls_data
                        }
                        print("-------*****------")
                        print(len(htls_data))
                        print("-------*****------")
                    else:
                        self.logger.error("No 'htlsData' found in 'initData'.")
                    # for city in inbound_cities:
                    #     yield {

                    #         # 'data': inbound_cities
                    #         # "cityUrl": city.get("cityUrl"),
                    #         # "code": city.get("code"),
                    #         # "count": city.get("count"),
                    #         # "id": city.get("id"),
                    #         # "imgUrl": city.get("imgUrl"),
                    #         # "name": city.get("name"),
                    #         # "recommendHotels": city.get("recommendHotels"),
                    #     }
                except Exception as e:
                    self.log(f"Error parsing JSON data: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found.")
