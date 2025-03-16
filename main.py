def calc_z_ratio(df,c,m,n):
    #calcualte z values and zj-cj values
    df.iloc[m+1,1]="zj"
    z=[df.iloc[1:m+1,0] @ df.iloc[1:m+1,alpha+2]  for alpha in range(n+m)]
    df.iloc[m+1,2:n+m+2]= z

    df.iloc[m+2,1]="zj-cj"
    df.iloc[m+2, 2:n+m+2]= np.subtract(z,c)
    entering_column__pos_index = np.argmin((df.iloc[m+2, 2:n+m+2])) +2
    entering_variable =df.iloc[0, entering_column__pos_index]
    print("entering_variable is ", entering_variable)


    #calcuate ratio on the basis of entering variable 
    ratios = np.divide(
        df.iloc[1: m+1,1],
          df.iloc[1:m+1, entering_column__pos_index],
          where=df.iloc[1:m+1, entering_column__pos_index] != 0
          )
    ratios = [x  if x>=0 else "-ve" for x in ratios]
    df.iloc[1:m+1,-1] = ratios

    exiting_row__pos_index = np.argmin(ratios) +1
    exiting_variable =df.index[exiting_row__pos_index]
    print("exiting_variable is ", exiting_variable)
    return (entering_variable, entering_column__pos_index, exiting_variable, exiting_row__pos_index)


def simplex_func(c, A, b, maximisation=True): 
    #assuming the lpp problem is to maximise z= cx subject to conditions Ax<= b
    m,n = len(A), len(A[0])
    print("m=",m,'n=',n)
    #m= number of rows of A which is exactly the number of conditions/equations
    # n = number of variables 
    basis = [f"s{i}" for i in range(1, m+1)]
    cost_dict = {**{f"x{i}": c[i] for  i in range(n)}, **{x:0 for x in basis}}
    c = list(cost_dict.values())
    df = pd.DataFrame(
        columns=[np.NaN," c -> "]+c+[np.NaN],
        index=["B"] + basis + [np.NaN, np.NaN]
        )
    df.iloc[0]=['cb', 'xb']+[f"x{i}" for i in range(1, n+1)]+basis+["Ratio"]
    df.iloc[1:m+1,0]= [cost_dict[x] for x in basis]
    df.iloc[1: m+1,1]=b
    df.iloc[1:m+1,2:n+2]=A
    df.iloc[1:m+1,n+2:n+m+2]=np.eye(m, dtype=int)

    #now our dataframe is ready for operations 

    ###first iteration 
    entering_variable, entering_column__pos_index, exiting_variable, exiting_row__pos_index=calc_z_ratio(df,c,m,n)
    print(df.fillna(" "))

    #analyse the situation and decide whether we have to go to next iteration or not

    #if no - we reached optimal solution
    #break


    #if yes - we need more iteration
    

    #transitioning to next iteration
    pivot_element = df.iloc[exiting_row__pos_index, entering_column__pos_index]
    df.iloc[exiting_row__pos_index, 1: n+m+2] /= pivot_element
    for i in range(1,m+1): 
        if i != exiting_row__pos_index:
            df.iloc[i, 1:n+m+2] -= df.iloc[exiting_row__pos_index, 1: n+m+2] * df.iloc[i,entering_column__pos_index]
    

    calc_z_ratio(df,c,m,n)
    #again analyse
    df = df.fillna(" ")
    print(df)

c = [3,5,4]
A = [[2,3,0],[0,2,5],[3,2,4]]
b=[8,10,15]
simplex_func(c,A,b)
