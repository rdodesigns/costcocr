# Receipt OCR Output Parser 

# Written by Matthew Adams, 2/1/15
# Current Version 1.0

# Changelog:
# 1.0: Initial version. Intended for parsing of item/item cost from a costco receipt.
# Assumes that each item is separated by a line, and within each line, all item data
# are separated by tabs. The item description is assumed to be the column prior to
# the item cost. All items, costs, and A marks parsed into lists.

# Function that displays desired line number (for debugging)
def displayline(file, line_num):
	file_1 = open(file)
	for i in range(0,line_num):
		line_read = file_1.readline()
	print '%r' %line_read
	file_1.close()
	return line_read

# Tests for specific character (used to deal with A/- cases)
def chartest(input, test_char):
	if input == test_char:
		output = 1
	else:
		output = 0
	return output

# Open text file, parse lines.
current_file = open('okout.txt')
file_whole = current_file.read()
parse_file = file_whole.split('\n')

'''
test = displayline('out.txt', 7)
print parse_file
'''

# initialize stuff
total = 0.0; rec_dict = {}; item_list = []; item_cost_list = []; A_list = [];

# Main parsing loop
for i in parse_file:
	item = []; item_cost = []; found_flag = 0; A_flag = 0; min_flag = 0
	n = i.split('\t')
	print n
	# if the last element in the list can be floated, assume it's the cost
	try: 
		item_cost = float(n[-1])
		item = n[-2]
		found_flag = 1
	# if last elementnot a float, remove letters at the end to look for '-' or 'A' 
	# characters, then search through prior columns in line.
	except:
		temp_list = n
		while (len(temp_list)>0 and found_flag == 0):
			temp = temp_list[-1]
			while (len(temp)>0 and found_flag == 0):
				A_flag = chartest(temp[-1],'A')
				min_flag = chartest(temp[-1],'-')
				temp = temp[:-1]
				try:
					item_cost = float(temp)
					found_flag = 1
					item = temp_list[-2]	
				except: pass
			temp_list.pop()
	
	# add item and cost to dict, lists, total
	if found_flag:
		# if minus flag found, deduct associated value from prior list item cost
		if min_flag:
			item_cost_list[-1] -= float(item_cost)
			total -= float(item_cost)
		else:
			rec_dict[item] = float(item_cost)
			total += float(item_cost)
			item_list.append(item)
			item_cost_list.append(item_cost)
			A_list.append(A_flag)
	else: pass

# Print everything		
print 'The dict is', rec_dict
print 
print 'The item list is', item_list
print 
print 'The cost list is', item_cost_list
print
print 'The A list is', A_list
print
print 'The total is $%.2f.' %total

if len(item_list) == len(item_cost_list) and len(item_list) == len(A_list):
	print 'The length of the list is %d' %len(item_list)
else:
	print 'The length of the lists do not match. Something is fucked.'
# Close file
current_file.close()	