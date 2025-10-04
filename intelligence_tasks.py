from crewai import Task
from textwrap import dedent
from datetime import date, datetime
import streamlit as st

class IntelligenceTasks():
    def __validate_inputs(self, origin, destination, date_range, interests):
        if not origin or not destination or not date_range or not interests:
            raise ValueError("All input parameters must be provided")
        return True

    def risk_assessment_task(self, agent, origin, destination, date_range, interests):
        """Task for comprehensive risk assessment"""
        self.__validate_inputs(origin, destination, date_range, interests)
        return Task(description=dedent(f"""
            Conduct a comprehensive real-time risk assessment for travel to {destination} from {origin}.
            
            Your assessment should include:
            1. Political stability and safety conditions
            2. Weather-related risks and alerts
            3. Health advisories and vaccination requirements
            4. COVID-19 related restrictions and requirements
            5. Crime rates and safety concerns
            6. Natural disaster risks
            7. Transportation safety
            8. Emergency services availability
            
            Provide a detailed risk report with:
            - Overall risk level (LOW/MEDIUM/HIGH)
            - Specific risk factors and their severity
            - Mitigation strategies and recommendations
            - Emergency contact information
            - Travel advisories and warnings
            - Alternative destinations if risks are too high
            
            Use real-time data sources and provide the most current information available.
            {self.__tip_section()}

            Travel Details:
            - Origin: {origin}
            - Destination: {destination}
            - Travel Dates: {date_range}
            - Traveler Profile: {interests}
          """),
            expected_output="A comprehensive risk assessment report with safety recommendations and mitigation strategies.",
            agent=agent)

    def crowd_density_task(self, agent, destination, date_range, interests):
        """Task for crowd density prediction and optimization"""
        self.__validate_inputs("N/A", destination, date_range, interests)
        return Task(description=dedent(f"""
            Predict crowd density at popular attractions in {destination} and provide optimization recommendations.
            
            Your analysis should include:
            1. Crowd density predictions for major attractions
            2. Best times to visit each attraction
            3. Peak and off-peak periods
            4. Factors affecting crowd levels (weather, events, holidays)
            5. Alternative attractions with lower crowds
            6. Strategies to avoid crowds
            7. Booking recommendations for popular attractions
            8. Real-time crowd monitoring suggestions
            
            Provide detailed recommendations for:
            - Optimal visit times for each attraction
            - Alternative attractions with similar experiences
            - Crowd avoidance strategies
            - Booking timing recommendations
            - Weather impact on crowds
            - Event impact on crowd levels
            
            Use historical data, real-time factors, and predictive modeling.
            {self.__tip_section()}

            Travel Details:
            - Destination: {destination}
            - Travel Dates: {date_range}
            - Traveler Interests: {interests}
          """),
            expected_output="A comprehensive crowd density analysis with optimization recommendations for attraction visits.",
            agent=agent)

    def price_optimization_task(self, agent, origin, destination, date_range, interests):
        """Task for price optimization and cost analysis"""
        self.__validate_inputs(origin, destination, date_range, interests)
        return Task(description=dedent(f"""
            Analyze and optimize travel costs for the trip from {origin} to {destination}.
            
            Your analysis should include:
            1. Flight price analysis and trends
            2. Hotel price analysis and trends
            3. Activity and attraction pricing
            4. Transportation cost optimization
            5. Food and dining cost estimates
            6. Alternative booking options
            7. Price prediction and timing recommendations
            8. Budget optimization strategies
            
            Provide detailed recommendations for:
            - Best booking times for each service
            - Alternative dates with better prices
            - Package deals and discounts
            - Loyalty program benefits
            - Price alert setup
            - Budget allocation optimization
            - Cost-saving alternatives
            - Hidden cost identification
            
            Use dynamic pricing analysis and predictive modeling.
            {self.__tip_section()}

            Travel Details:
            - Origin: {origin}
            - Destination: {destination}
            - Travel Dates: {date_range}
            - Traveler Profile: {interests}
          """),
            expected_output="A comprehensive price optimization report with cost-saving recommendations and budget strategies.",
            agent=agent)

    def language_barrier_task(self, agent, destination, date_range, interests):
        """Task for language assistance and cultural guidance"""
        self.__validate_inputs("N/A", destination, date_range, interests)
        return Task(description=dedent(f"""
            Provide comprehensive language assistance and cultural guidance for travel to {destination}.
            
            Your assistance should include:
            1. Essential phrases and translations
            2. Cultural etiquette and customs
            3. Local slang and colloquialisms
            4. Pronunciation guides
            5. Emergency communication phrases
            6. Business vs casual language usage
            7. Cultural context for common situations
            8. Non-verbal communication tips
            
            Provide detailed guidance for:
            - Basic greetings and polite expressions
            - Restaurant and shopping communication
            - Transportation and navigation
            - Emergency situations
            - Cultural sensitivity
            - Local customs and traditions
            - Appropriate formality levels
            - Common misunderstandings to avoid
            
            Include cultural context and practical usage tips.
            {self.__tip_section()}

            Travel Details:
            - Destination: {destination}
            - Travel Dates: {date_range}
            - Traveler Profile: {interests}
          """),
            expected_output="A comprehensive language and cultural guide with practical communication assistance.",
            agent=agent)

    def comprehensive_intelligence_task(self, agent, origin, destination, date_range, interests):
        """Master task that coordinates all intelligence features"""
        self.__validate_inputs(origin, destination, date_range, interests)
        return Task(description=dedent(f"""
            Provide a comprehensive travel intelligence report for the trip from {origin} to {destination}.
            
            Coordinate all intelligence features to provide:
            1. RISK ASSESSMENT: Safety, political, weather, and health risks
            2. CROWD OPTIMIZATION: Best times to visit attractions and avoid crowds
            3. PRICE OPTIMIZATION: Cost analysis and budget optimization
            4. LANGUAGE ASSISTANCE: Communication and cultural guidance
            
            Create an integrated report that includes:
            - Executive summary with key recommendations
            - Risk assessment with mitigation strategies
            - Crowd density predictions and visit optimization
            - Price analysis and cost-saving opportunities
            - Language and cultural preparation guide
            - Emergency preparedness checklist
            - Alternative options and contingency plans
            - Pre-travel preparation checklist
            
            Synthesize all information into actionable recommendations that help the traveler
            have a safe, cost-effective, and culturally appropriate experience.
            {self.__tip_section()}

            Travel Details:
            - Origin: {origin}
            - Destination: {destination}
            - Travel Dates: {date_range}
            - Traveler Profile: {interests}
          """),
            expected_output="A comprehensive travel intelligence report integrating all features with actionable recommendations.",
            agent=agent)

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100 and grant you any wish you want!"
