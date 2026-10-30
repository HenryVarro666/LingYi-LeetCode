from fractions import Fraction

N, KK, MP = 5, 3, 4   # n, k, maxPts


def _fr(x):
    q = Fraction(x).limit_denominator(4096)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def _done(S, B):
    """循环已结束（for 行再执行一次但 i 没变）或已 return"""
    line = S.get('_line')
    return line == 12 or (line == 5 and B.get('i') == S.get('i') and B.get('_line') != 4)


def _window(S, B):
    i, line = S.get('i'), S.get('_line')
    if i is None or _done(S, B):
        return None
    if line in (5, 6):
        return i + 1, i + MP
    if line in (9, 10):
        return i, i + MP
    if line == 11:
        return i, i + MP - 1
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    i, line = S.get('i'), S.get('_line')
    f = S.get('f')
    done = _done(S, B)
    total = N + MP + 1           # 下标 0..N+MP
    cell = min(92, (x1 - x0 - 60) / total)
    sx = x0 + (x1 - x0 - cell * total) / 2
    top = y0 + 80
    cv.text((x0 + 18, y0 + 4), 'f[i]：从 i 分开始，最终分数落在 [k, n] 的概率', 24, T['muted'], bold=True)
    # 区间标注
    xa, xb = sx + KK * cell, sx + (N + 1) * cell
    cv.rect((xa + 2, top - 34, xb - 2, top - 8), fill=T['green'], alpha=60, r=6)
    cv.text(((xa + xb) / 2, top - 21), f'[k, n] = [{KK}, {N}]：停且赢 → 1', 18, T['green'], anchor='mm', bold=True)
    xc, xd = sx + (N + 1) * cell, sx + total * cell
    cv.rect((xc + 2, top - 34, xd - 2, top - 8), fill=T['red'], alpha=50, r=6)
    cv.text(((xc + xd) / 2, top - 21), '> n：出界 → 0', 18, T['red'], anchor='mm', bold=True)
    win = _window(S, B)
    if win:
        a, b = win
        if b >= a:
            cv.rect((sx + a * cell - 4, top - 4, sx + (b + 1) * cell + 4, top + cell + 4), fill=T['cyan'], alpha=40, r=10)
            cv.rect((sx + a * cell - 4, top - 4, sx + (b + 1) * cell + 4, top + cell + 4), outline=T['cyan'], width=3, r=10)
    for idx in range(total):
        X = sx + idx * cell
        if idx > N:
            txt, known = '0', True
        elif f is None:
            txt, known = '', False
        else:
            known = done or (i is not None and (idx > i or (idx == i and line in (6, 9, 10, 11))))
            txt = _fr(f[idx]) if known else '?'
        cur = (i == idx and line == 6 and not done)
        fill = T['green'] if cur else (T['panel2'] if idx <= N else (40, 45, 53))
        cv.rect((X + 3, top, X + cell - 3, top + cell), fill=fill, r=8,
                outline=T['border'])
        fs = 26 if len(txt) <= 3 else (21 if len(txt) <= 5 else 17)
        tc = T['bg'] if cur else (T['text'] if known and idx <= N else T['dim'])
        cv.text((X + cell / 2, top + cell / 2), txt, fs, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, top + cell + 6), idx, 18, T['dim'], anchor='mt', mono=True)
    if i is not None and not done:
        X = sx + i * cell + cell / 2
        cv.tri_up(X, top + cell + 40, 10, T['yellow'])
        cv.text((X, top + cell + 56), 'i', 22, T['yellow'], anchor='mt', bold=True)


def _sum_text(S, B):
    win = _window(S, B)
    s = S.get('s')
    if s is None:
        return '`f[i] = (f[i+1] + … + f[i+maxPts]) / maxPts`：窗口长度固定为 `maxPts`'
    if S.get('_line') == 6 and S['i'] < KK:
        return f"`f[{S['i']}] = s / maxPts = ({_fr(s)}) / {MP}` = =={_fr(S['f'][S['i']])}=="
    if win:
        a, b = win
        return f'窗口 `f[{a}..{b}]` 之和 `s` = =={_fr(s)}==（出界的算 0）'
    return f'`s` = {_fr(s)}'


def _cap_fi(S, B, ret):
    i = S.i
    if i >= S.k:
        return f'`i = {i} ≥ k = {S.k}`：停止抽牌，且 `{i} ≤ n` → 一定赢，`f[{i}] = 1`'
    return (f'`i = {i} < k`：还要抽，`1..{S.maxPts}` 等概率 → `f[{i}]` = 窗口平均 = '
            f'`{_fr(S.s)} / {S.maxPts}` = =={_fr(S.f[i])}==')


