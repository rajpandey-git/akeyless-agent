import streamlit as st
import os
import json
from dotenv import load_dotenv
from akeyless_gemini_agent import AkeylessClient, AkeylessGeminiAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Akeyless AI Assistant",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better dark mode visibility
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4dabf7;
        text-align: center;
        padding: 1rem 0;
    }
    .secret-card {
        background-color: #2d3748;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4dabf7;
        color: #e2e8f0;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
    }
    .stat-label {
        font-size: 1rem;
        color: #ffffff;
        opacity: 0.95;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    .user-message {
        background-color: #1e3a5f;
        border-left: 4px solid #4dabf7;
    }
    .agent-message {
        background-color: #2d4a2e;
        border-left: 4px solid #69db7c;
    }
    
    /* Fix input text visibility */
    .stChatInput textarea {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
    }
    
    /* Fix general text visibility */
    p, span, div {
        color: #e2e8f0 !important;
    }
    
    /* Headers in dark mode */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'akeyless_client' not in st.session_state:
    st.session_state.akeyless_client = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def initialize_clients():
    """Initialize Akeyless and AI clients"""
    try:
        akeyless_access_id = os.getenv("AKEYLESS_ACCESS_ID")
        akeyless_access_key = os.getenv("AKEYLESS_ACCESS_KEY")
        akeyless_gateway_url = os.getenv("AKEYLESS_GATEWAY_URL", "https://api.akeyless.io")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not all([akeyless_access_id, akeyless_access_key, gemini_api_key]):
            st.error("❌ Missing environment variables. Please check your .env file.")
            return False
        
        st.session_state.akeyless_client = AkeylessClient(
            access_id=akeyless_access_id,
            access_key=akeyless_access_key,
            gateway_url=akeyless_gateway_url
        )
        
        st.session_state.agent = AkeylessGeminiAgent(
            st.session_state.akeyless_client,
            gemini_api_key
        )
        
        st.session_state.authenticated = True
        return True
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        return False

# Header
st.markdown('<div class="main-header">🔐 Akeyless AI Assistant</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://www.akeyless.io/wp-content/uploads/2021/06/akeyless-logo.svg", width=200)
    st.markdown("---")
    
    if not st.session_state.authenticated:
        st.info("👋 Welcome! Initializing connection...")
        if st.button("🔌 Connect to Akeyless", type="primary"):
            with st.spinner("Connecting..."):
                if initialize_clients():
                    st.success("✅ Connected successfully!")
                    st.rerun()
    else:
        st.success("✅ Connected to Akeyless")
        
        st.markdown("### 📊 Quick Stats")
        try:
            stats = st.session_state.akeyless_client.count_secrets_by_type()
            counts = stats.get('counts', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Secrets", counts.get('total', 0))
                st.metric("Static", counts.get('static', 0))
            with col2:
                st.metric("Rotated", counts.get('rotated', 0))
                st.metric("Dynamic", counts.get('dynamic', 0))
        except:
            st.warning("Unable to load stats")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Actions")
        if st.button("📋 List All Secrets"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "List all my secrets"
            })
            st.rerun()
        
        if st.button("📊 Secret Statistics"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Give me detailed statistics about my secrets"
            })
            st.rerun()
        
        st.markdown("---")
        if st.button("🔄 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("🚪 Disconnect"):
            st.session_state.authenticated = False
            st.session_state.akeyless_client = None
            st.session_state.agent = None
            st.session_state.chat_history = []
            st.rerun()

# Main content
if not st.session_state.authenticated:
    st.info("👈 Click 'Connect to Akeyless' in the sidebar to get started")
    
    # Show features
    st.markdown("### ✨ Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🤖 AI-Powered Chat
        - Natural language queries
        - Conversational interface
        - Smart secret retrieval
        """)
    
    with col2:
        st.markdown("""
        #### 🔐 Secret Management
        - View all secret types
        - Get secret values
        - Metadata inspection
        """)
    
    with col3:
        st.markdown("""
        #### 📊 Analytics
        - Secret statistics
        - Type breakdown
        - Quick actions
        """)

else:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📁 Secret Browser", "📊 Analytics"])
    
    # Tab 1: Chat Assistant
    with tab1:
        st.markdown("### 💬 Ask me anything about your secrets!")
        st.markdown("<p style='color: #a0aec0; margin-bottom: 2rem;'>Type your questions below and I'll help you manage your Akeyless secrets.</p>", unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong style="color: #4dabf7;">👤 You:</strong><br/><span style="color: #ffffff;">{message["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message agent-message"><strong style="color: #69db7c;">🤖 Agent:</strong><br/><span style="color: #ffffff;">{message["content"]}</span></div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Type your question here... (e.g., 'Get the secret MyFirstSecret')")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get agent response
            with st.spinner("🤖 Agent is thinking..."):
                try:
                    response = st.session_state.agent.chat(user_input)
                    st.session_state.chat_history.append({
                        "role": "agent",
                        "content": response
                    })
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "agent",
                        "content": f"Error: {str(e)}"
                    })
            
            st.rerun()
    
    # Tab 2: Secret Browser
    with tab2:
        st.markdown("### 🔍 Browse Your Secrets")
        st.markdown("<p style='color: #a0aec0;'>Search and explore your Akeyless secrets by path and type.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            path_input = st.text_input("Path", value="/", placeholder="Enter path (e.g., /prod)")
        with col2:
            secret_type = st.selectbox("Filter by Type", ["All", "Static", "Rotated", "Dynamic"])
        
        if st.button("🔍 Search", type="primary"):
            with st.spinner("Searching..."):
                try:
                    filter_type = None if secret_type == "All" else secret_type.lower()
                    secrets = st.session_state.akeyless_client.list_secrets(path_input, filter_type)
                    
                    items = secrets.get('items', [])
                    
                    if items:
                        st.success(f"✅ Found {len(items)} secrets")
                        
                        for item in items:
                            item_name = item.get('item_name', 'Unknown')
                            item_type = item.get('item_type', 'Unknown')
                            
                            with st.expander(f"🔐 {item_name} ({item_type})", expanded=False):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.markdown(f"<p style='color: #a0aec0;'><strong>Type:</strong> {item_type}</p>", unsafe_allow_html=True)
                                    st.markdown(f"<p style='color: #a0aec0;'><strong>Path:</strong> {item_name}</p>", unsafe_allow_html=True)
                                
                                with col2:
                                    if st.button(f"📥 Get Value", key=f"get_{item_name}"):
                                        try:
                                            if "STATIC" in item_type:
                                                result = st.session_state.akeyless_client.get_static_secret(item_name)
                                            elif "ROTATED" in item_type:
                                                result = st.session_state.akeyless_client.get_rotated_secret(item_name)
                                            else:
                                                result = {"error": "Type not supported"}
                                            
                                            if "error" not in result:
                                                if result.get("type") == "structured":
                                                    st.json(result.get("fields"))
                                                else:
                                                    st.code(result.get("value"))
                                            else:
                                                st.error(result.get("error"))
                                        except Exception as e:
                                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("ℹ️ No secrets found at this path")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Tab 3: Analytics
    with tab3:
        st.markdown("### 📊 Secret Analytics")
        st.markdown("<p style='color: #a0aec0; margin-bottom: 2rem;'>Visual overview of your secrets distribution and statistics.</p>", unsafe_allow_html=True)
        
        try:
            stats = st.session_state.akeyless_client.count_secrets_by_type()
            counts = stats.get('counts', {})
            items_by_type = stats.get('items_by_type', {})
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{counts.get('total', 0)}</div>
                    <div class="stat-label">Total Secrets</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="stat-number">{counts.get('static', 0)}</div>
                    <div class="stat-label">Static Secrets</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <div class="stat-number">{counts.get('rotated', 0)}</div>
                    <div class="stat-label">Rotated Secrets</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <div class="stat-number">{counts.get('dynamic', 0)}</div>
                    <div class="stat-label">Dynamic Secrets</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Breakdown by type
            st.markdown("### 📋 Secrets by Type")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 style='color: #4dabf7;'>Static Secrets</h4>", unsafe_allow_html=True)
                static_items = items_by_type.get('static', [])
                if static_items:
                    for item in static_items:
                        st.markdown(f"<p style='color: #e2e8f0;'>🔹 <code>{item}</code></p>", unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No static secrets")
            
            with col2:
                st.markdown("<h4 style='color: #4dabf7;'>Rotated Secrets</h4>", unsafe_allow_html=True)
                rotated_items = items_by_type.get('rotated', [])
                if rotated_items:
                    for item in rotated_items:
                        st.markdown(f"<p style='color: #e2e8f0;'>🔹 <code>{item}</code></p>", unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No rotated secrets")
            
            # Chart
            st.markdown("---")
            st.markdown("<h3 style='color: #4dabf7;'>📈 Distribution Chart</h3>", unsafe_allow_html=True)
            
            chart_data = {
                'Type': ['Static', 'Rotated', 'Dynamic', 'Other'],
                'Count': [
                    counts.get('static', 0),
                    counts.get('rotated', 0),
                    counts.get('dynamic', 0),
                    counts.get('other', 0)
                ]
            }
            
            st.bar_chart(chart_data, x='Type', y='Count', use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Unable to load analytics: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #a0aec0; padding: 1rem;'>
    <p style='color: #a0aec0;'>🔐 Akeyless AI Assistant | Powered by Gemini AI | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)