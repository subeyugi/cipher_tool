# ciphertool サンプルコード

from ciphertool import *

# モールス
print("[sample 1]")
sample1 = CipherObject("すべてあなたのせいです")
sample1.encode_morseJP().print() #<Str,59> －－－・－　・　・・　・－・－－　－－・－－　・－・　－・　・・－－　・－－－・　・－　・－・－－　・・　－－－・－

print("\n[sample 2]")
sample2 = CipherObject("・・－・・　・・　・・－　－－・・－　・－・－－　・－　・－・　・・・－　・－・　・－・－－　－－・－・　－・・－　－・　・・－－")
sample2.decode_morseJP().print() #<Str,13> どうひていなくなてしまたの

print("\n[sample 3]")
sample3 = CipherObject("100112101102110102010112")
sample3.decode_morseJP(letter="012").print() #<Str,7> ゆるして

# 進数変換
print("\n[sample 4]")
sample4 = CipherObject("232151400554512566264644105050115063005136351366340605104666615")
sample4.from_base_n(7).to_base_n(16).decode_from_hex("euc-jp").print() #<Str,11> あんしんをしてください

# 文字化け
print("\n[sample 5]")
sample5 = CipherObject("繝｡繝ｼ繝ｫ")
sample5.encode_to_hex("shift-jis").decode_from_hex("utf-8").print() #<Str,3> メール

# 一部補ってから復号
print("\n[sample 6]")
sample6 = CipherObject("011011111100110111000100 011001011111101100100011 001000101101010010110010 010000100110".replace(" ", ""))
sample6.insert(7, "101001001").from_base_n(2).to_base_n(16).decode_from_hex("euc-jp").print() #しんじてくれてありがとう

# 全探索
print("\n[sample 7]")
sample7 = CipherObject([6, 7, 2, 3])
sample7.num_to_alphabet().rot_bruteforce() #... 12 <Str,4> stop ...

print("\n[sample 8]")
sample8 = CipherObject("7783921599188497342462197636138661522987162")
sample8.to_list_int().add(-1).from_base_n(9).to_base_n(16).decode_from_hex_bruteforce() #... +82 shift-jis  <Str,17> わたしをみつめるめとおかえりのこえ ... 

print("\n[sample 9]")
# 混合（反転モールス、みかか、36進数、文字追加、2タッチ）
sample9 = CipherObject("－・・　・・－－　・・－－　・・－・・　－・・　・－－・・　・－－・・　－－－－　・－・・・")
base36 = sample9.decode_morseJP("－・　").encode_mikaka().to_int().to_base_n(36).print() #<Str,6> by3327
base36 = base36.substr(2, 6).insert(1, "", "1").decode_two_touch().print() #<Str,4> ささかま