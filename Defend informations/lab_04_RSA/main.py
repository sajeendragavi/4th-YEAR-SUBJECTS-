from base64 import b32encode, b32decode
from rsa import RSA
import sys

if __name__ == '__main__':
        filename = sys.argv[1]   #get file name as argument
        if len(sys.argv) == 2:
            rsa = RSA(p=199,q=179)
        else:
            rsa = RSA(p=int(sys.argv[2]),q=int(sys.argv[3]))
 
        with open(filename, 'rb') as file1:
            data = file1.read()
            print("\tP:", rsa.p, "\n\tQ:", rsa.q, "\n\tE:", rsa.e, "\n\tN:", rsa.n, "\n\tD:", rsa.d)
            str = b32encode(data)  #encodes bytes like object and return encoed bytes
            #print(str)
            dta = str.decode("ascii") #decode acscii string# retuurn the decoded byte
            #print(dta)
            print("Encrypting...")
            enc = rsa.encrypt_string(dta)
            with open(filename.split('.')[0] + ".encrypted", 'w',encoding="utf-8") as file2:
                file2.write(enc)
            print("Decrypting...")
            dec = rsa.decrypt_string(enc)
            restored = b32decode(dec)
            with open(filename.split('.')[0]  + ".decrypted", 'wb') as file4:
                file4.write(restored)
