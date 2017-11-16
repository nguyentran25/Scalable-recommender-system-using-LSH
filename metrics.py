#Caculate truth jaccard and find top nearest neighbor of item
from __future__ import division
import time
from lsh import LSH
import operator


# size = int(num_items * (num_items - 1) / 2) # Kich thuoc cua ma tran tam giac duoc luu duoi dang mang
# jaccard_similarity = [0 for x in range(size)]
# estjaccard_similarity = [0 for x in range(size)]
# def get_triangle_index(i, j, num_items):
#   if i == j:
#     sys.stderr.write("Ma tran tam giac khong co i == j")
#     sys.exit(1)
#   # vi trong ma tran a[i][j] = a[j][i] nen ta chi can luu a[i][j] va doi cho i, j neu muon tra a[j][i]
#   if j < i:
#     temp = i
#     i = j
#     j = temp
#   k = int(i * (num_items - (i + 1) / 2.0) + j - i) - 1
#   return k

# def jaccard_calc(num_items, set_of_user):
# 	print "\nCalculating Jaccard Similarities..."
# 	t0 = time.time()
# 	for i in range(0, num_items):
# 		set1 = set_of_user[i]
# 		for j in range(i+1, num_items):
# 			set2 = set_of_user[j]
# 			jaccard_similarity[get_triangle_index(i, j)] = (len(s1.intersection(s2)) / len(s1.union(s2)))

# chon ra k item gan voi item dang xet nhat
# def find_nearest_neighbors_item():
# 	similarity_list = [] # phan tu thu i chua k item gan voi item i nhat
# 	for 


def jaccard_calc(num_items, set_of_user):
	similarity_list = [] # phan tu thu i chua k item gan voi item i nhat
	print "\nCalculating Jaccard Similarities..."
	t0 = time.time()
	for i in range(0, num_items):
		if (i % 100) == 0:
			print "  (" + str(i) + " / " + str(num_items) + ")"
		temp = {}
		set1 = set_of_user[i]
		for j in range(0, num_items):
			set2 = set_of_user[j]
			J = (len(set1.intersection(set2)) / len(set1.union(set2)))
			if j != i:
				temp[j] = J
		temp = sorted(temp.items(), key=operator.itemgetter(1))
		#xoa phan tu thu i
		items_list = []
		for i in temp[-4:]:
			items_list.append(i[0])
		similarity_list.append(set(items_list))

	elapsed = (time.time() - t0)
	print "\nCalculating all Jaccard Similarities took %.2fsec" % elapsed
	return similarity_list


def accuracy_calc(pred, true, num_items):
	s1 = set()
	s2 = set()
	acc = []
	for i in xrange(num_items):
		s1 = set(pred[i])
		s2 = set(true[i])
		acc.append((len(s1.intersection(s2)) / len(s1.union(s2))))
	result = sum(acc) / num_items
	return result