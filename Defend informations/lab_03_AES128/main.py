from sys import argv
from aes128 import encrypt_block, decrypt_block
import hashlib


def write_to_bfile(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)


def read_from_bfile(file_name):
    file_to_encode = open(file_name, 'rb')
    data = file_to_encode.read()
    file_to_encode.close()
    return data


def main():
    if not argv[1] or not argv[2]:
        print("main.py file_to_crypt key_file")

    file_name = argv[1]
    key_file = argv[2]

    # files for results
    file_name_encoded = "encoded_" + file_name
    file_name_decoded = "decoded_" + file_name

    # data to encrypt
    data = read_from_bfile(file_name)   # the plain text as byte data
    #print('data check',data)
    if not data:
        print("file is empty. nothing to encrypt")
        return
    # print("data to encrypt: ", data)

    input_key = read_from_bfile(key_file)
    if not input_key:
        print("key is empty. try again")
        return
    if len(input_key) > 16:   #check the length of input key
        print("key is too long. try again")
        return
    for symbol in input_key:
        if symbol > 0xff:  #check whether represented in the hexadecimal numeral system
            print('key must contain only latin alphabet and numbers')
            return
    key = hashlib.md5(input_key).digest()    #contain hexadecimal digits  key b'O\x03j\xb9s\xf10d\\\x08\xd8\xf5j\x7f\x95\xa0'

    # encryption
    encrypted_data = []
    temp = []   #add the text ,from byte by byte
    flag = False
    for byte in data:
        flag = True
        temp.append(byte)   #byte as one symbols in data message
        #print('check temp true',temp)

        if len(temp) == 16:
            flag = False
            encrypted_part = encrypt_block(temp, key)   #import from aes128
            encrypted_data.extend(encrypted_part)
            del temp[:]
    if flag:
        #print('check flag',flag) #test
        for i in range(16 - len(temp)):
            temp.append(0x0)
            #print('check temp type',temp) #test
       # print('check encrypt type') #test
        encrypted_data.extend(encrypt_block(temp, key))

    write_to_bfile(file_name_encoded, bytes(encrypted_data))
    # print("encoded: ", encrypted_data)

    # decryption
    decrypted_data = []
    temp = []
    flag = False
    for byte in bytes(encrypted_data):
        flag = True
        temp.append(byte)
        if len(temp) == 16:
            flag = False
            decrypted_part = decrypt_block(temp, key)
            decrypted_data.extend(decrypted_part)
            del temp[:]
    if flag:
        for i in range(16 - len(temp)):
            temp.append(0x0)
        decrypted_data.extend(decrypt_block(temp, key))

    write_to_bfile(file_name_decoded, bytes(decrypted_data))
    # print("decoded: ", decrypted_data)


if __name__ == "__main__":
    main()
