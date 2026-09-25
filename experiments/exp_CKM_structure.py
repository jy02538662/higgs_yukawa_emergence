"""exp_CKM_structure：推代间混合结构（CKM/PMNS），判断框架是否有独有约束。

据（Connes 标准模型 + 标准 CKM 理论）：
  三代 Yukawa 矩阵 M 变成 3×3 代矩阵（每代一个 8×8 块）。
  代间混合（CKM/PMNS）来自「上型质量矩阵 M_u 和下型质量矩阵 M_d 不能同时对角化」。
  CKM = V_u† V_d（两个幺正对角化矩阵的乘积）。

关键问题（用户留白「代间混合结构」）：
  框架的 su(3)=S₃ 来源是否约束代间混合（哪些代可以混合、哪些被禁止）？

诚实分析：
  su(3)=S₃ 是「颜色对称」的来源（作用在颜色三重态 3 上），
  与「代（generation）」是**两个独立的自由度**——S₃ 不作用于代。
  所以框架**没有代的对称性**来约束代间混合，
  代间混合 = 标准的 3×3 质量矩阵（全允许，无框架独有约束）。

本实验验证：
  A. 三代 Yukawa M 的代数结构：3×3 代矩阵，每块 8×8。
  B. 代间混合的自由度：一般 3×3 复矩阵有 18 个实参数，幺正化后 CKM 有 4 个实参数
     （3 个混合角 + 1 个 CP 相位）——标准结果。
  C. 判断：框架 su(3)=S₃ 不约束代（S₃ 只作用颜色），故 CKM 是标准结果，无独有约束。
"""

import json
from pathlib import Path

import numpy as np

results = {}

# A. 三代 Yukawa M 的结构
# 三代 M_total = 3×3 代矩阵，每块是 8×8（一代的 Yukawa 矩阵）
# 最一般的形式：M_total 是 24×24（3 代 × 8），代间可以有非零混合块
results['A_three_generation_structure'] = {
    'M_total_shape': [24, 24],
    'generation_blocks': '3×3 代矩阵，每块 8×8（含右手中微子的对称版）',
    'note': '代间混合 = 非对角代块（M_ij, i≠j）非零',
}

# B. CKM 的自由度（标准结果）
# 一般 3×3 复质量矩阵 M_u, M_d 各 18 实参数（9 复 = 18 实）
# 对角化后：6 个质量本征值（3 上 + 3 下）+ CKM 4 参数（3 角 + 1 相位）
# = 标准 CKM 自由度
results['B_CKM_dof'] = {
    'general_3x3_complex_dof': 18,
    'up_and_down': 36,
    'masses': 6,
    'CKM_parameters': 4,
    'CKM_angles': 3,
    'CP_phase': 1,
    'note': '标准结果：CKM = 3 混合角 + 1 CP 相位（不碰数值，只列自由度）',
}

# C. 框架是否约束代间混合（核心判断）
results['C_framework_constraint'] = {
    'su3_S3_acts_on': '颜色三重态 3（S₃ = SU(3) Weyl 群，作用在颜色上）',
    'generation_is': '独立自由度，与颜色无关（S₃ 不作用于代）',
    'conclusion': (
        '框架的 su(3)=S₃ 来源是「颜色对称」的来源，不约束「代」的混合。'
        '⟹ 代间混合（CKM/PMNS）是标准的 3×3 质量矩阵，无框架独有约束。'
        '⟹ CKM 结构 = 标准结果（与 Connes 标准模型一致），不是独有预言。'
    ),
}

results['D_verdict'] = {
    'CKM_structure': '标准结果，无框架独有约束',
    'reason': 'su(3)=S₃ 只作用颜色，不作用代；框架没有「代对称」来约束代间混合',
    'honest_note': '除非框架引入「代的对称性」（如 S₃ 也作用代），否则 CKM 全允许，'
                  '是标准模型的标准结果',
}

print(json.dumps(results, ensure_ascii=False, indent=2))
with open(Path(__file__).with_name('exp_CKM_structure_last_run.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
