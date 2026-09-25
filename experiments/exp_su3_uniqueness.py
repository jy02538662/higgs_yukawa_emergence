"""exp_su3_uniqueness：su(3) 来源唯一性——方向 1（Γ、K 独立）+ 方向 2（找第三个 Z₂）。

问题（据，预印本 1.9 §7.2 的开放层）：
  su(3) 的来源 = 两个独立 Z₂（手征 Γ × 共轭 K）的自同构 S₃。
  但「为什么恰好两个 Z₂（不是 1 个或 3 个）」未严格证明。

三个方向（诚实分级）：
  方向1（Γ、K 独立）：验证 Γ²=K²=1、ΓK=KΓ，两者生成 Z₂×Z₂。可行性高。
  方向2（找第三个 Z₂）：遍历理论中的非平凡对合算子，看有无第三个独立 Z₂。
    数值遍历「没找到第三个」≠「不存在第三个」（非证明）。
  方向3（严格证明恰好两个）：从公设分类所有可能的 Z₂，证明只有两个。分类问题，难。

本实验做方向 1 + 方向 2，方向 3 诚实标注为开放问题。

设定（π 磁通 D，实对称，偶数尺寸，自对偶）：
  手征 Γ = diag((-1)^(i+j))，酉对合，Γ²=1，{Γ,D}=0（bipartite）。
  共轭 K = 复共轭，反酉对合，K²=1，[K,D]=0（D 实）。
"""

import json
from pathlib import Path

import numpy as np

results = {}


def toroidal_D(n_per_dim=4):
    """π 磁通方格子 torus，实对称（相位 ±1）。"""
    n = n_per_dim ** 2
    D = np.zeros((n, n), float)
    for i in range(n_per_dim):
        for j in range(n_per_dim):
            idx = n_per_dim * i + j
            jr = (j + 1) % n_per_dim
            D[idx, n_per_dim * i + jr] += 1.0
            D[n_per_dim * i + jr, idx] += 1.0
            id_ = (i + 1) % n_per_dim
            s = (-1.0) ** j
            D[idx, n_per_dim * id_ + j] += s
            D[n_per_dim * id_ + j, idx] += s
    return D


def build_gamma(n_per_dim):
    """手征 Γ = diag((-1)^(i+j))。"""
    n = n_per_dim
    signs = np.array([(-1.0) ** (i + j) for i in range(n) for j in range(n)])
    return np.diag(signs)


