from itertools import combinations

_N, _POS, _K = 5, 2, 2


def _plans(n, pos, k):
    """pos 看到恰好 k 个人的全部方案（pos 本人的方向另算 ×2）"""
    others = [i for i in range(n) if i != pos]
    out = []
    for vis in combinations(others, k):
        s = ''
        for i in range(n):
            if i == pos:
                s += '*'
            elif i < pos:
                s += 'L' if i in vis else 'R'
            else:
                s += 'R' if i in vis else 'L'
        out.append((s, vis))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, pos, k = S['n'], S['pos'], S['k']
    plans = _plans(n, pos, k)
    cv.text((x0 + 18, y0 + 4), f'n={n}，pos={pos}：从其余 {n - 1} 人里挑 {k} 个"被看见"的人，每种挑法方向唯一', 24, T['muted'], bold=True)
    cell = 64
    cols = 2
    rows = (len(plans) + cols - 1) // cols
    colw = (x1 - x0 - 40) / cols
    for t, (s, vis) in enumerate(plans):
        cx = x0 + 20 + (t % cols) * colw + (colw - n * cell) / 2
        cy = y0 + 70 + (t // cols) * (cell + 36)
        for i, ch in enumerate(s):
            X = cx + i * cell
            if ch == '*':
                fill, txt = T['yellow'], 'pos'
            elif i in vis:
                fill, txt = T['green'], ch
            else:
                fill, txt = T['panel2'], ch
            cv.rect((X + 3, cy, X + cell - 3, cy + cell - 8), fill=fill, r=8, outline=T['border'])
            cv.text((X + cell / 2, cy + (cell - 8) / 2), txt, 26 if ch != '*' else 20, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
    yb = y0 + 70 + rows * (cell + 36) + 10
    cv.text((x0 + 20, yb), f'绿色 = 被 pos 看见（共 {k} 个），灰色 = 看不见；一共 {len(plans)} 种 = C({n - 1}, {k})', 24, T['text'], bold=True)
    cv.text((x0 + 20, yb + 44), f'pos 自己选 L 或 R 都行 → ×2：{len(plans)} × 2 = {len(plans) * 2}', 26, T['yellow'], bold=True)


CONFIG = dict(
    num=3881, title='恰好看到 K 个人的方向选择', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='组合数 · 选出被看见的人',
    tags=['组合计数', '难度分 1761'],
    setup='''
from math import comb
''',
    code='''
class Solution:
    def countVisiblePeople(self, n: int, pos: int, k: int) -> int:
        # 这样写很慢，预处理的写法见另一份代码【Python3 预处理】
        return comb(n - 1, k) * 2 % 1_000_000_007
''',
    call=f'Solution().countVisiblePeople({_N}, {_POS}, {_K})',
    expect=12,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"`2 × C(n−1, k)` = `2 × C({S['n'] - 1}, {S['k']})` = ==2 × {__import__('math').comb(S['n'] - 1, S['k'])}== = =={2 * __import__('math').comb(S['n'] - 1, S['k'])}==", size=30, h=70),
    ],
    watch=['n', 'pos', 'k'],
    captions={
        'return comb': lambda S, B, ret: f"被看见的 `{S.k}` 人从其余 `{S.n - 1}` 人里选：`C({S.n - 1}, {S.k})` = {__import__('math').comb(S.n - 1, S.k)}；方向全部唯一；`pos` 自己 ×2；返回 =={ret}==",
    },
    cards=dict(
        one_liner='先选谁被看见，方向就全定了；pos 自己再乘 2',
        complexity='时间 `O(1)`（不计预处理），空间 `O(1)`',
        problem=['`n` 个人排一排，每人选 `L` 或 `R`',
                 '`pos` 左边的人选 `L` 才可见，右边的人选 `R` 才可见',
                 '求 `pos` 恰好看到 `k` 人的方案数（模 `10^9+7`）；示例：`n=5, pos=2, k=2` → `12`'],
        quote='一旦我们确定了被 pos 看到的 k 个人，那么这 k 个人的方向是唯一确定的……其余 n-1-k 个人不可见，方向也是唯一确定的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `n-1` 个人里选 `k` 个被看见：`C(n-1, k)` 种',
              '被选中的人和没被选中的人，方向都由所在位置唯一决定',
              '`pos` 本人向左向右都不影响计数：==乘 2==，答案 `2·C(n-1, k)`'],
        after=[dict(heading='n 很大时怎么算组合数', lines=[
            '`n` 到 `10^5`，`math.comb` 每次现算很慢',
            '原文的另一份代码：先预处理阶乘 `fac[i]` 和逆元阶乘 `inv_f[i]`',
            '`C(n, m) = fac[n] * inv_f[m] * inv_f[n-m] % MOD`，==O(1)== 一次',
            '预处理写在 class 外面，只初始化一次'])],
        summary=['复杂度 `O(1)`（`n` 大时需预处理阶乘和逆元，预处理 `O(n)`）',
                 '题里的 `pos` 其实不影响答案，只有 `n` 和 `k` 有用',
                 '别忘了 `pos` 自己的 ×2，以及最后取模',
                 '这里用 `math.comb`，原文还给了「Python3 预处理」写法：阶乘 + 逆元阶乘，更快'],
    ),
)
