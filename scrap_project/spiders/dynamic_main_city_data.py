import scrapy
import json
import re
import random
import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    hotel_id = Column(Integer)
    city_name = Column(String)
    title = Column(String)
    price = Column(String)
    rating = Column(String)
    room_type = Column(String)
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    image = Column(String)

class ScraperSpider(scrapy.Spider):
    name = "dynamic_main_city_data"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log("Found script containing `window.IBU_HOTEL` data.")
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)
            if match:
                try:
                    json_string = match.group(1)
                    data = json.loads(json_string)

                    htls_data = data.get("initData", {}).get("htlsData", {})
                    if htls_data:
                        inside_outside = ['inboundCities', 'outboundCities']
                        inbound_cities = htls_data.get(random.choice(inside_outside), [])
                        if inbound_cities:
                            city = random.choice(inbound_cities)
                            city_id = city.get("id")
                            city_url = f"https://uk.trip.com/hotels/list?city={city_id}"

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
        city = response.meta['city']
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log(f"Found script containing hotel list data for city {city.get('name')}.")
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)
            if match:
                try:
                    json_string = match.group(1)
                    data = json.loads(json_string)

                    hotel_list = data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])
                    if hotel_list:
                        for hotel in hotel_list:
                            hotel_basic_info = hotel.get("hotelBasicInfo", {})
                            comment_info = hotel.get("commentInfo", {})
                            room_info = hotel.get("roomInfo", {})
                            position_info = hotel.get("positionInfo", {})

                            img_url = hotel_basic_info.get("hotelImg")
                            img_name = os.path.basename(img_url)
                            img_path = os.path.join('images', img_name)

                            # Download and save the image locally
                            if img_url:
                                img_data = requests.get(img_url).content
                                with open(img_path, 'wb') as f:
                                    f.write(img_data)

                            yield {
                                "city_id": city.get("id"),
                                "hotel_id": hotel_basic_info.get("hotelId"),
                                "city_name": city.get("name"),
                                "title": hotel_basic_info.get("hotelName"),
                                "price": hotel_basic_info.get("price"),
                                "rating": comment_info.get("commentScore"),
                                "room_type": room_info.get("physicalRoomName"),
                                "Location": position_info.get("positionName"),
                                "latitude": position_info.get("coordinate", {}).get("lat"),
                                "longitude": position_info.get("coordinate", {}).get("lng"),
                                "image": img_name,  # Store the image file name in the database
                            }
                    else:
                        self.logger.error("No 'hotelList' found in 'firstPageList'.")
                except Exception as e:
                    self.log(f"Error parsing JSON data from city page: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data on city page.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found on city page.")
