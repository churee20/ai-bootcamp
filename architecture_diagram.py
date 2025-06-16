"""
AI Travel Planner - Service Architecture Diagram Generator
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Circle
import numpy as np

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9

def create_architecture_diagram():
    """Create service architecture diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Color definitions
    colors = {
        'frontend': '#E3F2FD',      # Light blue - Frontend
        'backend': '#FFF3E0',       # Light orange - Backend
        'ai': '#F3E5F5',            # Light purple - AI
        'data': '#E8F5E8',          # Light green - Data
        'external': '#FFEBEE',      # Light red - External
        'infrastructure': '#F5F5F5' # Light gray - Infrastructure
    }
    
    # Box style
    box_style = {
        'boxstyle': 'round,pad=0.3',
        'facecolor': 'white',
        'edgecolor': 'black',
        'linewidth': 1.5
    }
    
    # Title
    ax.text(10, 15.5, 'AI Travel Planner - Service Architecture Diagram', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Layer labels
    ax.text(10, 15, 'Multi-Layer Architecture with AI Integration', 
            ha='center', va='center', fontsize=14, color='gray')
    
    # ==================== FRONTEND LAYER ====================
    ax.text(10, 14.5, 'Frontend Layer (Streamlit UI)', 
            ha='center', va='center', fontsize=12, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['frontend']))
    
    # Frontend components
    frontend_components = [
        (3, 13.5, "User Input\nHandler", colors['frontend']),
        (7, 13.5, "Streamlit UI\nComponents", colors['frontend']),
        (11, 13.5, "Progress\nTracker", colors['frontend']),
        (15, 13.5, "Results\nDisplay", colors['frontend'])
    ]
    
    for x, y, text, color in frontend_components:
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)
    
    # ==================== BACKEND LAYER ====================
    ax.text(10, 12.5, 'Backend Layer (Multi-Agent System)', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['backend']))
    
    # Backend components
    backend_components = [
        (2, 11.5, "Travel\nCoordinator\nAgent", colors['backend']),
        (5, 11.5, "Destination\nResearch\nAgent", colors['backend']),
        (8, 11.5, "Accommodation\nAgent", colors['backend']),
        (11, 11.5, "Food &\nDining\nAgent", colors['backend']),
        (14, 11.5, "Transportation\nAgent", colors['backend']),
        (17, 11.5, "Budget\nManager\nAgent", colors['backend'])
    ]
    
    for x, y, text, color in backend_components:
        box = FancyBboxPatch((x-1, y-0.5), 2, 1, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)
    
    # ==================== AI LAYER ====================
    ax.text(10, 10, 'AI Layer (LLM & RAG)', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['ai']))
    
    # AI components
    ai_components = [
        (3, 9, "Azure OpenAI\nLLM", colors['ai']),
        (7, 9, "LangChain\nFramework", colors['ai']),
        (11, 9, "RAG\nSystem", colors['ai']),
        (15, 9, "Prompt\nEngineering", colors['ai'])
    ]
    
    for x, y, text, color in ai_components:
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)
    
    # ==================== DATA LAYER ====================
    ax.text(10, 7.5, 'Data Layer (Vector Database & Tools)', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['data']))
    
    # Data components
    data_components = [
        (2, 6.5, "ChromaDB\nVector Store", colors['data']),
        (5, 6.5, "Embedding\nModel", colors['data']),
        (8, 6.5, "Travel\nKnowledge\nBase", colors['data']),
        (11, 6.5, "ReAct\nTools", colors['data']),
        (14, 6.5, "Session\nStorage", colors['data']),
        (17, 6.5, "Configuration\nManager", colors['data'])
    ]
    
    for x, y, text, color in data_components:
        box = FancyBboxPatch((x-1, y-0.4), 2, 0.8, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)
    
    # ==================== EXTERNAL SERVICES ====================
    ax.text(10, 5, 'External Services', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['external']))
    
    # External services
    external_services = [
        (3, 4, "Azure OpenAI\nService", colors['external']),
        (7, 4, "OpenAI\nAPI", colors['external']),
        (11, 4, "Langfuse\nMonitoring", colors['external']),
        (15, 4, "Future APIs\n(Weather, Maps)", colors['external'])
    ]
    
    for x, y, text, color in external_services:
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)
    
    # ==================== INFRASTRUCTURE ====================
    ax.text(10, 2.5, 'Infrastructure', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['infrastructure']))
    
    # Infrastructure components
    infra_components = [
        (3, 1.5, "Python\nEnvironment", colors['infrastructure']),
        (7, 1.5, "Streamlit\nServer", colors['infrastructure']),
        (11, 1.5, "Local\nFile System", colors['infrastructure']),
        (15, 1.5, "Environment\nVariables", colors['infrastructure'])
    ]
    
    for x, y, text, color in infra_components:
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)
    
    # ==================== DATA FLOW ARROWS ====================
    
    # Frontend to Backend
    arrows = [
        # User input flow
        ((3, 13.1), (2, 12)),      # Input Handler → Coordinator
        ((7, 13.1), (2, 12)),      # UI Components → Coordinator
        ((11, 13.1), (2, 12)),     # Progress Tracker → Coordinator
        ((15, 13.1), (2, 12)),     # Results Display → Coordinator
        
        # Backend to AI
        ((2, 11), (3, 9.4)),       # Coordinator → Azure OpenAI
        ((2, 11), (7, 9.4)),       # Coordinator → LangChain
        ((2, 11), (11, 9.4)),      # Coordinator → RAG
        ((2, 11), (15, 9.4)),      # Coordinator → Prompt Engineering
        
        # AI to Data
        ((3, 8.6), (2, 6.9)),      # Azure OpenAI → ChromaDB
        ((7, 8.6), (5, 6.9)),      # LangChain → Embedding
        ((11, 8.6), (8, 6.9)),     # RAG → Knowledge Base
        ((15, 8.6), (11, 6.9)),    # Prompt Engineering → Tools
        
        # Data to Infrastructure
        ((2, 6.1), (3, 1.9)),      # ChromaDB → File System
        ((5, 6.1), (3, 1.9)),      # Embedding → Python Env
        ((8, 6.1), (11, 1.9)),     # Knowledge Base → File System
        ((11, 6.1), (7, 1.9)),     # Tools → Streamlit
        ((14, 6.1), (15, 1.9)),    # Session Storage → Env Vars
        
        # External connections
        ((3, 8.6), (3, 4.4)),      # Azure OpenAI → Azure Service
        ((7, 8.6), (7, 4.4)),      # LangChain → OpenAI API
        ((11, 8.6), (11, 4.4)),    # RAG → Langfuse
        
        # Backend agent connections
        ((2, 11), (5, 11)),        # Coordinator → Destination
        ((5, 11), (8, 11)),        # Destination → Accommodation
        ((8, 11), (11, 11)),       # Accommodation → Food
        ((11, 11), (14, 11)),      # Food → Transportation
        ((14, 11), (17, 11)),      # Transportation → Budget
        ((17, 11), (2, 11)),       # Budget → Coordinator (loop)
    ]
    
    # Draw arrows
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=12, fc="black", ec="black", linewidth=1.5)
        ax.add_patch(arrow)
    
    # Legend
    legend_elements = [
        patches.Patch(color=colors['frontend'], label='Frontend Layer'),
        patches.Patch(color=colors['backend'], label='Backend Layer'),
        patches.Patch(color=colors['ai'], label='AI Layer'),
        patches.Patch(color=colors['data'], label='Data Layer'),
        patches.Patch(color=colors['external'], label='External Services'),
        patches.Patch(color=colors['infrastructure'], label='Infrastructure')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('service_architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Service architecture diagram created: service_architecture_diagram.png")

def create_component_diagram():
    """Create detailed component interaction diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Color definitions
    colors = {
        'ui': '#E3F2FD',
        'agent': '#FFF3E0',
        'llm': '#F3E5F5',
        'data': '#E8F5E8',
        'tool': '#FFEBEE',
        'config': '#F5F5F5'
    }
    
    # Box style
    box_style = {
        'boxstyle': 'round,pad=0.3',
        'facecolor': 'white',
        'edgecolor': 'black',
        'linewidth': 1.5
    }
    
    # Title
    ax.text(9, 13.5, 'AI Travel Planner - Component Interaction Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Main components
    components = [
        # UI Layer
        (3, 12, "main_multi_agent.py\n(Entry Point)", colors['ui']),
        (9, 12, "StreamlitUI\n(ui/streamlit_ui.py)", colors['ui']),
        (15, 12, "UserInputHandler\n(components/)", colors['ui']),
        
        # Agent Layer
        (3, 10, "TravelCoordinatorAgent\n(agents/coordinator.py)", colors['agent']),
        (9, 10, "Specialized Agents\n(agents/*.py)", colors['agent']),
        (15, 10, "Agent Executor\n(LangChain)", colors['agent']),
        
        # LLM Layer
        (3, 8, "AzureChatOpenAI\n(config/config.py)", colors['llm']),
        (9, 8, "AzureOpenAIEmbeddings\n(config/config.py)", colors['llm']),
        (15, 8, "LangChain Framework\n(LangChain)", colors['llm']),
        
        # Tools Layer
        (3, 6, "ReAct Tools\n(tools/*.py)", colors['tool']),
        (9, 6, "SearchDestinationTool", colors['tool']),
        (15, 6, "WeatherTool\nAccommodationTool", colors['tool']),
        
        # Data Layer
        (3, 4, "ChromaDB\n(langchain_chroma)", colors['data']),
        (9, 4, "Vector Store\n(chroma_db/)", colors['data']),
        (15, 4, "Travel Data\n(data/travel_info.txt)", colors['data']),
        
        # Config Layer
        (3, 2, "Environment Variables\n(.env)", colors['config']),
        (9, 2, "Configuration\n(config/config.py)", colors['config']),
        (15, 2, "Requirements\n(requirements_*.txt)", colors['config'])
    ]
    
    # Draw components
    for x, y, text, color in components:
        box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)
    
    # Data flow arrows
    arrows = [
        # UI flow
        ((3, 11.5), (9, 11.5)),    # main → StreamlitUI
        ((9, 11.5), (15, 11.5)),   # StreamlitUI → UserInputHandler
        ((15, 11.5), (3, 9.5)),    # UserInputHandler → Coordinator
        
        # Agent flow
        ((3, 9.5), (9, 9.5)),      # Coordinator → Specialized Agents
        ((9, 9.5), (15, 9.5)),     # Specialized Agents → Agent Executor
        ((15, 9.5), (3, 7.5)),     # Agent Executor → AzureChatOpenAI
        
        # LLM flow
        ((3, 7.5), (9, 7.5)),      # AzureChatOpenAI → Embeddings
        ((9, 7.5), (15, 7.5)),     # Embeddings → LangChain
        ((15, 7.5), (3, 5.5)),     # LangChain → ReAct Tools
        
        # Tools flow
        ((3, 5.5), (9, 5.5)),      # ReAct Tools → SearchDestinationTool
        ((9, 5.5), (15, 5.5)),     # SearchDestinationTool → WeatherTool
        ((15, 5.5), (3, 3.5)),     # WeatherTool → ChromaDB
        
        # Data flow
        ((3, 3.5), (9, 3.5)),      # ChromaDB → Vector Store
        ((9, 3.5), (15, 3.5)),     # Vector Store → Travel Data
        ((15, 3.5), (3, 1.5)),     # Travel Data → Environment Variables
        
        # Config flow
        ((3, 1.5), (9, 1.5)),      # Environment Variables → Configuration
        ((9, 1.5), (15, 1.5)),     # Configuration → Requirements
        
        # Cross-layer connections
        ((3, 11.5), (3, 9.5)),     # main → Coordinator
        ((9, 11.5), (9, 9.5)),     # StreamlitUI → Specialized Agents
        ((15, 11.5), (15, 9.5)),   # UserInputHandler → Agent Executor
    ]
    
    # Draw arrows
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=10, fc="black", ec="black", linewidth=1.5)
        ax.add_patch(arrow)
    
    # Layer labels
    layer_labels = [
        (9, 12.8, "UI Layer"),
        (9, 10.8, "Agent Layer"),
        (9, 8.8, "LLM Layer"),
        (9, 6.8, "Tools Layer"),
        (9, 4.8, "Data Layer"),
        (9, 2.8, "Config Layer")
    ]
    
    for x, y, text in layer_labels:
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(color=colors['ui'], label='UI Components'),
        patches.Patch(color=colors['agent'], label='Agent System'),
        patches.Patch(color=colors['llm'], label='LLM & AI'),
        patches.Patch(color=colors['tool'], label='Tools'),
        patches.Patch(color=colors['data'], label='Data Storage'),
        patches.Patch(color=colors['config'], label='Configuration')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('component_interaction_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Component interaction diagram created: component_interaction_diagram.png")

def create_data_flow_diagram():
    """Create data flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Color definitions
    colors = {
        'input': '#E3F2FD',
        'process': '#FFF3E0',
        'storage': '#F3E5F5',
        'output': '#E8F5E8',
        'external': '#FFEBEE'
    }
    
    # Box style
    box_style = {
        'boxstyle': 'round,pad=0.3',
        'facecolor': 'white',
        'edgecolor': 'black',
        'linewidth': 1.5
    }
    
    # Title
    ax.text(8, 11.5, 'AI Travel Planner - Data Flow Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Data flow components
    components = [
        # Input
        (2, 10, "User Input\n(Destination, Duration,\nBudget, Preferences)", colors['input']),
        
        # Processing
        (6, 10, "Input Validation\n& Processing", colors['process']),
        (10, 10, "RAG Search\n(Context Retrieval)", colors['process']),
        (14, 10, "Multi-Agent\nProcessing", colors['process']),
        
        # Storage
        (2, 7, "ChromaDB\n(Vector Store)", colors['storage']),
        (6, 7, "Session Storage\n(Streamlit)", colors['storage']),
        (10, 7, "Configuration\n(.env)", colors['storage']),
        (14, 7, "Knowledge Base\n(travel_info.txt)", colors['storage']),
        
        # External
        (2, 4, "Azure OpenAI\nAPI", colors['external']),
        (6, 4, "OpenAI API\n(Fallback)", colors['external']),
        (10, 4, "Langfuse\n(Monitoring)", colors['external']),
        (14, 4, "Future APIs\n(Weather, Maps)", colors['external']),
        
        # Output
        (2, 1, "Travel Plan\n(Structured Data)", colors['output']),
        (6, 1, "Itinerary\n(JSON Format)", colors['output']),
        (10, 1, "Recommendations\n(Text)", colors['output']),
        (14, 1, "Cost Summary\n(Calculated)", colors['output'])
    ]
    
    # Draw components
    for x, y, text, color in components:
        box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)
    
    # Data flow arrows
    arrows = [
        # Input flow
        ((2, 9.5), (6, 9.5)),      # User Input → Validation
        ((6, 9.5), (10, 9.5)),     # Validation → RAG Search
        ((10, 9.5), (14, 9.5)),    # RAG Search → Multi-Agent
        
        # Storage connections
        ((10, 9.5), (2, 7.5)),     # RAG Search → ChromaDB
        ((6, 9.5), (6, 7.5)),      # Validation → Session Storage
        ((14, 9.5), (10, 7.5)),    # Multi-Agent → Configuration
        ((14, 9.5), (14, 7.5)),    # Multi-Agent → Knowledge Base
        
        # External API calls
        ((14, 9.5), (2, 4.5)),     # Multi-Agent → Azure OpenAI
        ((14, 9.5), (6, 4.5)),     # Multi-Agent → OpenAI API
        ((14, 9.5), (10, 4.5)),    # Multi-Agent → Langfuse
        ((14, 9.5), (14, 4.5)),    # Multi-Agent → Future APIs
        
        # Output flow
        ((14, 9.5), (2, 1.5)),     # Multi-Agent → Travel Plan
        ((14, 9.5), (6, 1.5)),     # Multi-Agent → Itinerary
        ((14, 9.5), (10, 1.5)),    # Multi-Agent → Recommendations
        ((14, 9.5), (14, 1.5)),    # Multi-Agent → Cost Summary
        
        # Feedback loops
        ((2, 1.5), (6, 9.5)),      # Travel Plan → Validation (feedback)
        ((6, 1.5), (10, 9.5)),     # Itinerary → RAG Search (feedback)
    ]
    
    # Draw arrows
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=10, fc="black", ec="black", linewidth=1.5)
        ax.add_patch(arrow)
    
    # Flow labels
    flow_labels = [
        (4, 10.3, "Input Processing"),
        (8, 10.3, "Context Retrieval"),
        (12, 10.3, "AI Processing"),
        (4, 7.3, "Data Storage"),
        (8, 7.3, "Configuration"),
        (12, 7.3, "Knowledge Base"),
        (4, 4.3, "External APIs"),
        (8, 4.3, "Fallback APIs"),
        (12, 4.3, "Monitoring"),
        (16, 4.3, "Future Services"),
        (4, 1.3, "Structured Output"),
        (8, 1.3, "JSON Format"),
        (12, 1.3, "Text Output"),
        (16, 1.3, "Calculated Data")
    ]
    
    for x, y, text in flow_labels:
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(color=colors['input'], label='Input Data'),
        patches.Patch(color=colors['process'], label='Processing'),
        patches.Patch(color=colors['storage'], label='Storage'),
        patches.Patch(color=colors['external'], label='External Services'),
        patches.Patch(color=colors['output'], label='Output Data')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('data_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Data flow diagram created: data_flow_diagram.png")

if __name__ == "__main__":
    print("Creating AI Travel Planner architecture diagrams...")
    
    # Create service architecture diagram
    create_architecture_diagram()
    
    # Create component interaction diagram
    create_component_diagram()
    
    # Create data flow diagram
    create_data_flow_diagram()
    
    print("\nAll architecture diagrams have been created!")
    print("- service_architecture_diagram.png: High-level service architecture")
    print("- component_interaction_diagram.png: Detailed component interactions")
    print("- data_flow_diagram.png: Data flow and processing") 