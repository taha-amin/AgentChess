# 🤖 AI Chess Agents: An AutoGen Chess Game

A fascinating chess application where two AI agents powered by OpenAI play chess against each other. Built using Streamlit and AutoGen, this application provides a visual interface to watch AI agents make strategic chess moves in real-time.

## 🌟 Features

### AI Agents
- Two AutoGen-powered chess agents playing against each other
- Real-time move generation and execution
- Strategic decision making using OpenAI's language models

### Interactive Interface
- Live chess board visualization
- Move history tracking
- Configurable number of game turns
- Easy-to-use Streamlit interface

### Game Management
- Complete chess ruleset implementation using python-chess
- Move validation and legal move checking
- Game state persistence using Streamlit session state
- Configurable maximum turns for demonstration purposes

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- OpenAI API key

### Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone [your-repository-url]
cd [project-directory]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run ai_chess_agent.py
```

## 💻 Usage

1. Start the application using the command above
2. Enter your OpenAI API key in the sidebar
3. Configure the number of turns you want the agents to play (default: 5)
   - Note: A complete chess game typically takes >200 turns
   - For demonstration purposes, 5-10 turns are recommended to conserve API usage
4. Watch as the AI agents play chess against each other!

## 📦 Dependencies

- streamlit: Web application framework
- chess==1.11.1: Chess game logic and rules
- autogen==0.6.1: AI agent framework
- cairosvg: SVG handling for board visualization
- pillow: Image processing

## ⚠️ Important Notes

- The number of turns directly affects API usage and runtime
- A full chess game (200+ turns) will consume significant API credits
- For demonstrations, it's recommended to start with 5-10 turns
- Keep your OpenAI API key secure and never share it publicly

## 🔑 API Key Configuration

The application requires an OpenAI API key to function. You can enter your API key in the sidebar of the Streamlit interface. The key is stored securely in the session state and is never displayed or logged.

To get an API key:
1. Sign up for an [OpenAI account](https://platform.openai.com/)
2. Navigate to the API section
3. Generate a new API key
4. Copy and paste the key into the application's sidebar

## 🎮 How It Works

The application uses AutoGen to create conversable agents that can play chess. These agents:
- Analyze the current board state
- Generate legal moves
- Make strategic decisions
- Execute moves on the virtual chess board

The game progress is visualized in real-time, allowing you to watch as the AI agents compete against each other.

