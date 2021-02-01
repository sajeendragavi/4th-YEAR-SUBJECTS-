import rsa
import crypto
import sys
sys.modules['Crypto'] = crypto
import os
from crypto.Hash import SHA256  #import relevant algorithm module  #SHA-2-family   SHA256


def hash_file(message_file):
    h = SHA256.new()        #piece of message to hash can be passed to new()
    with open(message_file, "rb") as f:
        while True:
            buf = f.read(1024) #don't want to store the entire file in memory, you can transfer it in pieces.
            #print('check buf:',buf)
            if len(buf) == 0:
                break
            h.update(buf)  #update to concatinate parts
    #print(h)
    #print( h.digest())
    return h.digest()  # hash like array baytov #Return the digest of the data passed to the update() method so far.


def make_signature(message_file, key): #encryption using msg file and private key

    h = hash_file(message_file)

    # crypto hash with closed keys
    signature = rsa.encrypt(h, key) #make a signature using rsa ,encrypt the hash code
    #print('check:',signature)
    # digital sign in file
    signature_file_name = input("signature filename:")   #create a new file as any name to save the signature
    with open(signature_file_name, "wb") as f:
        f.write(signature)

    print("Signature saved in file '{0}'".format(signature_file_name))

    return signature_file_name

# check


def check_signature(message_file, signature_file, key):  #descrypt using public key
    # read hash file
    h1 = hash_file(message_file)

    # encrypt
    signature = None
    with open(signature_file, "rb") as f:
        signature = f.read()

    try:
        h2 = rsa.decrypt(signature, key)
        #print('check:',h2)
    except rsa.pkcs1.DecryptionError:
        return False

    return (h1 == h2)   #checking the 2 hashes and return about they are same


def main():
    try:
        message_file = sys.argv[1]    #get the file as argument
    except IndexError:
        print("input error")
        return

    if not os.path.exists(message_file):
        print("file doesn't exist")
        return

    (privkey, pubkey) = rsa.newkeys(2048) #with a key size of nbits to generate a public/private key pair (rsa.PublicKey, rsa.PrivateKey)
    #print('check prk',privkey)
    #print('check puk',pubkey)

    signature_file = make_signature(message_file, privkey)  #encryption with message as a bytestring and with the public_key from the previous result
    filename = input("file with signature:")
    is_valid = check_signature(message_file, filename, pubkey) #descryption  message as the encrypted bytestring and with the private_key from the first result.

    if is_valid:
        print("All it's okay.")
    else:
        print("Wrong signature.")


if __name__ == '__main__':
    main()
