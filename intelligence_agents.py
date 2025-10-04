from crewai import Agent
from langchain_core.language_models.chat_models import BaseChatModel
from crewai import LLM
from tools.risk_assessment_tools import RiskAssessmentTools
from tools.crowd_density_tools import CrowdDensityTools
from tools.price_optimization_tools import PriceOptimizationTools
from tools.language_barrier_tools import LanguageBarrierTools
from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools

class IntelligenceAgents():
    def __init__(self, llm: BaseChatModel = None):
        if llm is None:
            self.llm = LLM(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm

        # Initialize intelligence tools
        self.risk_assessment_tool = RiskAssessmentTools()
        self.crowd_density_tool = CrowdDensityTools()
        self.price_optimization_tool = PriceOptimizationTools()
        self.language_barrier_tool = LanguageBarrierTools()
        
        # Initialize existing tools
        self.search_tool = SearchTools()
        self.browser_tool = BrowserTools()
        self.calculator_tool = CalculatorTools()

    def risk_assessment_agent(self):
        """Agent for real-time risk assessment and safety monitoring"""
        return Agent(
            role='Travel Risk Assessment Specialist',
            goal='Provide comprehensive real-time risk assessment including political situations, weather alerts, health advisories, and safety conditions',
            backstory="""You are an expert travel risk assessment specialist with extensive experience in 
            monitoring global travel conditions. You have access to real-time data sources and can 
            provide accurate risk assessments for any destination. You consider multiple factors 
            including political stability, weather conditions, health advisories, and safety records 
            to provide travelers with the most current and reliable risk information.""",
            tools=[self.risk_assessment_tool, self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def crowd_density_agent(self):
        """Agent for predicting crowd density at attractions"""
        return Agent(
            role='Crowd Density Prediction Expert',
            goal='Predict tourist density at attractions using ML models and provide recommendations for optimal visit times',
            backstory="""You are a data scientist specializing in crowd density prediction for tourist attractions. 
            You use machine learning models, historical data, and real-time factors to predict when attractions 
            will be crowded or quiet. You help travelers plan their visits to avoid crowds and have better 
            experiences at popular destinations.""",
            tools=[self.crowd_density_tool, self.search_tool, self.calculator_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def price_optimization_agent(self):
        """Agent for dynamic pricing and cost optimization"""
        return Agent(
            role='Travel Price Optimization Expert',
            goal='Find the best deals for flights, hotels, and activities using dynamic pricing analysis and predictive modeling',
            backstory="""You are a travel pricing expert with deep knowledge of airline pricing algorithms, 
            hotel revenue management, and activity pricing patterns. You use advanced analytics to predict 
            price trends and find the best deals for travelers. You help optimize travel budgets and 
            ensure travelers get maximum value for their money.""",
            tools=[self.price_optimization_tool, self.search_tool, self.calculator_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def language_barrier_agent(self):
        """Agent for solving language barriers with cultural context"""
        return Agent(
            role='Language and Cultural Bridge Specialist',
            goal='Break down language barriers with real-time translation, cultural context, and local slang integration',
            backstory="""You are a polyglot cultural expert who specializes in helping travelers communicate 
            effectively in foreign countries. You not only provide translations but also cultural context, 
            local slang, and etiquette guidance. You understand that effective communication goes beyond 
            literal translation and includes cultural nuances, appropriate formality levels, and local customs.""",
            tools=[self.language_barrier_tool, self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def travel_intelligence_coordinator(self):
        """Master agent that coordinates all intelligence features"""
        return Agent(
            role='Travel Intelligence Coordinator',
            goal='Coordinate all travel intelligence features to provide comprehensive travel insights and recommendations',
            backstory="""You are a senior travel intelligence coordinator who oversees all aspects of 
            travel intelligence. You coordinate risk assessment, crowd density predictions, price optimization, 
            and language assistance to provide travelers with a complete picture of their travel situation. 
            You synthesize information from multiple sources to provide actionable recommendations.""",
            tools=[
                self.risk_assessment_tool, 
                self.crowd_density_tool, 
                self.price_optimization_tool, 
                self.language_barrier_tool,
                self.search_tool, 
                self.browser_tool, 
                self.calculator_tool
            ],
            allow_delegation=True,
            llm=self.llm,
            verbose=True
        )
