from typing import List, Dict, Optional
from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError

from data_access.models import WeatherORM, PrecipitationDetailsORM
from business_logic.models import WeatherData

class WeatherRepository:
    def __init__(self):
        self.engine = None
        self.Session = None
        self._current_db_config = None

    def _get_session(self, db_config: Dict):
        if not self.engine or self._current_db_config != db_config:
            if db_config['port'] == '5432':
                db_url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            elif db_config['port'] == '3306':
                db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            else: 
                raise ValueError("Wrong User port config.")
            
            self.engine = create_engine(
                db_url,
                echo=False,
                pool_recycle=3600,
                pool_pre_ping=True
            )
            self.Session = sessionmaker(bind=self.engine)
            self._current_db_config = db_config
        return self.Session()

    def _get_or_create_precipitation_details(self, session, domain_obj: WeatherData) -> PrecipitationDetailsORM:
        details = session.query(PrecipitationDetailsORM).filter_by(
            condition_text=domain_obj.condition_text,
            precip_mm=domain_obj.precip_mm,
            humidity=domain_obj.humidity,
            cloud=domain_obj.cloud,
            should_go_outside=domain_obj.should_go_outside
        ).first()

        if not details:
            details = PrecipitationDetailsORM(
                condition_text=domain_obj.condition_text,
                precip_mm=domain_obj.precip_mm,
                humidity=domain_obj.humidity,
                cloud=domain_obj.cloud,
                should_go_outside=domain_obj.should_go_outside
            )
            session.add(details)
            try:
                session.flush()
                print(f"Created new precipitation details: {details}")
            except IntegrityError:
                session.rollback()
                details = session.query(PrecipitationDetailsORM).filter_by(
                    condition_text=domain_obj.condition_text,
                    precip_mm=domain_obj.precip_mm,
                    humidity=domain_obj.humidity,
                    cloud=domain_obj.cloud,
                    should_go_outside=domain_obj.should_go_outside
                ).first()
                if not details:
                    raise Exception("Failed to get or create precipitation details after rollback.")
        return details

    def save_all_initial(self, domain_objects: List[WeatherData], db_config: Dict):
        session = self._get_session(db_config)
        processed_count = 0
        try:
            for domain_obj in domain_objects:
                precipitation_details = self._get_or_create_precipitation_details(session, domain_obj)

                orm_obj = WeatherORM.from_domain_model(domain_obj)
                orm_obj.precipitation_details_id = precipitation_details.id

                session.add(orm_obj)
                processed_count += 1

            session.commit()
            print(f"Successfully saved {processed_count} initial weather records to PostgreSQL.")
        except Exception as e:
            session.rollback()
            print(f"Error during initial weather data save to PostgreSQL: {e}")
            raise
        finally:
            session.close()

    def get_weather_by_params(
        self,
        country: str,
        query_date: date,
        db_config: Dict,
        location_name: Optional[str] = None
    ) -> List[WeatherORM]:
        session = self._get_session(db_config)
        try:
            query = session.query(WeatherORM) \
                .options(joinedload(WeatherORM.precipitation_details_rel))
            query = query.filter(WeatherORM.country == country) \
                         .filter(func.date(WeatherORM.last_updated) == query_date)
            if location_name:
                query = query.filter(WeatherORM.location_name.ilike(f'%{location_name}%'))

            orm_results = query.all()
            return orm_results
        
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return []
        finally:
            session.close()