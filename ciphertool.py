# encode: utf-8
from enum import Enum

#table / hashmap
jp_morse_mp = {}
jp_morse_rmp = {}
en_morse_mp = {}
en_morse_rmp = {}
dakuten_mp = {}
dakuten_rmp = {}
two_touch_table = []
two_touch_rmp = {}
mikaka_mp = {}
mikaka_rmp = {}

# init
with open(r'source/morse_jp.txt', encoding='utf-8') as f:
    for e in f.read().splitlines():
        jp, morse = e.split()
        jp_morse_mp[jp] = morse
        jp_morse_rmp[morse] = jp

with open(r'source/morse_en.txt', encoding='utf-8') as f:
    for e in f.read().splitlines():
        en, morse = e.split()
        en_morse_mp[en] = morse
        en_morse_rmp[morse] = en
with open(r'source/dakuten.txt', encoding='utf-8') as f:
    for e in f.read().splitlines():
        jo, sp = e.split()
        dakuten_mp[jo] = sp
        dakuten_rmp[sp] = jo

with open(r'source/two_touch.txt', encoding='utf-8') as f:
    two_touch_table = list(map(list, f.read().splitlines()))
    for i in range(10):
        for j in range(10):
            two_touch_rmp[two_touch_table[i][j]] =  str((i + 1) % 10) + str((j + 1) % 10)

with open(r'source/mikaka.txt', encoding='utf-8') as f:
    his = f.readline()
    als = f.readline()
    for hi, al in zip(his, als):
        mikaka_mp[al] = hi
        mikaka_rmp[hi] = al

class T(Enum):
    Int = 0
    Str = 1
    Li_int = 2
    Li_obj = 3

