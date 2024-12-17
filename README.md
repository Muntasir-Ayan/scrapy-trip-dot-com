# Trip.com Property Scraper

A Scrapy-based web scraper that gathers property information from Trip.com, processes the data, and stores it in a PostgreSQL database. The project adheres to the following criteria:

- Extracts property data such as title, rating, location, latitude, longitude, room type, price, and images.
- Stores images in a directory and references them in a PostgreSQL database.
- Automatically creates database tables and directories.
- Includes unit tests with 80% code coverage.

---

## Features

- **Web Scraping**: Scrapes property data from Trip.com.
- **Dynamic Data Storage**: Saves data into a PostgreSQL database using SQLAlchemy.
- **Image Handling**: Stores images in a directory and maintains references in the database.
- **Automated Setup**: Automatically creates tables and directories for seamless integration.
- **Test Coverage**: Includes unit tests with at least 60% code coverage.

---

## Requirements

### System Requirements
- Python 3.10+
- PostgreSQL 13+
- Docker (for database containerization)

### Python Libraries
- Scrapy
- SQLAlchemy
- Psycopg2
- Pillow (for image handling)
- Pytest (for testing)
- Pytest-Cov (for code coverage)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Muntasir-Ayan/scrapy-trip-dot-com.git
cd scrapy-trip-dot-com
```

## Project Structure

```
.
├── scrap_project
│   ├── spiders
│   │   └── dynamic_main_city_data.py  # Main Scrapy Spider
│   ├── pipelines.py                   # Data Processing and Storage
│   ├── settings.py                    # Scrapy Settings
│   ├── items.py                       # Data Item Definitions
├── tests                              # Unit Tests
│   ├── test_spiders.py
│   ├── test_pipelines.py
├── images                             # Directory for Downloaded Images
├── requirements.txt                   # Dependencies List
├── README.md                          # Project Documentation
└── Dockerfile                         # Docker Configuration
```

---

### 2. Install Dependencies
Create a virtual environment and install the required Python libraries:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Desktop
Use Docker, Ensure Docker is running.
```bash
docker-compose up --build
```
To Stop docker
```bash
docker-compose down
```
### 4. Check Database 
Open new terminal (Docker should running)
```bash
docker exec -it scrapy-trip-dot-com-postgres-1 bash
psql -U user -d scrapydb
SELECT * FROM hotels;
```


### 6. Run Tests
To execute unit tests and check code coverage:
```bash
pytest --cov=scrap_project --cov-report=term-missing
```

---

## Data Schema

The PostgreSQL database uses the following schema:

### Table: `properties`
| Column        | Type       | Description                      |
|---------------|------------|----------------------------------|
| id            | Integer    | Primary Key                     |
| title         | String     | Property Title                  |
| rating        | Float      | Property Rating                 |
| location      | String     | Property Location               |
| latitude      | Float      | Latitude                        |
| longitude     | Float      | Longitude                       |
| room_type     | String     | Room Type                       |
| price         | String     | Property Price                  |
| image_path    | String     | Path to Stored Image            |

---
## Docker Encounter Issue
If you face any docker encounter issue, Use:
```bash
docker-compose build --no-cache
```


## Contributing

Feel free to fork the repository and submit pull requests. Make sure to write tests for any new features or changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact

For any inquiries or feedback, feel free to contact [Muntasir Ayan](mailto:mjayan439@gmail.com).
