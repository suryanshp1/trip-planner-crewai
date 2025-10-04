import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional
import os

class PriceOptimizationInput(BaseModel):
    origin: str = Field(..., description="Origin location")
    destination: str = Field(..., description="Destination location")
    departure_date: str = Field(..., description="Departure date")
    return_date: str = Field(..., description="Return date (optional)")
    trip_type: str = Field(default="flight", description="Type of booking (flight, hotel, activity)")

class PriceOptimizationTools(BaseTool):
    name: str = "Optimize travel prices and find best deals"
    description: str = "Dynamic pricing alerts for flights, hotels, and activities with predictive price modeling"
    args_schema: type[BaseModel] = PriceOptimizationInput

    def _run(self, origin: str, destination: str, departure_date: str, return_date: str = None, trip_type: str = "flight") -> str:
        try:
            optimization_data = {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "trip_type": trip_type,
                "analysis_time": datetime.now().isoformat(),
                "recommendations": {}
            }
            
            if trip_type == "flight":
                flight_data = self._analyze_flight_prices(origin, destination, departure_date, return_date)
                optimization_data["recommendations"]["flight"] = flight_data
            elif trip_type == "hotel":
                hotel_data = self._analyze_hotel_prices(destination, departure_date, return_date)
                optimization_data["recommendations"]["hotel"] = hotel_data
            elif trip_type == "activity":
                activity_data = self._analyze_activity_prices(destination, departure_date)
                optimization_data["recommendations"]["activity"] = activity_data
            else:
                # Analyze all types
                optimization_data["recommendations"]["flight"] = self._analyze_flight_prices(origin, destination, departure_date, return_date)
                optimization_data["recommendations"]["hotel"] = self._analyze_hotel_prices(destination, departure_date, return_date)
                optimization_data["recommendations"]["activity"] = self._analyze_activity_prices(destination, departure_date)
            
            # Generate overall recommendations
            optimization_data["overall_recommendations"] = self._generate_overall_recommendations(optimization_data["recommendations"])
            
            return json.dumps(optimization_data, indent=2)
            
        except Exception as e:
            return f"Error during price optimization: {str(e)}"

    def _analyze_flight_prices(self, origin: str, destination: str, departure_date: str, return_date: str = None) -> Dict:
        """Analyze flight prices and provide optimization recommendations"""
        try:
            # Search for flight prices
            search_query = f"flight prices {origin} to {destination} {departure_date}"
            if return_date:
                search_query += f" return {return_date}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Extract price information (simulated)
            current_price = self._extract_price_from_search(search_results, "flight")
            
            # Predict price trends
            price_trend = self._predict_price_trend("flight", departure_date)
            
            # Find alternative dates
            alternative_dates = self._find_alternative_dates(origin, destination, departure_date, "flight")
            
            return {
                "current_price": current_price,
                "price_trend": price_trend,
                "alternative_dates": alternative_dates,
                "recommendations": self._generate_flight_recommendations(current_price, price_trend, alternative_dates)
            }
            
        except Exception as e:
            return {
                "current_price": None,
                "price_trend": "unknown",
                "alternative_dates": [],
                "error": str(e)
            }

    def _analyze_hotel_prices(self, destination: str, check_in: str, check_out: str = None) -> Dict:
        """Analyze hotel prices and provide optimization recommendations"""
        try:
            # Search for hotel prices
            search_query = f"hotel prices {destination} {check_in}"
            if check_out:
                search_query += f" to {check_out}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Extract price information
            current_price = self._extract_price_from_search(search_results, "hotel")
            
            # Predict price trends
            price_trend = self._predict_price_trend("hotel", check_in)
            
            # Find alternative dates
            alternative_dates = self._find_alternative_dates(destination, destination, check_in, "hotel")
            
            return {
                "current_price": current_price,
                "price_trend": price_trend,
                "alternative_dates": alternative_dates,
                "recommendations": self._generate_hotel_recommendations(current_price, price_trend, alternative_dates)
            }
            
        except Exception as e:
            return {
                "current_price": None,
                "price_trend": "unknown",
                "alternative_dates": [],
                "error": str(e)
            }

    def _analyze_activity_prices(self, destination: str, activity_date: str) -> Dict:
        """Analyze activity prices and provide optimization recommendations"""
        try:
            # Search for activity prices
            search_query = f"tourist activities prices {destination} {activity_date}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Extract price information
            current_price = self._extract_price_from_search(search_results, "activity")
            
            # Predict price trends
            price_trend = self._predict_price_trend("activity", activity_date)
            
            return {
                "current_price": current_price,
                "price_trend": price_trend,
                "recommendations": self._generate_activity_recommendations(current_price, price_trend)
            }
            
        except Exception as e:
            return {
                "current_price": None,
                "price_trend": "unknown",
                "error": str(e)
            }

    def _extract_price_from_search(self, search_results: str, category: str) -> Optional[Dict]:
        """Extract price information from search results"""
        try:
            # This is a simplified price extraction
            # In a real implementation, you would use more sophisticated NLP or API calls
            
            price_keywords = ['$', 'USD', 'price', 'cost', 'rate']
            prices = []
            
            for line in search_results.split('\n'):
                for keyword in price_keywords:
                    if keyword in line.lower():
                        # Extract numbers that might be prices
                        import re
                        numbers = re.findall(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', line)
                        for num in numbers:
                            try:
                                price = float(num.replace(',', ''))
                                if 10 <= price <= 10000:  # Reasonable price range
                                    prices.append(price)
                            except ValueError:
                                continue
            
            if prices:
                avg_price = sum(prices) / len(prices)
                return {
                    "average": round(avg_price, 2),
                    "min": round(min(prices), 2),
                    "max": round(max(prices), 2),
                    "currency": "USD"
                }
            else:
                return None
                
        except Exception as e:
            return None

    def _predict_price_trend(self, category: str, target_date: str) -> str:
        """Predict price trend for the given category and date"""
        try:
            target_dt = datetime.fromisoformat(target_date)
            days_ahead = (target_dt - datetime.now()).days
            
            # Simulate price trend prediction based on historical patterns
            if category == "flight":
                if days_ahead > 60:
                    return "decreasing"  # Prices usually decrease far in advance
                elif days_ahead > 30:
                    return "stable"  # Stable prices
                elif days_ahead > 14:
                    return "increasing"  # Prices increase closer to date
                else:
                    return "highly_increasing"  # Last minute prices are high
            elif category == "hotel":
                if days_ahead > 30:
                    return "stable"
                else:
                    return "increasing"
            else:  # activity
                return "stable"
                
        except Exception as e:
            return "unknown"

    def _find_alternative_dates(self, origin: str, destination: str, target_date: str, category: str) -> List[Dict]:
        """Find alternative dates with better prices"""
        try:
            target_dt = datetime.fromisoformat(target_date)
            alternatives = []
            
            # Check dates within ±7 days
            for days_offset in range(-7, 8):
                if days_offset == 0:
                    continue
                    
                alt_date = target_dt + timedelta(days=days_offset)
                
                # Simulate price difference
                price_factor = 1.0
                if category == "flight":
                    if days_offset < 0:
                        price_factor = 0.9  # Earlier dates might be cheaper
                    else:
                        price_factor = 1.1  # Later dates might be more expensive
                
                alternatives.append({
                    "date": alt_date.isoformat(),
                    "price_factor": price_factor,
                    "savings_potential": "high" if price_factor < 0.95 else "medium" if price_factor < 1.05 else "low"
                })
            
            # Sort by price factor
            alternatives.sort(key=lambda x: x["price_factor"])
            
            return alternatives[:5]  # Return top 5 alternatives
            
        except Exception as e:
            return []

    def _generate_flight_recommendations(self, current_price: Optional[Dict], price_trend: str, alternative_dates: List[Dict]) -> List[str]:
        """Generate flight-specific recommendations"""
        recommendations = []
        
        if current_price:
            recommendations.append(f"Current average price: ${current_price['average']}")
        
        if price_trend == "decreasing":
            recommendations.append("Prices are trending down - consider waiting for better deals")
        elif price_trend == "increasing":
            recommendations.append("Prices are trending up - consider booking soon")
        elif price_trend == "highly_increasing":
            recommendations.append("Prices are rising rapidly - book immediately if price is acceptable")
        
        if alternative_dates:
            best_alt = alternative_dates[0]
            recommendations.append(f"Consider {best_alt['date']} for potential savings")
        
        recommendations.append("Set up price alerts for price drops")
        recommendations.append("Consider flexible dates for better deals")
        
        return recommendations

    def _generate_hotel_recommendations(self, current_price: Optional[Dict], price_trend: str, alternative_dates: List[Dict]) -> List[str]:
        """Generate hotel-specific recommendations"""
        recommendations = []
        
        if current_price:
            recommendations.append(f"Current average price: ${current_price['average']} per night")
        
        if price_trend == "increasing":
            recommendations.append("Hotel prices are rising - consider booking soon")
        
        if alternative_dates:
            best_alt = alternative_dates[0]
            recommendations.append(f"Consider checking in on {best_alt['date']} for better rates")
        
        recommendations.append("Book directly with hotels for potential discounts")
        recommendations.append("Consider alternative accommodations (Airbnb, hostels)")
        
        return recommendations

    def _generate_activity_recommendations(self, current_price: Optional[Dict], price_trend: str) -> List[str]:
        """Generate activity-specific recommendations"""
        recommendations = []
        
        if current_price:
            recommendations.append(f"Current average price: ${current_price['average']}")
        
        recommendations.append("Book activities in advance for better prices")
        recommendations.append("Look for combo deals and packages")
        recommendations.append("Consider free or low-cost alternatives")
        
        return recommendations

    def _generate_overall_recommendations(self, recommendations: Dict) -> List[str]:
        """Generate overall price optimization recommendations"""
        overall = []
        
        overall.append("🎯 PRICE OPTIMIZATION STRATEGY:")
        overall.append("1. Book flights 2-3 months in advance for best prices")
        overall.append("2. Use flexible date search to find cheaper options")
        overall.append("3. Set up price alerts for all bookings")
        overall.append("4. Consider package deals for additional savings")
        overall.append("5. Book refundable options when possible")
        
        return overall

    async def _arun(self, origin: str, destination: str, departure_date: str, return_date: str = None, trip_type: str = "flight") -> str:
        raise NotImplementedError("Async not implemented")
