from bloom_filter import BloomFilter
# from pybloom import BloomFilter
fruit = BloomFilter(100000, error_rate=0.001, filename='/tmp/fruit.bloom')
# fruit = BloomFilter(100000, error_rate=0.001)
[fruit.add(x) for x in ['apple', 'pear', 'orange']]
print('aple' in fruit)