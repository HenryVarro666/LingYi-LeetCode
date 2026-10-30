import math

# setup 里的 Nums 只是普通 list，额外记下 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
class Nums(list):
    def __init__(self, it):
        super().__init__(it)
        self.live = True
    def __iter__(self):
        return self._walk() if self.live else list.__iter__(self)
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Nums(list.__iter__(self))
        c.__dict__.update(self.__dict__)
        c.live = False
        return c
'''

NUMS, K = [4, 5, 0, -2, -3, 1], 5
N = len(NUMS)
RAW = [0]
for _x in NUMS:
    RAW.append(RAW[-1] + _x)
RES = [v % K for v in RAW]
RC = ['cyan', 'pink', 'yellow', 'green', 'purple', 'orange', 'blue']

CODE = '''
class Solution(object):
    def subarraysDivByK(self, A, K):

        f = [0] * K
        f[0] = 1

        s = 0
        res = 0
        for num in A:
            s += num
            s %= K
            res += f[s]
            f[s] += 1

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_ADD, L_MOD, L_RES, L_INC = _ln('s += num'), _ln('s %= K'), _ln('res += f[s]'), _ln('f[s] += 1')


def _p(S):
    a = S.get('A')
    p = getattr(a, 'pos', None)
    return p if p is not None and p < len(a) else None


def _done(S):
    """已经算出前缀和 p[j] 的最后一个下标 / 已经取好余数的最后一个下标"""
    a = S.get('A')
    p = getattr(a, 'pos', None)
    if p is None:
        return 0, 0
    if p >= N:
        return N, N
    L = S.get('_line')
    if L == L_ADD:
        return p + 1, p
    if L in (L_MOD, L_RES, L_INC):
        return p + 1, p + 1
    return p, p


def _stored(S):
    c = S.get('f')
    return sum(c) if isinstance(c, list) else 0


def _hits(S):
    if S.get('_line') != L_RES or _p(S) is None:
        return []
    D = _done(S)[0]
    return [j for j in range(D) if RES[j] == RES[D]]


