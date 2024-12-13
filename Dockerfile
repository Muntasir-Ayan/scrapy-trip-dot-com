# Use Python 3.9 image
FROM python:3.9-slim

# Set work directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Scrapy project into the container
COPY . /app/

# Set the default command to run Scrapy crawl
CMD ["scrapy", "crawl", "scraper"]