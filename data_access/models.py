from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from business_logic.models import WeatherData

Base = declarative_base()

class PrecipitationDetailsORM(Base):

    __tablename__ = 'precipitation_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    condition_text = Column(String(255), nullable=False)
    precip_mm = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    cloud = Column(Integer, nullable=False)
    should_go_outside = Column(Boolean, nullable=False)

    weathers = relationship('WeatherORM', back_populates='precipitation_details_rel')

class WeatherORM(Base):

    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    location_name = Column(String(255), nullable=False)
    last_updated = Column(DateTime, nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(String(50))
    feels_like_celsius = Column(Float)
    visibility_km = Column(Float)
    uv_index = Column(Float)
    sunrise = Column(String(20))
    sunset = Column(String(20))

    precipitation_details_id = Column(Integer, ForeignKey('precipitation_details.id'), nullable=True)
    precipitation_details_rel = relationship('PrecipitationDetailsORM', back_populates='weathers')

    @classmethod
    def from_domain_model(cls, domain_obj: WeatherData):
        return cls(
            country=domain_obj.country,
            location_name=domain_obj.location_name,
            last_updated=domain_obj.last_updated,
            temperature_celsius=domain_obj.temperature_celsius,
            wind_kph=domain_obj.wind_kph,
            wind_degree=domain_obj.wind_degree,
            wind_direction=domain_obj.wind_direction,
            feels_like_celsius=domain_obj.feels_like_celsius,
            visibility_km=domain_obj.visibility_km,
            uv_index=domain_obj.uv_index,
            sunrise=domain_obj.sunrise,
            sunset=domain_obj.sunset,
            precipitation_details_id=None
        )
