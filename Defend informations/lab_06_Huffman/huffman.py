import heapq
import os

class HeapNode:                         #Build a tree of the above process
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None     #used objects to maintain tree structure
		self.right = None

	def __cmp__(self, other):
		if(other == None):
			return -1
		if(not isinstance(other, HeapNode)):
			return -1
		return self.freq > other.freq

	def __lt__(self, other):
		return self.freq < other.freq


class HuffmanCoding:
	def __init__(self, path):  #path as file located place
		self.path = path
		self.heap = []    #columnNames = [] defines an empty list   #  object path
		self.codes = {}    #(char: code,   }
		self.reverse_mapping = {}       #{code ; char,  }

	# functions for compression:

	def make_frequency_dict(self, text):    #Building frequency dictionary
		frequency = {}     #columnNames = {} defines an empty dict
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		#print('check',frequency)
		return frequency    #return the composed of a collection of (character, frequency) pairs

	def make_heap(self, frequency):
		for key in frequency:
			#print(key)
			#print(frequency[key])
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)     #Push the value item onto the heap, maintaining the heap invariant
		#print('check node:',node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)    #Pop and return the smallest item from the heap
			node2 = heapq.heappop(self.heap)
			#print('check heap:',self.heap)
			#print('check n2:',node2)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)   #Push the value item onto the heap


	def make_codes_helper(self, root, current_code): #check the root and make the code
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			#print('check code',self.codes)
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")
		#print('check:code',current_code)


	def make_codes(self):                 #create code
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):    #text will encode here
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
			#print('encode text',self.codes[character])
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"       #put 0 infront

		padded_info = "{0:08b}".format(extra_padding) #and filling till make 8 bit format
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
			#print('byte check',b)
		#print('abyte check',b)
		return b      # returns an array of bytes of the given size and initialization values


	def compress(self):  #argument as file
		filename, file_extension = os.path.splitext(self.path)     #split the file name and extension
		output_path = filename + ".bin"     #creting output  file

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:    #r+-Open for reading and writing. /wb -file is opened for writing in binary mode
			text = file.read()
			text = text.rstrip()   #returns a copy of the string with trailing characters removed
			#print(text)
			frequency = self.make_frequency_dict(text)  #find the frequency have each character
			# print("Frequency:", frequency)
			self.make_heap(frequency)
			self.merge_nodes()
			#print("nodes:", self.merge_nodes)
			self.make_codes()  #create code checking roots
			#print("Codes:", self.codes)
			encoded_text = self.get_encoded_text(text)
			#print("Encoded text:", encoded_text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			#print("Encodedp text:", padded_encoded_text)
			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
		return output_path


	""" functions for decompression: """

	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)   #Returns an integer value, which is equivalent  of binary string in the given base.


		padded_encoded_text = padded_encoded_text[8:]  #from index  8 slice
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			#print(self.reverse_mapping)
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character    #get again character
				current_code = ""

		return decoded_text


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)   #read one byte:
			while len(byte) > 0:
				byte = ord(byte)   # return an integer representing the Unicode code point of that
				bits = bin(byte)[2:].rjust(8, '0')   #byte in to bits and set 0 s to fill 8 bits
				bit_string += bits
				byte = file.read(1)
			#print('show:',bit_string)
			encoded_text = self.remove_padding(bit_string)
			# print(encoded_text)
			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)
		return output_path
