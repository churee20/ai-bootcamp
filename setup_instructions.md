# AI Travel Planner - Setup Instructions

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### 2. Clone the Repository
```bash
git clone https://github.com/churee20/ai-bootcamp.git
cd ai-bootcamp
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements_multi_agent.txt
```

### 5. Environment Setup
Create a `.env` file in the project root with your API keys:

```env
# Azure OpenAI Settings (Recommended)
AOAI_API_KEY="your_azure_openai_api_key"
AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
AOAI_DEPLOY_GPT4O="your_deployment_name"
AOAI_API_VERSION="2024-05-01-preview"
AOAI_EMBEDDING_DEPLOYMENT="your_embedding_deployment_name"

# OpenAI Settings (Alternative)
OPENAI_API_KEY="your_openai_api_key"
OPENAI_MODEL="gpt-4o"

# Optional: Langfuse for monitoring
LANGFUSE_PUBLIC_KEY="your_langfuse_public_key"
LANGFUSE_SECRET_KEY="your_langfuse_secret_key"
```

### 6. Setup RAG (Optional)
If you have Azure OpenAI API keys, you can set up RAG functionality:

```bash
python ingest_data.py
```

### 7. Run the Application
```bash
# Multi-Agent version (Recommended)
python -m streamlit run main_multi_agent.py

# Basic version
python -m streamlit run main.py
```

## 📁 Project Structure

```
ai-bootcamp/
├── main_multi_agent.py          # Main application (Multi-Agent)
├── main.py                      # Basic version
├── requirements_multi_agent.txt # Dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
├── setup_instructions.md        # This file
├── agents/                      # Multi-Agent system
│   ├── coordinator.py           # Main coordinator agent
│   └── [specialized_agents]     # Specialized agents
├── tools/                       # ReAct tools
├── config/                      # Configuration
├── components/                  # UI components
├── ui/                          # Streamlit UI
├── data/                        # RAG data
└── tests/                       # Test files
```

## 🔧 Features

### Multi-Agent System
- **Travel Coordinator Agent**: Main orchestrator
- **Destination Research Agent**: Destination information
- **Accommodation Agent**: Hotel and lodging
- **Food & Dining Agent**: Restaurant recommendations
- **Transportation Agent**: Travel logistics
- **Activity Planner Agent**: Activities and attractions
- **Budget Manager Agent**: Cost management

### RAG (Retrieval-Augmented Generation)
- ChromaDB vector database
- Azure OpenAI embeddings
- Context-aware responses

### UI Features
- Streamlit-based interface
- Step-by-step workflow
- Real-time progress tracking
- Interactive results display

## 🎯 Usage

1. **Launch the application**
2. **Enter travel preferences**:
   - Destination
   - Duration
   - Group size
   - Travel style
   - Budget range
   - Activities preferences
   - Food preferences
   - Transportation preferences

3. **Click "Multi Agent Run"** to generate your travel plan
4. **Review the results** and use additional features

## 🔑 API Key Setup

### Azure OpenAI (Recommended)
1. Create an Azure OpenAI resource
2. Deploy GPT-4o model
3. Deploy text-embedding-3-large model
4. Get API key and endpoint
5. Add to `.env` file

### OpenAI (Alternative)
1. Get API key from OpenAI
2. Add to `.env` file

## 🐛 Troubleshooting

### Common Issues

1. **"API key not found"**
   - Check `.env` file exists
   - Verify API key format
   - Ensure no extra spaces

2. **"ChromaDB error"**
   - Delete `chroma_db/` folder
   - Re-run `python ingest_data.py`

3. **"Module not found"**
   - Activate virtual environment
   - Run `pip install -r requirements_multi_agent.txt`

4. **"Streamlit not found"**
   - Install Streamlit: `pip install streamlit`

## 📊 Demo Mode

If no API keys are provided, the application runs in demo mode:
- Uses pre-generated sample data
- Shows UI functionality
- Demonstrates workflow

## 🔄 Development

### Adding New Features
1. Create new agent in `agents/` directory
2. Add tools in `tools/` directory
3. Update coordinator agent
4. Test with `python -m streamlit run main_multi_agent.py`

### Testing
```bash
python -m pytest tests/
```

## 📝 License

This project is part of the AI Bootcamp curriculum.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the README.md
- Create an issue on GitHub 