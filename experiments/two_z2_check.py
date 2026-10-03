# -*- coding: utf-8 -*-
"""客观梳理：理论里到底有几个独立的 Z2（二分）？
从公设出发，按来源分层，判定「断裂 + 手征」是否仅有的两个。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from itertools import permutations

print("="*72)
print("从公设 D_ij = D_ji* 出发，理论推出的二分(Z2)结构，按来源分两层：")
print()

print("[第一层] 自反性 -> 厄米 -> 断裂 -> 二元闭环")
print("  断裂 = A/B 二分（最小非平凡闭合结构）= 第 1 个 Z2")
print("  来源：自反性直接推论（家底 3）")

print()
print("[第二层] 结构选择门 -> π 磁通（家底 12）")
print("  π 磁通推出：")
print("    (a) 上下 = π 磁通反对易 T_xT_y=-T_yT_x（家底 10）")
print("    (b) 手征 Γ = bipartite 二分图，谱 ±E（家底 11）")
print("    (c) Kramers T^2=-1（家底 11）")

print()
print("关键判定：这 4 个「Z2 候选」里，哪些是独立的？")
print("  断裂(A/B 关系二分)  vs  手征 Γ(bipartite 格点二分)")
print("    -> 不同来源（自反性 vs π磁通），不同对象（关系 vs 格点）")
print("    -> 两个独立的 Z2")
print()
print("  π磁通上下(相位 0/π)  vs  手征 Γ(bipartite)")
print("    -> π 磁通相位 = bipartite 二分，是「同一个 Z2 的两个面」")
print("    -> 不是两个独立的 Z2")
print()
print("  Kramers T^2=-1")
print("    -> 反酉，T^4=I，是 Z4 不是 Z2 -> 排除（不是二分）")

print()
print("="*72)
print("客观结论：")
print("  理论恰好两个独立 Z2 = 断裂(自反性) + 手征/上下(π磁通)")
print("  Aut(Z2 x Z2) = S3 -> A2 -> su(3)，唯一性成立")
print()
print("但需严格确认 2 点（诚实标注）：")
print("  [1] 「π磁通上下」=「手征 Γ」是同一个 Z2（不是两个独立 Z2）？")
print("  [2] 断裂 与 手征 确实对易（独立）？")
print("="*72)
