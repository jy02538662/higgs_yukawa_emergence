"""exp3 门 4 第 2 步：Yukawa 矩阵对颜色的结构——Schur 引理是否强制平庸。

关键问题（决定「第三种颜色 Yukawa 耦合不同」这个独有预言候选是否成立）：

用户框架的独有预言候选：颜色 3=2⊕1 分解 ⟹ 第三种颜色 Yukawa 耦合不同于前两种。

但这里有个必须诚实验证的分叉：
  - 若完整 SU(3) 对称活着（预印本 1.9 用 Serre 构造给出完整连续 su(3)），
    则 Schur 引理强制：任何 SU(3) 不变的 Yukawa 耦合对颜色是平庸的 m·I₃，
    「第三种颜色不同」不成立。
  - 3=2⊕1 只是「限制到 SU(2) 子代数（λ1,λ2,λ3 生成）看」的分支规则，
    它不破坏完整 SU(3)。

本实验符号验证 Schur 引理：
  A. 找所有与 su(3) 全部 8 个生成元 λa 对易的 3×3 矩阵，证明只有 c·I₃。
  B. 3=2⊕1 分支（限制到 su(2) 子代数）下，与 su(2)（λ1,λ2,λ3）对易的
     矩阵是 diag(a, a, b)（前两色平权，第三色可不同）——这才是「第三色不同」的空间。
  C. 结论：完整 SU(3) ⟹ 三色平权；只有「退到 su(2) 子代数」才允许第三色不同。
     即「第三种颜色 Yukawa 耦合不同」⟺ 完整 SU(3) 破缺到 SU(2)。
"""

import json
from pathlib import Path

import numpy as np

results = {}

# Gell-Mann 矩阵
lam = {}
lam['l1'] = np.array([[0,1,0],[1,0,0],[0,0,0]])
lam['l2'] = np.array([[0,-1j,0],[1j,0,0],[0,0,0]])
lam['l3'] = np.array([[1,0,0],[0,-1,0],[0,0,0]])
lam['l4'] = np.array([[0,0,1],[0,0,0],[1,0,0]])
lam['l5'] = np.array([[0,0,-1j],[0,0,0],[1j,0,0]])
lam['l6'] = np.array([[0,0,0],[0,0,1],[0,1,0]])
lam['l7'] = np.array([[0,0,0],[0,0,-1j],[0,1j,0]])
lam['l8'] = np.array([[1,0,0],[0,1,0],[0,0,-2]])/np.sqrt(3)
all8 = [lam[k] for k in ['l1','l2','l3','l4','l5','l6','l7','l8']]
su2 = [lam['l1'], lam['l2'], lam['l3']]


def commutator_space_dim(gens, n=3):
    """找所有与 gens 对易的 n×n 复矩阵张成的空间维数（复零空间维数）。

    解 X 使 [X, g] = Xg - gX = 0 对所有 g ∈ gens。
    vec(Xg - gX) = (g^T ⊗ I - I ⊗ g) vec(X)，复 9×9 作用在 vec(X)。
    用复 SVD 求零空间维数。
    """
    I = np.eye(n)
    rows = []
    for g in gens:
        M = np.kron(g.T, I) - np.kron(I, g)  # 复 n²×n²
        rows.append(M)
    A = np.vstack(rows)  # 复 (k·n²)×n²
    u, s, vh = np.linalg.svd(A)
    nullity = int(np.sum(s < 1e-10))
    return nullity


# A. 与完整 su(3) 对易的空间维数
dim_su3 = commutator_space_dim(all8)
# B. 与 su(2) 子代数对易的空间维数
dim_su2 = commutator_space_dim(su2)

results['A_centralizer_su3'] = {
    'dim': int(dim_su3),
    'expect': 1,
    'verdict': '与完整 su(3) 对易的矩阵空间 = 1 维（只有 c·I₃，Schur 引理，3 是不可约表示）',
}

results['B_centralizer_su2'] = {
    'dim': int(dim_su2),
    'expect': 2,
    'verdict': '与 su(2) 子代数对易的矩阵空间 = 2 维（diag(a,a,b)：前两色平权，第三色独立）',
}

results['C_conclusion'] = {
    'schur_lemma': (
        '完整 SU(3) ⟹ Yukawa 对颜色平庸（m·I₃，三色平权）。'
        '3=2⊕1 是限制到 su(2) 子代数的分支规则，不破坏完整 SU(3)。'
    ),
    'third_color_different_requires': (
        '「第三种颜色 Yukawa 耦合不同」⟺ 完整 SU(3) 破缺到 SU(2) 子代数。'
        '但预印本 1.9 用 Serre 构造给出完整连续 su(3)（不是只有 su(2)）。'
        '所以这个独有预言候选在「完整 SU(3) 活着的框架」里不成立。'
    ),
    'honest_verdict': (
        '「第三种颜色 Yukawa 耦合不同」这个候选 = v9 已标的「2⊕1 结构印记」'
        '（标准分支规则，任何 SU(3) 理论都有），不是独有预言。'
        '除非框架声称「颜色 SU(3) 在低能破缺到 SU(2)」，但那是另一个'
        '大胆的主张（对 QCD 的偏离），需要独立证据，不能从 3=2⊕1 分支规则推出。'
    ),
}

print(json.dumps(results, ensure_ascii=False, indent=2))
with open(Path(__file__).with_name('exp_yukawa_color_schur_last_run.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
