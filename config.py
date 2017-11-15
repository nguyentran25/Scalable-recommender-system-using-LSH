"""
config.py
Daniel Goldbach
2013 November

Constants, filenames, directories, etc.
"""

# Location of data sets for load_data.py
BOOKS_FILE = './Data/books.csv'
RATINGS_FILE = './Data/ratings.csv'

# LSH parameters
BLOCK_SIZE = 2   # ~ r
NUM_BLOCKS = 256  # ~ p
NUM_HASH_FUNCTIONS = 512 # ~ K
NUM_NEAREST_NEIGHBORS = 4 # ~ nn