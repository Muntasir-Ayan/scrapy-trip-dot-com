import pytest
from scrapy.http import Request, Response
from scrap_project.middlewares import ScrapProjectSpiderMiddleware, ScrapProjectDownloaderMiddleware

@pytest.fixture
def spider_middleware():
    return ScrapProjectSpiderMiddleware()

@pytest.fixture
def downloader_middleware():
    return ScrapProjectDownloaderMiddleware()

def test_spider_middleware_process_spider_input(spider_middleware):
    # Test if process_spider_input returns None correctly
    response = Response(url="https://example.com")
    assert spider_middleware.process_spider_input(response, None) is None

def test_spider_middleware_process_spider_output(spider_middleware):
    # Test process_spider_output correctly returns the result
    response = Response(url="https://example.com")
    result = [Request(url="https://example.com/page1"), Request(url="https://example.com/page2")]
    processed = list(spider_middleware.process_spider_output(response, result, None))
    assert len(processed) == 2

def test_spider_middleware_process_start_requests(spider_middleware):
    # Test process_start_requests with start_requests
    start_requests = [Request(url="https://example.com/page1"), Request(url="https://example.com/page2")]
    processed = list(spider_middleware.process_start_requests(start_requests, None))
    assert len(processed) == 2

def test_downloader_middleware_process_request(downloader_middleware):
    # Test if process_request correctly returns None
    request = Request(url="https://example.com")
    assert downloader_middleware.process_request(request, None) is None

def test_downloader_middleware_process_response(downloader_middleware):
    # Test if process_response correctly returns the response
    response = Response(url="https://example.com")
    request = Request(url="https://example.com")
    assert downloader_middleware.process_response(request, response, None) == response

def test_downloader_middleware_process_exception(downloader_middleware):
    # Test if process_exception correctly returns None
    request = Request(url="https://example.com")
    exception = Exception("Test exception")
    assert downloader_middleware.process_exception(request, exception, None) is None