def _arc_dn(cv, p0, p1, drop, color, width=4, head=13):
    (x0, y0), (x1, y1) = p0, p1
    cx, cy = (x0 + x1) / 2, max(y0, y1) + drop
    pts = []
    for i in range(41):
        t = i / 40
        pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                    (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
    cv.line(pts, color, width)
    (xa, ya), (xb, yb) = pts[-3], pts[-1]
    ang = math.atan2(yb - ya, xb - xa)
    a1, a2 = ang + math.pi * 0.83, ang - math.pi * 0.83
    cv.poly([(xb, yb), (xb + head * math.cos(a1), yb + head * math.sin(a1)),
             (xb + head * math.cos(a2), yb + head * math.sin(a2))], color)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ncol = N + 1
    W = x1 - x0 - 150
    cw = min(140, W / ncol)
    sx = x0 + 130 + (W - cw * ncol) / 2
    X = lambda j: sx + j * cw + cw / 2
    (D, Dr), st, p = _done(S), _stored(S), _p(S)
    hits = _hits(S)
    live = S.get('_line') in (L_ADD, L_MOD, L_RES, L_INC)
    cv.text((x0 + 18, y0 + 4), '前缀和 p[j] 和它对 K 的余数（同色 = 同余，下划线 = 已记进 f）', 22, T['muted'], bold=True)
    ya, yb, yc = y0 + 70, y0 + 160, y0 + 252
    ch = 56
    for lab, yy in (('A', ya), ('p[j]', yb), (f'p % {K}', yc)):
        cv.text((sx - 16, yy + ch / 2), lab, 24, T['muted'], anchor='rm', bold=True)
    past = p if p is not None else (N if D >= N else 0)
    for j in range(ncol):
        xc = X(j)
        cv.text((xc, y0 + 40), f'j={j}', 18, T['dim'], anchor='mt', mono=True)
        bw = cw - 16
        if j == 0:
            cv.text((xc, ya + ch / 2), '空前缀', 20, T['dim'], anchor='mm', bold=True)
        else:
            cur = p == j - 1
            cv.rect((xc - bw / 2, ya, xc + bw / 2, ya + ch), fill=T['panel'] if j - 1 < past else T['panel2'],
                    outline=T['pink'] if cur else T['border'], width=4 if cur else 1, r=10)
            cv.text((xc, ya + ch / 2), NUMS[j - 1], 28, T['pink'] if cur else T['text'], anchor='mm', bold=True)
        have, haver = j <= D, j <= Dr
        newest = live and have and j == D
        cv.rect((xc - bw / 2, yb, xc + bw / 2, yb + ch), fill=T['panel2'] if have else None,
                outline=T['yellow'] if newest else T['border'], width=4 if newest else 1, r=10)
        cv.text((xc, yb + ch / 2), RAW[j] if have else '?', 28, (T['red'] if RAW[j] < 0 else T['text']) if have else T['dim'],
                anchor='mm', bold=True)
        c = T[RC[RES[j] % len(RC)]]
        cv.rect((xc - bw / 2, yc, xc + bw / 2, yc + ch + 6), fill=c if haver else None,
                outline=T['text'] if j in hits else T['border'], width=4 if j in hits else 1, r=10)
        cv.text((xc, yc + ch / 2 + 3), RES[j] if haver else '?', 30, T['bg'] if haver else T['dim'], anchor='mm', bold=True)
        if j < st and haver:
            cv.rect((xc - bw / 2, yc + ch + 12, xc + bw / 2, yc + ch + 18), fill=c, r=3)
    for j in hits:
        _arc_dn(cv, (X(D), yc + ch + 22), (X(j), yc + ch + 22), 24 + 8 * (D - j), T['green'], 4)


def _fx(S, B):
    L = S.get('_line')
    if _p(S) is None:
        return 'p[j] − p[i−1] = 区间和；区间和是 K 的倍数 ⇔ 两个前缀和 ==模 K 同余=='
    D, Dr = _done(S)
    if L == L_RES:
        hs = _hits(S)
        if hs:
            return (f"余数 `{S['s']}` 之前出现过 `{len(hs)}` 次（{'、'.join('p[%d]' % j for j in hs)}）→ ==新增 {len(hs)} 个==")
        return f"余数 `{S['s']}` 之前没出现过 → 这一步不增加答案"
    if L == L_INC:
        return f"把 `p[{D}] % K = {S['s']}` 也记进 `f`，留给后面的前缀配对"
    if L == L_ADD:
        return f"`p[{D}] = {RAW[D]}`（`s` 里存的是上一个余数 + `num`，还没取模）"
    if L == L_MOD:
        return f"`p[{D}] = {RAW[D]}`，`{RAW[D]} % {K} = {RES[D]}`" + ('（负数也被调成了非负）' if RAW[D] < 0 else '')
    return '区间和是 K 的倍数 ⇔ 两个前缀和 ==模 K 同余=='


CONFIG = dict(
    num=974, title='和可被 K 整除的子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和之差 · 余数计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1676'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().subarraysDivByK(Nums({NUMS}), {K})',
    expect=7,
    views=[
        dict(type='text', fn=_fx, h=84, size=26),
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='f', label='f（下标 = 余数，值 = 该余数的前缀和已出现几次）', cell=110, h=170,
             pointers={'s': 'blue'}, color=lambda S, i, v: RC[i % len(RC)] if v else None),
    ],
    watch=['num', ('s', 's', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [0] * K': '`f[r]`：余数为 `r` 的前缀和出现了几次，余数只有 `0 ~ K−1`，长度 `K = {K}`',
        'f[0] = 1': '空前缀（和为 0）的余数是 0，先记 1 次：==这样从 A[0] 开始的子数组也能配上对==',
        'res = 0': '`res` 累计满足条件的子数组个数',
        's = 0': '`s` 是当前前缀和对 K 的余数',
        'for num in A': lambda S, B, ret: (f'往右扫：取下一个数 `num = {S.num}`' if _p(S) is not None else '`A` 扫完了'),
        's += num': lambda S, B, ret: f'`s = {B.s} + ({S.num}) = {S.s}`：上一个余数加上 `num`，还没取模',
        's %= K': lambda S, B, ret: (f'`{B.s} % {S.K} = {S.s}`：这就是 `p[{_done(S)[0]}] mod K`'
                                     + ('，负数被调成了非负余数' if B.s < 0 else '')),
        'res += f[s]': lambda S, B, ret: (f'`f[{S.s}] = {S.f[S.s]}`：之前有 `{S.f[S.s]}` 个前缀和与当前前缀 ==模 K 同余==，'
                                          f'各对应一个子数组 → `res = {B.res} + {S.f[S.s]} = {S.res}`'),
        'f[s] += 1': lambda S, B, ret: (f'先数完答案，再把当前余数记进 `f`：`f[{S.s}] = {S.f[S.s]}`。==顺序反了会自己和自己配对=='
                                        if _p(S) == 0 else f'再把当前余数记进 `f`：`f[{S.s}] = {S.f[S.s]}`'),
        'return res': '答案：和被 `{K}` 整除的子数组共 =={res}== 个',
    },
    cards=dict(
        one_liner='区间和 = 两个前缀和之差，模 K 同余就是 K 的倍数',
        complexity='时间 `O(n + K)`，空间 `O(K)`',
        problem=['给整数数组 `A` 和整数 `K`，统计元素和==能被 K 整除==的非空连续子数组个数',
                 f'示例：`A = {NUMS}, K = {K}` → `7`',
                 '例如 `[5]`、`[5,0]`、`[0]`、`[-2,-3]`，共 7 个'],
        quote='转化到前缀和就是p[j]与p[i - 1]模K同余数。……检测s mod K之前出现的次数并更新答案，然后将s mod K也加入到dict中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p[j] = p[i−1] + s`，所以区间和 `s = p[j] − p[i−1]`，一次减法就能算出',
              '`s` 是 K 的倍数 ⇔ `p[j]` 与 `p[i−1]` ==除以 K 的余数相同==',
              '一边算前缀和一边记「每种余数出现了几次」，当前余数之前出现过几次，就新增几个子数组'],
        result='返回 `7`：这 7 个子数组的和分别是 5、5、5、0、0、−5、−5，都是 5 的倍数',
        summary=['时间 `O(n + K)`，空间 `O(K)`',
                 '`f[0] = 1` 不能漏：它代表「空前缀」，不然以 `A[0]` 开头的子数组会漏掉',
                 '==先 `res += f[s]`，再 `f[s] += 1`==：顺序反了，当前前缀会和自己配对',
                 '原文讲的是 dict，代码用长为 K 的数组 `f` 代替，思路相同；Python 的 `%` 对负数也给非负余数',
                 '原文是 Python 2 风格（`class Solution(object)`），本题代码无需改动'],
    ),
)
