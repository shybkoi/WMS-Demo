# -*- coding: windows-1251 -*-
#a=7467 #=0x1D2B b16 =5RF b36: (5*36*36+(ord('R')-ord('A')+10)*36+15)

############# From decimal to any based system

def num_to_char_16(n):
    if n < 10:
        return chr(ord('0')+n)
    return chr(ord('A')+n-10)

def num_to_char_26(n):
    return chr(ord('A')+n)

def num_to_char_36(n):
    if n < 10:
        return chr(ord('0')+n)
    return chr(ord('A')+n-10)

def num_to_char_any(n, base):
    if base == 16:
        return num_to_char_16(n)
    if base == 26:
        return num_to_char_26(n)
    if base == 36:
        return num_to_char_36(n)
        
def dec_to_any(n10, base):
    #gets array of ostatki
    
    delimoe = n10
    delitel = base
    #chastnoe
    ostatok = delitel
    ostatki = []
    while (delimoe >= delitel):
        ostatok = delimoe % delitel
        delimoe = delimoe / delitel
        ostatki.insert(0, ostatok)
    ostatki.insert(0, delimoe)

    #convert array of ostatki to chars
    
    return reduce(lambda all_s, n: all_s + num_to_char_any(n, base), ostatki, '')

############# From any based system to decimal

def char_to_num_any(c, base):
    if base == 16:
        return char_to_num_16(c)
    if base == 26:
        return char_to_num_26(c)
    if base == 36:
        return char_to_num_36(c)

def char_to_num_16(c):
    c = c.upper()

    if ord('A') <= ord(c) <= ord('F'):
        return ord(c)-ord('A')+10

    if ord('0') <= ord(c) <= ord('9'):
        return ord(c)-ord('0')

    raise ArithmeticError('Symbol %s is not in base 16' % c)

def char_to_num_26(c):
    c = c.upper()

    if ord(c) < ord('A') or ord(c) > ord('Z'):
        raise ArithmeticError('Symbol %s is not in base 26' % c)
    return ord(c)-ord('A')

def char_to_num_36(c):
    c = c.upper()

    if ord('A') <= ord(c) <= ord('Z'):
        return ord(c)-ord('A')+10

    if ord('0') <= ord(c) <= ord('9'):
        return ord(c)-ord('0')

    raise ArithmeticError('Symbol %s is not in base 36' % c)

def any_to_dec(s_num, base):
    return reduce(lambda dec, c: (dec + char_to_num_any(c, base)) * base, s_num[:-1], 0) + char_to_num_any(s_num[-1], base)
    """dec = 0
    for c in s_num[:-1]:
        dec = (dec + char_to_num_any(c, base)) * base
    return dec + char_to_num_any(s_num[-1], base)"""

# Test
#print dec_to_any(a, 16)
#print dec_to_any(a, 36)
#print any_to_dec('1D2B', 16) #7467 b10
#print any_to_dec('VBBC0', 36) #52596000
#print any_to_dec('BA', 26) #26
#print any_to_dec('FE', 16) #254
#print any_to_dec('G', 16) #Error
#print any_to_dec('0', 26) #Error
#print any_to_dec('*', 36) #Error


# Try login b26 to b36 - no!!!
#20symbols of base 26 max = ZZZZZZZZZZZZZZZZZZZZb26 = 100000000000000000000b26 - 1 = 26**20 - 1
#print dec_to_any(26**20 - 1, 36) #1XJYGVH0MB7XW7G0A9R b36 - 19 symbols - ne zamorachivaemsja + budet vidno v b26 login pri pechati


#structure: 
#LLLLLLL                              TTTTT                   CCCC
#hash of login+salt (7symb b36)       datetime (5symb b36)    crc16 (4symb b16)

#LLLLLLL - hash of str(login + halt_salt) - from 0 to 2**32-1 (=1Z141Z3 b36 len=7)
#print dec_to_any(2**32-1, 36)

#TTTTT-minutes from 01.01.2010 00:00 (max=VBBC0 b36 (5 symb))

#CCCC-CRC16 of str (LLLLLLL + TTTTT + hash_salt) - from 0 to 2**16-1 (=FFFF b16 len=4    =1EKF b36 len=4)
#print dec_to_any(2**16-1, 36)




#between 01.01.2100-01.01.2010 47335680 minutes = S6KG0 b36 (5 symb)
#print dec_to_any(47335680, 36)

#between 01.01.2100-01.01.2000 52596000 minutes = VBBC0 b36 (5 symb)
#print dec_to_any(52596000, 36)

#how to many years from 01.01.2010 00:00 in 5 symbols minutes pomeschaetsja
#print any_to_dec('ZZZZZ', 36) #60466175 minutes max coded in 5 symbols - 19.12.2124  9:35:00
