# ETL Core Components

## Directory Structure

```
etl/
├── entities/                 # Entity-based ETL modules
│   ├── capsules/            # Capsule data ETL
│   │   ├── extract.py       # Data extraction from SpaceX API
│   │   ├── transform.py     # Data transformation logic
│   │   └── load.py          # Data loading into PostgreSQL
│   ├── company/             # Company data ETL
│   ├── cores/               # Core data ETL
│   ├── crew/                # Crew data ETL
│   ├── landpads/            # Landing pad data ETL
│   ├── launches/            # Launch data ETL
│   ├── launchpads/          # Launch pad data ETL
│   ├── payloads/            # Payload data ETL
│   ├── roadster/            # Roadster data ETL
│   ├── rockets/             # Rocket data ETL
│   ├── ships/               # Ship data ETL
│   └── starlink/            # Starlink data ETL
├── sql/                     # Database schema
│   └── create_tables.sql    # Table creation scripts
└── README.md                # This file
```

### SQL

It defines the [Star schema data model](https://en.wikipedia.org/wiki/Star_schema) to encapsulate
the `SpaceX data model`. I chose the Star schema data model because it aligns well with the
analytical needs of the platform, optimizing for fast, efficient querying and simplifying the
structure for both development and reporting. Since the goal is to enable easy exploration of SpaceX
data, the Star schema provides a clear separation between measurable events (facts) and descriptive
attributes (dimensions). **This data model is not complete** for practical reasons but covers
enough to understand how the data modeling could be.

I moved the original IDs from the SpaceX API to external_id fields in the Star schema because those
IDs are specific to the source system and don’t always fit cleanly into how we structure
relationships in a warehouse. In a Star schema, we typically generate our own surrogate keys to keep
joins efficient and to give us more control over how we handle updates or changes in the data over
time. Keeping the original API IDs as external_id just makes it easier to trace things back to the
source when needed, without letting them drive the structure of the model.

## Complete Star Schema

```
                                    ┌─────────────────┐
                                    │   dim_rocket    │
                                    └─────────────────┘
                                             ▲
                                             │ FK: rocket_id
                                             │
                                    ┌─────────────────┐
                                    │  fact_launches  │
                                    └─────────────────┘
                                             │
                                             │ FK: site_id
                                             ▼
                                    ┌─────────────────┐
                                    │ dim_launch_site │
                                    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    dim_core     │◄───┤bridge_launch_core├───►│  fact_launches  │
│                 │    │ FK: core_id     │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   dim_payload   │◄───┤bridge_launch_payload├───►│  fact_launches  │
│                 │    │ FK: payload_id  │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┘
│    dim_crew     │◄───┤bridge_launch_crew├───►│  fact_launches  │
│                 │    │ FK: crew_id     │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     dim_ship    │◄───┤bridge_launch_ship├───►│  fact_launches  │
│                 │    │ FK: ship_id     │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   dim_capsule   │◄───┤bridge_launch_capsule├───►│  fact_launches  │
│                 │    │ FK: capsule_id  │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  dim_starlink   │◄───┤bridge_launch_starlink├───►│  fact_launches  │
│                 │    │ FK: starlink_id │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   dim_failure   │◄───┤bridge_launch_failure├───►│  fact_launches  │
│                 │    │ FK: failure_id  │    │                 │
│                 │    │ FK: launch_id   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```


### Entities

It defines the `Python API extract, transform and load` for all the SpaceX entities. These APIs will
be used in the pipelines:
- with-airflow 
- without-airflow
