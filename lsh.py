# MIN HASH, TRA VE LIST GOM CAC PHAN TU LA 

from __future__ import division
import re
import random
import time
import operator
# from load_data import Database

class LSH():
	def __init__(self, K, p, r, nn, items):
		self.nextPrime = 4294967311
		self.maxID = 2**32-1
		self.K = K
		self.p = p
		self.r = r
		self.num_nearest_neighbors = nn
		self.num_items = 0
		self.items = items # danh sach co phan tu thu i la tap hop cac user thich item thu i
		self.cluster = {} # cac item co tap r ma bam giong nhau duoc bam vao cung 1 cum
						  # khoa cua moi cum la tap r gia tri la gia tri bam cua tung ham bam doi voi mot item,
						  # neu cac item co tap r gia tri giong nhau thi tuc la cung khoa, va duoc bam vao cung 1 cum
		self.hash = {} # moi item se co mot tap gom p khoa, ung voi p cum
		self.similarity = {} # danh sach co phan tu thu i la danh sach cac item tuong tu item thu i

	# chon ra K gia tri ngau nhien
	def pick_random_coeffs(self, K):
		randList = []
		while K > 0:
			randIndex = random.randint(0, self.maxID)
			while randIndex in randList:
				randIndex = random.randint(0, self.maxID)
			randList.append(randIndex)
			K = K - 1
		return randList

	# chon ra ho K ham bam
	def pick_family_MIH_functions(self):
		self.coeffA = self.pick_random_coeffs(self.K)
		self.coeffB = self.pick_random_coeffs(self.K)

	def locality_senstive_hashing(self, item_id):
		self.num_items += 1
		print "Item: ", item_id
		self.hash[item_id] = self.minHash(item_id)
		if len(self.cluster) == 0:
			for key in self.hash[item_id]:
				self.cluster[key] = [item_id] #them item dang xet vao cum co khoa key
		else:
			for key in self.hash[item_id]:
				if self.cluster.has_key(key):
					self.cluster[key].append(item_id)
				else:
					self.cluster[key] = [item_id]

	def minHash(self, item_id):
		cnt = 0
		keys_list = [] # danh sach p khoa cua item dang xet o p cum
		for i in xrange(self.p):
			hashCodes_list = [] # danh sach cac hashCode cua item dang xet o cum thu i,
								# day cung chinh la khoa cua item o cum do
			for j in xrange(self.r):
				minHashCode = self.nextPrime + 1
				for user in self.items[item_id]:
					hashCode = (self.coeffA[cnt] * user + self.coeffB[cnt]) % self.nextPrime 
					if hashCode < minHashCode:
						minHashCode = hashCode
				hashCodes_list.append(minHashCode)
				cnt += 1
			keys_list.append(tuple(hashCodes_list))
		return keys_list

	def find_similarity_items(self, item_id):
		freq_of_items_list = {} # so lan xuat hien cua cac item trong cung cum voi item dang xet
		for key in self.hash[item_id]:
			for item in self.cluster[key]: # cac item co khoa la key
				if item != item_id:
					if freq_of_items_list.has_key(item):
						freq_of_items_list[item] += 1
					else:
						freq_of_items_list[item] = 1
		freq_of_items_list = sorted(freq_of_items_list.items(), key=operator.itemgetter(1))
		freq_of_items_list = freq_of_items_list[-self.num_nearest_neighbors:]
		items_list = [int(i[0]) for i in freq_of_items_list]
		self.similarity[item_id] = items_list

	def remove_item_from_clusters(self, item_id):
		for key in self.hash[item_id]:
			self.cluster[key].remove(item_id)
			if len(self.cluster[key]) == 0:
				self.cluster.pop(key, None)

	def find_all_similarity(self):
		for i in xrange(self.num_items):
			self.find_similarity_items(i)
		return self.similarity

	# def similarity_calc(self):
	# 	for i in xrange(self.num_items):
	# 		nn_tmp = {}
	# 		for mih in self.hash[i]:
	# 			list_users = self.cluster[mih]
	# 			for user in list_users:
	# 				if nn_tmp.has_key(user):
	# 					nn_tmp[user] += 1
	# 				else:
	# 					nn_tmp[user] = 1
	# 		nn_tmp = sorted(nn_tmp.items(), key=operator.itemgetter(1))
	# 		nn_tmp = nn_tmp[-self.num_nearest_neighbors:]
	# 		# nn_tmp.remove((i, 32))
	# 		list_tmp = [int(i[0]) for i in nn_tmp]
	# 		self.similarity.append(list_tmp)

# test:
if __name__ == '__main__':	
	model_base = Database()
	model_base.load_data_from_ratings_file()
	model_lsh = LSH(256, 128, 2,10, model_base.set_of_user)
	model_lsh.pick_family_MIH_functions()
	for item_id in xrange(10):
		model_lsh.locality_senstive_hashing(item_id)
	for item_id in xrange(10):
		print item_id
		model_lsh.remove_item_from_clusters(item_id)
	print model_lsh.cluster
	model_lsh.find_similarity_items(99)
	print model_lsh.similarity[99]
	model_lsh.similarity_calc()
	for i in model_lsh.hash[1]:
		print i, len(model_lsh.cluster[i])

	for i in model_lsh.hash:
		print len(model_lsh.hash[i])

	for i in model_lsh.similarity:
		print len(i)
		print model_lsh.similarity