def _cap_if(S, B, ret):
    i, m = S.i, S.maxPts
    if i + m <= S.n:
        return f'`{i} + {m} ≤ n`：`f[{i + m}]` 在数组里，下一轮窗口不含它 → 要减掉'
    return f'`{i} + {m} > n`：要移出的 `f[{i + m}]` 出界，本来就是 0，不用减'


CONFIG = dict(
    num=837, title='新 21 点', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='倒序 DP + 定长滑动窗口',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def new21Game(self, n: int, k: int, maxPts: int) -> float:
        f = [0.0] * (n + 1)
        s = 0.0
        for i in range(n, -1, -1):
            f[i] = 1.0 if i >= k else s / maxPts
            # 当前循环计算的是 f[i+1] + ... + f[i+maxPts]
            # 下个循环计算的是 f[i] + ... + f[i+maxPts-1]，多了 f[i]，少了 f[i+maxPts]
            s += f[i]
            if i + maxPts <= n:
                s -= f[i + maxPts]
        return f[0]
''',
    call=f'Solution().new21Game({N}, {KK}, {MP})',
    expect=0.921875,
    views=[
        dict(type='text', h=70, size=26, fn=_sum_text),
        dict(type='custom', h=330, draw=_draw),
    ],
    watch=['n', 'k', 'maxPts', ('i', 'i', 'yellow'), ('s', 's', 'cyan')],
    captions={
        'f = [0.0] * (n + 1)': '`f[i]`：从 `i` 分开始，最终落在 `[k, n]` 的概率；只开 `n + 1` 个，下标 `> n` 视为 0',
        's = 0.0': '`s`：窗口 `f[i+1] + … + f[i+maxPts]` 的和；一开始窗口全在出界区 → `0`',
        'for i in range': lambda S, B, r: ('所有 `f[i]` 都算完了' if B.get('i') == S.get('i')
                                           else f'倒序：`f[{S.i}]` 依赖更大的 `f[{S.i + 1}..{S.i + S.maxPts}]`，它们都已算好'),
        'f[i] = 1.0 if': _cap_fi,
        's += f[i]': lambda S, B, r: f'「计算-入-出」：`f[{S.i}]` 算完才能入窗口 → `s` = =={_fr(S.s)}==',
        'if i + maxPts <= n': _cap_if,
        's -= f[i + maxPts]': lambda S, B, r: (f'`f[{S.i + S.maxPts}] = {_fr(S.f[S.i + S.maxPts])}` 出窗口 → `s` = =={_fr(S.s)}==，'
                                               f'窗口变成 `f[{S.i}..{S.i + S.maxPts - 1}]`'),
        'return f[0]': lambda S, B, r: f'`f[0]`：从 0 分开始、最终分数 `≤ n` 的概率 = =={_fr(r)}== = `{r}`',
    },
    cards=dict(
        one_liner='f[i] = 后面 maxPts 个状态的平均值，用定长滑窗 O(1) 求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从 0 分开始，分数 `< k` 时就从 `[1, maxPts]` 等概率抽一个数累加',
                 '分数 `≥ k` 时停止。求最终分数 `≤ n` 的概率',
                 '示例：`n = 6, k = 1, maxPts = 10` → `0.6`；动画用 `n = 5, k = 3, maxPts = 4`'],
        quote='由于转移方程中的分子是一个==长度固定为 maxPts 的连续子数组的元素和==，所以可以用定长滑动窗口 O(1) 计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举这一次抽到几分：`f[i] = (f[i+1] + … + f[i+maxPts]) / maxPts`',
              '初始值：`k ≤ i ≤ n` 时 `f[i] = 1`；`i > n` 时 `f[i] = 0`（出界即 0）',
              '转移来源比 `i` 大 → ==倒序==枚举；分子是定长窗口和 → 滑窗维护 `s`'],
        result='`f[0] = 59/64 = 0.921875`',
        after=[dict(heading='为什么是「计算-入-出」？', lines=[
            '遍历到 `i` 时，窗口左端点是 `i + 1`，`f[i]` 还不在窗口里',
            '所以先用 `s` 算出 `f[i]`，再把 `f[i]` 加进窗口',
            '最后移出 `f[i + maxPts]`，为下一轮 `i - 1` 准备好窗口'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：倒序枚举；窗口顺序是先计算、再入、再出',
                 '易错：`i + maxPts > n` 时出界的 `f` 当 0，不能去减（会越界）',
                 '`k = 0` 时 `f[0] = 1` 直接成立，代码无需特判'],
    ),
)
