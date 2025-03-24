import numpy as np 
import pandas as pd
import streamlit as st

def corner_method(df):
    '''assuming the problem to be balanced here'''
    if sum(df.iloc[0:-1,-1]) != sum(df.iloc[-1,0:-1]): 
        return "Unbalanced transportation problem"
    output_cost_arr = []

    while len(df)>1:
        st.write()
        st.write('-'*20)
        df.iloc[-1,-1]= sum(df.iloc[0:-1,-1])
        st.write(df)
        st.write()
        element, supply, demand = df.iloc[0,0], df.iloc[0,-1], df.iloc[-1,0]
        st.write("the element in the north west corner is ", element)
        st.write("corresponding demand is ", demand, " and supply is ", supply)
        
        minn = min(demand, supply)
        if demand < supply:
            st.write("We fulfill the demand of ", demand, " of ", df.columns[0], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.iloc[0,-1] -= minn
            df.drop(df.columns[0],axis='columns', inplace=True)
        elif demand > supply: 
            st.write("We fulfill the supply of ", supply, " of ", df.index[0], " thus allocating ", supply ," items to cost " , element)
            st.write()
            df.iloc[-1,0] -= minn
            df.drop(df.index[0],inplace=True)
        else: 
            st.write("We fulfill the demand & supply of ", demand, " of ", df.columns[0]," and ", df.index[0], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.drop(df.index[0],inplace=True)
            df.drop(df.columns[0],axis='columns', inplace=True)
        output_cost_arr.append([element,minn])
        
    st.write("The cost we get from the solution of North West corner method is ")
    cost_parts = [f"{x[0]} x {x[1]}" for x in output_cost_arr]
    cost_expression = " + ".join(cost_parts)
    output_cost = sum([x[0]*x[1] for x in output_cost_arr])

    st.markdown("##### The cost we get from the solution of Vogel's approximation method is:")
    st.markdown(f"**{cost_expression} = {output_cost}**")

    return output_cost
        
        
def least_cost_method(df):
    

    output_cost_arr = []    
    while len(df)>1:
        a = df.iloc[0:-1, 0:-1]
    #the element with lowest cost has the following position
        row, col = list(np.unravel_index(np.argmin(a), a.shape))
        #corresponding supply and demands are
        demand, supply = df.iloc[-1,col],df.iloc[row, -1]
        element = df.iloc[row, col]
        minn = min(demand, supply)
        df.iloc[-1,-1]= sum(df.iloc[0:-1,-1])
        st.write()
        st.write("-"*20)
        st.write(df)
        st.write()
        st.write("the least cost in the above matrix is ", element)
        st.write("the corresponding supply is ", supply ," and demand is ", demand)
        
        if demand < supply:
            st.write("We fulfill the demand of ", demand, " of ", df.columns[col], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.iloc[row,-1] -= minn
            df.drop(df.columns[col],axis='columns', inplace=True)
        elif demand > supply: 
            st.write("We fulfill the supply of ", supply, " of ", df.index[row], " thus allocating ", supply ," items to cost " , element)
            st.write()
            df.iloc[-1,col] -= minn
            df.drop(df.index[row],inplace=True)
        else: 
            st.write("We fulfill the demand & supply of ", demand, " of ", df.columns[col]," and ", df.index[row], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.drop(df.index[row],inplace=True)
            df.drop(df.columns[col],axis='columns', inplace=True)
        output_cost_arr.append([element,minn])

    st.write("The cost we get from the solution of Least cost method is ")
    cost_parts = [f"{x[0]} x {x[1]}" for x in output_cost_arr]
    cost_expression = " + ".join(cost_parts)
    output_cost = sum([x[0]*x[1] for x in output_cost_arr])

    st.markdown("##### The cost we get from the solution of Vogel's approximation method is:")
    st.markdown(f"**{cost_expression} = {output_cost}**") 

    return output_cost
    
def vam_method(df): 
    m,n = df.shape
    m,n = m-2 , n-2
    # in this method we will be required one additional row and column for penalties 
    df.loc['penalties']= np.nan
    df['penalties'] =np.nan

    output_cost_arr = []
    st.write("In the Vogel's Approximation method, we calculate penalties for each row and column, where penalty = second lowest cost in row(or col) - lowest cost in row (or col)")
    while len(df)> 2:
        m,n = df.shape
        m,n = m-2 , n-2
    #calculate row penalties
        
        for i in range(len(df)-2): 
            temp_arr = sorted(df.iloc[i, 0:-2])
            if len(temp_arr)> 1:
                df.iloc[i,-1] = temp_arr[1]-temp_arr[0]
            elif len(temp_arr)==1: 
                df.iloc[i,-1] = temp_arr[0]
        
    #calculate column penalties
        for i in range(len(df.iloc[0])-2): 
            temp_arr = sorted(df.iloc[ 0:-2,i])
            if len(temp_arr) > 1:
                df.iloc[-1,i] = temp_arr[1]-temp_arr[0]
            elif len(temp_arr)==1: 
                df.iloc[-1,i] = temp_arr[0]
    
        #a list containing all penalities 
        penalties = np.hstack((df.iloc[0:-2,-1], df.iloc[-1, 0:-2]))
        ind = np.argmax(penalties)
    
        if ind < m: 
            #this is a row penalty
            #our focus element will be the lowest cost in this row
            
            col = np.argmin(df.iloc[ind, 0:-2])
            row = ind
            element = df.iloc[row, col]
            
        else: 
            #this is a column penalty
            #our focus element will be the lowest cost in this column
            col = ind - m
            row = np.argmin(df.iloc[0:-2,col])
            element= df.iloc[row, col]
            st.write(f"element = {element}")
    
    
        #now we will apply the standard approach of allocation
        #now we have the target element , we also want the demand and supply corresponding to it
        demand , supply = df.iloc[-2, col], df.iloc[row, -2]
    

        minn = min(demand, supply)
        df.iloc[-2,-2]= sum(df.iloc[0:-2,-2])
        st.write()
        st.write("-"*20)
        st.write(df)
        st.write()
        if ind < m:
            st.write(f"the highest penalty is of the row corresponding to {df.index[ind]} ")
        else: 
            st.write(f"the highest peanlty is of the column corresponding to {df.columns[ind - m]}")
        st.write("the least cost here is ", element)
        st.write("the corresponding supply is ", supply ," and demand is ", demand)
        
        if demand < supply:
            st.write("We fulfill the demand of ", demand, " of ", df.columns[col], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.iloc[row,-2] -= minn
            df.drop(df.columns[col],axis='columns', inplace=True)
        elif demand > supply: 
            st.write("We fulfill the supply of ", supply, " of ", df.index[row], " thus allocating ", supply ," items to cost " , element)
            st.write()
            df.iloc[-2,col] -= minn
            df.drop(df.index[row],inplace=True)
        else: 
            st.write("We fulfill the demand & supply of ", demand, " of ", df.columns[col]," and ", df.index[row], " thus allocating ", demand ," items to cost " , element)
            st.write()
            df.drop(df.index[row],inplace=True)
            df.drop(df.columns[col],axis='columns', inplace=True)
        output_cost_arr.append([element,minn])

    st.write("The cost we get from the solution of Vogel's approximation method is ")

    cost_parts = [f"{x[0]} x {x[1]}" for x in output_cost_arr]
    cost_expression = " + ".join(cost_parts)
    output_cost = sum([x[0]*x[1] for x in output_cost_arr])

    st.markdown("##### The cost we get from the solution of Vogel's approximation method is:")
    st.markdown(f"**{cost_expression} = {output_cost}**")

    return output_cost

