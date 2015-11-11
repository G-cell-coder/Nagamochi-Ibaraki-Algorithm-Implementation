#===========================IMPLEMENTATION OF NAGAMOCHI-IBARAKI ALGORITHM====================

import random

#----------------------------CRITICAL EDGES - COMPUTING FUNCTION----------------------
def critical_edges(n, l):
    cnt = 0                                     # Counter to update on No. of Criticcal edges
    for i in range(1,n):
        for j in range(0,i):
            if(adj[i][j]>0):                    # Check if there is a link between i & j 
                adj[i][j]-=1                    # Delete the Link between i & j
                localdegree = nagamochi(adj, n) # Calling algorithm to compute the connectivity
                adj[i][j]+=1                    # Re-add the deleted link between i & j
                if(localdegree<l):              # If current connectivity < original connectivity
                    cnt+=1                      # Increase the critical edges
    return cnt                                  # Return the final value of critical edge

#----------------------------NEXTNODE MA-ORDERING - COMPUTING FUNCTION-----------------
def get_nextnode(nag_matrix, src_list, tot):
    edge_adj = 0                                # Edge adjancency to src_list
    for i in range(tot):
        if(i in src_list):
            continue                            # If current node is in src_list ignore this loop
        edge = 0
        for j in src_list:                      # Foreach node j compute cost to src_list
            edge += nag_matrix[i][j]
        if (edge>=edge_adj):                    # If the current number of edge is max,then it is the next node
            edge_adj= edge
            nxt_node = i
    return nxt_node                             # Return the next node

#----------------------------MA-ORDERING COMPUTING FUNCTION----------------------------
def get_MAOrder(nag_matrix, tot):
    choosenode = random.randint(0,tot-1)        # Choosing a random node
    ma_order = [choosenode]                     
    while(len(ma_order) <tot):                  # Form the next node by appending
        ma_order.append(get_nextnode(nag_matrix,ma_order,tot)) 
    return ma_order                             # Return computed ma_ordering pattern

#----------------------------DEGREE - COMPUTING FUNCTION-------------------------------
def get_degree(nag_matrix, n):
    return sum(nag_matrix[n])                   # Return the degree of the selected node


#----------------------------MERGING GRAPH - FUNCTION----------------------------------
def merge_node(src_mat,s,t):
    src_mat[s][t]= src_mat[t][s]= 0             # Initialize to zero the links between nodes to be merged
    new_len = len(src_mat)-1                    # Compute length of new matrix
    tgt_mat = [[0 for i in range(new_len)] for j in range(new_len)]
    p=0
    for i in range(new_len+1):
        q=0
        flag=0
        for j in range(0,i+1):
            if(i==max(s,t)):                    # Ignoring one of the nodes to be merged
                flag=1
                break
            if(i==min(s,t)):                    # Consider the other node & sum it with ignored node
                tgt_mat[p][q] = tgt_mat[q][p] = src_mat[min(s,t)][j]+src_mat[max(s,t)][j]
            else:                               # Compute the links for rest of the nodes
                if(j!=s and j!=t):
                    tgt_mat[p][q] = tgt_mat[q][p] = src_mat[i][j]
                else:
                    if(j==max(s,t)):
                        continue
                    tgt_mat[p][q] = tgt_mat[q][p] = src_mat[i][s]+src_mat[i][t]
            if(p==q):
                tgt_mat[p][q]=0
            q+=1
        if(flag==0):
            p+=1    
    return tgt_mat
                
#-----------------------------IMPLEMENTATION OF NAGAMOCHI-IBARAKI ALGORITHM-----------------------
def nagamochi(nag_matrix, tot):
    if(tot==2):                                 # Return the degree of the last node if only 2 nodes in graph
        return get_degree(nag_matrix,0)      
    ma_order = get_MAOrder(nag_matrix,tot)       # First form the MA Ordering
    last_ind = len(ma_order)-1                  # Get index of last node
    lambda_g = get_degree(nag_matrix,ma_order[last_ind]) # Get degree of the last node
    nag_matrix=merge_node(nag_matrix,ma_order[last_ind],ma_order[last_ind-1]) # Merge the last 2 nodes
    return (min(lambda_g,nagamochi(nag_matrix, tot-1))) # Recursively compute connectivity till the graph contracts to 2 noded graph

#------------------------------GRAPH GENERATING FUNCTION------------------------------------------
def genearate_graph(n, maxedges):
    global adj
    cnt = 0                                     # Counter for track of current number of edges
    while(cnt<maxedges):                        # Check if maxedges already added
        for i in range(n):                      
            for j in range(n):
                if (i == j):                    # Exclude self-loops
                    adj[i][j] = adj[j][i] = 0
                else:
                    x = random.randint(0,1)     # Generate a random 0/1
                    if (x == 1):                # If 1, add the link between i & j
                        adj[i][j] = adj[j][i] = adj[i][j]+1
                        cnt+=x                  # Increament the number of edges in graph
                        if (cnt >= maxedges):   # Check if max edges reached
                            break
            if (cnt >= maxedges):
                break

n=22                                            # Set the number of nodes to 22
print("No. OF EDGES\tDEGREE\tLAMBDA\tCRITICAL EDGES")
print("============\t======\t======\t==============")
for m in range(40,405,5):                       # Varies the addition of edges from 40 to 400, 405 is upperlimt which is excluded
    adj=cpy=[[0 for i in range(n)] for j in range(n)]
    di = 2*m/n                                  # Compute the average degree with the standard formulation 2* (max_edges)/(No. of Nodes)
    generate_graph(n,m)                         # Generated a graph of 22 nodes & m edges
    l = nagamochi(adj, n)                       # Compute the connectivity of the graph
    criticaledges = critical_edges(n,l)                 # Compute the critical edge of the graph
    print(str(m)+"\t\t"+str(di)+"\t"+str(l)+"\t"+str(criticaledges)) # Print the results
