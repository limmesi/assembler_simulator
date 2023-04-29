class Register_16_bit:
    def __init__(self, name):
        self.H = Register_8_bit(name, 'H')
        self.L = Register_8_bit(name, 'L')
        self.name = name

    def __getitem__(self, idx):
        if idx < 8:
            return self.H[idx]
        elif idx < 16:
            return self.L[idx - 8]
        else:
            print('Out of range. It is 16-bit reg. ')

    def __setitem__(self, idx, value):
        if idx < 8:
            self.H[idx] = value
        elif idx < 16:
            self.L[idx - 8] = value
        else:
            print('Out of range. It is 16-bit reg. ')

    def __len__(self):
        return 16

    def register(self):
        register = self.H.reg + self.L.reg
        str_register = ''.join(str(bit) for bit in register)
        return str_register


class Register_8_bit:
    def __init__(self, name, half):
        self.name = name + half
        self.reg = [1, 0, 0, 0, 0, 0, 0, 1]

    def __getitem__(self, idx):
        return self.reg[idx]

    def __setitem__(self, idx, value):
        self.reg[idx] = value

    def __len__(self):
        return 8

    def register(self):
        str_register = ''.join(str(bit) for bit in self.reg)
        return str_register


if __name__ == '__main__':
    A = Register_16_bit('A')
    A[1] = 1
    print(A[7])
