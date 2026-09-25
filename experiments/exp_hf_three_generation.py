"""exp2 门 4 第 1 步（续）：确定有限 Hilbert 空间 H_F = 三代费米子。

据（Connes 标准模型 + 预印本 1.9）：
  H_F 承载三代费米子。每代（不含右手中微子，标准 Connes 版本）15 个 Weyl 费米子：
    - 轻子：左旋二重态 L=(ν_L, e_L)（SU(2) 二重态，无色），右旋单态 e_R
    - 夸克：左旋二重态 Q=(u_L, d_L)（SU(2) 二重态 × 色三重态），
             右旋单态 u_R（色三），d_R（色三）

  表示（SU(2)×SU(3)）：
    L:(2,1)  e_R:(1,1)  Q:(2,3)  u_R:(1,3)  d_R:(1,3)
  维度/代 = 2 + 1 + 2×3 + 3 + 3 = 15（Weyl）⟹ ×2(粒子反粒子)×3(代) = 90。

框架独有点（预印本 1.9 §六，exp1 已验）：
  颜色三重态 3 = 2⊕1（旋量⊕相位），所以 Q:(2,3) = (2, 2⊕1) = (2,2)⊕(2,1)。
  即「弱二重态 × 色三重态」在框架里 = 「弱2 × 色旋量2」⊕「弱2 × 色相位1」。
  这给出一个结构关系：色三重态内部 = 一个「自旋1/2 旋量对」+ 一个「相位单态」。

本实验：
  A. H_F 维度 = 90（三代，每代 15 Weyl，粒子反粒子 ×2）。
  B. 颜色 3=2⊕1 分解 Q:(2,3)=(2,2)⊕(2,1)，验证维度一致。
  C. 诚实边界：只定表示结构，不碰三代质量谱数值（红线）。
"""

import json
from pathlib import Path

results = {}

# A. H_F 维度
# 每代 Weyl 费米子（不含右手中微子）：
# L=(ν_L,e_L): SU(2) 二重态 dim 2，无色 → 2
# e_R: 单态 → 1
# Q=(u_L,d_L): SU(2) 二重态 dim 2 × SU(3) 三重态 dim 3 → 6
# u_R: 单态 × 色三 → 3
# d_R: 单态 × 色三 → 3
dim_per_gen = 2 + 1 + 6 + 3 + 3
dim_weyl = dim_per_gen * 3  # 三代
dim_HF = dim_weyl * 2  # 粒子 + 反粒子

results['A_HF_dimension'] = {
    'dim_per_generation': dim_per_gen,
    'dim_three_generations_weyl': dim_weyl,
    'dim_HF_with_antiparticles': dim_HF,
    'note': '每代 15 Weyl 费米子，三代 45，含反粒子 90（标准 Connes 维度）',
}

# B. 颜色 3=2⊕1 分解 Q:(2,3)
# Q:(2,3) = 弱二重态(2) × 色三重态(3)
# 颜色 3 = 2⊕1（exp1：色旋量 2 + 色相位 1）
# ⟹ Q = (2, 2⊕1) = (2,2) ⊕ (2,1)
# (2,2)：弱2 × 色旋量2 = 4 维
# (2,1)：弱2 × 色相位1 = 2 维
# 总 4+2 = 6 = 2×3 ✓
dim_Q = 2 * 3
dim_Q_decomposed = (2 * 2) + (2 * 1)
results['B_color_3_2oplus1'] = {
    'Q_dim_original': dim_Q,
    'Q_decomposed_as_22oplus21': (2 * 2, 2 * 1),
    'dim_consistent': dim_Q == dim_Q_decomposed,
    'note': 'Q:(2,3) = (2,2)⊕(2,1) = 弱2×色旋量2 ⊕ 弱2×色相位1，维度 4+2=6=2×3 ✓',
}

# C. 结构关系（框架独有的挖掘点）
results['C_unique_structure'] = {
    'statement': (
        '框架独有：色三重态 3 = 旋量2 ⊕ 相位1。'
        '所以每个带颜色的费米子（夸克），其颜色内部结构 = 一个「自旋1/2 旋量对」+ 一个「相位单态」。'
        '这意味着：夸克的颜色三重态，内部 3 个颜色分量不是平权的——'
        '其中 2 个构成一个旋量二重态（有 SU(2) 结构），1 个是相位单态。'
        '这是 Connes 标准模型没有的（他输入 3，颜色三分量平权）。'
    ),
    'potential_prediction': (
        '若框架对，则「颜色三分量不是平权的，而是 2⊕1 分解」——'
        '这可能给出一个可检验的结构预言：在某种极端条件（如色禁闭破缺/高能）下，'
        '夸克的 2⊕1 颜色结构会显现（2 个分量成对，1 个分量单独）。'
        '具体可观测形式待 exp3/exp4 用 Yukawa 结构验证。'
    ),
}

results['C_honest_boundary'] = {
    'red_line': '只定表示结构（三代、3=2⊕1），不碰三代质量谱数值（数字巧合红线）',
    'three_generations_status': '「为什么三代」本身是开放问题（本文不解释，只接受三代为输入）',
}

print(json.dumps(results, ensure_ascii=False, indent=2))
with open(Path(__file__).with_name('exp_hf_three_generation_last_run.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
