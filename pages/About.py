import streamlit as st

def show_about():
    st.title("ℹ️ About Lagos Crime Prediction System")

    st.markdown("""
    Welcome to the **Lagos Crime Prediction System** — an AI-powered dashboard designed to visualize, analyze, and predict crime patterns across Lagos State.

    ### 🎯 Purpose
    - 🛡️ Support law enforcement and policymakers with actionable insights  
    - 🔍 Identify high-risk areas for proactive intervention  
    - 📅 Predict likely crime types based on time and location  

    ---

    ### 🧠 Technology Stack
    - 🐍 **Python** for backend and ML logic  
    - 📊 **Streamlit**, **Plotly**, and **Seaborn** for interactive visualizations  
    - 🧮 **Scikit-learn** for crime prediction modeling  
    - 📂 **Pandas** & **NumPy** for data preprocessing  

    ---

    ### 👨‍💻 Developer
    **Lucky Osehi**  
    Passionate about public safety, smart cities, and data-driven governance.  
    Reach out: [📧 Luckynize24@gmail.com](mailto:Luckynize24@gmail.com)

    ---
    """)

    # Optional: Team credits, future roadmap, or data disclaimer
    with st.expander("📌 Project Notes"):
        st.markdown("""
        - 🔐 Only authorized admins can access prediction logs  
        - 📍 Data is based on historical crime records and may not reflect real-time updates  
        - 📦 This tool is open for collaboration — contact us for partnership or feature requests.
        """)

    st.caption("© 2025 Lagos Crime Prediction System | Built with ❤️ using Streamlit")
    st.markdown("For issues or suggestions, please contact the admin.")