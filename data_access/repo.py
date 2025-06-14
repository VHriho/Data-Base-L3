from typing import List, Dict, Optional
from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError

from data_access.models import WeatherORM, PrecipitationDetailsORM
from business_logic.models import WeatherData, PrecipitationDetails

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

    def _get_or_create_precipitation_details(self, session, domain_obj: PrecipitationDetails) -> PrecipitationDetailsORM:
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
                print(f"Created new unique precipitation details (ID: {details.id}): {details.condition_text}")
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
                    raise Exception("Failed to get or create precipitation details after rollback due to concurrent creation.")
        return details

    def save_all_initial(self, domain_objects: List[WeatherData], db_config: Dict):
        session = self._get_session(db_config)
        processed_count = 0
        try:
            for domain_obj in domain_objects:

                unique_precipitation_details_orm = self._get_or_create_precipitation_details(
                    session, domain_obj.precipitation_details
                )
                weather_orm_obj = WeatherORM.from_domain_model(domain_obj)

                weather_orm_obj.precipitation_details_rel = unique_precipitation_details_orm

                session.add(weather_orm_obj)
                processed_count += 1

            session.commit()
            print(f"Successfully saved {processed_count} weather records to {db_config.get('database', 'unknown')}.")
        except Exception as e:
            session.rollback()
            print(f"Error during weather data save to {db_config.get('database', 'unknown')}: {e}")
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
            if country:
                query = query.filter(WeatherORM.country == country)
            if query_date:
                query = query.filter(func.date(WeatherORM.last_updated) == query_date)
            if location_name:
                query = query.filter(WeatherORM.location_name.ilike(f'%{location_name}%'))

            orm_results = query.all()
            return orm_results
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return []
        finally:
            session.close()
