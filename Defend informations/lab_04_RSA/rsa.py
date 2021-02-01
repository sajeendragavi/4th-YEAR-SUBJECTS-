import crypto
import sys
sys.modules['Crypto'] = crypto
from Crypto.Util import number
from random import randrange


class RSA(object):
    def __init__(self, p=None, q=None, bits=8):
        if not p:
            p = number.getPrime(bits)
       # print('check p;',p)
        if not q:
            q = number.getPrime(bits)
        #print('check q;',q)
        self.p = p if number.isPrime(p) else exit(-1)
        self.q = q if number.isPrime(q) else exit(-1)
        self.n = p * q # Their product n = p * q is calculated, which is called the modulus.
        self.phi = (p - 1) * (q - 1) # The value of the Euler function of the number n is calculated:
        self.e = self.get_e(self.phi, bits) # An integer is selected that is relatively prime with the value of the function phi (n)
        self.d = self.get_d(self.e, self.phi) # The number d is calculated, which is multiplicatively inverse to the number e modulo phi (n)
        # The pair (e, n) is published as an RSA public key. #encryption
        # The pair (d, n) plays the role of an RSA private key and is kept secret. #descryption
    def crypt(self, char, key):
        #if char == splitter:
        #    return splitter
        '''
        С = M**e mod N
        M’ = C**d mod N
        '''
        return char**key % self.n

    def encrypt_string(self, string):
        res = ""
        for char in string:
            ch = self.crypt(ord(char), self.d)   #ord- returns the number representing the unicode code of a specified character.
           # print("Char->char: ", char, ch)
            res += chr(ch)
            #print(char, type(char))
        #print('result:',res)
        return res

    def decrypt_string(self, string):
        res = ""
        for char in string:
            ch = self.crypt(ord(char), self.e)
            #print("char->dchar: ", ord(char), ch)
            res += chr(ch)
            #print('result:',res)
        return res

    @staticmethod
    def get_d(e, phi):
        return number.inverse(e, phi) # e**-1 mod phi
        #return e**-1 % phi
        
#a*x+b*y=gcd(a,b) x=d, gcd = e, phi - some k
#if a==0 -> x=0,y=1 -> return b
#int x1 y1
#int d = gcd(b%a,a,x1,y1)
#x=y-(b/a)*x
#y=x1
#return d

    @staticmethod
    def get_e(phi, bits=192):
        # (e*d) mod fi == 1
        while True:
            result = randrange(2,255)
            modulus = number.GCD(result, phi)  #greatest common devisor  #long Return the GCD of x and y.
            if modulus == 1:
                return result



#for understanding
    #@staticmethod
   # def get_greatest_common_divisor(a, b):
    #    while b != 0:
     #       a, b = b, a % b
     #   return a

#The @staticmethod decorator is similar to @classmethod in that it can be called from an uninstantiated class object,
# Many operations in public key encryption involve the(modp) operation and where we take the modulus of a prime number.
# This is defined as a finite field. In this case we will use Python to generate a random n-bit prime number.
#Многие операции при шифровании с открытым ключом включают операцию (modp), где мы берем модуль простого числа.
# Это определяется как конечное поле. В этом случае мы будем использовать Python для генерации случайного n-битного простого числа.
