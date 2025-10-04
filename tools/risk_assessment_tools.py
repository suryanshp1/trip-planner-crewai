import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import os

class RiskAssessmentInput(BaseModel):
    location: str = Field(..., description="The location to assess risk for")
    date_range: str = Field(..., description="The date range for travel")

class RiskAssessmentTools(BaseTool):
    name: str = "Assess travel risks and safety conditions"
    description: str = "Real-time monitoring of political situations, weather alerts, health advisories, and safety conditions"
    args_schema: type[BaseModel] = RiskAssessmentInput

    def _run(self, location: str, date_range: str) -> str:
        try:
            risk_data = {
                "location": location,
                "date_range": date_range,
                "assessment_time": datetime.now().isoformat(),
                "risks": []
            }
            
            # Weather Risk Assessment
            weather_risk = self._assess_weather_risk(location, date_range)
            if weather_risk:
                risk_data["risks"].append(weather_risk)
            
            # Political/Safety Risk Assessment
            safety_risk = self._assess_safety_risk(location)
            if safety_risk:
                risk_data["risks"].append(safety_risk)
            
            # Health Advisory Assessment
            health_risk = self._assess_health_risk(location)
            if health_risk:
                risk_data["risks"].append(health_risk)
            
            # COVID-19 Risk Assessment
            covid_risk = self._assess_covid_risk(location)
            if covid_risk:
                risk_data["risks"].append(covid_risk)
            
            # Calculate overall risk score
            overall_risk = self._calculate_overall_risk(risk_data["risks"])
            risk_data["overall_risk_score"] = overall_risk
            risk_data["risk_level"] = self._get_risk_level(overall_risk)
            
            return json.dumps(risk_data, indent=2)
            
        except Exception as e:
            return f"Error during risk assessment: {str(e)}"

    def _assess_weather_risk(self, location: str, date_range: str) -> dict:
        """Assess weather-related risks using OpenWeatherMap API"""
        try:
            # Using OpenWeatherMap API (free tier available)
            api_key = os.getenv('OPENWEATHER_API_KEY', '')
            if not api_key:
                return {
                    "type": "weather",
                    "level": "medium",
                    "message": "Weather data unavailable - API key not configured",
                    "recommendation": "Check weather forecasts manually before travel"
                }
            
            # Get current weather and forecast
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                weather_data = response.json()
                weather_id = weather_data['weather'][0]['id']
                
                # Assess risk based on weather conditions
                if weather_id < 300:  # Thunderstorm
                    return {
                        "type": "weather",
                        "level": "high",
                        "message": f"Thunderstorm conditions detected: {weather_data['weather'][0]['description']}",
                        "recommendation": "Consider postponing travel or prepare for severe weather"
                    }
                elif weather_id < 600:  # Rain/Drizzle
                    return {
                        "type": "weather",
                        "level": "low",
                        "message": f"Rainy conditions: {weather_data['weather'][0]['description']}",
                        "recommendation": "Pack rain gear and waterproof items"
                    }
                elif weather_id < 700:  # Snow
                    return {
                        "type": "weather",
                        "level": "medium",
                        "message": f"Snow conditions: {weather_data['weather'][0]['description']}",
                        "recommendation": "Check road conditions and pack warm clothing"
                    }
                else:
                    return {
                        "type": "weather",
                        "level": "low",
                        "message": f"Clear conditions: {weather_data['weather'][0]['description']}",
                        "recommendation": "Good weather for travel"
                    }
            else:
                return {
                    "type": "weather",
                    "level": "medium",
                    "message": "Weather data unavailable",
                    "recommendation": "Check weather forecasts manually"
                }
        except Exception as e:
            return {
                "type": "weather",
                "level": "medium",
                "message": f"Weather assessment error: {str(e)}",
                "recommendation": "Check weather forecasts manually"
            }

    def _assess_safety_risk(self, location: str) -> dict:
        """Assess political and safety risks using web search"""
        try:
            # Search for recent safety information
            search_query = f"{location} safety travel advisory 2024"
            
            # Use existing search tool
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Analyze search results for safety keywords
            safety_keywords = ['warning', 'advisory', 'danger', 'unsafe', 'avoid', 'caution']
            risk_indicators = sum(1 for keyword in safety_keywords if keyword.lower() in search_results.lower())
            
            if risk_indicators > 3:
                return {
                    "type": "safety",
                    "level": "high",
                    "message": "Multiple safety concerns detected in recent reports",
                    "recommendation": "Review travel advisories and consider alternative destinations"
                }
            elif risk_indicators > 1:
                return {
                    "type": "safety",
                    "level": "medium",
                    "message": "Some safety concerns detected",
                    "recommendation": "Stay informed about local conditions and follow safety guidelines"
                }
            else:
                return {
                    "type": "safety",
                    "level": "low",
                    "message": "No major safety concerns detected",
                    "recommendation": "Standard travel precautions recommended"
                }
        except Exception as e:
            return {
                "type": "safety",
                "level": "medium",
                "message": f"Safety assessment error: {str(e)}",
                "recommendation": "Check official travel advisories"
            }

    def _assess_health_risk(self, location: str) -> dict:
        """Assess health-related risks"""
        try:
            # Search for health advisories
            search_query = f"{location} health advisory travel vaccination requirements 2024"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Check for health-related keywords
            health_keywords = ['vaccination', 'required', 'mandatory', 'outbreak', 'disease', 'health warning']
            health_indicators = sum(1 for keyword in health_keywords if keyword.lower() in search_results.lower())
            
            if health_indicators > 2:
                return {
                    "type": "health",
                    "level": "medium",
                    "message": "Health requirements or advisories detected",
                    "recommendation": "Check vaccination requirements and health advisories"
                }
            else:
                return {
                    "type": "health",
                    "level": "low",
                    "message": "No major health concerns detected",
                    "recommendation": "Standard health precautions recommended"
                }
        except Exception as e:
            return {
                "type": "health",
                "level": "low",
                "message": f"Health assessment error: {str(e)}",
                "recommendation": "Check official health advisories"
            }

    def _assess_covid_risk(self, location: str) -> dict:
        """Assess COVID-19 related risks"""
        try:
            search_query = f"{location} COVID-19 travel restrictions requirements 2024"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            covid_keywords = ['covid', 'pandemic', 'restrictions', 'quarantine', 'testing', 'vaccination']
            covid_indicators = sum(1 for keyword in covid_keywords if keyword.lower() in search_results.lower())
            
            if covid_indicators > 2:
                return {
                    "type": "covid",
                    "level": "medium",
                    "message": "COVID-19 related requirements detected",
                    "recommendation": "Check current COVID-19 travel requirements and restrictions"
                }
            else:
                return {
                    "type": "covid",
                    "level": "low",
                    "message": "No major COVID-19 restrictions detected",
                    "recommendation": "Standard COVID-19 precautions recommended"
                }
        except Exception as e:
            return {
                "type": "covid",
                "level": "low",
                "message": f"COVID-19 assessment error: {str(e)}",
                "recommendation": "Check official COVID-19 travel guidelines"
            }

    def _calculate_overall_risk(self, risks: list) -> float:
        """Calculate overall risk score (0-100)"""
        if not risks:
            return 0.0
        
        risk_weights = {"low": 1, "medium": 2, "high": 3}
        total_weight = sum(risk_weights.get(risk.get("level", "low"), 1) for risk in risks)
        max_possible = len(risks) * 3
        return (total_weight / max_possible) * 100 if max_possible > 0 else 0

    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to risk level"""
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    async def _arun(self, location: str, date_range: str) -> str:
        raise NotImplementedError("Async not implemented")
