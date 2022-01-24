# stunning-octo-doodle-ncap

A simple web API for NHTSA NCAP rollover stability measurements. A short
exercise in writing a RESTful APIs.

## NHTSA NCAP rollover stability measurements

In the interest of road safety, the US National Highway Transportation Safety
Administration's (NHTSA) New Car Assessment Program (NCAP) includes a
measurement of a vehicle's mass properties to assess its resistance to rolling
over. Vehicle measurements are published annually and made available in the
public domain.

### Measured properties

In simplistic terms, a road vehicle can be thought of as a large rigid body.
The properties of this rigid body are correlated with the vehicle's rollover
stability.

- Track width: the distance between the left and right wheel, measured per axle
- Wheelbase: the distance between the front and rear wheels
- Weight: the total weight of the vehicle
- Centre-of-gravity: the location which the vehicle rigid body can be reduced to a point mass in a simplification
  - Longitudinal position: the distance of the centre of gravity longitudinally behind the front axle
  - Lateral position: the distance of the centre of gravity laterally relative the vehicle centre plane
  - Height: the distance of the centre of gravity above the road plane

Two interesting metrics can be derived from these measurements.

- Static Stability Factor (SSF): a measure of the vehicle's ability to resist rollover. It is computed as T/2h.
  - A larger number indicates a higher intrinsic resistance to rollover
- Weight distribution: the percentage of weight over the front axle
  - An interesting metric from a dynamics and handling perspective

### User Stories

For the purpose of this exercise, we define plausible user stories for the API.

As an analyst, I need to be able to programmatically query the result of the
NHTSA NCAP rollover stability measurements because I want to develop
visualizations to understand trends in rollover stability.

As a test operator, I need a way to save the results of a vehicle measurement
because they will be referred upon and distributed for public consumption.

## Getting Started

### Starting up for the first time

Bring up Docker containers

```bash
make docker-up
```

**NOTE**: While the `web` containers depend on `database`, the `database`
container may not be ready by the time. If this happens, you may need to start
and stop the containers to try again.

```bash
# No wait-for-it.sh :(
make docker-stop
make docker-start
```

Run the database migrations

```bash
make migrate
```

Populate the database with data

```bash
make db-populate
```

Rebuild the Docker images

```bash
make build
```

Tear everything down

```bash
make docker-down
```

### Development and testing

The app uses the local environment for development and testing. The following
version of Python was used during development.

```
Python 3.10.1 (main, Dec 18 2021, 23:53:45) [GCC 11.1.0] on linux
```

Start by making virtual environment.

```bash
python -m venv env
source env/bin/activate
```

or

```bash
virtualenv env
source env/bin/activate
```

Install development packages

```bash
pip install -r requirements/development.txt
```

Run tests

```bash
make test
```

Lint

```bash
make lint
```

## API Reference

The app is shipped with `DEBUG=True`. The API can be exercised in-browser using
the Django REST framework front-end. http://localhost:8000/api/vehicles/

### List

Lists vehicles in the database. This view is paginated to 100 vehicles per
page. Returns a list of JSON objects.

`GET /api/vehicles/`

Query parameters

- `order_by`: str, sort by attribute.
  - **Valid attributes**: `"id"`
- `descending`: bool, sort in descending order
- `page`: int, the page number for pagination

Example:

```
$ curl http://localhost:8000/api/vehicles/?order_by=id&descending=True

[
    {
        "id": 52,
        "ncap_year": 2004,
        "model_year": 2005,
        "make": "Scion",
        "model": "XA",
        "drivetrain": "FWD",
        "body_style": "Sedan",
        "engine_type": "1.5L I4",
        "transmission_type": "Auto",
        "front_track": 57.3,
        "rear_track": 56.2,
        "average_track": 56.7,
        "wheelbase": 93.4,
        "test_weight": 2527.3,
        "cg_long": 37.7,
        "cg_lat": -1.1,
        "cg_height": 22.58,
        "stability_factor": 1.256,
        "weight_distribution": 0.596359743
    },
    ...
    {
        "id": 1,
        "ncap_year": 2004,
        "model_year": 2003,
        "make": "Toyota",
        "model": "Tacoma XCab SR5",
        "drivetrain": "4WD",
        "body_style": "Pickup",
        "engine_type": "2.7L I4",
        "transmission_type": "Auto",
        "front_track": 59.3,
        "rear_track": 59.0,
        "average_track": 59.1,
        "wheelbase": 122.6,
        "test_weight": 3833.9,
        "cg_long": 50.5,
        "cg_lat": -1.3,
        "cg_height": 26.33,
        "stability_factor": 1.123,
        "weight_distribution": 0.588091354
    }
]
```

### Get

Get a vehicle by id. Returns a JSON object.

`GET /api/vehicles/<id>`

Where:

- `id`: int, the id of the vehicle

Example:

```
$ curl http://localhost:8000/api/vehicles/32/
{
    "id": 32,
    "ncap_year": 2004,
    "model_year": 2004,
    "make": "Hyundai",
    "model": "Tiburon",
    "drivetrain": "FWD",
    "body_style": "Sedan",
    "engine_type": "2.0L I4",
    "transmission_type": "Auto",
    "front_track": 58.7,
    "rear_track": 58.5,
    "average_track": 58.6,
    "wheelbase": 99.7,
    "test_weight": 3233.9,
    "cg_long": 38.2,
    "cg_lat": -1.1,
    "cg_height": 20.57,
    "stability_factor": 1.424,
    "weight_distribution": 0.6168505517
}
```

