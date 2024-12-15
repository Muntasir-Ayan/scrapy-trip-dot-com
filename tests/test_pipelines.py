import os
from unittest.mock import MagicMock, patch
from scrap_project.pipelines import PostgresPipeline, Hotel
from sqlalchemy.orm import sessionmaker

def test_pipeline_save_item(tmpdir, mocker):
    # Create a mock spider
    spider = MagicMock()
    spider.settings.get = MagicMock(side_effect=lambda key, default=None: {
        "DATABASE_URL": "sqlite:///:memory:",  # Use SQLite for testing
        "IMAGES_STORE": str(tmpdir)           # Temporary directory for images
    }.get(key, default))

    # Initialize pipeline
    pipeline = PostgresPipeline()
    pipeline.open_spider(spider)

    # Create a mock item
    item = {
        "city_id": 1,
        "hotel_id": 101,
        "city_name": "Test City",
        "title": "Test Hotel",
        "price": "100 USD",
        "rating": "4.5",
        "room_type": "Deluxe",
        "Location": "City Center",
        "latitude": "123.456",
        "longitude": "-123.456",
        "image": "http://example.com/image.jpg",
    }

    # Mock requests.get for image download
    mock_requests = mocker.patch("scrap_project.pipelines.requests.get")
    mock_requests.return_value.content = b"fake_image_data"

    # Process item
    processed_item = pipeline.process_item(item, spider)

    # Validate database entry
    session = sessionmaker(bind=pipeline.engine)()
    saved_item = session.query(Hotel).first()

    assert saved_item.city_name == "Test City"
    assert saved_item.image == "image.jpg"  # Check the stored file name
    assert os.path.exists(os.path.join(tmpdir, "image.jpg"))  # Image should be saved

    # Close pipeline
    pipeline.close_spider(spider)
