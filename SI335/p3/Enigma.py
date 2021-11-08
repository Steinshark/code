class Enigma():
    class Rotor:
        def __init__(self, offset):
            self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
            self.input  = [self.alphabet[i] for i in range(0,26)]
            self.output = [self.alphabet[(i+offset)%26] for i in range(0,26)]
            self.encrypts = 0
            self.place = 0
            self.original_pos = offset
            self.offset = offset

        def __repr__(self):
            return str(self.input) + "\n" + str(self.output)
        def scramble(self, offset):
            self.output = self.output[offset:] + self.output[0:offset]
        def iter_rotor(self):
            self.scramble(1)
            self.offset  = (self.offset + 1) % 26
        def place_in_offset(self,offset):
            self.offset = offset
            self.output = [self.alphabet[(i+self.original_pos)%26] for i in range(0,26)]
            self.output = [self.output[(i+self.offset)%26] for i in range(0,26)]
            self.encrypts = 0
        def encrypt(self,letter):
            x = self.output[self.input.index(letter)]
            self.encrypts += 1
            if self.place == 0 or (self.encrypts % (26*self.place)) == 0:
                self.iter_rotor()
            return x
        def decrypt(self,letter):
            x = self.input[self.output.index(letter)]
            self.encrypts += 1
            if self.place == 0 or (self.encrypts % (26*self.place)) == 0:
                self.iter_rotor()
            return x
    def __init__(self):
        # these are the default offsets of each of the rotors
        init = [17,8,3,22,9]
        self.rotors = [self.Rotor(init[i]) for i in range(5)]
        self.run()
    def build_plugboard(self):
        print("set 10 plug board connections:")
        self.plugboard = {}
        self.plugboard2 = {}
        used = []
        for i in range(0,10):
            x = input("plug: ")
            while x in used:
                print(str(x) + " was already used")
                x = input("plug: ")
            used.append(x)
            y = input("into: ")
            while y in used:
                print(str(y) + " was already used")
                y = input("into: ")
            used.append(y)
            self.plugboard[x] = y
            self.plugboard2[y] = x
    def choose_rotors(self):
        print("Chose 3 of the 5 rotors to encrypt with:")
        inputs = []
        for i in range(0,3):
            user_in = int(input("Rotor" + str(i+1) + ": "))
            inputs.append(user_in)
        self.encrypting_rotor = [self.rotors[x-1] for x in inputs]
        for rotor in self.encrypting_rotor:
            rotor.place = self.encrypting_rotor.index(rotor)
    def set_rotors(self):
        print("SET ROTOR POSITIONS:")
        offsets = []
        for i in range(0,3):
            offsets.append(int(input("Rotor " + str(i) + ": ")))
            self.encrypting_rotor[i].place_in_offset(offsets[i])
    def encrypt(self):
        m = input("MESSAGE: ")
        m = m.lower()
        encrypted = ""
        for letter in m:
            if letter == " ":
                encrypted += " "
                continue
            for rotor in self.encrypting_rotor:
                letter = rotor.encrypt(letter)
            try:
                letter = self.plugboard[letter]
            except KeyError:
                try:
                    letter = self.plugboard2[letter]
                except KeyError:
                    pass
            encrypted += letter
        print("encrypted to: " + encrypted)
        print("\n\n")
    def decrypt(self):
        e = input("DECRYPT: ")
        self.set_rotors()
        decrypted = ""
        for letter in e:
            if letter == " ":
                decrypted += " "
                continue
            try:
                letter = self.plugboard[letter]
            except KeyError:
                try:
                    letter = self.plugboard2[letter]
                except KeyError:
                    pass
            for rotor in reversed(self.encrypting_rotor):
                letter = rotor.decrypt(letter)
            decrypted += letter

        print("decrypted to " + decrypted)
    def run(self):
        u_in = input("ENCRYPT or DECRYPT: ")
        if u_in == "ENCRYPT":
            self.build_plugboard()
            self.choose_rotors()
            self.set_rotors()
            self.encrypt()
        elif u_in == "DECRYPT":
            self.build_plugboard()
            self.choose_rotors()
            self.decrypt()


if __name__ == "__main__":
    while True:
        e = Enigma()
