import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="FinTech: Cost & ROI Estimator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """Injects custom CSS for a modern, dark-mode neon aesthetic."""
    st.markdown("""
        <style>
        /* Neon Button Styling */
        .stButton>button {
            border: 1px solid #00f3ff;
            color: #00f3ff;
            background-color: transparent;
            transition: 0.3s;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #00f3ff;
            color: #121212;
            box-shadow: 0 0 10px #00f3ff;
        }
        
        /* Metric Styling overrides */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }
        
        /* Custom text classes for profits and losses */
        .neon-green { color: #39ff14; font-weight: bold; font-size: 1.2rem; }
        .neon-red { color: #ff073a; font-weight: bold; font-size: 1.2rem; }
        .neon-blue { color: #00f3ff; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CORE LOGIC & STATE MANAGEMENT
# ==========================================
def initialize_state():
    """Initializes session state for calculation history."""
    if 'history' not in st.session_state:
        st.session_state.history = pd.DataFrame(columns=[
            "Fixed Costs", "Variable Cost/Unit", "Selling Price", 
            "Units Sold", "Total Cost", "Revenue", "Net Profit", "ROI (%)"
        ])

def calculate_financials(fixed_costs: float, var_cost_per_unit: float, selling_price: float, units: int) -> dict:
    """Calculates all core financial metrics."""
    total_var_cost = var_cost_per_unit * units
    total_cost = fixed_costs + total_var_cost
    total_revenue = selling_price * units
    net_profit = total_revenue - total_cost
    
    # Handle division by zero
    roi = (net_profit / total_cost * 100) if total_cost > 0 else 0.0
    
    # Calculate Break-Even Point (BEP) in units
    contribution_margin = selling_price - var_cost_per_unit
    if contribution_margin > 0:
        bep_units = fixed_costs / contribution_margin
    else:
        bep_units = float('inf') # Never breaks even
        
    return {
        "total_cost": total_cost,
        "total_var_cost": total_var_cost,
        "total_revenue": total_revenue,
        "net_profit": net_profit,
        "roi": roi,
        "bep_units": bep_units
    }

def save_to_history(data: dict, inputs: dict):
    """Saves the current calculation to the pandas DataFrame in session state."""
    new_row = pd.DataFrame([{
        "Fixed Costs": inputs['fixed_costs'],
        "Variable Cost/Unit": inputs['var_cost_per_unit'],
        "Selling Price": inputs['selling_price'],
        "Units Sold": inputs['units'],
        "Total Cost": data['total_cost'],
        "Revenue": data['total_revenue'],
        "Net Profit": data['net_profit'],
        "ROI (%)": round(data['roi'], 2)
    }])
    st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

# ==========================================
# 3. VISUALIZATION FUNCTIONS
# ==========================================
def plot_break_even(fixed_costs, var_cost_per_unit, selling_price, max_units):
    """Generates an interactive Plotly Break-Even line chart."""
    x_vals = list(range(0, int(max_units * 1.5) + 10, max(1, int(max_units * 0.1))))
    costs = [fixed_costs + (var_cost_per_unit * x) for x in x_vals]
    revenues = [selling_price * x for x in x_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=costs, mode='lines', name='Total Cost', line=dict(color='#ff073a', width=3)))
    fig.add_trace(go.Scatter(x=x_vals, y=revenues, mode='lines', name='Total Revenue', line=dict(color='#39ff14', width=3)))
    fig.add_hline(y=fixed_costs, line_dash="dash", line_color="gray", annotation_text="Fixed Costs")

    fig.update_layout(
        title="Break-Even Analysis",
        xaxis_title="Units Produced/Sold",
        yaxis_title="Amount ($)",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

def plot_cost_breakdown(fixed_costs, total_var_cost):
    """Generates an interactive Plotly Pie chart for cost breakdown."""
    fig = px.pie(
        values=[fixed_costs, total_var_cost], 
        names=['Fixed Costs', 'Total Variable Costs'],
        title="Cost Breakdown",
        color_discrete_sequence=['#00f3ff', '#ff9900'],
        hole=0.4 # Makes it a modern donut chart
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=40, b=0))
    return fig

# ==========================================
# 4. UI COMPONENTS & LAYOUT
# ==========================================
def render_sidebar():
    """Renders the team recognition sidebar."""
    with st.sidebar:
        st.markdown("### 👨‍💻 Development Team")
        st.markdown("---")
        # EXAMINER FOCUS: Highly visible team section
        st.info("**[Student Name 1]**\n\nReg: [Registration Number 1]")
        st.info("**[Student Name 2]**\n\nReg: [Registration Number 2]")
        st.info("**[Student Name 3]**\n\nReg: [Registration Number 3]")
        st.markdown("---")
        st.markdown("<p style='font-size: 0.8rem; color: gray;'>Final Year ICT Project<br>Academic Year 2025-2026</p>", unsafe_allow_html=True)

def main():
    inject_custom_css()
    initialize_state()
    render_sidebar()

    # Main Header
    st.title("⚡ FinTech: Manufacturing Cost & ROI Estimator")
    st.markdown("Advanced financial modeling tool for analyzing manufacturing viability, break-even points, and dynamic profitability scenarios.")
    st.markdown("---")

    # Tabs for clean layout
    tab1, tab2, tab3 = st.tabs(["📊 Core Analysis", "🎛️ Sensitivity Scenarios", "📂 Calculation History"])

    with tab1:
        st.subheader("1. Financial Inputs")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fixed_costs = st.number_input("Total Fixed Costs ($)", min_value=0.0, value=10000.0, step=500.0)
        with col2:
            var_cost_per_unit = st.number_input("Variable Cost / Unit ($)", min_value=0.0, value=25.0, step=1.0)
        with col3:
            selling_price = st.number_input("Selling Price / Unit ($)", min_value=0.0, value=65.0, step=1.0)
        with col4:
            units_sold = st.number_input("Units Produced & Sold", min_value=0, value=500, step=10)

        if st.button("🚀 Calculate Financials", use_container_width=True):
            if selling_price <= var_cost_per_unit:
                st.warning("⚠️ **Warning:** Selling price is lower than or equal to variable cost. You will never break even!")

            # Calculate and Save
            results = calculate_financials(fixed_costs, var_cost_per_unit, selling_price, units_sold)
            save_to_history(results, {'fixed_costs': fixed_costs, 'var_cost_per_unit': var_cost_per_unit, 'selling_price': selling_price, 'units': units_sold})

            # Display Metrics
            st.markdown("### 2. Financial Report")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Cost", f"${results['total_cost']:,.2f}")
            m2.metric("Total Revenue", f"${results['total_revenue']:,.2f}")
            
            # Custom styled metrics for Profit/Loss and ROI
            if results['net_profit'] > 0:
                m3.markdown(f"**Net Profit:** <br><span class='neon-green'>+${results['net_profit']:,.2f}</span>", unsafe_allow_html=True)
                m4.markdown(f"**ROI:** <br><span class='neon-green'>{results['roi']:.2f}%</span>", unsafe_allow_html=True)
            elif results['net_profit'] < 0:
                m3.markdown(f"**Net Loss:** <br><span class='neon-red'>-${abs(results['net_profit']):,.2f}</span>", unsafe_allow_html=True)
                m4.markdown(f"**ROI:** <br><span class='neon-red'>{results['roi']:.2f}%</span>", unsafe_allow_html=True)
            else:
                m3.metric("Net Profit", "$0.00")
                m4.metric("ROI", "0.00%")

            # Break-even info
            with st.expander("🔍 View Detailed Insights", expanded=True):
                if results['bep_units'] != float('inf'):
                    st.info(f"**Break-Even Point:** You need to sell **{int(results['bep_units']) + 1}** units to start making a profit.")
                
                # Charts
                chart_col1, chart_col2 = st.columns([3, 2])
                with chart_col1:
                    st.plotly_chart(plot_break_even(fixed_costs, var_cost_per_unit, selling_price, units_sold), use_container_width=True)
                with chart_col2:
                    st.plotly_chart(plot_cost_breakdown(fixed_costs, results['total_var_cost']), use_container_width=True)

    with tab2:
        st.subheader("Sensitivity Analysis (What-If Scenarios)")
        st.write("Adjust the sliders below to see how changes in your market environment affect profitability.")
        
        scol1, scol2 = st.columns(2)
        with scol1:
            price_change = st.slider("Selling Price Fluctuation (%)", min_value=-50, max_value=50, value=0, step=5)
        with scol2:
            cost_change = st.slider("Variable Cost Fluctuation (%)", min_value=-50, max_value=50, value=0, step=5)
            
        new_price = selling_price * (1 + (price_change / 100))
        new_var_cost = var_cost_per_unit * (1 + (cost_change / 100))
        
        scen_results = calculate_financials(fixed_costs, new_var_cost, new_price, units_sold)
        
        st.markdown(f"**Adjusted Selling Price:** ${new_price:.2f} | **Adjusted Var. Cost:** ${new_var_cost:.2f}")
        
        sm1, sm2 = st.columns(2)
        profit_color = "neon-green" if scen_results['net_profit'] >= 0 else "neon-red"
        sm1.markdown(f"**Scenario Net Profit:** <br><span class='{profit_color}'>${scen_results['net_profit']:,.2f}</span>", unsafe_allow_html=True)
        sm2.markdown(f"**Scenario ROI:** <br><span class='{profit_color}'>{scen_results['roi']:.2f}%</span>", unsafe_allow_html=True)

    with tab3:
        st.subheader("Data Export & Calculation History")
        if st.session_state.history.empty:
            st.info("No calculations performed yet. Run a calculation in the 'Core Analysis' tab to see history.")
        else:
            st.dataframe(st.session_state.history, use_container_width=True)
            
            # Export to CSV
            csv = st.session_state.history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download History as CSV",
                data=csv,
                file_name="fintech_roi_history.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
