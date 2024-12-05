import numpy as np
import random 

class RSA:
    def __init__(self, n_max=100):
        """
        n_max : int
            max value for primes

        primes : list
            list des nombres premiers inférieurs à n_max
        """
        self.n_max = n_max
        self.primes = self.crible(n_max)
    
    def isprem(self, n):  
        """
        Retourne True si n est premier, False dans le cas contraire.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        r = int(n**0.5) + 1
        
        for x in range(3, r, 2):
            if n % x == 0:
                return False
        return True
    
    
    def crible(self, n):
        """Retourn tous les nombres premiers inférieurs ou égaux à n"""
        primes = []
        for i in range(2, n+1):
            if self.isprem(i):
                primes.append(i)
        return primes
    
    
    def puissance_modulaire(self, a, n, m):
        """
        Calcule a^n mod m
        """
        p = 1
        a = a % m
        while n > 0:
            if n % 2 == 1:  # si n est impair
                p = (p * a) % m
            a = (a * a) % m
            n = n // 2
        return p
    
    def inverse_modulaire(self, a, m):
        """Calcule l'inverse de a modulo m."""
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1 if self.puissance_modulaire(a,1,m0) == 1 else None
                
    def gcd(self, a, b):
        """Calcul du PGCD de a et b"""
        while b != 0:
            a, b = b, a % b
        return a

    def generer_cles(self):
        """Génère les clés publiques et privées."""
        
        p = random.choice(self.primes)
        q = random.choice(self.primes)
        while q == p:
            q = random.choice(self.primes)
        
        n = p * q
        m = (p - 1) * (q - 1)
        
        # Choisir e tel que 1 < e < m et gcd(e, m) == 1
        e = random.randint(2, m-1)
        while self.gcd(e, m) != 1:
            e = random.randint(2, m-1)
        
        d = self.inverse_modulaire(e, m)
        if d is None:
            raise ValueError("Impossible de trouver l'inverse modulaire. Réessayez.")
        
        return e, d, n


    def crypter(self, message, e, n):
        """Crypte un message en utilisant la clé publique (e, n)."""
        ascii_message = [ord(char) for char in message]
        blocs = [self.puissance_modulaire(code, e, n) for code in ascii_message]
        # Utiliser 5 chiffres pour les blocs
        return ''.join(f"{bloc:05}" for bloc in blocs)


    def decrypter(self, message_crypte, d, n):
        """Décrypte un message en utilisant la clé privée (d, n)."""
        blocs = [int(message_crypte[i:i+5]) for i in range(0, len(message_crypte), 5)]
        ascii_message = [self.puissance_modulaire(bloc, d, n) for bloc in blocs]
        return ''.join(chr(code) for code in ascii_message)

if __name__ == "__main__":
    rsa = RSA(n_max=100)
    e, d, n = rsa.generer_cles()
    print(f"Clé publique (e, n): ({e}, {n})")
    print(f"Clé privée (d, n): ({d}, {n})")
    
    message = "Hello"
    message_crypte = rsa.crypter(message, e, n)
    print(f"Message crypté: {message_crypte}")
    
    message_decrypte = rsa.decrypter(message_crypte, d, n)
    print(f"Message décrypté: {message_decrypte}") 
