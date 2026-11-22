import requests
import argparse
import sys
from datetime import datetime
from typing import Dict ,Any ,Optional
import json
class WeatherAPI :
    def __init__ (self ,api_key :str ):
        self .api_key =api_key
        self .base_url ="https://api.openweathermap.org/data/2.5"
    def get_current_weather (self ,city :str ,units :str ="metric")->Optional [Dict [str ,Any ]]:
        url =f"{self .base_url }/weather"
        params ={
        "q":city ,
        "appid":self .api_key ,
        "units":units ,
        "lang":"ru"
        }
        try :
            response =requests .get (url ,params =params ,timeout =10 )
            response .raise_for_status ()
            return response .json ()
        except requests .exceptions .RequestException as e :
            print (f"Ошибка при запросе к API: {e }")
            return None
        except json .JSONDecodeError :
            print ("Ошибка при разборе ответа от API")
            return None
    def get_forecast (self ,city :str ,units :str ="metric")->Optional [Dict [str ,Any ]]:
        url =f"{self .base_url }/forecast"
        params ={
        "q":city ,
        "appid":self .api_key ,
        "units":units ,
        "lang":"ru"
        }
        try :
            response =requests .get (url ,params =params ,timeout =10 )
            response .raise_for_status ()
            return response .json ()
        except requests .exceptions .RequestException as e :
            print (f"Ошибка при запросе к API: {e }")
            return None
        except json .JSONDecodeError :
            print ("Ошибка при разборе ответа от API")
            return None
class WeatherFormatter :
    @staticmethod
    def format_current_weather (weather_data :Dict [str ,Any ])->str :
        if not weather_data :
            return "Нет данных о погоде"
        city =weather_data .get ("name","Неизвестный город")
        country =weather_data .get ("sys",{}).get ("country","")
        temp =weather_data .get ("main",{}).get ("temp",0 )
        feels_like =weather_data .get ("main",{}).get ("feels_like",0 )
        humidity =weather_data .get ("main",{}).get ("humidity",0 )
        pressure =weather_data .get ("main",{}).get ("pressure",0 )
        description =weather_data .get ("weather",[{}])[0 ].get ("description","")
        wind_speed =weather_data .get ("wind",{}).get ("speed",0 )
        weather_main =weather_data .get ("weather",[{}])[0 ].get ("main","").lower ()
        weather_emoji =WeatherFormatter ._get_weather_emoji (weather_main )
        output =f
        return output .strip ()
    @staticmethod
    def format_forecast (forecast_data :Dict [str ,Any ])->str :
        if not forecast_data :
            return "Нет данных о прогнозе"
        city =forecast_data .get ("city",{}).get ("name","Неизвестный город")
        country =forecast_data .get ("city",{}).get ("country","")
        forecasts =forecast_data .get ("list",[])[:8 ]
        output =f
        for forecast in forecasts :
            dt =datetime .fromtimestamp (forecast .get ("dt",0 ))
            temp =forecast .get ("main",{}).get ("temp",0 )
            description =forecast .get ("weather",[{}])[0 ].get ("description","")
            weather_main =forecast .get ("weather",[{}])[0 ].get ("main","").lower ()
            weather_emoji =WeatherFormatter ._get_weather_emoji (weather_main )
            output +=f"║ {dt .strftime ('%d.%m %H:%M')} {weather_emoji } {temp :.1f}°C - {description .capitalize ()}\n"
        output +="╚══════════════════════════════════════════════════════════════╝"
        return output
    @staticmethod
    def _get_weather_emoji (weather_main :str )->str :
        emoji_map ={
        "clear":"☀️",
        "clouds":"☁️",
        "rain":"🌧️",
        "drizzle":"🌦️",
        "thunderstorm":"⛈️",
        "snow":"❄️",
        "mist":"🌫️",
        "fog":"🌫️",
        "haze":"🌫️"
        }
        return emoji_map .get (weather_main ,"🌤️")
def main ():
    parser =argparse .ArgumentParser (
    description ="WeatherCLI - Получение информации о погоде через терминал",
    formatter_class =argparse .RawDescriptionHelpFormatter ,
    epilog ="""
Примеры использования:
  python weather_cli.py Москва
  python weather_cli.py "Санкт-Петербург" --forecast
  python weather_cli.py London --units imperial
        """
    )
    parser .add_argument (
    "city",
    help ="Название города для получения погоды"
    )
    parser .add_argument (
    "--forecast","-f",
    action ="store_true",
    help ="Показать прогноз погоды на ближайшие 24 часа"
    )
    parser .add_argument (
    "--units","-u",
    choices =["metric","imperial","kelvin"],
    default ="metric",
    help ="Единицы измерения температуры (по умолчанию: metric)"
    )
    parser .add_argument (
    "--api-key",
    default ="b08681bea8dc12a0892e01f22b6de693",
    help ="API ключ для OpenWeatherMap (по умолчанию используется встроенный)"
    )
    args =parser .parse_args ()
    if not args .api_key :
        print ("Ошибка: Не указан API ключ для OpenWeatherMap")
        sys .exit (1 )
    weather_api =WeatherAPI (args .api_key )
    formatter =WeatherFormatter ()
    try :
        if args .forecast :
            print (f"Получение прогноза погоды для города: {args .city }...")
            forecast_data =weather_api .get_forecast (args .city ,args .units )
            if forecast_data :
                print (formatter .format_forecast (forecast_data ))
            else :
                print ("Не удалось получить прогноз погоды. Проверьте название города.")
                sys .exit (1 )
        else :
            print (f"Получение текущей погоды для города: {args .city }...")
            weather_data =weather_api .get_current_weather (args .city ,args .units )
            if weather_data :
                print (formatter .format_current_weather (weather_data ))
            else :
                print ("Не удалось получить данные о погоде. Проверьте название города.")
                sys .exit (1 )
    except KeyboardInterrupt :
        print ("\nПрограмма прервана пользователем")
        sys .exit (0 )
    except Exception as e :
        print (f"Произошла неожиданная ошибка: {e }")
        sys .exit (1 )
if __name__ =="__main__":
    main ()