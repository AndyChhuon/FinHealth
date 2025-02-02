import streamlit as st

from modules.chatbot import chatbot

with st.sidebar:
    st.logo("assets/chart_icon.png")
    st.markdown(
            f"""
            <div style="
                display: flex;
                flex-direction: column;
                font-size: 17px;
                gap: 5px;">
            <a class="sidebar-url" href="http://localhost:8501/" target="_self" style="text-decoration: none; color: white; width: 100%">
                Home
            </a>
            <a class="sidebar-url" href="http://localhost:8501/analysis" target="_self" style="text-decoration: none; color: white; width: 100%;">
                Personal Analysis
            </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    #st.page_link(page='http://localhost:8501/', label="Home")
    #st.page_link(page='http://localhost:8501/analysis', label="Personal Analysis")

st.markdown(
    r"""
    <style>
    .stAppHeader {
        border-bottom: 1px solid grey;
    }
    .stAppToolbar {
        top: 15px;
    }
    .stAppDeployButton {
        visibility: hidden;
        display: none;
    }
    .st-emotion-cache-hzo1qh {
        top: 11px;
    }
    .st-emotion-cache-6qob1r {
        border-right: 1px solid grey;
    }
    .stSidebar {
        width: 220px !important;
        background-color: rgb(25 29 37);
    }
    .st-emotion-cache-kgpedg {
        align-items: center;
        padding: 1rem 1.5rem 1.5rem 1rem;
    }
    .st-emotion-cache-13lvdqn {
        height: 2rem;
    }
    .sidebar-url {
        text-decoration: none;
        color: white; 
        width: 100%;
        border-radius: 7px;
        text-indent: 10px;
        line-height: 32px;
    }
    .sidebar-url:hover {
        background-color: rgb(47, 51, 61);
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True
)
st.title('Personal Analysis')


import streamlit as st

# Create the form
with st.form(key='financial_wellness_form'):
    # Risk Tolerance
    risk_tolerance = st.selectbox('What is your risk tolerance?', ['Low', 'Medium', 'High'])
    
    # Annual Salary
    annual_salary = st.number_input('What is your annual salary?', min_value=0, step=1000)
    
    # Investment Duration
    investment_duration = st.selectbox('How long are you planning to invest for?', 
                                      ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'])
    
    # Current Savings/Investments
    savings_investments = st.number_input('What is the total amount of savings or investments you currently have?', min_value=0, step=1000)
    
    # Debt Amount
    debt_amount = st.number_input('What is the total amount of debt you have?', min_value=0, step=1000)
    
    # Monthly Expenses
    monthly_expenses = st.number_input('What is your average monthly expense?', min_value=0, step=100)
    
    # Emergency Fund
    months_covered = st.number_input('How many months of expenses does your emergency fund cover?', min_value=0, step=1)
    
    # Financial Goals
    financial_goals = st.text_area('What are your primary financial goals? (e.g., retirement, buying a home, paying off debt, etc.)')
    
    # Tax Filing Status
    tax_status = st.selectbox('What is your tax filing status?', ['Single', 'Married', 'Head of Household'])
    
    # Investment Knowledge
    investment_knowledge = st.selectbox('How would you rate your knowledge of investing?', ['Novice', 'Intermediate', 'Experienced'])
    
    # Retirement Plans
    retirement_contribution = st.number_input('How much are you currently contributing to a retirement plan?', min_value=0, step=100)
    
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Handle form submission

prompt = """Provide general financial wellness advice based on the following principles:

1. **Risk Tolerance**: Explain the importance of understanding one’s risk tolerance when making investment decisions. Discuss how it affects the type of assets (stocks, bonds, real estate, etc.) an individual should consider.

2. **Investment Duration**: Provide guidance on how investment horizons (short-term, medium-term, and long-term) should influence investment strategies. Offer insights into how long-term investments typically have higher growth potential but come with more volatility.

3. **Emergency Fund**: Explain why having an emergency fund is crucial and suggest the ideal amount (typically 3-6 months of expenses). Discuss how it serves as a safety net in case of unexpected financial hardships.

4. **Debt Management**: Give advice on how to manage debt effectively. Discuss strategies like paying off high-interest debt first and how reducing debt can improve overall financial health.

5. **Retirement Planning**: Stress the importance of planning for retirement early and contributing consistently to retirement savings accounts like 401(k)s, IRAs, or similar plans. Offer general advice on how to start retirement planning.

6. **Investment Knowledge**: Suggest how increasing one’s knowledge of investing can lead to better decision-making. Recommend resources for learning about different investment types and strategies.

7. **Financial Goals**: Discuss the importance of setting clear financial goals (e.g., saving for a house, retirement, education) and how these goals can help guide investment and savings strategies. 

Keep it concise."""


if submit_button:
    prompt = f"""
        I need you to analyze the following personal financial data to help provide tailored advice:

        Risk Tolerance: {risk_tolerance}
        Annual Salary: ${annual_salary}
        Investment Duration: {investment_duration}
        Current Savings/Investments: ${savings_investments}
        Debt Amount: ${debt_amount}
        Monthly Expenses: ${monthly_expenses}
        Emergency Fund: {months_covered} months covered
        Financial Goals: {financial_goals}
        Tax Filing Status: {tax_status}
        Investment Knowledge: {investment_knowledge}
        Retirement Contribution: ${retirement_contribution}

        Based on this information, provide the following:

        1. Investment Strategy: What is the most appropriate investment strategy for this individual, considering their risk tolerance, investment duration, and investment knowledge?

        2. Concerns/Red Flags: Are there any concerns or red flags in their financial situation, such as high debt levels, insufficient emergency fund, or low retirement contributions?

        3. Improvement Suggestions: How can this individual improve their financial situation in terms of savings, investments, and managing debt?

        4. Focus Areas for Financial Goals: What types of financial goals should they focus on (short-term vs long-term) based on their current situation?

        Keep it concise.
        """



chatbot(prompt, submit_button)