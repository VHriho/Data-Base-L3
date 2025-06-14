import datetime
from business_logic.services import WeatherService
from data_access.repo import WeatherRepository

def run_interface(service: WeatherService, db_config: dict):
    print("\n--- Interface for obtaining weather information ---")

    while True:
        country = input("Enter country or 'exit' to exit: ").strip()
        if country.lower() == 'exit':
            break

        date_str = input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            query_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please try again.")
            continue

        location_name = input("Enter the name of the area (leave blank to search nationwide): ").strip()

        print(f"\nWeather search for {country} on {query_date}")
        if location_name:
            print(f"in the area '{location_name}':")
        else:
            print("throughout the country:")

        try:
            weather_records = service.get_weather_data_by_params(
                country=country,
                query_date=query_date,
                db_config=db_config,
                location_name=location_name if location_name else None
            )

            if weather_records:
                print("\nWeather information found:")
                for record in weather_records:
                    print(f"  Location: {record.location_name}, "
                          f"UPD: {record.last_updated.strftime('%Y-%m-%d %H:%M')}, "
                          f"Temperature: {record.temperature_celsius}°C, "
                          f"Conditions: {record.precipitation_details.condition_text}, "
                          f"Wind: {record.wind_kph} km/h, "
                          f"Feels like: {record.feels_like_celsius}°C, "
                          f"UV-index: {record.uv_index}, "
                          f"Sunrise: {record.sunrise}, "
                          f"Sunset: {record.sunset}, "
                          f"Should go outside?: {'YES' if record.precipitation_details.should_go_outside else 'NO'}")
                print("-" * 30)
            else:
                print("Weather information not found for the specified parameters.")
                print("-" * 30)
        except Exception as e:
            print(f"Error while retrieving data: {e}")