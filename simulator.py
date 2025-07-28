import streamlit as st

st.title("Fancy Calculator 💡")

form = st.form('Cost Calculator')
# User Inputs
a = form.number_input("Enter value A:", value=1.0)
b = form.number_input("Enter value B:", value=3.0)
submit = form.form_submit_button('Calculate')

def calculation(a,b):
    res = a * b
    return res

# Output
result = calculation(a,b)
if submit:
    st.metric("Result (A * B)", result)