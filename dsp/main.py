import random
import math

def main():
    dft_by_correlation()

def convolution1():
    xm = [0, 1, -1, 2, 0, 3, 1, 4, 2, 5, 3, 1]
    hn = [0, 1, 2, 3, 2, 1, 0] # low-pass filter
    yn = [0 for i in range (len(xm)+len(hn))]
    print(hn)

    for i in range(len(xm)):
        for j in range(len(hn)):
            yn[i+j] += xm[i] + hn[j]
    
    print(yn)
    
# discrete Fourier transform by correlation.
def dft_by_correlation():
    N = 512
    # xn = [random.randint(0, 255) for i in range(N)]
    xn = [128*( math.cos((2*math.pi*200*i)/N)+math.cos((2*math.pi*72*i)/N) ) for i in range(N)]
    print(xn)
    reX = [0 for i in range(N/2+1)]
    imX = [0 for i in range(N/2+1)]

    for k in range(N/2+1):
        for i in range(N):
            reX[k] += xn[i]*math.cos((2*math.pi*k*i)/N)
            imX[k] -= xn[i]*math.sin((2*math.pi*k*i)/N)

    print([(0 if (i < 1) else i) for i in imX])
    print([(0 if (i < 1) else i) for i in reX])
    

if __name__ == "__main__":
    main()