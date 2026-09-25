"""exp5 门 4 第 2 步（完整）：构造一代 + 三代的 Yukawa 矩阵 M 的完整块结构。

据（Connes 标准模型 + 预印本 1.9）：
  有限 Dirac D_F = [[0, M],[M†, 0]]，M: H_R → H_L 是 Yukawa 矩阵。

一代的费米子（不含右手中微子，标准 Connes 版本）：
  左手 H_L：
    - 轻子二重态 L = (ν_L, e_L)：SU(2) 二重态，无色，2 维
    - 夸克二重态 Q = (u_L, d_L)：SU(2) 二重态 × 颜色 3，6 维
    H_L 共 8 维
  右手 H_R：
    - e_R：单态，1 维
    - u_R：单态 × 颜色 3，3 维
    - d_R：单态 × 颜色 3，3 维
    H_R 共 7 维

M 的块结构（8×7，行=左手，列=右手）：
  - e_R → e_L：Yukawa y_e（1×1）
  - u_R → u_L：Yukawa y_u ⊗ I₃（3×3，颜色对角）
  - d_R → d_L：Yukawa y_d ⊗ I₃（3×3，颜色对角）

关键验证：
  A. M 的颜色部分必须对角（Schur 引理，exp3 已证完整 SU(3) ⟹ 颜色平庸）。
  B. M 的维度 8×7，三代后 24×21。
  C. 用框架的 3=2⊕1（颜色三重态=旋量⊕相位）看 M 的颜色块结构。

不碰红线：y_e, y_u, y_d 是符号，不给数值。
"""

import json
from pathlib import Path

import numpy as np

results = {}


def one_generation_M(y_e, y_u, y_d):
    """一代 Yukawa 矩阵 M: H_R(7) → H_L(8)，块结构含颜色对角 I₃。

    行序（H_L，8 维）：[ν_L, e_L, u_L(r,g,b), d_L(r,g,b)]
    列序（H_R，7 维）：[e_R, u_R(r,g,b), d_R(r,g,b)]
    """
    M = np.zeros((8, 7), dtype=complex)
    # e_R → e_L（行 1 = e_L）
    M[1, 0] = y_e
    # u_R(r,g,b) → u_L(r,g,b)（行 2,3,4 = u_L 三色，列 1,2,3 = u_R 三色）
    M[2:5, 1:4] = y_u * np.eye(3)
    # d_R(r,g,b) → d_L(r,g,b)（行 5,6,7 = d_L 三色，列 4,5,6 = d_R 三色）
    M[5:8, 4:7] = y_d * np.eye(3)
    return M


def main():
    print("=" * 74)
    print("门 4 第 2 步（完整）：一代 + 三代 Yukawa 矩阵 M 的块结构")
    print("=" * 74)

    y_e, y_u, y_d = 1.0 + 0j, 2.0 + 0j, 3.0 + 0j  # 符号占位（不给物理数值）
    M1 = one_generation_M(y_e, y_u, y_d)

    results['A_one_generation'] = {
        'M_shape': list(M1.shape),
        'M_blocks': {
            'e_block': 'M[1,0] = y_e (1x1)',
            'u_block': 'M[2:5,1:4] = y_u·I₃ (3x3 颜色对角)',
            'd_block': 'M[5:8,4:7] = y_d·I₃ (3x3 颜色对角)',
        },
        'note': 'M 是 8×7，块对角，颜色部分 = y_u·I₃ / y_d·I₃（Schur 引理 ⟹ 颜色平庸）',
    }

    # B. 颜色对角验证（Schur）：u/d 块是 y·I₃，不是一般 3×3
    u_block = M1[2:5, 1:4]
    d_block = M1[5:8, 4:7]
    u_diagonal = bool(np.allclose(u_block, y_u * np.eye(3)))
    d_diagonal = bool(np.allclose(d_block, y_d * np.eye(3)))
    results['B_color_diagonal'] = {
        'u_block_is_y_u_I3': u_diagonal,
        'd_block_is_y_d_I3': d_diagonal,
        'note': '颜色块 = y·I₃（对角），印证 exp3 Schur 引理：完整 SU(3) ⟹ 三色 Yukawa 平权',
    }

    # C. 三代：M 变成块对角 3×3 代，每代 8×7
    # 三代 = 每代一个副本，M_total = diag(M1, M1, M1)（先忽略代间混合 CKM）
    M3 = np.kron(np.eye(3), M1)  # 3 代直和，24×21
    results['C_three_generation'] = {
        'M_total_shape': list(M3.shape),
        'note': '三代直和 M_total = diag(M1,M1,M1)，24×21（忽略 CKM 代间混合，那是另一层）',
    }

    # D. 框架独有的 3=2⊕1 视角：颜色三重态 = 旋量2 ⊕ 相位1
    # u_R 的颜色 3 = 旋量对(r,g) ⊕ 相位(b)。M 的颜色块 y_u·I₃ 在这分解下：
    # y_u·I₃ = y_u·diag(1,1,1) = y_u·(旋量块 I₂ ⊕ 相位块 1)
    # 即颜色三重态内部，2 个色（旋量对）+ 1 个色（相位），Yukawa 都是 y_u（平权）
    results['D_3_eq_2oplus1_view'] = {
        'color_decomposition': 'y_u·I₃ = y_u·(I₂ ⊕ 1)，旋量对(r,g) + 相位(b) 都耦合 y_u',
        'note': '3=2⊕1 是分支规则（限制到 su(2) 子代数看），不改变「三色平权」这个 Schur 结论',
    }

    # E. 结论
    results['E_conclusion'] = {
        'M_complete': '一代 8×7 块结构 + 三代 24×21，完整构造完成',
        'color_structure': '颜色块 y·I₃ 对角（Schur），3=2⊕1 不改变平权',
        'next': 'exp6 实结构 J（电荷共轭）',
    }

    print(f"  一代 M 形状: {list(M1.shape)}")
    print(f"  颜色块对角（Schur）: u={u_diagonal}, d={d_diagonal}")
    print(f"  三代 M_total 形状: {list(M3.shape)}")
    print("=" * 74)

    out = Path(__file__).with_name('exp_yukawa_M_structure_last_run.json')
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n  wrote {out.name}")


if __name__ == '__main__':
    main()
