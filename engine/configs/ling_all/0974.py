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

NUMS, K = [3, -4, 2, -2, 1], 4
N = len(NUMS)
RAW = [0]
for _x in NUMS:
    RAW.append(RAW[-1] + _x)
RES = [v % K for v in RAW]
RC = ['cyan', 'pink', 'yellow', 'green', 'purple', 'orange', 'blue']

CODE = '''
class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        cnt = [0] * k
        ans = s = 0
        for x in nums:
            cnt[s] += 1
            s = (s + x) % k
            ans += cnt[s]
        return ans
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_S, L_ANS = _ln('s = (s + x)'), _ln('ans += cnt[s]')


def _p(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    """已经算出余数的最后一个前缀下标"""
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    if p is None:
        return 0
    if p >= N:
        return N
    return p + 1 if S.get('_line') in (L_S, L_ANS) else p


def _stored(S):
    c = S.get('cnt')
    return sum(c) if isinstance(c, list) else 0


def _hits(S):
    if S.get('_line') != L_ANS or _p(S) is None:
        return []
    D = _done(S)
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
    cw = min(150, W / ncol)
    sx = x0 + 130 + (W - cw * ncol) / 2
    X = lambda j: sx + j * cw + cw / 2
    D, st, p = _done(S), _stored(S), _p(S)
    hits = _hits(S)
    cv.text((x0 + 18, y0 + 4), '前缀和 s[j] 和它对 k 取模的余数（同色 = 同余，下划线 = 已存进 cnt）', 22, T['muted'], bold=True)
    ya, yb, yc = y0 + 70, y0 + 160, y0 + 252
    ch = 56
    for lab, yy in (('nums', ya), ('s[j]', yb), (f's % {K}', yc)):
        cv.text((sx - 16, yy + ch / 2), lab, 24, T['muted'], anchor='rm', bold=True)
    for j in range(ncol):
        xc = X(j)
        cv.text((xc, y0 + 40), f'j={j}', 18, T['dim'], anchor='mt', mono=True)
        bw = cw - 16
        # nums 行：第 j 个前缀由 nums[j-1] 加进来
        if j == 0:
            cv.text((xc, ya + ch / 2), '空前缀', 20, T['dim'], anchor='mm', bold=True)
        else:
            cur = p == j - 1
            cv.rect((xc - bw / 2, ya, xc + bw / 2, ya + ch), fill=T['panel'] if (j - 1 < (p if p is not None else (N if _done(S) >= N else 0))) else T['panel2'],
                    outline=T['pink'] if cur else T['border'], width=4 if cur else 1, r=10)
            cv.text((xc, ya + ch / 2), NUMS[j - 1], 28, T['pink'] if cur else T['text'], anchor='mm', bold=True)
        # 前缀和行
        have = j <= D
        newest = have and j == D and S.get('_line') in (L_S, L_ANS)
        cv.rect((xc - bw / 2, yb, xc + bw / 2, yb + ch), fill=T['panel2'] if have else None,
                outline=T['yellow'] if newest else T['border'], width=4 if newest else 1, r=10)
        cv.text((xc, yb + ch / 2), RAW[j] if have else '?', 28, (T['red'] if RAW[j] < 0 else T['text']) if have else T['dim'],
                anchor='mm', bold=True)
        # 余数行
        c = T[RC[RES[j] % len(RC)]]
        cv.rect((xc - bw / 2, yc, xc + bw / 2, yc + ch + 6), fill=c if have else None, alpha=255 if have else 255,
                outline=T['text'] if (j in hits or (newest and hits)) else T['border'], width=4 if j in hits else 1, r=10)
        cv.text((xc, yc + ch / 2 + 3), RES[j] if have else '?', 30, T['bg'] if have else T['dim'], anchor='mm', bold=True)
        if j < st and have:
            cv.rect((xc - bw / 2, yc + ch + 12, xc + bw / 2, yc + ch + 18), fill=c, r=3)
    # 同余配对的弧线
    for j in hits:
        _arc_dn(cv, (X(D), yc + ch + 22), (X(j), yc + ch + 22), 24 + 8 * (D - j), T['green'], 4)
    # 负数前缀和提示
    if 0 <= D <= N and RAW[D] < 0 and S.get('_line') in (L_S, L_ANS):
        cv.text((X(D), yb - 6), f'{RAW[D]} % {K} = {RES[D]}', 20, T['red'], anchor='mb', bold=True)


def _fx(S, B):
    L = S.get('_line')
    if L == L_ANS and _p(S) is not None:
        D = _done(S)
        hs = _hits(S)
        if hs:
            return (f"`s[{D}]` 余数 `{S['s']}`，前面同余：{'、'.join('s[%d]' % j for j in hs)} → ==新增 {len(hs)} 个==")
        return f"`s[{D}]` 的余数 `{S['s']}` 前面没出现过 → 新增 ==0 个=="
    if L == L_S and _p(S) is not None:
        D = _done(S)
        if RAW[D] < 0:
            return f'前缀和 `s[{D}] = {RAW[D]}` 是负数，取模调整成非负余数 `{RES[D]}`：`-1` 和 `3` 同余'
        return f'`s[{D}] = {RAW[D]}`，模 {K} 得 `{RES[D]}`'
    return '子数组和 = `s[r] − s[l]`；被 k 整除 ⇔ 两个前缀和 ==模 k 同余=='


CONFIG = dict(
    num=974, title='和可被 K 整除的子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 同余 · 数组计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1676'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().subarraysDivByK(Nums({NUMS}), {K})',
    expect=4,
    views=[
        dict(type='text', fn=_fx, h=84, size=26),
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='cnt', label='cnt（下标 = 余数，值 = 该余数的前缀和已有几个）', cell=110, h=170,
             pointers={'s': 'blue'}, color=lambda S, i, v: RC[i % len(RC)] if v else None),
    ],
    watch=['x', ('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [0] * k': '`cnt[r]` 记「余数为 `r` 的前缀和出现了几个」，余数只有 `0 ~ k−1`，开一个长为 `k = {k}` 的数组',
        'ans = s = 0': '`s` 是==前缀和对 k 的余数==（边走边取模），初始 `s = 0` 就是空前缀 `s[0]`',
        'for x in nums': lambda S, B, ret: (f'枚举右端点：取下一个数 `x = {S.x}`' if _p(S) is not None else '`nums` 遍历完了，循环结束'),
        'cnt[s] += 1': lambda S, B, ret: (f'先把上一个前缀的余数 `{S.s}` 存进 `cnt`：`cnt[{S.s}] = {S.cnt[S.s]}`。'
                                          f'==先存旧的再算新的==：空前缀自动入库，也不会自己配自己'),
        's = (s + x) % k': lambda S, B, ret: (
            f'`({B.s} + ({S.x})) = {B.s + S.x}` 是负数，`% {S.k}` 把它调成非负余数 `{S.s}`：负数 `-1` 和 `3` 同余，要归到同一格'
            if B.s + S.x < 0 else f'`s = ({B.s} + ({S.x})) % {S.k} = {S.s}`：加上 `x`，得到新前缀和的余数'),
        'ans += cnt[s]': lambda S, B, ret: (f'前面余数同为 `{S.s}` 的前缀有 `{S.cnt[S.s]}` 个，每个都能和当前前缀配成一个被 {S.k} 整除的子数组 → '
                                            f'`ans = {B.ans} + {S.cnt[S.s]} = {S.ans}`'),
        'return ans': '遍历结束，和可被 `{k}` 整除的子数组一共 =={ans}== 个',
    },
    cards=dict(
        one_liner='前缀和模 k 同余的两个位置之间，子数组和一定是 k 的倍数',
        complexity='时间 `O(n + k)`，空间 `O(k)`',
        problem=['给整数数组 `nums` 和整数 `k`，统计元素和==能被 k 整除==的非空子数组个数',
                 '示例：`nums = [4,5,0,-2,-3,1], k = 5` → `7`',
                 f'本视频：`{NUMS}, k = {K}` → `4`'],
        quote='题目要求 (s[r] − s[l]) mod k = 0，即 s[r] 与 s[l] ==关于模 k 同余==。把前缀和的每一项都模 k，就变成了 560 题（相当于 560 题的 k=0）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组 `[l, r)` 的和是 `s[r] − s[l]`；它被 k 整除 ⇔ 两个前缀和==模 k 余数相同==',
              '枚举右端点 `r`，只要数一数前面有几个前缀和的余数等于 `s[r] % k`，就是以 `r` 结尾的答案',
              '有负数：`k = 4` 时 `-1` 和 `3` 同余，必须归到同一格，否则漏算'],
        result='返回 `4`：`[-4]`、`[2,-2]`、`[-4,2,-2]` 和整个数组，和分别是 −4、0、−4、0',
        summary=['时间 `O(n + k)`，空间 `O(k)`：建数组要 `O(k)`，遍历 `O(n)`',
                 '==先 `cnt[s] += 1` 再更新 `s`==：空前缀 `s[0] = 0` 自动入库，不用写 `cnt[0] = 1`',
                 '负数前缀和要取成非负余数：Python 的 `%` 自带，换成 C++/Java 要写 `(s % k + k) % k`',
                 '写法一用 `defaultdict` 哈希表，思路相同、空间 `O(min(n, k))`；本视频选数组写法',
                 '前置题：560 和为 K 的子数组（本题是同余版）'],
    ),
)
