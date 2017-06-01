import string
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import minimize

letter_list=list(string.ascii_uppercase)

poly_size=input('Polynomial Size: ')
poly_helper=[]
helper_string=''
for x in range(0,int(poly_size)):
    helper_string+=str(letter_list[x])+'*x^'+str(int(poly_size)-x-1)+' + '
helper_string=helper_string[0:len(poly_helper)-3]
print(helper_string)
u_coeffs=[]
for x in range(0,int(poly_size)):
    poly_val=input('Polynomial term '+letter_list[x]+': ')
    u_coeffs.append(int(poly_val))

u=np.poly1d(u_coeffs)

# All good up to here
