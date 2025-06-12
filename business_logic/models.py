from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class WeatherData:
    country: str
    location_name: str
    last_updated: datetime
    temperature_celsius: float
    condition_text: str
    wind_kph: float
    wind_degree: int
    wind_direction: str
    precip_mm: float
    humidity: int
    cloud: int
    feels_like_celsius: float
    visibility_km: float
    uv_index: float
    sunrise: str
    sunset: str
    should_go_outside: Optional[bool] = None


    @classmethod
    def from_csv_row(cls, row_data: Dict[str, Any]):
        try:
            _last_updated = row_data.get('last_updated')
            if isinstance(_last_updated, str):
                _last_updated = datetime.strptime(_last_updated, '%Y-%m-%d %H:%M')
            elif not isinstance(_last_updated, datetime):
                raise ValueError(f"Invalid date/time format for last_updated: {_last_updated}")

            return cls(
                country=row_data.get('country', ''),
                location_name=row_data.get('location_name', ''),
                last_updated=_last_updated,
                temperature_celsius=float(row_data.get('temperature_celsius', 0.0)),
                condition_text=row_data.get('condition_text', ''),
                wind_kph=float(row_data.get('wind_kph', 0.0)),
                wind_degree=int(row_data.get('wind_degree', 0)),
                wind_direction=row_data.get('wind_direction', ''),
                precip_mm=float(row_data.get('precip_mm', 0.0)),
                humidity=int(row_data.get('humidity', 0)),
                cloud=int(row_data.get('cloud', 0)),
                feels_like_celsius=float(row_data.get('feels_like_celsius', 0.0)),
                visibility_km=float(row_data.get('visibility_km', 0.0)),
                uv_index=float(row_data.get('uv_index', 0.0)),
                sunrise=row_data.get('sunrise', ''),
                sunset=row_data.get('sunset', '')
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"CSV data conversion error for WeatherData: {row_data} - {e}")