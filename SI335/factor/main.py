from bigfloat import *
import rsa
setcontext(precision(100))

# Get these out of the way
PUBLIC_KEY_STR  = ('5', '51920810450204744019132202403246112884629925425640897326550851544998255968235697331455544257')
PRIVATE_KEY_STR =  '1020030004000050000060000007'
MSG =   ['5080044126181721789233854922898628577148116526837171122073893653562240462050342871828852352',\
        '47663457319497582431639743851163036404759938700967098764353207435832459054562859608117724917',\
        '35107969399143803990579815241040585869683532263491464401546024483633320709503998314295077841']

# Convert to BigFloats
private_key = BigFloat.exact(PRIVATE_KEY_STR,100)
nums = {'pub1'  :   BigFloat.exact(PUBLIC_KEY_STR[0],120),\
        'pub2'  :   BigFloat.exact(PUBLIC_KEY_STR[1],320),\
        'priv1' :   BigFloat.exact(PRIVATE_KEY_STR[0],120),\
        'priv2' :   BigFloat.exact(PRIVATE_KEY_STR[1],120)}


#ISINT?
def is_int(n):
    return floor(n) == ceil(n)
#ISPRIME?
def is_prime(n):
    return find_fact(n) == False
# Check for factors
def find_fact(num):
    for i in range(3,int(1+sqrt(num)),2):
        if i % 10000 == 0:
            print("iteration " + str(i))
        div = num / i

        if is_int(div):
            return div
    return False
def factor_private_key():
    global nums
    fact1 = find_fact(private_key)
    fact2 = private_key / fact1
    if fact1 < fact2:
        nums['priv1'] = fact1
        nums['priv2'] = fact2
    else:
        nums['priv1'] = fact2
        nums['priv2'] = fact1

factor_private_key()

def RSA_decode():
    global nums
    global MSG
    p = nums['priv1']
    q = nums['priv2']
    n = p * q
    e = nums['pub1']
    lam = (p-1)*(q-1)

    for d in range(1,lam):
        if (d * e) == 1 % lam:
            break
    print("computed d as " + str(d))
    private_k = rsa.PrivateKey(n,e,d,p,q)

    messages = [rsa.decrypt(i,private_k) for i in MSG]

    for i in messages:
        print(i)

RSA_decode()
