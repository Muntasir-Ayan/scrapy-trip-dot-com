import scrapy
from scrapy.http import HtmlResponse, Request
from scrap_project.spiders.dynamic_main_city_data import ScraperSpider  # Assuming this is your spider's location

def test_parse(mocker):
    # Mock response with relevant script data
    html = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "htlsData": {
                "inboundCities": [{"id": 123, "name": "Test City"}],
                "outboundCities": []
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://uk.trip.com/hotels/?locale=en-GB&curr=GBP", body=html, encoding='utf-8')
    spider = ScraperSpider()

    # Call parse method
    result = list(spider.parse(response))

    # Make sure the response is parsed correctly and a request is yielded
    assert len(result) == 1  # Ensure one request is yielded
    assert result[0].url == "https://uk.trip.com/hotels/list?city=123"  # Check the URL

def test_parse_city_data(mocker):
    # Mock response with relevant script data
    html = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "firstPageList": {
                "hotelList": [
                    {
                        "hotelBasicInfo": {
                            "hotelId": 101,
                            "hotelName": "Test Hotel",
                            "price": "100 USD",
                            "hotelImg": "http://example.com/image.jpg"
                        },
                        "commentInfo": {"commentScore": "4.5"},
                        "roomInfo": {"physicalRoomName": "Deluxe"},
                        "positionInfo": {
                            "positionName": "City Center",
                            "coordinate": {"lat": "123.456", "lng": "-123.456"}
                        }
                    }
                ]
            }
        }
    };
    </script>
    """
    # Create the response
    response = HtmlResponse(url="https://uk.trip.com/hotels/list?city=123", body=html, encoding='utf-8')

    # Manually create a request with meta to pass to the spider's parse method
    request = Request(url="https://uk.trip.com/hotels/list?city=123", meta={"city": {"id": 123, "name": "Test City"}})
    
    # Pass the response with the request object
    spider = ScraperSpider()

    # Call parse_city_data method (passing response that is linked with request meta)
    result = list(spider.parse_city_data(response.replace(request=request)))

    # Ensure one item is yielded
    assert len(result) == 1
    hotel = result[0]
    assert hotel["title"] == "Test Hotel"
    assert hotel["price"] == "100 USD"
