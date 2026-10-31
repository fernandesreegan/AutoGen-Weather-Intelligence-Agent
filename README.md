# 🌦️ AutoGen Weather Intelligence Agent

An AI-powered Weather Intelligence Agent built using **Microsoft AutoGen, OpenAI, DuckDuckGo Search, and Streamlit**. The application retrieves recent weather information for user-selected cities and generates concise, AI-powered weather summaries.

## 🚀 Features

- 🤖 **Autonomous AI Agent:** Built with Microsoft AutoGen AgentChat.
- 🔎 **Real-Time Web Search:** Uses the free, keyless DuckDuckGo Search (`ddgs`) package.
- 🧠 **AI-Powered Analysis:** OpenAI GPT models analyze and summarize search results.
- 🌍 **City-Based Search:** Search weather updates for any city.
- 💻 **Interactive Dashboard:** User-friendly Streamlit interface with quick city selections.
- 📊 **Execution Logs:** View agent conversations, tool calls, and raw search results.
- 📝 **Structured Output:** Generates weather summaries in exactly three short lines.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Microsoft AutoGen | AI agent framework |
| OpenAI GPT | Language model |
| DuckDuckGo (`ddgs`) | Web search integration |
| Streamlit | Interactive web interface |
| python-dotenv | Environment variable management |

## 📂 Project Structure

```text
AutoGen-Weather-Intelligence-Agent/
│
├── weather_news.py       # AutoGen weather search agent
├── app.py                # Streamlit dashboard
├── requirements.txt      # Python dependencies
├── .env                  # OpenAI API key (not committed)
├── .gitignore
└── README.md
```

*Adjust the filenames to match your actual project.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/AutoGen-Weather-Intelligence-Agent.git
cd AutoGen-Weather-Intelligence-Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -U autogen-agentchat "autogen-ext[openai]" ddgs streamlit python-dotenv
```

### 4. Configure OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

⚠️ Never commit your `.env` file or API keys to GitHub.

### 5. Run the Application

For the Streamlit dashboard:

```bash
streamlit run app.py
```

Open your browser at:

```text
http://localhost:8501
```

For the command-line agent, if implemented separately:

```bash
python weather_news.py
```

## 🔄 How It Works

```text
       👤 User Enters City
                |
                v
       🤖 AutoGen AI Agent
                |
                v
       🔎 DuckDuckGo Search
                |
                v
       🌐 Recent Weather Data
                |
                v
       🧠 OpenAI GPT Analysis
                |
                v
       🌦️ 3-Line Weather Summary
                |
                v
       💻 Streamlit Dashboard
```

The agent uses `reflect_on_tool_use=True` to interpret the retrieved search results and generate a concise response instead of displaying raw tool output.

## 📚 Learning Outcomes

**Topic: Web Search Integration with AutoGen**

- Understanding AI agent tool calling
- Creating Python functions with type hints and descriptive docstrings
- Integrating DuckDuckGo Search without a search API key
- Configuring AutoGen AssistantAgent
- Understanding `reflect_on_tool_use=True`
- Building an interactive Streamlit application
- Inspecting agent execution logs

## 🔮 Future Enhancements

- 📍 Automatic location detection
- 📅 Multi-day weather forecasts
- 🚨 Severe weather alerts
- 📈 Historical weather trends
- 🌐 Multi-language weather summaries

## 👨‍💻 Author

**Fernandes Reegan**

AI & Automation Enthusiast | Database Administrator

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐.

Feedback, suggestions, and contributions are welcome!!
