from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks
from intelligence_agents import IntelligenceAgents
from intelligence_tasks import IntelligenceTasks
from datetime import datetime, timedelta
from dotenv import load_dotenv
import argparse
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os


class TripCrew:
    def __init__(self, origin, cities, date_range, interests, enable_intelligence=False):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.enable_intelligence = enable_intelligence
        #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
        self.llm = LLM(model="gemini/gemini-2.0-flash")

    def run(self):
        try:
            agents = TripAgents(llm=self.llm)
            tasks = TripTasks()

            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.cities,
                self.interests,
                self.date_range
            )

            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            crew = Crew(
                agents=[
                    city_selector_agent, local_expert_agent, travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                verbose=True
            )

            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def run_with_intelligence(self):
        """Run trip planning with AI-powered intelligence features"""
        try:
            # Run basic trip planning
            basic_result = self.run()
            
            if not basic_result:
                return None
            
            print("\n" + "="*60)
            print("🧠 AI-POWERED TRAVEL INTELLIGENCE ANALYSIS")
            print("="*60)
            
            # Initialize intelligence agents
            intel_agents = IntelligenceAgents(llm=self.llm)
            intel_tasks = IntelligenceTasks()
            
            # Run intelligence analysis
            intelligence_crew = Crew(
                agents=[
                    intel_agents.risk_assessment_agent(),
                    intel_agents.crowd_density_agent(),
                    intel_agents.price_optimization_agent(),
                    intel_agents.language_barrier_agent()
                ],
                tasks=[
                    intel_tasks.risk_assessment_task(
                        intel_agents.risk_assessment_agent(),
                        self.origin, self.cities, self.date_range, self.interests
                    ),
                    intel_tasks.crowd_density_task(
                        intel_agents.crowd_density_agent(),
                        self.cities, self.date_range, self.interests
                    ),
                    intel_tasks.price_optimization_task(
                        intel_agents.price_optimization_agent(),
                        self.origin, self.cities, self.date_range, self.interests
                    ),
                    intel_tasks.language_barrier_task(
                        intel_agents.language_barrier_agent(),
                        self.cities, self.date_range, self.interests
                    )
                ],
                verbose=True
            )
            
            intelligence_result = intelligence_crew.kickoff()
            
            # Combine results
            combined_result = f"""
{basic_result}

{intelligence_result}
            """
            
            return combined_result
            
        except Exception as e:
            print(f"An error occurred during intelligence analysis: {str(e)}")
            return self.run()  # Fallback to basic planning

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ['GEMINI_API_KEY', 'SERPER_API_KEY', 'BROWSERLESS_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file or environment.")
        return

    parser = argparse.ArgumentParser(description='AI Travel Planner')
    
    parser.add_argument('--origin', '-o', 
                       type=str, 
                       required=True,
                       help='Your current location (e.g., "San Mateo, CA")')
    
    parser.add_argument('--destination', '-d', 
                       type=str, 
                       required=True,
                       help='Destination city and country (e.g., "Bali, Indonesia")')
    
    parser.add_argument('--start-date', '-s',
                       type=validate_date,
                       required=True,
                       help='Start date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--end-date', '-e',
                       type=validate_date,
                       required=True,
                       help='End date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--interests', '-i',
                       type=str,
                       required=True,
                       help='Your interests and trip details (e.g., "2 adults who love swimming, dancing, hiking")')
    
    parser.add_argument('--intelligence', '--ai',
                       action='store_true',
                       help='Enable AI-powered travel intelligence features (risk assessment, crowd density, price optimization, language assistance)')

    args = parser.parse_args()

    # Validate dates
    if args.end_date <= args.start_date:
        print("Error: End date must be after start date")
        return

    # Format date range as string
    date_range = f"{args.start_date} to {args.end_date}"

    print("\n🏖️ VacAIgent - AI Travel Planner")
    print("================================")
    print(f"\nPlanning your trip...")
    print(f"From: {args.origin}")
    print(f"To: {args.destination}")
    print(f"Dates: {date_range}")
    print(f"Interests: {args.interests}")
    if args.intelligence:
        print("🧠 AI Intelligence Features: ENABLED")
    print("\nThis may take a few minutes. Please wait while our AI agents work on your perfect trip...\n")

    trip_crew = TripCrew(args.origin, args.destination, date_range, args.interests, enable_intelligence=args.intelligence)
    
    if args.intelligence:
        result = trip_crew.run_with_intelligence()
    else:
        result = trip_crew.run()

    if result:
        print("\n✨ Your Trip Plan ✨")
        print("===================\n")
        print(result)
    else:
        print("\n❌ Failed to generate trip plan. Please try again.")

if __name__ == "__main__":
    main()