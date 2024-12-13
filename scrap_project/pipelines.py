import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

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

class PostgresPipeline:
    def open_spider(self, spider):
        # PostgreSQL connection via SQLAlchemy
        self.engine = create_engine('postgresql://user:password@postgres/scrapydb')
        Base.metadata.create_all(self.engine)  # Automatically create the table
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Ensure the images directory exists
        if not os.path.exists('images'):
            os.makedirs('images')

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # Download and save image to local directory
        img_url = item['image']
        img_name = os.path.basename(img_url)
        img_path = os.path.join('images', img_name)

        if img_url:
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as f:
                f.write(img_data)

        # Save item to PostgreSQL
        hotel = Hotel(
            city_id=item['city_id'],
            hotel_id=item['hotel_id'],
            city_name=item['city_name'],
            title=item['title'],
            price=item['price'],
            rating=item['rating'],
            room_type=item['room_type'],
            location=item['Location'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            image=img_name,  # Store the image file name in the database
        )

        self.session.add(hotel)
        return item
