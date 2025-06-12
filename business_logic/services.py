from typing import List, Dict, Optional
from datetime import date

from business_logic.models import WeatherData
from data_access.csv_reader import CSVDataReader
from data_access.repo import WeatherRepository

class WeatherService:
    def __init__(self):
        self.csv_reader = CSVDataReader()
        self.repo = WeatherRepository()

    def _calculate_should_go_outside(self, weather: WeatherData) -> bool:
        if weather.wind_kph > 20:
            return False
        if weather.temperature_celsius < 0 or weather.temperature_celsius > 35:
            return False
        
        bad_precipitation_keywords = [
            "heavy", "drizzle", "thunder"
        ]
        
        if weather.precip_mm > 0.5:
            return False

        condition_text_lower = weather.condition_text.lower()
        if any(keyword in condition_text_lower for keyword in bad_precipitation_keywords):
             return False

        if weather.visibility_km < 1:
            return False
        
        if weather.uv_index > 7:
            return False
        
        if weather.cloud > 90:
            return False

        return True 

    def load_initial_data(self, csv_file_path: str, db_config: Dict):

        print(f"Starting weather data loading from {csv_file_path} to PostgreSQL:")
        
        raw_data = self.csv_reader.read(csv_file_path)
        if not raw_data:
            print("No data to load.")
            return

        domain_objects: List[WeatherData] = []
        for row in raw_data:
            try:
                obj = WeatherData.from_csv_row(row)
                obj.should_go_outside = self._calculate_should_go_outside(obj)
                domain_objects.append(obj)
            except ValueError as e:
                print(f"Error processing CSV row: {row} - {e}.")
                continue

        if not domain_objects:
            print("No valid objects created for loading.")
            return

        self.repo.save_all_initial(domain_objects, db_config)
        print("Initial weather data load completed")

    def get_weather_data_by_params(
        self,
        country: str,
        query_date: date,
        db_config: Dict,
        location_name: Optional[str] = None) -> List[WeatherData]:
        
        orm_records = self.repo.get_weather_by_params(
            country=country,
            query_date=query_date,
            db_config=db_config,
            location_name=location_name
        )

        weather_data_list: List[WeatherData] = []
        for orm_rec in orm_records:
            precipitation_details = orm_rec.precipitation_details_rel

            weather_data_list.append(WeatherData(
                country=orm_rec.country,
                location_name=orm_rec.location_name,
                last_updated=orm_rec.last_updated,
                temperature_celsius=orm_rec.temperature_celsius,
                condition_text=precipitation_details.condition_text if precipitation_details else "N/A",
                precip_mm=precipitation_details.precip_mm if precipitation_details else 0.0,
                humidity=precipitation_details.humidity if precipitation_details else 0,
                cloud=precipitation_details.cloud if precipitation_details else 0,
                should_go_outside=precipitation_details.should_go_outside if precipitation_details else None,
                wind_kph=orm_rec.wind_kph,
                wind_degree=orm_rec.wind_degree,
                wind_direction=orm_rec.wind_direction,
                feels_like_celsius=orm_rec.feels_like_celsius,
                visibility_km=orm_rec.visibility_km,
                uv_index=orm_rec.uv_index,
                sunrise=orm_rec.sunrise,
                sunset=orm_rec.sunset
            ))
        return weather_data_list
