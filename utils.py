from register import *


def ADD(A, B):
    result = []
    carry = 0
    for i in range(len(A) - 1, -1, -1):
        summ = A[i] + B[i] + carry
        carry = 1 if summ > 1 else 0
        result.insert(0, summ % 2)

    for i, bit in enumerate(result):
        A[i] = bit


def SUB(A, B):
    result = []
    borrow = 0
    for i in range(len(A) - 1, -1, -1):
        diff = A[i] - B[i] - borrow
        if diff < 0:
            borrow = 1
            result.insert(0, 0)
        else:
            borrow = 0
            result.insert(0, diff % 2)

    for i, bit in enumerate(result):
        A[i] = bit


def MOV(A, B):
    for i in range(len(A) - 1, -1, -1):
        A[i] = B[i]


if __name__ == '__main__':
    Ax = Register_16_bit('A')
    Bx = Register_16_bit('B')
    Ax[7] = 0
    Ax[8] = 0
    print(Ax.register())
    print(Bx.register())
    ADD(Ax, Bx)
    print(Ax.register())
