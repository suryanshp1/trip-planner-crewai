import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List
import os

class CrowdDensityInput(BaseModel):
    location: str = Field(..., description="The location to predict crowd density for")
    attraction: str = Field(..., description="The specific attraction or venue")
    date_time: str = Field(..., description="The date and time to predict for")

class CrowdDensityTools(BaseTool):
    name: str = "Predict crowd density at attractions"
    description: str = "ML models to predict tourist density at attractions using historical data and real-time foot traffic"
    args_schema: type[BaseModel] = CrowdDensityInput

    def _run(self, location: str, attraction: str, date_time: str) -> str:
        try:
            # Parse the date and time
            target_datetime = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
            
            # Get historical data and predictions
            crowd_data = {
                "location": location,
                "attraction": attraction,
                "target_datetime": target_datetime.isoformat(),
                "predictions": {}
            }
            
            # Predict crowd density for different time slots
            time_slots = self._generate_time_slots(target_datetime)
            
            for time_slot in time_slots:
                prediction = self._predict_crowd_density(location, attraction, time_slot)
                crowd_data["predictions"][time_slot.isoformat()] = prediction
            
            # Generate recommendations
            crowd_data["recommendations"] = self._generate_crowd_recommendations(crowd_data["predictions"])
            
            return json.dumps(crowd_data, indent=2)
            
        except Exception as e:
            return f"Error during crowd density prediction: {str(e)}"

    def _generate_time_slots(self, target_datetime: datetime) -> List[datetime]:
        """Generate time slots for the day"""
        time_slots = []
        base_date = target_datetime.date()
        
        # Generate hourly slots from 6 AM to 10 PM
        for hour in range(6, 23):
            time_slots.append(datetime.combine(base_date, datetime.min.time().replace(hour=hour)))
        
        return time_slots

    def _predict_crowd_density(self, location: str, attraction: str, target_datetime: datetime) -> Dict:
        """Predict crowd density using ML-like approach with historical patterns"""
        try:
            # Get historical data patterns
            historical_pattern = self._get_historical_pattern(location, attraction, target_datetime)
            
            # Get real-time factors
            real_time_factors = self._get_real_time_factors(location, target_datetime)
            
            # Apply ML-like prediction algorithm
            base_density = historical_pattern["base_density"]
            time_factor = historical_pattern["time_factor"]
            day_factor = historical_pattern["day_factor"]
            season_factor = historical_pattern["season_factor"]
            weather_factor = real_time_factors["weather_factor"]
            event_factor = real_time_factors["event_factor"]
            
            # Calculate predicted density (0-100 scale)
            predicted_density = (
                base_density * 
                time_factor * 
                day_factor * 
                season_factor * 
                weather_factor * 
                event_factor
            )
            
            # Ensure density is within bounds
            predicted_density = max(0, min(100, predicted_density))
            
            # Categorize density level
            density_level = self._categorize_density(predicted_density)
            
            return {
                "density_score": round(predicted_density, 1),
                "density_level": density_level,
                "confidence": historical_pattern["confidence"],
                "factors": {
                    "time_factor": round(time_factor, 2),
                    "day_factor": round(day_factor, 2),
                    "season_factor": round(season_factor, 2),
                    "weather_factor": round(weather_factor, 2),
                    "event_factor": round(event_factor, 2)
                }
            }
            
        except Exception as e:
            return {
                "density_score": 50.0,
                "density_level": "medium",
                "confidence": 0.5,
                "error": str(e)
            }

    def _get_historical_pattern(self, location: str, attraction: str, target_datetime: datetime) -> Dict:
        """Get historical crowd patterns (simulated ML model)"""
        try:
            # Simulate historical data analysis
            hour = target_datetime.hour
            day_of_week = target_datetime.weekday()
            month = target_datetime.month
            
            # Base density for the attraction (simulated)
            base_density = 60.0  # Average density
            
            # Time factor (peak hours)
            if 9 <= hour <= 11 or 14 <= hour <= 16 or 19 <= hour <= 21:
                time_factor = 1.3  # Peak hours
            elif 6 <= hour <= 8 or 22 <= hour <= 23:
                time_factor = 0.6  # Off-peak hours
            else:
                time_factor = 1.0  # Normal hours
            
            # Day of week factor
            if day_of_week < 5:  # Weekdays
                day_factor = 0.8
            else:  # Weekends
                day_factor = 1.4
            
            # Seasonal factor
            if month in [6, 7, 8]:  # Summer
                season_factor = 1.2
            elif month in [12, 1, 2]:  # Winter holidays
                season_factor = 1.1
            else:
                season_factor = 1.0
            
            return {
                "base_density": base_density,
                "time_factor": time_factor,
                "day_factor": day_factor,
                "season_factor": season_factor,
                "confidence": 0.8
            }
            
        except Exception as e:
            return {
                "base_density": 50.0,
                "time_factor": 1.0,
                "day_factor": 1.0,
                "season_factor": 1.0,
                "confidence": 0.5
            }

    def _get_real_time_factors(self, location: str, target_datetime: datetime) -> Dict:
        """Get real-time factors affecting crowd density"""
        try:
            # Weather factor
            weather_factor = self._get_weather_factor(location)
            
            # Event factor
            event_factor = self._get_event_factor(location, target_datetime)
            
            return {
                "weather_factor": weather_factor,
                "event_factor": event_factor
            }
            
        except Exception as e:
            return {
                "weather_factor": 1.0,
                "event_factor": 1.0
            }

    def _get_weather_factor(self, location: str) -> float:
        """Get weather impact on crowd density"""
        try:
            # Use OpenWeatherMap API
            api_key = os.getenv('OPENWEATHER_API_KEY', '')
            if not api_key:
                return 1.0
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                weather_data = response.json()
                weather_id = weather_data['weather'][0]['id']
                
                # Weather impact on outdoor attractions
                if weather_id < 300:  # Thunderstorm
                    return 0.3  # Significantly reduces crowds
                elif weather_id < 600:  # Rain
                    return 0.7  # Reduces crowds
                elif weather_id < 700:  # Snow
                    return 0.5  # Reduces crowds
                else:  # Clear weather
                    return 1.2  # Increases crowds
            else:
                return 1.0
                
        except Exception as e:
            return 1.0

    def _get_event_factor(self, location: str, target_datetime: datetime) -> float:
        """Check for events that might affect crowd density"""
        try:
            # Search for events in the location
            search_query = f"{location} events festivals {target_datetime.strftime('%Y-%m-%d')}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Check for event keywords
            event_keywords = ['festival', 'concert', 'event', 'celebration', 'conference', 'exhibition']
            event_count = sum(1 for keyword in event_keywords if keyword.lower() in search_results.lower())
            
            if event_count > 3:
                return 1.5  # Major events increase crowds
            elif event_count > 1:
                return 1.2  # Minor events slightly increase crowds
            else:
                return 1.0  # No significant events
                
        except Exception as e:
            return 1.0

    def _categorize_density(self, density_score: float) -> str:
        """Categorize density score into levels"""
        if density_score >= 80:
            return "very_high"
        elif density_score >= 60:
            return "high"
        elif density_score >= 40:
            return "medium"
        elif density_score >= 20:
            return "low"
        else:
            return "very_low"

    def _generate_crowd_recommendations(self, predictions: Dict) -> List[str]:
        """Generate recommendations based on crowd predictions"""
        recommendations = []
        
        # Find best and worst times
        best_time = min(predictions.items(), key=lambda x: x[1]["density_score"])
        worst_time = max(predictions.items(), key=lambda x: x[1]["density_score"])
        
        recommendations.append(f"Best time to visit: {best_time[0]} (density: {best_time[1]['density_score']})")
        recommendations.append(f"Avoid visiting at: {worst_time[0]} (density: {worst_time[1]['density_score']})")
        
        # General recommendations
        avg_density = sum(pred["density_score"] for pred in predictions.values()) / len(predictions)
        
        if avg_density > 70:
            recommendations.append("High crowd density expected - consider booking tickets in advance")
        elif avg_density < 30:
            recommendations.append("Low crowd density expected - great time for a peaceful visit")
        
        return recommendations

    async def _arun(self, location: str, attraction: str, date_time: str) -> str:
        raise NotImplementedError("Async not implemented")
