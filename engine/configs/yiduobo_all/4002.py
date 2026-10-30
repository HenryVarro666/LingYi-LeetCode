from itertools import product
from math import comb as _comb

_N, _K = 5, 3
_ALL = [c for c in product(range(1, _N + 1), repeat=_K) if sum(c) == _N]
assert len(_ALL) == _comb(_N - 1, _K - 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    odd = [all(v % 2 for v in c) for c in _ALL]
    cv.text((x0 + 18, y0 + 4), f'{_N} 个球排一行，插 {_K - 1} 块隔板分成 {_K} 段 = 一个序列', 24, T['muted'], bold=True)
    cols = 2
    cw = (x1 - x0 - 40) / cols
    d = 30
    for i, c in enumerate(_ALL):
        X0 = x0 + 30 + (i % cols) * cw
        Y = y0 + 56 + (i // cols) * 64
        is_odd = odd[i]
        hot = line >= 16 and is_odd
        gone = line >= 17 and is_odd
        x = X0
        for si, seg in enumerate(c):
            for b in range(seg):
                col = T['pink'] if hot else (T['green'] if line >= 13 and not is_odd and line >= 16 else T['blue'])
                if gone:
                    col = (110, 70, 80)
                cv.rect((x, Y, x + d, Y + d), fill=col, r=d // 2)
                x += d + 6
            if si < len(c) - 1:
                cv.line([(x + 1, Y - 8), (x + 1, Y + d + 8)], T['yellow'], 4)
                x += 14
        cv.text((X0 + 5 * (d + 6) + 2 * 14 + 14, Y + d / 2), ','.join(map(str, c)), 22, T['dim'] if gone else T['text'], anchor='lm', mono=True, bold=True)
        if gone:
            cv.line([(X0 - 4, Y + d / 2), (x + 90, Y + d / 2)], T['pink'], 3)
    yb = y0 + 56 + 3 * 64 + 4
    if line >= 13:
        cv.text((x0 + 20, yb), f'全部序列：C({_N - 1}, {_K - 1}) = {len(_ALL)} 个', 24, T['text'], bold=True)
    if line >= 16:
        cv.text((x0 + 20, yb + 38), f'每段补 1 个球后两两成组 → 粉色 = 全奇数的序列，共 {sum(odd)} 个', 24, T['pink'], bold=True)


def _arrays(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    fac, ivf = S.get('fac', []), S.get('inv_fac', [])
    m = max(len(fac), len(ivf), 1)
    cell = min(170, (x1 - x0 - 150) / m)
    sx = x0 + 130
    for r, (name, arr, col) in enumerate((('fac[i]', fac, 'blue'), ('inv_fac[i]', ivf, 'cyan'))):
        y = y0 + 10 + r * 72
        cv.text((x0 + 20, y + 24), name, 22, T[col], anchor='lm', bold=True, mono=True)
        for i, v in enumerate(arr):
            X = sx + i * cell
            new = i == len(arr) - 1 and i > 1
            cv.rect((X + 3, y, X + cell - 3, y + 48), fill=T['panel2'], outline=T[col] if new else T['border'], width=3 if new else 1, r=8)
            cv.text((X + cell / 2, y + 24), v, 22, T['text'], anchor='mm', bold=True, mono=True)


def _term(S):
    line = S.get('_line', 0)
    if line >= 16 and 'm' in S:
        return f"`m = (n+k)//2 = {S['m']}`，全奇数序列 `C(m−1, k−1)` = `C({S['m'] - 1}, {S['k'] - 1})` = =={S.get('odd')}=="
    if line >= 13 and 'res' in S:
        return f"全部序列 `C(n−1, k−1)` = `C({S['n'] - 1}, {S['k'] - 1})` = =={S['res']}== （隔板法）"
    return '先预处理阶乘 `fac` 和阶乘逆元 `inv_fac`，用来算组合数'


CONFIG = dict(
    num=4002, title='统计有效序列数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='插板法 · 总数减全奇数',
    tags=['组合计数', '难度分 1912'],
    code='''
class Solution(object):
    def countValidSequences(self, n, k):
        
        inv = [1, 1]
        fac = [1, 1]
        inv_fac = [1, 1]
        mod = 10 ** 9 + 7
        for v in range(2, n):
            inv.append(-(mod // v) * inv[mod % v] % mod)
            fac.append(fac[-1] * v % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)
        
        res = fac[n - 1] * inv_fac[k - 1] % mod * inv_fac[n - k] % mod
        if (n + k) % 2 == 0:
            m = (n + k) // 2
            odd = fac[m - 1] * inv_fac[k - 1] % mod * inv_fac[m - k] % mod
            res -= odd
            if res < 0:
                res += mod
        
        return res
''',
    call=f'Solution().countValidSequences({_N}, {_K})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='custom', draw=_arrays, h=160),
        dict(type='text', fn=_term, size=26, h=60),
    ],
    watch=['v', ('res', 'res', 'green'), 'm', ('odd', 'odd', 'pink')],
    skip=['inv = [1', 'fac = [1', 'inv_fac = [1', 'mod = 10'],
    captions={
        'for v in range': lambda S, B, r: (f'递推第 `{S.v}` 项' if S.get('v') is not None and not ('v' in B and S.v == B.v) else '阶乘、逆元预处理完毕'),
        'inv.append': '线性求逆元：`inv[{v}] = −(mod // {v}) × inv[mod % {v}]` 取模 = {inv[-1]}',
        'fac.append(fac[-1]': '`fac[{v}] = fac[{v - 1}] × {v}` = {fac[-1]}',
        'inv_fac.append(inv_fac': '`inv_fac[{v}] = inv_fac[{v - 1}] × inv[{v}]` = {inv_fac[-1]}（阶乘的逆元）',
        'res = fac': '全部划分：`C({n - 1}, {k - 1})` = `{n - 1}! / ({k - 1}! × {n - k}!)` = =={res}==',
        'if (n + k)': lambda S, B, r: (f'`n + k = {S.n + S.k}` 是偶数 → 补一个球后能两两成组，才存在全奇数的划分' if (S.n + S.k) % 2 == 0 else f'`n + k = {S.n + S.k}` 是奇数 → 不可能全是奇数，不用减'),
        'm = (n + k)': '每段先补 1 个球（共 `k` 个），再两个一组：一共 `m = (n+k)//2 = {m}` 组',
        'odd = fac': '`m` 组分成 `k` 段：`C({m - 1}, {k - 1})` = =={odd}==',
        'res -= odd': '总数减去全奇数划分：`{B.res} − {odd}` = =={res}==',
        'if res < 0': lambda S, B, r: ('`res < 0`，补一个 `mod`' if S.res < 0 else f'`res = {S.res}` 不是负数，不用补 `mod`'),
        'res += mod': '取模后的差可能为负，补回 `mod`',
        'return res': '至少含一个偶数的序列共 =={ret}== 个',
    },
    cards=dict(
        one_liner='先数所有划分，再减去全是奇数的划分',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `n` 拆成 `k` 个正整数，要求乘积为==偶数==，数有多少种序列（模 `10^9+7`）',
                 '示例：`n=5, k=3` → `3`（`[1,2,2]`、`[2,1,2]`、`[2,2,1]`）'],
        quote='乘积为偶数，意味着拆分出来的正整数中至少存在一个偶数……不如反过来思考，即计算出所有可能的划分方案数，减去划分出来的元素都是奇数的划分方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 个球有 `n−1` 个空隙，选 `k−1` 个插隔板：`C(n−1, k−1)`',
              '全奇数：每段先补 1 个球变成偶数，两个一组，共 `m = (n+k)/2` 组',
              '`m` 组分成 `k` 个非空段：`C(m−1, k−1)`；`n+k` 为奇数则为 0',
              '组合数要取模：线性递推逆元，预处理阶乘和阶乘逆元'],
        summary=['时间 `O(n)`（预处理），空间 `O(n)`',
                 '`n + k` 是奇数时不可能拆成 `k` 个奇数，直接不减',
                 '减法后可能为负，要 `+ mod` 补回',
                 '预处理只做到 `fac[n−1]`：循环是 `range(2, n)`，下标最大 `n−1`',
                 '对比灵神：他用 `2y−1` 代换 + 预处理；yiduobo 用「补球再两两成组」，最终同一个公式',
                 '原文已是 Python 3 可直接运行的写法，未做修改'],
    ),
)
