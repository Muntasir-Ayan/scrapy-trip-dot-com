import pytest
from scrapy.utils.project import get_project_settings

@pytest.fixture
def settings():
    return get_project_settings()

def test_download_delay(settings):
    # Ensure that DOWNLOAD_DELAY is set to 3 as per settings
    assert settings.get('DOWNLOAD_DELAY') == 3

def test_postgres_connection(settings):
    # Ensure that the database settings are correct
    assert settings.get('POSTGRES_HOST') == 'postgres'
    assert settings.get('POSTGRES_PORT') == '5432'
    assert settings.get('POSTGRES_DBNAME') == 'scrapydb'
    assert settings.get('POSTGRES_USER') == 'user'
    assert settings.get('POSTGRES_PASSWORD') == 'password'

def test_item_pipelines(settings):
    # Check if PostgresPipeline is properly configured in ITEM_PIPELINES
    assert 'scrap_project.pipelines.PostgresPipeline' in settings.get('ITEM_PIPELINES')

def test_images_store(settings):
    # Test if the images store directory is set correctly
    assert settings.get('IMAGES_STORE') == './images'
