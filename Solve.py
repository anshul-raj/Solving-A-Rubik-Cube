"""
ADA-PS4 Q4
Submitted by-
Himanshu Raj (2018038)
Anshul Raj (2018020)
"""
from rubik import *
from collections import deque
import time

def shortest_path(start, end):			#normal bfs to get the moves
	moves = list(quarter_twists)
	visited={}
	visited[start]=[]					#making a dictionary for visited perms as keys and moves to obtain them as values
	queue = deque()
	queue.append(start)					#starting node for bfs is start
	while(True):
		if(end in visited):				#if end is in visited, then print the moves
			return visited[end]
		if(len(queue)==0):				#if queue is empty then break the loop
			break
		u=queue.popleft()				#pop 1 element from queue
		for i in range(len(moves)):
			temp=perm_apply(moves[i],u)	#apply all 6 combinations of moves on u
			if(temp not in visited):
				visited[temp]=visited[u]+[moves[i]]	#note the moves to obtain them from starting perm
				queue.append(temp)		#add it to queue
	return None							#if end is not reached then no soltuion exists, hence return None

def shortest_path_optmized(start, end):	#omptimized bfs to get the moves
	if start==end:
		return []

	moves = list(quarter_twists)
	MyQueue = deque()
	MyQueue.append(start)
	visited = {start : []}
	depth = {start : 0}
	MovesMade = {start : -1}
	PathFollowed = {start : -1}

	R_MyQueue = deque()
	R_MyQueue.append(end)
	R_visited = {end : []}
	R_depth = {end : 0}
	R_MovesMade = {end : -1}
	R_PathFollowed = {end : -1}
	
	while(len(MyQueue)!=0 and len(R_MyQueue)!=0):

		new = MyQueue.popleft()
		
		if depth[new]==7:			#observation that depth=7 will give all perms
			break

		for move in moves:			#bfs from start
			new_state = perm_apply(move,new)	#applying all 6 combos on new

			if new_state not in visited:		#if not already visited then take a note of this
				visited[new_state] = 0
				MovesMade[new_state] = move
				PathFollowed[new_state] = new
				depth[new_state] = depth[new] + 1
				MyQueue.append(new_state)
			if new_state in R_visited:			#if we found the new state obtained in reverse bfs then we've got our path
				return calculatePath(new_state,MovesMade,PathFollowed,R_MovesMade,R_PathFollowed)
	
	# ----------------------------------- #

		new = R_MyQueue.popleft()	#bfs from end

		if R_depth[new]==7: 
			break

		for move in moves:					
			new_state = perm_apply(move,new)	#applying all 6 combos on new

			if new_state not in R_visited:		#if not already visited then take a note of this
				R_visited[new_state] = 0
				R_MovesMade[new_state] = move
				R_PathFollowed[new_state] = new
				R_depth[new_state] = R_depth[new] + 1
				R_MyQueue.append(new_state)

			if new_state in visited:		#if we found the new state obtained in forward bfs then we've got our path
				return calculatePath(new_state,MovesMade,PathFollowed,R_MovesMade,R_PathFollowed)
	return None		#if end not reached from start then return None, no solutions

def calculatePath(cur,moves_made,path_followed,R_moves_made,R_path_followed):
	ans = []
	current = cur
	while(moves_made[current]!=-1):
		ans.append(moves_made[current])
		current = path_followed[current]
		if current==-1:
			break
	
	ans = ans[::-1]

	current = cur
	while(R_moves_made[current]!=-1):
		ans.append(perm_inverse(R_moves_made[current]))
		current = R_path_followed[current]
		if current==-1:
			break

	return ans

def verification(start,sequence,result):		#for verifying the results
	current = start
	for i in range(len(sequence)):
		current = perm_apply(sequence[i],current)
	return current==result

def printSequence(seq):							#for printing the sequence of moves
	if seq==None:
		print(seq)
		return
	print(list(map(lambda x:quarter_twists_names[x],seq)))

if __name__ == "__main__":
	start = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
	end = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)

	start_time = time.time()					
	ans1 = shortest_path_optmized(start,end)	#calculating the optimized path
	end_time = time.time()

	printSequence(ans1)							#answer and execution time
	print("Optimized Execution time :",end_time - start_time)
	print()
	
	start_time = time.time()
	ans2 = shortest_path(start,end)				#calculating path
	end_time = time.time()

	printSequence(ans2)							#answer and execution time
	print("Normal Execution time :",end_time - start_time)

	if(ans1!=None):
		if(verification(start,ans1,end)):	#verifying result
			print('Verified')