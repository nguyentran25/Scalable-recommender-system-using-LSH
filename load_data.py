#LOAD_DATA

import pandas as pd
# import os
import config

class Database():
	def __init__(self):
		self.num_items = 0
		self.set_of_user = [] #list gom cac phan tu la tap hop, phan tu thu i la tap hop cac user da rate item thu i
		self.book_titles_list = [] #danh sach ten cua sach, phan tu thu i la ten cua sach thu i
		self.top_rated_books = []
		self.top_popular_books = []

	def create_set_of_user(self, ratings_base):
		map_item_to_users = {} #anh xa tu item den list cac user da rate cho item do
		size = ratings_base.shape[0]
		for i in xrange(size):
			item_id = ratings_base[i][0]
			if map_item_to_users.has_key(item_id):
				if ratings_base[i][2] >=3:
					map_item_to_users[item_id].append(ratings_base[i][1])
			else:
				map_item_to_users[item_id] = [ratings_base[i][1]]

		for i in map_item_to_users.keys():
			i = int(i)
			self.set_of_user.append(set(map_item_to_users[i]))
		self.num_items = len(self.set_of_user)

	def load_data_from_ratings_file(self):
		r_cols = ['book_id', 'uid', 'rating', 'unix_timestamp']
		ratings_base = pd.read_csv(config.RATINGS_FILE, sep=',', names=r_cols, encoding='latin-1')
		ratings_base = ratings_base.as_matrix()
		ratings_base[:, :2] -= 1 # chuan hoa du lieu, bat dau tu chi so 0
		self.create_set_of_user(ratings_base)

	def load_data_from_books_file(self):
		books_base = pd.read_csv(config.BOOKS_FILE)
		# create list of book titles
		for i in xrange(self.num_items):
			self.book_titles_list.append(books_base['title'][i])

		# create top 10 rated books list
		sorted_books_base1 = books_base.sort_values(by = ['average_rating','ratings_count'], ascending=False)
		sorted_books_base1 = sorted_books_base1.reset_index(drop=True)
		for i in xrange(10):
			self.top_rated_books.append([sorted_books_base1['title'][i], round(sorted_books_base1['average_rating'][i], 2)])

		# create top 10 popular books list
		sorted_books_base2 = books_base.sort_values(by = ['ratings_count', 'average_rating'], ascending=False)
		sorted_books_base2 = sorted_books_base2.reset_index(drop=True)
		for i in xrange(10):
			self.top_popular_books.append([sorted_books_base2['title'][i],\
			 sorted_books_base2['ratings_count'][i], round(sorted_books_base2['average_rating'][i], 2)])

		# delete
		del books_base
		del sorted_books_base1, sorted_books_base2

	def find_name_of_book(self, string):
		matching = [x for x in xrange(self.num_items) if string in self.book_titles_list[x].lower()]
		return matching

	def add_item(self):
		self.num_items += 1
		print "Nhap ten sach: "
		item_name = raw_input()
		print "Nhap cac user thich sach nay (cach nhau boi khoang trang (space),\
				 nhan enter de ket thuc viec nhap): "
		user_rates_list = raw_input()
		user_rates_list = [int(x.strip()) for x in user_rates_list.split()]
		self.set_of_user.append(set(user_rates_list))
		self.book_titles_list.append(item_name)
		return self.num_items - 1


	def update_item_rates(self, item_id):
		print "Nhap id cua cac user (cach nhau boi khoang trang (space), nhan enter de ket thuc viec nhap): "
		user_rates_list = raw_input()
		user_rates_list = [int(x.strip()) for x in user_rates_list.split()]
		user_rates_list = set(user_rates_list)
		self.set_of_user[item_id] = self.set_of_user[item_id].union(user_rates_list)
		

# test

# model_base = Database()
# model_base.load_data_from_ratings_file()
# model_base.load_data_from_books_file()

# print " moi nhap"
# string = raw_input()
# string = string.lower()
# print "cac sach co ten"
# matching = model_base.find_name_of_book(string)

# a =[1,2,3]
# model_base.update_item_rates(100)
# for i in model_base.set_of_user[100]:
# 	print i + 10