# -*- coding: utf-8 -*-
"""验证「实化(realification)」能否拧直类型翻转，把 w 的 120° 显式化。
关键：复框架里 酉 vs 反酉 是两类；实化后都变实正交，类型区分是否消失？
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

print("="*72)
print("[1] 实化 C -> R^2：z = x + iy 映射到 (x, y)")
print("    酉 w = e^{2pi i/3}（相位旋转 120°）：z -> w*z")
w = np.exp(2j*np.pi/3)
# w 在 R^2 上的实表示：w*z 的实部虚部
# w = cos120 + i sin120 = -0.5 + i*0.866
W = np.array([[w.real, -w.imag],[w.imag, w.real]])
print("    w 的实化矩阵 = 旋转 120°:")
print("    ", np.round(W,3), "  det =", round(np.linalg.det(W),3), "(+1 旋转)")

print("\n[2] 反酉 K（复共轭 z->zbar）实化后")
K = np.array([[1,0],[0,-1]])  # (x,y) -> (x,-y)
print("    K 实化 = 反射 (x,y)->(x,-y):", K.tolist(), "  det =", round(np.linalg.det(K),3), "(-1 反射)")

print("\n[3] 关键：实化后，酉(旋转 det+1) 和 反酉(反射 det-1) 都变实正交")
print("    但区分没消失——变成了 旋转 vs 反射 (det +1 vs -1)")
print("    '类型翻转' -> '取向翻转'，不是消除")

print("\n[4] 3 阶类型翻转 g（det=-1）实化后存在吗？")
print("    det(g^3) = det(g)^3 = (-1)^3 = -1，但 det(I)=1 -> 矛盾")
print("    所以 3 阶 det=-1 实正交不存在：3-循环实化后必是 det=+1(旋转)")

print("\n[5] 净结论：")
print("    实化确实拧直了反线性(K 变实线性)，但把'类型翻转'翻译成'取向翻转(det±1)'")
print("    w 的 120° 从'隐藏相位'变'显式旋转角'——这正是 A2 根夹角 120°")
print("    但 S3(Weyl群) -> SU(3)(李群) 仍缺 A2 Cartan 矩阵，只是 120° 现在显式了")
print("="*72)
