# API Documentation

**start API** `./startup.sh`

### GET Requests

#### Get All Stations
- **URL:** `http://0.0.0.0:8000/api/stations`
- **Method:** `GET`
- **Description:** Retrieve all stations.

#### Get Station by ID
- **URL:** `http://0.0.0.0:8000/api/station/333`
- **Method:** `GET`
- **Description:** Retrieve a station by its ID.

#### Get Stations by Name
- **URL:** `http://0.0.0.0:8000/api/stations/teurastamo`
- **Method:** `GET`
- **Description:** Retrieve stations by name.

### POST Request

#### Create a New Station
- **URL:** `http://0.0.0.0:8000/api/stations`
- **Method:** `POST`
- **Description:** Create a new station.
- **Request Body:**
  ```json
  {
      "Adress": "123 Main St",
      "FID": 123231,
      "Kapasiteet": 20,
      "Kaupunki": "Helsinki",
      "Kuva": "http://example.com/image.jpg",
      "Name": "Cental Station 1",
      "Namn": "Huvudstation 1",
      "Nimi": "Cityn keskusasema",
      "Operaattor": "City Bikes",
      "Osoite": "123 Main St",
      "Stad": "Helsinki",
      "x": 27.93545,
      "y": 62.16952
  }

#### PUT Request
#### Update an Existing Station

- **URL** `http://0.0.0.0:8000/api/station/6656`
- **Method** `PUT`
- **Description** Update an existing station.
- **Request Body**
  ```json
  {
      "Adress": "123 Main St",
      "FID": 123231,
      "Kapasiteet": 20,
      "Kaupunki": "Helsinki",
      "Kuva": "http://example.com/image.jpg",
      "Name": "Cental Station 1 Update",
      "Namn": "Huvudstation 1 Update",
      "Nimi": "Cityn keskusasema Updated",
      "Operaattor": "City Bikes",
      "Osoite": "123 Main St",
      "Stad": "Helsinki",
      "x": 27.93545,
      "y": 62.16952
  }

### DELETE Request

#### Delete a Station

- **URL** `http://0.0.0.0:8000/api/station/6657`
- **Method** `DELETE`
- **Description** Delete a station by its ID.

