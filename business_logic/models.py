from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass
class PrecipitationDetails:
    condition_text: str
    precip_mm: float
    humidity: int
    cloud: int
    should_go_outside: bool

@dataclass
class WeatherData:
    country: str
    location_name: str
    last_updated: datetime
    temperature_celsius: float
    wind_kph: float
    wind_degree: int
    wind_direction: str
    feels_like_celsius: float
    visibility_km: float
    uv_index: float
    sunrise: str
    sunset: str
    precipitation_details: PrecipitationDetails

    @classmethod
    def from_csv_row(cls, row_data: Dict[str, Any]):
        try:
            _last_updated = row_data.get('last_updated')
            if isinstance(_last_updated, str):
                _last_updated = datetime.strptime(_last_updated, '%Y-%m-%d %H:%M')
            elif not isinstance(_last_updated, datetime):
                raise ValueError(f"Invalid date/time format for last_updated: {_last_updated}")
            
            precipitation_details_obj = PrecipitationDetails(
                condition_text=row_data.get('condition_text', ''),
                precip_mm=float(row_data.get('precip_mm', 0.0)),
                humidity=int(row_data.get('humidity', 0)),
                cloud=int(row_data.get('cloud', 0)),
                should_go_outside=bool(row_data.get('should_go_outside', False))
            )
            return cls(
                country=row_data.get('country', ''),
                location_name=row_data.get('location_name', ''),
                last_updated=_last_updated,
                temperature_celsius=float(row_data.get('temperature_celsius', 0.0)),
                wind_kph=float(row_data.get('wind_kph', 0.0)),
                wind_degree=int(row_data.get('wind_degree', 0)),
                wind_direction=row_data.get('wind_direction', ''),
                feels_like_celsius=float(row_data.get('feels_like_celsius', 0.0)),
                visibility_km=float(row_data.get('visibility_km', 0.0)),
                uv_index=float(row_data.get('uv_index', 0.0)),
                sunrise=row_data.get('sunrise', ''),
                sunset=row_data.get('sunset', ''),
                precipitation_details=precipitation_details_obj 
            )
        
        except (ValueError, TypeError) as e:
            raise ValueError(f"CSV data conversion error for WeatherData: {row_data} - {e}")