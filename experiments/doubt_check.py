# -*- coding: utf-8 -*-
"""推疑虑 2 和 3。
疑虑2：理论里两个 Z2（断裂+手征）是否独立、自动给 S3？
疑虑3：类型翻转（A6 不物理）实化后是否变成物理的 120° 旋转？
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from itertools import permutations

w = np.exp(2j*np.pi/3)

print("="*72)
print("[疑虑2] 两个独立 Z2 -> Z2xZ2 -> S3")
print("  断裂 a（对合 a^2=e）+ 手征 b（对合 b^2=e），独立")
print("  Z2xZ2 = {e,a,b,ab}，3 个非平凡元素 {a,b,ab} 都阶2")
print("  Aut = 置换 {a,b,ab} 的群 = S3")
print("  元素数 =", len(list(permutations(range(3)))), "= 6")
print("  结论：只要有两个独立 Z2，S3 自动出现（无手放）")

print("\n[疑虑3] 类型翻转实化后是否物理")
print("  A6：3-循环把酉 Γ 映到反酉 K（类型翻转），4x4 不物理")
print("  实化 C2 -> R4：")
Gamma = np.diag([1,1,-1,-1])   # 手征 Γ=σ3（酉对合）实化
K     = np.diag([1,-1,1,-1])   # 复共轭（反酉对合）实化
GK    = np.diag([1,-1,-1,1])   # ΓK 实化
print("    Γ 实化 =", Gamma.diagonal().tolist(), "(酉对合)")
print("    K 实化 =", K.diagonal().tolist(), "(反酉对合 -> 实正交)")
print("    ΓK 实化 =", GK.diagonal().tolist())
print("    三者都变实正交 -> 类型区分消失")

print("\n  3-循环（置换 {Γ,K,ΓK}）实化后：")
g = np.array([[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]])  # 3-循环置换
ev = np.round(np.linalg.eigvals(g),4)
print("    特征值 =", ev, " = {1,1,w,w^2}")
print("    在 2 维不变子空间 = 120° 旋转（实正交 det=+1）")
print("    det(g) =", round(np.linalg.det(g),3))
print("    结论：类型翻转实化后 = 物理的 120° 旋转，不再是'不物理'")

print("\n" + "="*72)
print("疑虑推的结果：")
print("  疑虑2：两个独立 Z2 自动给 S3（无手放）—— 成立")
print("  疑虑3：类型翻转实化后是物理的 120° 旋转 —— 成立")
print("  但这只是'形式上'的成立，还需查最深的疑虑1/4（是否真唯一/非循环）")
print("="*72)
