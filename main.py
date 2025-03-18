import streamlit as st
import numpy as np
import pandas as pd
from algorithms import *
st.title("Transportation Problem Solver")
st.text("Since any transportation problem can be seen as the problem of transportation from 'm' number of factories to 'n' number of warehouses. So we will stick to this context in this solver.")
st.subheader("Enter the dimensions of cost matrix: ")

col1, col2 = st.columns(2, gap='large', vertical_alignment='center',border=False)
with col1:
    num_rows = st.number_input(label="number of rows/ number of factories ", max_value=20, min_value=1, value=3)
with col2 : 
    num_cols = st.number_input(label="number of columns/ number of warehouses ", max_value=20, min_value=1, value=3)



with st.form(key = "dataframe_matrix", clear_on_submit=False, enter_to_submit=True, border = False): 

    st.subheader("Enter the cost matrix: ")
    A = []
    for row in range(num_rows):
        row_input = []
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            with cols[col_idx] : 
                input = st.number_input("", value=5, key = f"row {row} and col {col_idx}")
            row_input.append(input)
        A.append(row_input)

    st.subheader("Enter the supply matrix: ")
    S=[]
    cols = st.columns(num_rows)
    for i in range(num_rows): 
        with cols[i]: 
            input = st.number_input(f"supply by F{i+1}", value = 1, key = f"supply row {i}")
        S.append(input)


    st.subheader("Enter the demands matrix: ")
    D = []
    cols = st.columns(num_cols)
    for i in range(num_cols): 
        with cols[i]: 
            input = st.number_input(f"demand by W{i+1}", value = 1, key = f"demand col {i}")
        D.append(input)

    st.subheader("Algorithm to use: ")
    algo = st.radio(label='Algorithm to use: ', options=['North-West corner method', 'Least cost method', "Vogel's approximation method"], index = 2, horizontal = True, label_visibility = "collapsed")
    submit_button = st.form_submit_button("Solve")

if submit_button: 
    m,n = len(A), len(A[0])
    
    st.header("Problem:")
    st.text("Here W1 represent Warehouse 1   and similarly F1 represent Factory 1 and so on.")
    if sum(S) == sum(D):
        df = pd.DataFrame(0,index = [f'F{i}' for i in range(1, m+1)] +['demands'], columns= [f'W{i}' for i in range(1, n+1)]+['supplies'],dtype = int)
        df.iloc[0:-1, 0:-1] = A
        df.iloc[0:-1, -1]=S
        df.iloc[-1, 0:-1] = D

    elif sum(S)< sum(D): 
        #introduce a dummy supply 
        st.write("Since we are short of supply here, we add a dummy supplier with zero costs, to make this problem a balanced transportation problem")
        df = pd.DataFrame(0,index = [f'F{i}' for i in range(1, m+1)] +['dummy']+['demands'], columns= [f'W{i}' for i in range(1, n+1)]+['supplies'],dtype = int)
        df.iloc[0:-2, 0:-1] = A
        df.iloc[0:-2, -1]=S
        df.iloc[-2,0:-1]=0
        df.iloc[-1, 0:-1] = D
        df.iloc[-2,-1]=sum(D) - sum(S)
    
    else: 
        #introduce a dummy demand 
        st.write("Since we are short of demand here, we add a dummy warehouse with zero costs, to make this problem a balanced transportation problem")
        df = pd.DataFrame(0,index = [f'F{i}' for i in range(1, m+1)] +['demands'], columns= [f'W{i}' for i in range(1, n+1)]+['dummy']+['supplies'],dtype = int)
        df.iloc[0:-1, 0:-2] = A
        df.iloc[0:-1, -1]=S
        df.iloc[-1, 0:-2] = D
        df.iloc[0:-1, -2]=0
        df.iloc[-1, -2] = sum(S) - sum(D)

    df.iloc[-1,-1]= max(sum(S), sum(D))


    st.write(df)
    st.write("Our goal is to allocate different supply to different demands in such a way that we have to pay the least cost")
    st.write("We have different algorithms to find such allocations: Here we are using ")
    st.markdown(f"**{algo}**")

    if algo == "Vogel's approximation method": 
        vam_method(df.copy())
    elif algo == 'North-West corner method':
        corner_method(df.copy())
    elif algo =='Least cost method': 
        least_cost_method(df.copy())
