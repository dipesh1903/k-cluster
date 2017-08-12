
from math import sqrt
from PIL import Image, ImageDraw
import random
class bicluster:
	def __init__(self,vec,left=None,right=None, distance=0.0,id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance


def getdata(filename):
	lines = [line for line in open(filename,'r')]
	
	colnames = lines[0].strip().split('\t')[1:]
	
	rowname=[]
	data=[]
	for line in lines[1:]:
		
		p = line.strip().split('\t')
		rowname.append(p[0])
		data.append([float(x) for x in p[1:]])
	

	return rowname,colnames,data


	

def pearson(d1,d2):
	
	
	sum1 = sum(d1)
	sum2 = sum(d2)

	sumsq1 = sum([pow(i,2) for i in d1])
	sumsq2 = sum([pow(i,2) for i in d2])

	sump = sum([d1[i]*d2[i] for i in range(len(d2))])

	num = sump - (sumsq1*sumsq2)/len(d1)
	den = sqrt((sumsq1 - pow(sum1,2)/len(d1))* (sumsq2 - pow(sum2,2)/len(d1)))
	if den == 0: return 0

	return 1.0 - (num/den)
	


# def hcluster(rows, distance = pearson):
# 	distances={}
# 	clusterid = -1
	
# 	clust = [bicluster(rows[i],id=i) for i in range(len(rows))]
# 	y = len(clust[0].vec)
	
	
# 	while len(clust)>1:
		
# 		lowestpair = (0,1)
# 		closest = distance(clust[0].vec, clust[1].vec)

# 		for i in range(len(clust)):
# 			for j in range(i+1,len(clust)):
# 				if (clust[i].id, clust[j].id) not in distances:
# 						distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

# 				d = distances[(clust[i].id, clust[j].id)]
# 				if d<closest:
# 					lowestpair = (i,j)
# 					closest = d

# 		merge = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0 for i in range(y)]
# 		newcluster = bicluster(merge, left = clust[lowestpair[0]], right = clust[lowestpair[1]],
# 		distance = closest, id = clusterid)
# 		clusterid -= 1
# 		del clust[lowestpair[1]]
# 		del clust[lowestpair[0]]
# 		clust.append(newcluster)
		
# 	return clust[0]


# def printclust(clust,labels=None,n=0):
# # indent to make a hierarchy layout
# 	for i in range(n): print (' ', end='')
# 	if clust.id<0:
# 	# negative id means that this is branch
# 		print ('-')
# 	else:
# 	# positive id means that this is an endpoint
# 		if labels==None: print (clust.id)
# 		else: print (labels[clust.id])
# 	# now print the right and left branches
# 	if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
# 	if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)

# def height(clust):
# 	if clust.left==None and clust.right==None: return 1
# 	return getheight(clust.left)+ getheight(clust.right)

# def getdepth(clust):
# 	if clust.left == None and clust.right==None: return 0

# 	return max(getdepth(clust.left), getdepth(clust.right))+ clust.distance

# def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
# # height and width
# 	h=getheight(clust)*20
# 	w=1200
# 	depth=getdepth(clust)
# 	# width is fixed, so scale distances accordingly
# 	scaling=float(w-150)/depth
# 	# Create a new image with a white background
# 	img=Image.new('RGB',(w,h),(255,255,255))
# 	draw=ImageDraw.Draw(img)
# 	draw.line((0,h/2,10,h/2),fill=(255,0,0))
# 	# Draw the first node
# 	drawnode(draw,clust,10,(h/2),scaling,labels)
# 	img.save(jpeg,'JPEG')def kcluster(rows,distance=pearson,k=4):
# Determine the minimum and maximum values for each point
def kcluster(rows,distance=pearson,k=4):
	ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
	for i in range(len(rows[0]))]
	
	# Create k randomly placed centroids
	clusters=[[random.random( )*(ranges[i][1]-ranges[i][0])+ranges[i][0]
	for i in range(len(rows[0]))] for j in range(k)]
	
	lastmatches=None
	for t in range(100):
		print ('Iteration %d' % t)
		bestmatches=[[] for i in range(k)]
		# Find which centroid is the closest for each row
		
		for j in range(len(rows)):
			row=rows[j]
			bestmatch=0
			for i in range(k):
				d=distance(clusters[i],row)
				if d<distance(clusters[bestmatch],row): bestmatch=i
			bestmatches[bestmatch].append(j)
		# If the results are the same as last time, this is complete
		if bestmatches==lastmatches: break
		lastmatches=bestmatches

		for i in range(k):
			avgs=[0.0]*len(rows[0])
			
			if len(bestmatches[i])>0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m]+=rows[rowid][m]
				for j in range(len(avgs)):
					avgs[j]/=len(bestmatches[i])
				clusters[i]=avgs
	return bestmatches