### Create

Create a vehicle with the specified attributes. Accepts a JSON payload. Returns
a JSON object.

`POST /api/vehicles/`

Payload:

- `ncap_year`: int, year the measurement was reported as part of NCAP
- `model_year`: int, model year of the vehicle
- `make`: str, vehicle manufacturer name
- `model`: str, vehicle model name
- `drivetrain`: str, vehicle drivetrain type
  - **Valid options**: AWD, FWD, RWD, 4WD
- `body_style`: str, vehicle body style
  - **Valid options**: Convertible, Hatchback, Pickup, Sedan, SUV, Van, Wagon
- `engine_type`: str, the engine size and configuration
- `transmission_type`: str, the transmission type
- `front_track`: number, the distance between wheels on the front axle, inches
- `rear_track`: number, the distance between wheels on the rear axle, inches
- `average_track`: number, the average distance between wheels on each axle, inches
- `wheelbase`: number, the distance between the front and rear axles, inches
- `test_weight`: number, the measured weight of the vehicle, lbs
- `cg_long`: number, the longitudinal position of the vehicle CG relative to
  the front axle, inches
- `cg_lat`: number, the lateral position of the vehicle CG relative to the
  vehicle centre plane, inches
- `cg_height`: number, the height of the vehicle CG above the ground, inches

Example:

```
$ curl \
  -X POST \
  http://localhost:8000/api/vehicles/ \
  -H "Content-Type: application/json" \
  -d \
  "
  {
    \"ncap_year\": 2005,
    \"model_year\": 2005,
    \"make\": \"Chrysler\",
    \"model\": \"PT Cruiser\",
    \"drivetrain\": \"FWD\",
    \"body_style\": \"Wagon\",
    \"engine_type\": \"2.4L I4\",
    \"transmission_type\": \"Auto\",
    \"front_track\": 58.3,
    \"rear_track\": 58.3,
    \"average_track\": 58.3,
    \"wheelbase\": 102.8,
    \"test_weight\": 3297,
    \"cg_long\": 41.6,
    \"cg_lat\": -0.7,
    \"cg_height\": 22.32
  }
  "
{
    "id": 53,
    "ncap_year": 2005,
    "model_year": 2005,
    "make": "Chrysler",
    "model": "PT Cruiser",
    "drivetrain": "FWD",
    "body_style": "Wagon",
    "engine_type": "2.4L I4",
    "transmission_type": "Auto",
    "front_track": 58.3,
    "rear_track": 58.3,
    "average_track": 58.3,
    "wheelbase": 102.8,
    "test_weight": 3297.0,
    "cg_long": 41.6,
    "cg_lat": -0.7,
    "cg_height": 22.32,
    "stability_factor": 1.3060035842293907,
    "weight_distribution": 0.5953307392996109
}
```

## Architecture

The app makes use of the Django framework using a PostgreSQL database for
persistence. Django REST Framework is used to simplify creating the API. attrs
is used for data classes.

A three-tiered architecture is used to organize the app.

- **Views** handle incoming requests
- **Services** handle business logic and validation
- **Repositories** handle access to the data provider

Additionally, domain objects are represented as **Entities** between layers.
The architecture is visualized in the figure below.

```
+---------------+ +---------------+ +---------------+
|               | |               | |               |
|     Views     | |   Services    | |   Repository  |
|               | |               | |               |
+---------------+ +---------------+ +---------------+
+---------------------------------------------------+
|                     Entities                      |
+---------------------------------------------------+
```

### Data modelling

Although the data provided in the NCAP Rollover Stability Measurements presents
an opportunity for normalization, the data is represented in a single `Vehicle`
table for simplicity.

Note that the attributes `stability_factor` and `weight_distribution` are
derived values. They are denormalized in the database schema because these
attributes may be interesting to query against in an analysis.

### Data validation

The `attrs` library is used to define entities and includes provisions to
validate its arguments in its constructor. Validation occurs any time the
entity's constructor is called. As entities are used as an exchange datatype
between logical layers, validation will occur:

- In the service layer, when constructing an entity from arguments
- In the repository layer, when mapping the data source to the entity

## Discussion

These are items that were not explored during this exercise.

- No evaluation of alternative technologies, frameworks or persistence strategies
  - The choice of Django as the framework of choice is solely based on my
    experience with the framework
- No consideration to "design for scale"
  - The architecture of the app does not consider deployment into a production environment
  - Deployment strategy (ex. containers vs lambdas) is not considered
  - Alternative persistence strategies (ex. noSQL) and the scale of is not considered
  - Cost implications of the above are not considered
  - Performance tuning and caching are not considered
- No consideration of continuous integration
  - Although CI can be implemented via Github Actions, it is not considered in
    this exercise
- Type hints are incomplete and is not part of linting
- How the NCAP Rollover Stability Measurement structured data is obtained is
  not in scope
  - tl;dr, PDF text is obtained (from the PDF directly, or via OCR) and is hand
    formatted into a CSV-like structure
- Endpoints to support analysis of the (ex. mean, median, percentiles) are not
  implemented due to time constraints
  - The scope of the app is limited to simple operations (list, view, and create)
- The list endpoint does not return the count of vehicles or the number of
  pages to the client
