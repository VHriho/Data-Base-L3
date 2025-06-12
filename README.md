# Data Base Migrations Project
A Layered Architecture style program that describes the database structure using an ORM model. File reading and refactoring-migration of the weather database.
```text
business_logic/                     # Core business logic and domain models
├── models.py                       # Defines the core domain models
└── services.py                     # Contains business services that orchestrate operations, interact with repositories, and apply business rules.
data_access/                        # Handles all data persistence operations
├── csv_reader.py                   # Utility for reading and parsing data from CSV files.
├── models.py                       # Defines SQLAlchemy ORM models, mapping database tables to Python objects.
└── repo.py                         # Contains repository implementations for interacting with the database.
presentation/                       # User interface or API layer
└── interface.py                    # Contains the main entry point for user interaction or API definitions.
flyway/                             # Database migration management
├── mysql_migrations/               # Flyway configuration and SQL scripts specifically for MySQL.
│   ├── V1__initial_schema.sql      # Initial schema creation script for MySQL.
│   └── flyway.conf                 # Flyway configuration for MySQL database connection.
└── pg_migrations/                  # Flyway configuration and SQL scripts specifically for PostgreSQL.
│   ├── V1__initial_schema.sql      # Initial schema creation script for PostgreSQL.
│   └── flyway.conf                 # Flyway configuration for PostgreSQL database connection.
GlobalWeatherRepository.csv         # Data source in CSV format.
main.ipynb                          # Jupyter Notebook for interactive development, testing, and execution.
config.py                           # Centralized configuration for database connections and other settings.
