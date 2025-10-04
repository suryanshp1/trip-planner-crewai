from crewai import Crew, LLM
from trip_agents import TripAgents, StreamToExpander
from trip_tasks import TripTasks
from intelligence_agents import IntelligenceAgents
from intelligence_tasks import IntelligenceTasks
import streamlit as st
import datetime
import sys
from langchain_openai import OpenAI


st.set_page_config(page_icon="✈️", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class TripCrew:

    def __init__(self, origin, cities, date_range, interests, enable_intelligence=False):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.enable_intelligence = enable_intelligence
        # Convert date_range to string format for better handling
        self.date_range = f"{date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}"
        self.output_placeholder = st.empty()
        self.llm = LLM(model="gemini/gemini-2.0-flash")
        # self.llm = OpenAI(
        #     temperature=0.7,
        #     model_name="gpt-4",
        # )

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
            self.output_placeholder.markdown(result)
            return result
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    def run_with_intelligence(self):
        """Run trip planning with AI-powered intelligence features"""
        try:
            # Run basic trip planning
            basic_result = self.run()
            
            if not basic_result:
                return None
            
            # Add intelligence analysis section
            st.markdown("---")
            st.markdown("## 🧠 AI-Powered Travel Intelligence Analysis")
            
            # Initialize intelligence agents
            intel_agents = IntelligenceAgents(llm=self.llm)
            intel_tasks = IntelligenceTasks()
            
            # Create tabs for different intelligence features
            tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Risk Assessment", "👥 Crowd Density", "💰 Price Optimization", "🗣️ Language Assistance"])
            
            with tab1:
                st.markdown("### Risk Assessment & Safety Analysis")
                with st.spinner("Analyzing travel risks and safety conditions..."):
                    risk_agent = intel_agents.risk_assessment_agent()
                    risk_task = intel_tasks.risk_assessment_task(
                        risk_agent, self.origin, self.cities, self.date_range, self.interests
                    )
                    risk_crew = Crew(agents=[risk_agent], tasks=[risk_task], verbose=True)
                    risk_result = risk_crew.kickoff()
                    st.markdown(risk_result)
            
            with tab2:
                st.markdown("### Crowd Density Predictions")
                with st.spinner("Predicting crowd levels at attractions..."):
                    crowd_agent = intel_agents.crowd_density_agent()
                    crowd_task = intel_tasks.crowd_density_task(
                        crowd_agent, self.cities, self.date_range, self.interests
                    )
                    crowd_crew = Crew(agents=[crowd_agent], tasks=[crowd_task], verbose=True)
                    crowd_result = crowd_crew.kickoff()
                    st.markdown(crowd_result)
            
            with tab3:
                st.markdown("### Price Optimization Analysis")
                with st.spinner("Analyzing prices and finding best deals..."):
                    price_agent = intel_agents.price_optimization_agent()
                    price_task = intel_tasks.price_optimization_task(
                        price_agent, self.origin, self.cities, self.date_range, self.interests
                    )
                    price_crew = Crew(agents=[price_agent], tasks=[price_task], verbose=True)
                    price_result = price_crew.kickoff()
                    st.markdown(price_result)
            
            with tab4:
                st.markdown("### Language & Cultural Assistance")
                with st.spinner("Preparing language and cultural guidance..."):
                    lang_agent = intel_agents.language_barrier_agent()
                    lang_task = intel_tasks.language_barrier_task(
                        lang_agent, self.cities, self.date_range, self.interests
                    )
                    lang_crew = Crew(agents=[lang_agent], tasks=[lang_task], verbose=True)
                    lang_result = lang_crew.kickoff()
                    st.markdown(lang_result)
            
            return basic_result
            
        except Exception as e:
            st.error(f"An error occurred during intelligence analysis: {str(e)}")
            return self.run()  # Fallback to basic planning


if __name__ == "__main__":
    icon("🏖️ VacAIgent")

    st.subheader("Let AI agents plan your next vacation!",
                 divider="rainbow", anchor=False)

    import datetime

    today = datetime.datetime.now().date()
    next_year = today.year + 1
    jan_16_next_year = datetime.date(next_year, 1, 10)

    with st.sidebar:
        st.header("👇 Enter your trip details")
        with st.form("my_form"):
            location = st.text_input(
                "Where are you currently located?", placeholder="San Mateo, CA")
            cities = st.text_input(
                "City and country are you interested in vacationing at?", placeholder="Bali, Indonesia")
            date_range = st.date_input(
                "Date range you are interested in traveling?",
                min_value=today,
                value=(today, jan_16_next_year + datetime.timedelta(days=6)),
                format="MM/DD/YYYY",
            )
            interests = st.text_area("High level interests and hobbies or extra details about your trip?",
                                     placeholder="2 adults who love swimming, dancing, hiking, and eating")
            
            # Intelligence features toggle
            st.markdown("### 🧠 AI Intelligence Features")
            enable_intelligence = st.checkbox(
                "Enable AI-Powered Travel Intelligence", 
                value=False,
                help="Includes risk assessment, crowd density predictions, price optimization, and language assistance"
            )

            submitted = st.form_submit_button("Submit")

        st.divider()

        # Credits to joaomdmoura/CrewAI for the code: https://github.com/joaomdmoura/crewAI
        st.sidebar.markdown(
        """
        Credits to [**@joaomdmoura**](https://twitter.com/joaomdmoura)
        for creating **crewAI** 🚀
        """,
            unsafe_allow_html=True
        )

        st.sidebar.info("Click the logo to visit GitHub repo", icon="👇")
        st.sidebar.markdown(
            """
        <a href="https://github.com/joaomdmoura/crewAI" target="_blank">
            <img src="https://raw.githubusercontent.com/joaomdmoura/crewAI/main/docs/crewai_logo.png" alt="CrewAI Logo" style="width:100px;"/>
        </a>
        """,
            unsafe_allow_html=True
        )

    # Check if form was submitted and process the trip planning
    if submitted:
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                # Store original stdout
                original_stdout = sys.stdout
                try:
                    # Redirect stdout to StreamToExpander
                    sys.stdout = StreamToExpander(st)
                    trip_crew = TripCrew(location, cities, date_range, interests, enable_intelligence=enable_intelligence)
                    
                    if enable_intelligence:
                        result = trip_crew.run_with_intelligence()
                    else:
                        result = trip_crew.run()
                finally:
                    # Always restore original stdout
                    sys.stdout = original_stdout
            status.update(label="✅ Trip Plan Ready!",
                          state="complete", expanded=False)

        st.subheader("Here is your Trip Plan", anchor=False, divider="rainbow")
        st.markdown(result)