class CipherObject:
    def __init__(self):
        self.type = None
        self.val = None
    
    def __init__(self, val, tp = None):
        self.type = tp
        self.val = val
        if tp:
            self.type = tp
        elif type(val) == int:
            self.type = T.Int
        elif type(val) == str:
            self.type = T.Str
        elif type(val) == list and type(val[0]) == int:
            self.type = T.Li_int
        elif type(val) == list and type(val[0]) == CipherObject:
            self.type = T.Li_obj
        else:
            self.error_message(f'__init__({type(val[0])})')

    def print(self):
        if self.type == T.Li_obj:
            print('[')
            for e in self.val:
                e.print()
            print(']')
        elif self.type == T.Str:
            print(f'<{self.type.name},{len(self.val)}> ', end='')
            for e in self.val:
                try:
                    print(e, end='')
                except:
                    print('�', end='')
            print()
        elif self.type == T.Li_int:
            print(f'<{self.type.name},{len(self.val)}> {self.val}')
        else:
            print(f'<{self.type.name}> {self.val}')
        return self

    def error_message(self, s: str):
        print('[error] ' + s, flush=True)
        exit()

    def to_str(self):
        if self.type == T.Int:
            return CipherObject(str(self.val))
        elif self.type == T.Li_int:
            return CipherObject([str(e) for e in self.val])
        elif self.type == T.Li_obj:
            return CipherObject([e.to_str() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.to_str()')
    
    def to_int(self):
        if self.type == T.Str:
            return CipherObject(int(self.val))
        elif self.type == T.Li_obj:
            return CipherObject([e.to_int() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.to_int()')

    def to_list_int(self):
        if self.type == T.Str:
            return CipherObject([int(e) for e in self.val])

    def to_base_n(self, base: int, list_out=False):
        if self.type == T.Int:
            n = self.val
            result = []
            while n > 0:
                result.append(n % base)
                n //= base
            result.reverse()
            if list_out:
                return CipherObject(result)
            else:
                return CipherObject(result).list_to_str()
        elif self.type == T.Li_int:
            result = []
            for e in self.val:
                result.append(CipherObject(e).to_base_n(base).val)
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.to_base_n(base, list_out) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.to_base_n(<{type(base).__name__}>{base})')

    def from_base_n(self, base: int):
        result = 0
        if self.type == T.Str:
            for e in self.val:
                result *= base
                if ord('0') <= ord(e) <= ord('9'):
                    if int(e) < base:
                        result += int(e)
                    else:
                        self.error_message(f'The base must be lager than each digit.\n<{type(self.val).__name__}>{self.val}.from_base_n(<{type(base).__name__}>{base})')
                elif ord('a') <= ord(e) <= ord('z'):
                    if ord(e) - ord('a') + 10 < base:
                        result += ord(e) - ord('a') + 10
                    else:
                        self.error_message(f'The base must be lager than each digit.\n<{type(self.val).__name__}>{self.val}.from_base_n(<{type(base).__name__}>{base})')
            return CipherObject(result)
        elif self.type == T.Li_int:
            for e in self.val:
                result *= base
                result += e
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.from_base_n(base) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.from_base_n(<{type(base).__name__}>{base})')

    def list_to_str(self):
        if self.type == T.Li_int:
            result = ''
            for e in self.val:
                assert(0 <= e < 36)
                if e <= 9:
                    result += str(e)
                else:
                    result += chr(e + ord('a') - 10)
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject(CipherObject(e) for e in self.val)
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.list_to_str()')

    def decode_from_hex(self, code_type: str):
        if self.type == T.Str:
            s = self.val
            if code_type == 'utf-16':
                now = ''
                result = ''
                for i in range(0, len(s), 4):
                    now += s[i:i+4]
                    try:
                        result += chr(int(now, 16))
                    except:
                        result += '�'
                    now = ''
                return CipherObject(result)
            else:
                b = bytes.fromhex(s)
                return CipherObject(b.decode(encoding=code_type, errors='replace'))
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_from_hex(code_type) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.decode_from_hex(<{type(code_type).__name__}>{code_type})')

    def encode_to_hex(self, code_type: str):
        if self.type == T.Str:
            s = self.val
            if code_type == 'utf-16':
                result = ''
                for e in s:
                    result += hex(ord(e))[2:]
                return CipherObject(result)
            else:
                return CipherObject(s.encode(encoding=code_type, errors='replace').hex())
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_to_hex(code_type=code_type) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode(<{type(code_type).__name__}>{code_type})')

    def encode_morseJP(self, letter='・－　'):
        if self.type == T.Str:
            s = self.dakuten_split(False).val
            result = ''
            for e in s:
                if e in jp_morse_mp:
                    result += jp_morse_mp[e] + '　'
                else:
                    result += e + '　'
            return CipherObject(result).replace("・－　", letter)
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_morseJP(letter=letter) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode_morseJP(<{type(letter).__name__}>{letter})')

    def decode_morseJP(self, letter='・－　'):
        if self.type == T.Str:
            s = CipherObject(self.val).replace(letter, '・－　').val
            while s[-1] == '　':
                s = s[:-1]
            result = ''
            for e in s.split('　'):
                if e in jp_morse_rmp:
                    result += jp_morse_rmp[e]
                else:
                    result += e
            return CipherObject(result).dakuten_join(False)
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_morseJP(letter=letter) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.decode_morseJP(<{type(letter).__name__}>{letter})')

    def encode_morseEN(self, letter='・－　'):
        if self.type == T.Str:
            s = self.val
            result = ''
            for e in s:
                if e in en_morse_mp:
                    result += en_morse_mp[e] + '　'
                else:
                    result += e + '　'
            return CipherObject(result).replace("・－　", letter)
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_morseEN(letter=letter) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode_morseEN(<{type(letter).__name__}>{letter})')

    def decode_morseEN(self, letter='・－　'):
        if self.type == T.Str:
            s = CipherObject(self.val).replace(letter, '・－　').val
            while s[-1] == '　':
                s = s[:-1]
            result = ''
            for e in s.split('　'):
                if e in en_morse_rmp:
                    result += en_morse_rmp[e]
                else:
                    result += e
            return CipherObject(result).dakuten_join(False)
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_morseEN(letter=letter) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.decode_morseEN(<{type(letter).__name__}>{letter})')

    def dakuten_split(self, first=False):
        if self.type == T.Str:
            s = self.val
            s2 = ''
            for e in s:
                if e in dakuten_mp:
                    if e in dakuten_mp:
                        dakuten = dakuten_mp[e]
                        if first:
                            if len(dakuten) == 2:
                                s2 += dakuten_mp[e][1] + dakuten_mp[e][0]
                            else:
                                s2 += dakuten_mp[e]
                        else:
                            s2 += dakuten
                    else:
                        s2 += e
                else:
                    s2 += e
            return CipherObject(s2)
        elif self.type == T.Li_obj:
            return CipherObject([e.dakuten_split(first=first) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.dakuten_split(<{type(first).__name__}>{first})')

    def dakuten_join(self, first=False):
        if self.type == T.Str:
            s = self.val
            pre = ''
            result = []
            for e in s:
                if e == '゛' or e == '゜':
                    if first:
                        pre = e
                    else:
                        if result[-1] + e in dakuten_rmp:
                            result[-1] = dakuten_rmp[result[-1] + e]
                        else:
                            result.append(e)
                else:
                    if pre == '':
                        result.append(e)
                    else:
                        if e + pre in dakuten_rmp: 
                            result.append(dakuten_rmp[e + pre])
                        else:
                            result.append(e + pre)
                    pre = ''
            return CipherObject(''.join(result))
        elif self.type == T.Li_obj:
            return CipherObject([e.dakuten_join(first=first) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.dakuten_join(<{type(first).__name__}>{first})')
        
        
    def rot(self, shift: int):
        if self.type == T.Str:
            s = self.val
            result = ''
            for e in s:
                result += chr((ord(e) - ord('a') + shift) % 26 + ord('a'))
            return CipherObject(result)
        elif self.type == T.Li_int:
            result = [e + shift for e in self.val]
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.rot(shift) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.rot(<{type(shift).__name__}>{shift})')
    
    def join(self):
        if self.type == T.Li_obj:
            result = ''
            for e in self.val:
                result += e.val
            return CipherObject(result)
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.join()')

    def encode_two_touch(self):
        if self.type == T.Str:
            s = self.val
            result = ''
            for e in s:
                result += two_touch_rmp[e]
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_two_touch() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode_two_touch()')

    def decode_two_touch(self):
        if self.type == T.Str:
            s = self.val
            assert(len(s) % 2 == 0)
            result = ''
            for i in range(0, len(s), 2):
                result += two_touch_table[(int(s[i]) + 9) % 10][(int(s[i + 1]) + 9) % 10]
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_two_touch() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.decode_two_touch()')

    def decode_mikaka(self):
        if self.type == T.Str:
            s = self.val
            result = ''
            for e in s:
                result += mikaka_mp[e]
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_mikaka() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.decode_mikaka()')
    
    def encode_mikaka(self):
        if self.type == T.Str:
            s = self.val
            result = ''
            for e in s:
                result += mikaka_rmp[e]
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_mikaka() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode_mikaka()')

    def num_to_alphabet(self):
        if self.type == T.Int:
            return CipherObject(chr(self.val + ord('a')))
        if self.type == T.Li_int:
            return CipherObject(''.join([chr(e + ord('a')) for e in self.val]))
        elif self.type == T.Li_obj:
            return CipherObject([e.num_to_alphabet() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.num_to_alphabet()')
    
    def reverse(self):
        if self.type == T.Str:
            return CipherObject(''.join(list(reversed(self.val))))
        elif self.type == T.Li_int:
            return CipherObject(list(reversed(self.val)))
        elif self.type == T.Li_obj:
            return CipherObject([e.reverse() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.reverse()')
    
    def replace(self, letter_from: str, letter_to: str):
        if self.type == T.Str:
            mp = {}
            result = ''
            assert(len(letter_from) == len(letter_to))
            for e, f in zip(letter_from, letter_to):
                mp[e] = f
            for e in self.val:
                if e in mp:
                    result += mp[e]
                else:
                    result += e
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.replace(letter_from, letter_to) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.replace(<{type(letter_from).__name__}>{letter_from}, <{type(letter_to).__name__}>{letter_to})')

    def decode_visunel(self, key: str):
        if self.type == T.Str:
            s = self.val
            result = ''
            for i in range(len(s)):
                result += chr((ord(s[i]) - ord(key[i % len(key)])) % 26 + ord('a'))
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.decode_visunel() for e in self.val])
    
    def encode_visunel(self, key: str):
        if self.type == T.Str:
            s = self.val
            result = ''
            for i in range(len(s)):
                result += chr((ord(s[i]) + ord(key[i % len(key)])) % 26 + ord('a'))
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.encode_visunel() for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.encode_visunel(<{type(key).__name__}>{key})')

    def split(self, interval: int):
        s = self.val
        result = []
        if self.type == T.Str:
            for i in range(len(s)):
                if i % interval == 0:
                    result.append(s[i])
                else:
                    result[-1] += s[i]
            return CipherObject([CipherObject(e) for e in result])
        elif self.type == T.Li_int:
            for i in range(len(s)):
                if i % interval == 0:
                    result.append([s[i]])
                else:
                    result[-1].append(s[i])
            return CipherObject([CipherObject(e) for e in result])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.split(<{type(interval).__name__}>{interval})')
        
    def insert(self, interval: int, l: str, r=""):
        if self.type == T.Str:
            s = self.val
            result = ''
            for i in range(0, len(s)):
                if i % interval == 0:
                    result += l
                result += s[i]
                if i % interval == interval - 1:
                    result += r
            return CipherObject(result)
        elif self.type == T.Li_obj:
            return CipherObject([e.insert(interval, l) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.insert(<{type(l).__name__}>{l}, <{type(r).__name__}>{r})')
    
    def add(self, a: int):
        if self.type == T.Int:
            return CipherObject(self.val + a)
        elif self.type == T.Li_int:
            return CipherObject([e + a for e in self.val])
        elif self.type == T.Li_obj:
            return CipherObject([e.add(a) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.add(<{type(a).__name__}>{a})')

    def mod(self, a: int):
        if self.type == T.Int:
            return CipherObject(self.val % a)
        elif self.type == T.Li_int:
            return CipherObject([e % a for e in self.val])
        elif self.type == T.Li_obj:
            return CipherObject([e.mod(a) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.add(<{type(a).__name__}>{a})')

    def substr(self, l, r):
        if self.type == T.Str:
            return CipherObject(self.val[l:r])
        elif self.type == T.Li_obj:
            return CipherObject([e.substr(l, r) for e in self.val])
        self.error_message(f'\n<{type(self.val).__name__}>{self.val}.add(<{type(l).__name__}>{l}), <{type(r).__name__}>{r})')
                

    def rot_bruteforce(self):
        if self.type == T.Str:
            print("rot_bruteforce")
            for i in range(26):
                print(f"{i:2d} ", end = "")
                CipherObject(self.val).rot(i).print()
    
    def decode_from_hex_bruteforce(self):
        if self.type == T.Str:
            print("decode_from_hex_bruteforce")
            encodes = ["utf-8", "utf-16", "shift-jis", "euc-jp"]
            adds = ["e38", "30", "82", "a4"]
            intervals = [3, 2, 2, 2]
            for e in encodes:
                print(f"{e:14s} ", end="")
                CipherObject(self.val).decode_from_hex(e).print()
            for enc, ad, itv in zip(encodes, adds, intervals):
                print(f"{"+"+ad+" "+enc:14s} ", end="")
                CipherObject(self.val).insert(itv, ad).decode_from_hex(enc).print()

    def encode_to_hex_bruteforce(self):
        if self.type == T.Str:
            print("encode_to_hex_bruteforce")
            encodes = ["utf-8", "utf-16", "shift-jis", "euc-jp"]
            adds = ["e31", "30", "8a", "a4"]
            ls = [3, 2, 2, 2]
            rs = [6, 4, 4, 4]
            for e in encodes:
                print(f"{e:14s} ", end="")
                CipherObject(self.val).encode_to_hex(e).print()
            for enc, ad, l, r in zip(encodes, adds, ls, rs):
                print(f"{"-"+ad+" "+enc:14s} ", end="")
                CipherObject(self.val).encode_to_hex(enc).split(r).substr(l, r).join().print()
