import streamlit as st

# Title and introduction
st.title("FinTech: Manufacturing Cost & ROI Estimator")
st.write("Welcome! This tool helps estimate Return on Investment (ROI) based on manufacturing costs.")

# 1. Input Variables (This acts like the input() function)
st.header("Enter Your Financial Data")

fixed_costs = st.number_input("Total Fixed Costs (e.g., Rent, Salaries in $)", min_value=0.0, value=1000.0)
variable_cost_per_unit = st.number_input("Variable Cost per Unit (in $)", min_value=0.0, value=20.0)
selling_price = st.number_input("Selling Price per Unit (in $)", min_value=0.0, value=50.0)
units_sold = st.number_input("Number of Units Produced and Sold", min_value=0, value=100)

# 2. Logic and Math Operations
# When the user clicks the button, the calculations run
if st.button("Calculate ROI"):
    
    # Basic math to find costs and revenue
    total_variable_cost = variable_cost_per_unit * units_sold
    total_cost = fixed_costs + total_variable_cost
    total_revenue = selling_price * units_sold
    net_profit = total_revenue - total_cost
    
    # Output section (This acts like the print() function)
    st.header("Financial Report")
    st.write(f"**Total Cost:** ${total_cost}")
    st.write(f"**Total Revenue:** ${total_revenue}")
    
    # 3. If-Else Logic for Profit, Loss, and ROI
    if total_cost > 0:
        # Calculate ROI percentage
        roi = (net_profit / total_cost) * 100
        
        if net_profit > 0:
            st.success(f"**Net Profit:** ${net_profit}")
            st.success(f"**Return on Investment (ROI):** {roi:.2f}%")
            st.write("Result: The manufacturing process is currently profitable.")
            
        elif net_profit < 0:
            # We use abs() to show the loss as a positive number
            st.error(f"**Net Loss:** ${abs(net_profit)}") 
            st.error(f"**Return on Investment (ROI):** {roi:.2f}%")
            st.write("Result: You are operating at a loss. Consider reducing costs or raising the price.")
            
        else:
            st.info("Result: Break-even point reached. No profit, no loss.")
    else:
        st.warning("Total cost is zero. Please enter valid costs to calculate ROI.")