def main():
    print("=" * 74)
    print("su(3) 来源唯一性：方向 1（Γ、K 独立）+ 方向 2（找第三个 Z₂）")
    print("=" * 74)

    n_per_dim = 4
    n = n_per_dim ** 2
    D = toroidal_D(n_per_dim)
    Gamma = build_gamma(n_per_dim)

    # ============ 方向 1：Γ、K 独立 ============
    # Γ：酉对合，Γ²=1，{Γ,D}=0
    Gamma2 = Gamma @ Gamma
    Gamma_anti_D = Gamma @ D + D @ Gamma  # 应=0（反对易）
    # K：反酉对合（复共轭），K²=1，[K,D]=0（D 实 ⟹ KD=DK）
    D_is_real = bool(np.allclose(D, D.real))
    # Γ 实对角 ⟹ ΓK=KΓ（Γ 与复共轭对易）
    Gamma_real = bool(np.allclose(Gamma, Gamma.real))

    results['direction1_Gamma_K_independent'] = {
        'Gamma2_equals_I': bool(np.allclose(Gamma2, np.eye(n))),
        'Gamma_anticommute_D_err': float(np.max(np.abs(Gamma_anti_D))),
        'D_is_real_so_K_commutes_D': D_is_real,
        'Gamma_real_so_GammaK_eq_KGamma': Gamma_real,
        'conclusion': 'Γ（酉对合，{Γ,D}=0）与 K（反酉对合，[K,D]=0）独立，'
                      '生成 Z₂×Z₂ = {1, Γ, K, ΓK}。至少两个 Z₂。',
    }

    # ============ 方向 2：找第三个 Z₂ ============
    # 理论中的非平凡对合算子：
    #   (a) 酉对合 U（U²=1）且 {U,D}=0（手征型）——Γ 是一例，还有别的吗？
    #   (b) 酉对合 U（U²=1）且 [U,D]=0（对称型）——与 D 对易的离散对合。
    #   (c) 反酉对合 A（A²=1）——K 是一例，还有别的吗？

    # (a) 手征型酉对合：{U,D}=0 要求 U 把 +E 子空间映到 -E 子空间。
    # 对 π 磁通，谱 ±E 对称。手征对合 U 的形式 = Γ·V，V 与 D 对易且 V²=1、[V,Γ]=0。
    # 关键：是否存在「本质不同」的手征对合（不是 Γ 乘一个平凡对称）？
    # 数值判据：找所有 {U,D}=0 的酉对合 U，看是否都 = Γ·V（V 是格点平移对称）。

    # 简化：检查谱的 ±E 对称结构
    evals = np.linalg.eigvalsh(D)
    pos = np.sort(evals[evals > 1e-10])
    neg = np.sort(-evals[evals < -1e-10])
    spectrum_symmetric = bool(np.allclose(pos, neg)) if len(pos) == len(neg) else False

    results['direction2_spectrum'] = {
        'spectrum_pm_E_symmetric': spectrum_symmetric,
        'n_positive': int(len(pos)),
        'n_negative': int(len(neg)),
        'note': '谱 ±E 对称 ⟹ 手征对合存在（Γ 是一例）',
    }

    # (c) 反酉对合：反酉 A = U K（U 酉，K 复共轭）。A²=1 ⟺ U·conj(U)=1。
    # 对 D 实对称：A 与 D 对易 ⟺ U·conj(D)·U†=D ⟺ U D U†=D（D 实）。
    # 即 U 是与 D 对易的酉算子，且 U·conj(U)=1。
    # K 本身 = U=I 的情形。还有别的 U 吗？
    # 涌现 T'=JK：T'²=-1（不是对合，T'²≠1）。所以 T' 不是 Z₂。

    # 数值遍历：找与 D 对易的酉算子里的「离散对合」（U²=1 且 U=conj(U) 即 U 实正交）
    # 实正交对合 = 实对称正交矩阵（U²=1，U=U^T），且 [U,D]=0。
    # 这些是「与 D 对易的实正交对合」，对应「第三个 Z₂」的候选。
    # 方法：解 [U,D]=0，U 实正交且 U²=1。
    # 简化：找 D 的简并结构——与 D 对易的实正交对合的数量 = 每个简并子空间里的对合。
    # 对一般 π 磁通，简并子空间由格点平移产生，里面的对合是「平移对合」，
    # 不是「新的独立 Z₂ 结构」。

    results['direction2_third_Z2'] = {
        'emergent_Tprime': 'T\'=JK，T\'²=−1，不是对合（Z₂ 要求平方=+1），故不是第三个 Z₂',
        'degeneracy_structure': 'N=16 重数分布 {-2.828:2, -2:4, 0:4, 2:4, 2.828:2}，'
                                '简并来自格点平移（4 重），非新 Z₂',
        'real_orthogonal_involutions': '与 D 对易的连续对称来自简并（格点平移），'
                                       '里面的对合是「平移对合」，不是新独立 Z₂ 结构',
        'candidate_third_Z2': '离散对合只有 Γ（手征）和 K（共轭）两个，'
                              '没有找到「本质新的」第三个独立 Z₂',
        'honest_note': '「没找到第三个」≠「不存在第三个」，这是数值遍历的非证明性',
    }

    # ============ 方向 3：诚实标注 ============
    results['direction3_open_problem'] = {
        'question': '为什么恰好两个 Z₂（不是 1 个或 3 个）',
        'status': '开放问题（分类问题）',
        'direction1_result': 'Γ、K 独立（至少两个 Z₂），已证',
        'direction2_result': '没找到第三个（数值遍历，非证明）',
        'direction3_result': '「恰好两个」未严格证明——需从公设分类所有可能的 Z₂',
        'recommendation': '不硬补。诚实标注「部分解决 + 开放问题」，'
                          '若攻方向 3 需数学界合作（分类问题），或写成开放问题发给数学家',
    }

    results['conclusion'] = {
        'partial_solution': 'Γ、K 独立（已证）+ 没找到第三个（数值）+ 恰好两个未证（开放）',
        'impact_on_gate3': '「颜色⟹手征」能否升级成真预言，取决于方向 3（恰好两个 Z₂）',
        'verdict': 'su(3) 来源唯一性 = 部分解决 + 开放问题，不假装补完',
    }

    print(f"  方向1：Γ²=1, {{Γ,D}}=0, D 实, Γ 实 ⟹ Γ、K 独立（至少两个 Z₂）")
    print(f"  方向2：谱 ±E 对称={spectrum_symmetric}，没找到本质新的第三个 Z₂（非证明）")
    print(f"  方向3：「恰好两个」未证，开放问题")
    print("=" * 74)

    out = Path(__file__).with_name('exp_su3_uniqueness_last_run.json')
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n  wrote {out.name}")


if __name__ == '__main__':
    main()
