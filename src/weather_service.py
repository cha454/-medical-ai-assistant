"""
Service de météo utilisant l'API OpenWeather
Permet de récupérer les informations météorologiques d'une région
"""

import os
import requests
from datetime import datetime

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            print("⚠️ OPENWEATHER_API_KEY non configurée - Service météo désactivé")
        else:
            print("✓ Service météo OpenWeather initialisé")
    
    def is_available(self):
        """Vérifie si le service météo est disponible"""
        return self.api_key is not None
    
    def get_weather(self, city, country_code=None, units="metric", lang="fr"):
        """
        Récupère la météo actuelle pour une ville
        
        Args:
            city: Nom de la ville
            country_code: Code pays ISO (ex: FR, US, CA) - optionnel
            units: metric (Celsius) ou imperial (Fahrenheit)
            lang: Langue de la réponse (fr, en, es, etc.)
        
        Returns:
            dict: Informations météo ou None si erreur
        """
        if not self.is_available():
            return {
                "error": "Service météo non disponible",
                "message": "Clé API OpenWeather manquante"
            }
        
        try:
            # Construire la requête
            location = f"{city},{country_code}" if country_code else city
            
            params = {
                "q": location,
                "appid": self.api_key,
                "units": units,
                "lang": lang
            }
            
            # Appel API météo actuelle
            response = requests.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data, units)
            
            elif response.status_code == 404:
                return {
                    "error": "Ville non trouvée",
                    "message": f"Impossible de trouver '{city}'. Vérifiez l'orthographe."
                }
            
            elif response.status_code == 401:
                return {
                    "error": "Clé API invalide",
                    "message": "La clé API OpenWeather est invalide"
                }
            
            else:
                return {
                    "error": f"Erreur API ({response.status_code})",
                    "message": response.text
                }
        
        except requests.exceptions.Timeout:
            return {
                "error": "Timeout",
                "message": "L'API OpenWeather ne répond pas"
            }
        
        except Exception as e:
            return {
                "error": "Erreur interne",
                "message": str(e)
            }
    
    def get_forecast(self, city, country_code=None, units="metric", lang="fr", days=5):
        """
        Récupère les prévisions météo pour les prochains jours
        
        Args:
            city: Nom de la ville
            country_code: Code pays ISO - optionnel
            units: metric ou imperial
            lang: Langue de la réponse
            days: Nombre de jours (max 5 avec l'API gratuite)
        
        Returns:
            dict: Prévisions météo ou None si erreur
        """
        if not self.is_available():
            return {
                "error": "Service météo non disponible",
                "message": "Clé API OpenWeather manquante"
            }
        
        try:
            location = f"{city},{country_code}" if country_code else city
            
            params = {
                "q": location,
                "appid": self.api_key,
                "units": units,
                "lang": lang,
                "cnt": days * 8  # 8 prévisions par jour (toutes les 3h)
            }
            
            response = requests.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_data(data, units, days)
            
            elif response.status_code == 404:
                return {
                    "error": "Ville non trouvée",
                    "message": f"Impossible de trouver '{city}'"
                }
            
            else:
                return {
                    "error": f"Erreur API ({response.status_code})",
                    "message": response.text
                }
        
        except Exception as e:
            return {
                "error": "Erreur interne",
                "message": str(e)
            }
    
    def _format_weather_data(self, data, units):
        """Formate les données météo de l'API"""
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"
        
        return {
            "success": True,
            "location": {
                "city": data["name"],
                "country": data["sys"]["country"],
                "coordinates": {
                    "lat": data["coord"]["lat"],
                    "lon": data["coord"]["lon"]
                }
            },
            "current": {
                "temperature": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "temp_min": round(data["main"]["temp_min"], 1),
                "temp_max": round(data["main"]["temp_max"], 1),
                "temp_unit": temp_unit,
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "icon_url": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            },
            "wind": {
                "speed": data["wind"]["speed"],
                "speed_unit": speed_unit,
                "direction": data["wind"].get("deg", 0)
            },
            "clouds": {
                "coverage": data["clouds"]["all"]
            },
            "visibility": data.get("visibility", 0),
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
            "timestamp": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _format_forecast_data(self, data, units, days):
        """Formate les prévisions météo"""
        temp_unit = "°C" if units == "metric" else "°F"
        
        forecasts = []
        for item in data["list"][:days * 8]:
            forecasts.append({
                "datetime": item["dt_txt"],
                "temperature": round(item["main"]["temp"], 1),
                "feels_like": round(item["main"]["feels_like"], 1),
                "temp_min": round(item["main"]["temp_min"], 1),
                "temp_max": round(item["main"]["temp_max"], 1),
                "humidity": item["main"]["humidity"],
                "description": item["weather"][0]["description"].capitalize(),
                "icon": item["weather"][0]["icon"],
                "icon_url": f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
                "wind_speed": item["wind"]["speed"],
                "clouds": item["clouds"]["all"]
            })
        
        return {
            "success": True,
            "location": {
                "city": data["city"]["name"],
                "country": data["city"]["country"]
            },
            "temp_unit": temp_unit,
            "forecasts": forecasts,
            "count": len(forecasts)
        }
    
    def get_weather_summary(self, city, country_code=None, lang="fr"):
        """
        Récupère un résumé météo formaté pour l'IA
        Parfait pour intégrer dans une conversation
        """
        weather = self.get_weather(city, country_code, lang=lang)
        
        if "error" in weather:
            return f"❌ Impossible de récupérer la météo : {weather['message']}"
        
        current = weather["current"]
        location = weather["location"]
        
        summary = f"""🌤️ **Météo à {location['city']}, {location['country']}**

📍 **Actuellement :**
- 🌡️ Température : {current['temperature']}{current['temp_unit']} (ressenti {current['feels_like']}{current['temp_unit']})
- ☁️ Conditions : {current['description']}
- 💧 Humidité : {current['humidity']}%
- 💨 Vent : {weather['wind']['speed']} {weather['wind']['speed_unit']}
- 🌅 Lever du soleil : {weather['sunrise']}
- 🌇 Coucher du soleil : {weather['sunset']}

📊 **Températures :**
- Min : {current['temp_min']}{current['temp_unit']}
- Max : {current['temp_max']}{current['temp_unit']}
"""
        
        return summary

# Instance globale
weather_service = WeatherService()

# Test
if __name__ == "__main__":
    print("Test du service météo OpenWeather\n")
    
    if weather_service.is_available():
        # Test météo actuelle
        print("=== Météo actuelle à Paris ===")
        result = weather_service.get_weather("Paris", "FR")
        if "error" not in result:
            print(f"Ville : {result['location']['city']}")
            print(f"Température : {result['current']['temperature']}{result['current']['temp_unit']}")
            print(f"Conditions : {result['current']['description']}")
        else:
            print(f"Erreur : {result['message']}")
        
        print("\n=== Résumé météo ===")
        summary = weather_service.get_weather_summary("Paris", "FR")
        print(summary)
    else:
        print("Service météo non disponible - Configurez OPENWEATHER_API_KEY dans .env")
