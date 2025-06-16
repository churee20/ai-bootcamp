"""
AI Travel Planner - User Flow Diagram Generator
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Font settings for better compatibility
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def create_user_flow_diagram():
    """Create user flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Color definitions
    colors = {
        'start': '#4CAF50',      # Green - Start
        'input': '#2196F3',      # Blue - Input
        'process': '#FF9800',    # Orange - Process
        'decision': '#9C27B0',   # Purple - Decision
        'result': '#F44336',     # Red - Result
        'end': '#607D8B'         # Gray - End
    }
    
    # Box style definition
    box_style = {
        'boxstyle': 'round,pad=0.5',
        'facecolor': 'white',
        'edgecolor': 'black',
        'linewidth': 2
    }
    
    # 1. Start
    start_box = FancyBboxPatch((4.5, 11), 1, 0.5, **box_style)
    start_box.set_facecolor(colors['start'])
    ax.add_patch(start_box)
    ax.text(5, 11.25, 'Start\n✈️', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 2. Application Launch
    app_box = FancyBboxPatch((3.5, 10), 3, 0.5, **box_style)
    app_box.set_facecolor(colors['input'])
    ax.add_patch(app_box)
    ax.text(5, 10.25, 'Launch Streamlit App\n🌐', ha='center', va='center', fontsize=11)
    
    # 3. API Key Check
    api_box = FancyBboxPatch((3.5, 9), 3, 0.5, **box_style)
    api_box.set_facecolor(colors['decision'])
    ax.add_patch(api_box)
    ax.text(5, 9.25, 'Check API Key\n🔑', ha='center', va='center', fontsize=11)
    
    # 4. AI Mode (API Key Available)
    ai_box = FancyBboxPatch((7, 8), 2, 0.5, **box_style)
    ai_box.set_facecolor(colors['input'])
    ax.add_patch(ai_box)
    ax.text(8, 8.25, 'AI Mode\n🤖', ha='center', va='center', fontsize=11)
    
    # 5. Demo Mode (No API Key)
    demo_box = FancyBboxPatch((1, 8), 2, 0.5, **box_style)
    demo_box.set_facecolor(colors['input'])
    ax.add_patch(demo_box)
    ax.text(2, 8.25, 'Demo Mode\n🎭', ha='center', va='center', fontsize=11)
    
    # 6. Travel Info Input (AI Mode)
    input_ai_box = FancyBboxPatch((6.5, 7), 3, 0.5, **box_style)
    input_ai_box.set_facecolor(colors['input'])
    ax.add_patch(input_ai_box)
    ax.text(8, 7.25, 'Input Travel Info\n📝', ha='center', va='center', fontsize=11)
    
    # 7. Travel Info Input (Demo Mode)
    input_demo_box = FancyBboxPatch((0.5, 7), 3, 0.5, **box_style)
    input_demo_box.set_facecolor(colors['input'])
    ax.add_patch(input_demo_box)
    ax.text(2, 7.25, 'Input Travel Info\n📝', ha='center', va='center', fontsize=11)
    
    # 8. RAG Search (AI Mode Only)
    rag_box = FancyBboxPatch((6.5, 6), 3, 0.5, **box_style)
    rag_box.set_facecolor(colors['process'])
    ax.add_patch(rag_box)
    ax.text(8, 6.25, 'RAG Search\n🔍', ha='center', va='center', fontsize=11)
    
    # 9. Multi Agent Execution (AI Mode)
    agent_ai_box = FancyBboxPatch((6.5, 5), 3, 0.5, **box_style)
    agent_ai_box.set_facecolor(colors['process'])
    ax.add_patch(agent_ai_box)
    ax.text(8, 5.25, 'Multi Agent Run\n🤖', ha='center', va='center', fontsize=11)
    
    # 10. Demo Data Generation (Demo Mode)
    demo_data_box = FancyBboxPatch((0.5, 5), 3, 0.5, **box_style)
    demo_data_box.set_facecolor(colors['process'])
    ax.add_patch(demo_data_box)
    ax.text(2, 5.25, 'Generate Demo Data\n🎭', ha='center', va='center', fontsize=11)
    
    # 11. Success Check
    success_box = FancyBboxPatch((3.5, 4), 3, 0.5, **box_style)
    success_box.set_facecolor(colors['decision'])
    ax.add_patch(success_box)
    ax.text(5, 4.25, 'Generation Success?\n❓', ha='center', va='center', fontsize=11)
    
    # 12. Success - Display Results
    result_box = FancyBboxPatch((3.5, 3), 3, 0.5, **box_style)
    result_box.set_facecolor(colors['result'])
    ax.add_patch(result_box)
    ax.text(5, 3.25, 'Display Travel Plan\n📋', ha='center', va='center', fontsize=11)
    
    # 13. Failure - Error Handling
    error_box = FancyBboxPatch((7, 2), 2, 0.5, **box_style)
    error_box.set_facecolor(colors['result'])
    ax.add_patch(error_box)
    ax.text(8, 2.25, 'Error Handling\n⚠️', ha='center', va='center', fontsize=11)
    
    # 14. Additional Features
    additional_box = FancyBboxPatch((3.5, 2), 3, 0.5, **box_style)
    additional_box.set_facecolor(colors['input'])
    ax.add_patch(additional_box)
    ax.text(5, 2.25, 'Additional Features\n🔄', ha='center', va='center', fontsize=11)
    
    # 15. End
    end_box = FancyBboxPatch((4.5, 1), 1, 0.5, **box_style)
    end_box.set_facecolor(colors['end'])
    ax.add_patch(end_box)
    ax.text(5, 1.25, 'End\n🏁', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Arrow connections
    arrows = [
        # Main flow
        ((5, 11), (5, 10.5)),  # Start → App Launch
        ((5, 10), (5, 9.5)),   # App Launch → API Check
        
        # API Key branching
        ((6.5, 9), (8, 8.5)),  # Has API Key → AI Mode
        ((3.5, 9), (2, 8.5)),  # No API Key → Demo Mode
        
        # AI Mode flow
        ((8, 8), (8, 7.5)),    # AI Mode → Input
        ((8, 7), (8, 6.5)),    # Input → RAG Search
        ((8, 6), (8, 5.5)),    # RAG Search → Agent Run
        ((8, 5), (5, 4.5)),    # Agent Run → Success Check
        
        # Demo Mode flow
        ((2, 8), (2, 7.5)),    # Demo Mode → Input
        ((2, 7), (2, 6.5)),    # Input → (Skip)
        ((2, 6.5), (2, 5.5)),  # Skip → Demo Data
        ((2, 5), (5, 4.5)),    # Demo Data → Success Check
        
        # Result branching
        ((5, 4), (5, 3.5)),    # Success → Display Results
        ((6.5, 4), (8, 2.5)),  # Failure → Error Handling
        
        # Additional features and end
        ((5, 3), (5, 2.5)),    # Display Results → Additional Features
        ((5, 2), (5, 1.5)),    # Additional Features → End
        ((8, 2), (5, 2.5)),    # Error Handling → Additional Features
    ]
    
    # Draw arrows
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="black", ec="black", linewidth=2)
        ax.add_patch(arrow)
    
    # Branch labels
    ax.text(6.5, 9.1, 'Yes', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text(3.5, 9.1, 'No', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text(6.5, 4.1, 'Fail', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text(3.5, 4.1, 'Success', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Title
    ax.text(5, 11.8, 'AI Travel Planner - User Flow Diagram', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(color=colors['start'], label='Start'),
        patches.Patch(color=colors['input'], label='Input'),
        patches.Patch(color=colors['process'], label='Process'),
        patches.Patch(color=colors['decision'], label='Decision'),
        patches.Patch(color=colors['result'], label='Result'),
        patches.Patch(color=colors['end'], label='End')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('user_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("User flow diagram created: user_flow_diagram.png")

def create_detailed_flow_diagram():
    """Create detailed system flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Color definitions
    colors = {
        'ui': '#E3F2FD',        # Light blue - UI
        'ai': '#FFF3E0',        # Light orange - AI
        'data': '#F3E5F5',      # Light purple - Data
        'process': '#E8F5E8',   # Light green - Process
        'decision': '#FFEBEE'   # Light red - Decision
    }
    
    # Box style
    box_style = {
        'boxstyle': 'round,pad=0.3',
        'facecolor': 'white',
        'edgecolor': 'black',
        'linewidth': 1.5
    }
    
    # UI steps
    ui_steps = [
        (1, 13, "1. App Launch\n🌐", colors['ui']),
        (1, 12, "2. Sidebar Info\n📊", colors['ui']),
        (1, 11, "3. Travel Input\n📝", colors['ui']),
        (1, 10, "4. Input Validation\n✅", colors['ui']),
        (1, 9, "5. Input Summary\n📋", colors['ui']),
        (1, 8, "6. Multi Agent Button\n🤖", colors['ui']),
        (1, 7, "7. Progress Display\n⏳", colors['ui']),
        (1, 6, "8. Results Display\n📊", colors['ui']),
        (1, 5, "9. Additional Features\n🔄", colors['ui']),
        (1, 4, "10. Restart Option\n🔄", colors['ui'])
    ]
    
    # AI processing steps
    ai_steps = [
        (4, 13, "API Key Check\n🔑", colors['ai']),
        (4, 12, "LLM Initialization\n🤖", colors['ai']),
        (4, 11, "Tools Setup\n🔧", colors['ai']),
        (4, 10, "Agent Setup\n🎯", colors['ai']),
        (4, 9, "RAG Search\n🔍", colors['ai']),
        (4, 8, "Agent Execution\n⚡", colors['ai']),
        (4, 7, "Response Parsing\n📄", colors['ai']),
        (4, 6, "Result Validation\n✅", colors['ai']),
        (4, 5, "Error Handling\n⚠️", colors['ai'])
    ]
    
    # Data processing steps
    data_steps = [
        (7, 13, "Env Variables\n⚙️", colors['data']),
        (7, 12, "ChromaDB Connect\n🗄️", colors['data']),
        (7, 11, "Embedding Model\n🧠", colors['data']),
        (7, 10, "Vector Search\n🔍", colors['data']),
        (7, 9, "Context Generation\n📚", colors['data']),
        (7, 8, "Prompt Augmentation\n📝", colors['data']),
        (7, 7, "Response Generation\n💬", colors['data']),
        (7, 6, "Data Structuring\n📊", colors['data']),
        (7, 5, "Session Storage\n💾", colors['data'])
    ]
    
    # Decision points
    decision_points = [
        (10, 12, "API Key\nExists?", colors['decision']),
        (10, 10, "RAG\nActive?", colors['decision']),
        (10, 8, "Agent\nSuccess?", colors['decision']),
        (10, 6, "Parsing\nSuccess?", colors['decision']),
        (10, 4, "Additional\nFeatures?", colors['decision'])
    ]
    
    # Draw all boxes
    all_boxes = ui_steps + ai_steps + data_steps + decision_points
    
    for x, y, text, color in all_boxes:
        box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, **box_style)
        box.set_facecolor(color)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)
    
    # Arrow connections
    arrows = [
        # UI flow
        ((1, 12.7), (1, 12.3)),  # 1 → 2
        ((1, 11.7), (1, 11.3)),  # 2 → 3
        ((1, 10.7), (1, 10.3)),  # 3 → 4
        ((1, 9.7), (1, 9.3)),    # 4 → 5
        ((1, 8.7), (1, 8.3)),    # 5 → 6
        ((1, 7.7), (1, 7.3)),    # 6 → 7
        ((1, 6.7), (1, 6.3)),    # 7 → 8
        ((1, 5.7), (1, 5.3)),    # 8 → 9
        ((1, 4.7), (1, 4.3)),    # 9 → 10
        
        # AI flow
        ((4, 12.7), (4, 12.3)),  # API Check → LLM Init
        ((4, 11.7), (4, 11.3)),  # LLM → Tools
        ((4, 10.7), (4, 10.3)),  # Tools → Agent
        ((4, 9.7), (4, 9.3)),    # Agent → RAG
        ((4, 8.7), (4, 8.3)),    # RAG → Agent Exec
        ((4, 7.7), (4, 7.3)),    # Agent Exec → Parsing
        ((4, 6.7), (4, 6.3)),    # Parsing → Validation
        ((4, 5.7), (4, 5.3)),    # Validation → Error
        
        # Data flow
        ((7, 12.7), (7, 12.3)),  # Env → ChromaDB
        ((7, 11.7), (7, 11.3)),  # ChromaDB → Embedding
        ((7, 10.7), (7, 10.3)),  # Embedding → Vector
        ((7, 9.7), (7, 9.3)),    # Vector → Context
        ((7, 8.7), (7, 8.3)),    # Context → Prompt
        ((7, 7.7), (7, 7.3)),    # Prompt → Response
        ((7, 6.7), (7, 6.3)),    # Response → Structure
        ((7, 5.7), (7, 5.3)),    # Structure → Session
        
        # Cross flow
        ((1.4, 12), (3.6, 12)),  # UI → AI
        ((4.4, 11), (6.6, 11)),  # AI → Data
        ((4.4, 9), (6.6, 9)),    # AI → Data (RAG)
        ((7.4, 8), (9.6, 8)),    # Data → Decision
        ((10.4, 8), (4.4, 8)),   # Decision → AI
        ((4.4, 6), (9.6, 6)),    # AI → Decision
        ((10.4, 6), (1.4, 6)),   # Decision → UI
    ]
    
    # Draw arrows
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=15, fc="black", ec="black", linewidth=1.5)
        ax.add_patch(arrow)
    
    # Section labels
    ax.text(1, 13.5, 'UI Layer\nUser Interface', ha='center', va='center', 
            fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['ui']))
    
    ax.text(4, 13.5, 'AI Layer\nAI Processing', ha='center', va='center', 
            fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['ai']))
    
    ax.text(7, 13.5, 'Data Layer\nData Processing', ha='center', va='center', 
            fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['data']))
    
    ax.text(10, 13.5, 'Decision Points\nDecision Logic', ha='center', va='center', 
            fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['decision']))
    
    # Title
    ax.text(6, 13.8, 'AI Travel Planner - Detailed System Flow Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(color=colors['ui'], label='UI Layer'),
        patches.Patch(color=colors['ai'], label='AI Layer'),
        patches.Patch(color=colors['data'], label='Data Layer'),
        patches.Patch(color=colors['decision'], label='Decision Points')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('detailed_user_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Detailed system flow diagram created: detailed_user_flow_diagram.png")

def create_simple_flow_diagram():
    """Create a simple text-based flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Simple flow steps
    steps = [
        (5, 9, "Start", "#4CAF50"),
        (5, 8, "Launch App", "#2196F3"),
        (5, 7, "Check API Key", "#9C27B0"),
        (3, 6, "Demo Mode", "#FF9800"),
        (7, 6, "AI Mode", "#FF9800"),
        (3, 5, "Input Travel Info", "#2196F3"),
        (7, 5, "Input Travel Info", "#2196F3"),
        (7, 4, "RAG Search", "#FF9800"),
        (7, 3, "Multi Agent Run", "#FF9800"),
        (5, 2, "Display Results", "#F44336"),
        (5, 1, "End", "#607D8B")
    ]
    
    # Draw steps
    for x, y, text, color in steps:
        circle = plt.Circle((x, y), 0.3, color=color, ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Draw arrows
    arrows = [
        ((5, 8.7), (5, 8.3)),   # Start → Launch
        ((5, 7.7), (5, 7.3)),   # Launch → Check API
        ((4.7, 7), (3.3, 6.3)), # Check → Demo
        ((5.3, 7), (6.7, 6.3)), # Check → AI
        ((3, 5.7), (3, 5.3)),   # Demo → Input
        ((7, 5.7), (7, 5.3)),   # AI → Input
        ((7, 4.7), (7, 4.3)),   # AI Input → RAG
        ((7, 3.7), (7, 3.3)),   # RAG → Agent
        ((6.7, 3), (5.3, 2.3)), # Agent → Results
        ((3, 4.7), (5, 2.3)),   # Demo → Results
        ((5, 1.7), (5, 1.3)),   # Results → End
    ]
    
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=15, fc="black", ec="black", linewidth=2)
        ax.add_patch(arrow)
    
    # Title
    ax.text(5, 9.5, 'AI Travel Planner - Simple Flow', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('simple_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Simple flow diagram created: simple_flow_diagram.png")

if __name__ == "__main__":
    print("Creating AI Travel Planner user flow diagrams...")
    
    # Create simple flow diagram first
    create_simple_flow_diagram()
    
    # Create detailed flow diagram
    create_detailed_flow_diagram()
    
    # Create main user flow diagram
    create_user_flow_diagram()
    
    print("\nAll diagrams have been created!")
    print("- simple_flow_diagram.png: Simple overview")
    print("- detailed_user_flow_diagram.png: Detailed system flow")
    print("- user_flow_diagram.png: Main user flow") 