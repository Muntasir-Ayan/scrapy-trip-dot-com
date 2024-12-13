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
    image = Column(String)  # Store image file name

class PostgresPipeline:
    def open_spider(self, spider):
        # Database connection
        DATABASE_URL = spider.settings.get("DATABASE_URL", "postgresql://user:password@postgres/scrapydb")
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)  # Automatically create the table
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Ensure images directory exists
        self.image_dir = spider.settings.get("IMAGES_STORE", "images")
        os.makedirs(self.image_dir, exist_ok=True)

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # Download and save the image
        img_url = item.get("image")
        if img_url:
            img_name = os.path.basename(img_url)
            img_path = os.path.join(self.image_dir, img_name)
            try:
                img_data = requests.get(img_url, timeout=10).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
                item["image"] = img_name  # Store file name in the database
                spider.logger.info(f"Downloaded image: {img_name}")
            except requests.RequestException as e:
                spider.logger.error(f"Failed to download image {img_url}: {e}")
                item["image"] = None

        # Save item to the database
        hotel = Hotel(
            city_id=item["city_id"],
            hotel_id=item["hotel_id"],
            city_name=item["city_name"],
            title=item["title"],
            price=item["price"],
            rating=item["rating"],
            room_type=item["room_type"],
            location=item["Location"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            image=item["image"],  # Reference image file name
        )
        self.session.add(hotel)
        spider.logger.info(f"Added hotel to session: {hotel.title}")
        self.session.commit()  # Ensure commit for each item
        return item
