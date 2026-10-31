import asyncio
import sys
import os
import streamlit as st
from dotenv import load_dotenv
from ddgs import DDGS
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Set Windows asyncio loop policy
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="AutoGen Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .weather-card {
        background: #F0F7FF;
        border-left: 6px solid #2563EB;
        padding: 22px;
        border-radius: 10px;
        font-size: 1.15rem;
        line-height: 1.8;
        color: #1E293B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Optimized Search Tool
def get_weather_news(city: str) -> str:
    """Search the web for current weather conditions, temperature in Celsius, and news updates for a specific city."""
    print(f"\n[Tool Execution] Fetching live data for: {city}")
    try:
        with DDGS() as ddgs:
            # Enhanced query requesting Celsius metrics
            query = f"current weather temperature celsius today {city} weather forecast news"
            results = list(ddgs.text(query, max_results=6))
            if not results:
                return f"No live search data retrieved for {city}."
            return str(results)
    except Exception as e:
        return f"Error executing DuckDuckGo search: {str(e)}"

# Async Agent Execution
async def run_weather_agent(city_name: str, model_name: str):
    model_client = OpenAIChatCompletionClient(model=model_name)

    weather_agent = AssistantAgent(
        name="weather_news_agent",
        model_client=model_client,
        tools=[get_weather_news],
        reflect_on_tool_use=True,
        system_message=(
            "You are a precise weather news agent. "
            "Always call the get_weather_news tool first. "
            "Extract exact current weather details, temperature in Celsius (or °C/°F), and sky conditions. "
            "Do NOT output generic phrases like 'visit websites' or 'check forecasts'. "
            "Format your final output as EXACTLY 3 short, informative lines."
        )
    )

    result = await weather_agent.run(task=f"What is the live weather news and temperature for {city_name}?")
    
    await model_client.close()
    return result.messages

# --- UI Layout ---

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Agent Settings")
    
    api_key_env = os.getenv("OPENAI_API_KEY")
    if api_key_env:
        st.success("OpenAI API Key: Loaded ✅")
    else:
        st.warning("Missing API Key in `.env`")
        user_key = st.text_input("Enter OpenAI API Key:", type="password")
        if user_key:
            os.environ["OPENAI_API_KEY"] = user_key
            st.success("Key set for session!")

    model_choice = st.selectbox("LLM Architecture", ["gpt-4o-mini", "gpt-4o"], index=0)
    
    st.markdown("---")
    st.markdown("### 🤖 Architecture Details")
    st.caption("**Framework:** AutoGen AgentChat")
    st.caption("**Tool Engine:** Keyless `ddgs` Python SDK")
    st.caption("**Reflection:** `reflect_on_tool_use=True`")

# Header Section
st.markdown("""
    <div class="header-box">
        <h1>🌦️ AutoGen Weather Intelligence Agent</h1>
        <p>Autonomous Tool Execution & Real-Time Weather Analysis</p>
    </div>
""", unsafe_allow_html=True)

# Main Grid Layout
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🔍 Query Location")
    
    city_input = st.text_input("Enter City Name:", placeholder="e.g., Chennai, Trichy, Coimbatore, Madurai...")
    
    st.markdown("**Quick Preset Cities:**")
    btn_cols = st.columns(4)
    preset_city = None
    if btn_cols[0].button("Chennai", use_container_width=True):
        preset_city = "Chennai"
    if btn_cols[1].button("Trichy", use_container_width=True):
        preset_city = "Trichy"
    if btn_cols[2].button("Coimbatore", use_container_width=True):
        preset_city = "Coimbatore"
    if btn_cols[3].button("Madurai", use_container_width=True):
        preset_city = "Madurai"

    target_city = preset_city if preset_city else city_input
    execute_search = st.button("Run Weather Agent 🚀", type="primary", use_container_width=True)

with col_right:
    st.subheader("📊 Agent Analysis & Output")
    
    if (execute_search or preset_city) and target_city.strip():
        with st.spinner(f"Agent executing tool call for **{target_city}**..."):
            try:
                # Run AutoGen Agent
                messages = asyncio.run(run_weather_agent(target_city, model_choice))
                
                # Extract final response
                agent_final_output = messages[-1].content
                formatted_output = agent_final_output.replace("\n", "<br>")
                
                # Display Styled Weather Card
                st.markdown(f"""
                    <div class="weather-card">
                        <b>Location:</b> {target_city.capitalize()}<br><br>
                        {formatted_output}
                    </div>
                """, unsafe_allow_html=True)
                
                # Display Interactive Thought Log / Tool Execution Trace
                with st.expander("🛠️ View Agent Execution Logs & Raw Tool Data"):
                    for msg in messages:
                        st.markdown(f"**Role (`{msg.source}`):**")
                        st.code(msg.content, language="json" if "{" in str(msg.content) else "text")

            except Exception as ex:
                st.error(f"Execution Error: {str(ex)}")
    elif execute_search and not target_city.strip():
        st.info("Please select or enter a city to trigger the agent.")
    else:
        st.info("Select a quick preset or type a city name to begin analysis.")