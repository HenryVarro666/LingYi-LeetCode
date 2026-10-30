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

NUMS = [4, 3, 1, 2, 4]
N = len(NUMS)
XS = [0]
for _x in NUMS:
    XS.append(XS[-1] ^ _x)
BITS = max(NUMS).bit_length()
RC = ['cyan', 'pink', 'yellow', 'green', 'purple', 'orange', 'blue']
_vals = []
for _v in XS:
    if _v not in _vals:
        _vals.append(_v)
COLOR = {v: RC[i % len(RC)] for i, v in enumerate(_vals)}

CODE = '''
class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        ans = s = 0
        cnt = defaultdict(int)
        cnt[0] = 1
        for x in nums:
            s ^= x
            ans += cnt[s]
            cnt[s] += 1
        return ans
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_X, L_ANS, L_INC = _ln('s ^= x'), _ln('ans += cnt[s]'), _ln('cnt[s] += 1')


def _b(v):
    return format(v, f'0{BITS}b')


def _p(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    if p is None:
        return 0
    if p >= N:
        return N
    return p + 1 if S.get('_line') in (L_X, L_ANS, L_INC) else p


def _stored(S):
    c = S.get('cnt')
    return sum(c.values()) if isinstance(c, dict) else 0


def _hits(S):
    if S.get('_line') != L_ANS or _p(S) is None:
        return []
    D = _done(S)
    return [j for j in range(D) if XS[j] == XS[D]]


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
    live = S.get('_line') in (L_X, L_ANS, L_INC)
    cv.text((x0 + 18, y0 + 4), '每个数的二进制 和 前缀异或 s[j]（同色 = 值相同，下划线 = 已存进 cnt）', 22, T['muted'], bold=True)
    ya, yb = y0 + 70, y0 + 178
    ch = 78
    cv.text((sx - 16, ya + ch / 2), 'nums', 24, T['muted'], anchor='rm', bold=True)
    cv.text((sx - 16, yb + ch / 2), 's[j]', 24, T['muted'], anchor='rm', bold=True)
    # 配对区间：nums 中第 j+1..D 列，异或和 = 0
    for j in hits:
        a, b = X(j + 1) - cw / 2 + 4, X(D) + cw / 2 - 4
        cv.rect((a, ya - 8, b, ya + ch + 8), fill=T['green'], alpha=45, r=12)
        cv.rect((a, ya - 8, b, ya + ch + 8), outline=T['green'], width=3, r=12)
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
            cv.text((xc, ya + 24), NUMS[j - 1], 28, T['pink'] if cur else T['text'], anchor='mm', bold=True)
            cv.text((xc, ya + 56), _b(NUMS[j - 1]), 24, T['pink'] if cur else T['muted'], anchor='mm', mono=True)
        have = j <= D
        newest = live and have and j == D
        c = T[COLOR[XS[j]]]
        cv.rect((xc - bw / 2, yb, xc + bw / 2, yb + ch), fill=c if have else None,
                outline=T['text'] if (j in hits or newest) else T['border'], width=4 if (j in hits or newest) else 1, r=10)
        if have:
            cv.text((xc, yb + 24), XS[j], 28, T['bg'], anchor='mm', bold=True)
            cv.text((xc, yb + 56), _b(XS[j]), 24, T['bg'], anchor='mm', mono=True)
        else:
            cv.text((xc, yb + ch / 2), '?', 30, T['dim'], anchor='mm', bold=True)
        if have and j < st:
            cv.rect((xc - bw / 2, yb + ch + 6, xc + bw / 2, yb + ch + 12), fill=c, r=3)
    for j in hits:
        _arc_dn(cv, (X(D), yb + ch + 20), (X(j), yb + ch + 20), 24 + 8 * (D - j), T['green'], 4)


def _fx(S, B):
    L = S.get('_line')
    if _p(S) is None:
        return '美丽子数组 ⇔ 每一位上 1 的个数都是偶数 ⇔ 子数组的 ==异或和 = 0=='
    D = _done(S)
    if L == L_X:
        return f"`s[{D}] = s[{D - 1}] ^ {NUMS[D - 1]} = {_b(XS[D - 1])} ^ {_b(NUMS[D - 1])} = {_b(XS[D])}`"
    if L == L_ANS:
        hs = _hits(S)
        if hs:
            j = hs[-1]
            return (f"`s[{D}] = s[{j}] = {_b(XS[D])}` → `nums[{j}..{D - 1}]` 异或和为 0：每一位 1 都成对 → "
                    f"==新增 {len(hs)} 个==")
        return f"`s[{D}] = {_b(XS[D])}` 前面没出现过 → 新增 ==0 个=="
    return '美丽子数组 ⇔ 每一位上 1 的个数都是偶数 ⇔ 子数组的 ==异或和 = 0=='


CONFIG = dict(
    num=2588, title='统计美丽子数组数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀异或 + 哈希表（相当于 560 题 k=0）',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1697'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().beautifulSubarrays(Nums({NUMS}))',
    expect=2,
    views=[
        dict(type='text', fn=_fx, h=84, size=26),
        dict(type='custom', draw=_draw, h=340),
        dict(type='map', var=lambda S: {a: b for a, b in S['cnt'].items() if b} if 'cnt' in S else None,
             label='cnt：前缀异或值 → 出现次数', fmt=lambda a, b: f's={a}（{a:0{BITS}b}）有 {b} 个', h=110, font=26),
    ],
    watch=['x', ('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = 0': '`s` 是前缀异或，`ans` 是答案，都从 0 开始；`s` 的初值 0 对应空前缀 `s[0]`',
        'cnt = defaultdict': '`cnt[v]` 记录「前缀异或等于 `v`」的前缀出现了几次，查不到时是 0',
        'cnt[0] = 1': '空前缀 `s[0] = 0` 先存进去：==否则从 nums[0] 开始的美丽子数组配不上对==',
        'for x in nums': lambda S, B, ret: (f'枚举右端点：取下一个数 `x = {S.x}`（二进制 `{_b(S.x)}`）' if _p(S) is not None
                                            else '`nums` 遍历完了，循环结束'),
        's ^= x': lambda S, B, ret: f'`s = {B.s} ^ {S.x} = {S.s}`（`{_b(S.s)}`）：异或像加法，把 `x` 并入前缀',
        'ans += cnt[s]': lambda S, B, ret: (
            f'前面有 `{S.cnt[S.s]}` 个前缀异或也是 `{S.s}` → 它们之间的子数组异或和为 0（每列 1 的个数为偶数）→ `ans = {B.ans} + {S.cnt[S.s]} = {S.ans}`'
            if S.cnt[S.s] else f'前面没有前缀异或等于 `{S.s}` → 加 0，`ans` 仍是 `{S.ans}`'),
        'cnt[s] += 1': '==查完再存==：把 `s = {s}` 记进 `cnt`，`cnt[{s}] = {cnt[s]}`，留给后面的前缀配对',
        'return ans': '美丽子数组一共 =={ans}== 个',
    },
    cards=dict(
        one_liner='美丽 ⇔ 异或和为 0；前缀异或 + 哈希表，数相同前缀的对数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一次操作：选两个数，把它们==同一个二进制位上的 1 同时减掉==。能把子数组变成全 0，就叫美丽子数组',
                 '统计 `nums` 里美丽子数组的个数',
                 f'示例：`{NUMS}` → `2`（`[3,1,2]` 和整个数组）'],
        quote='一次操作，可以把某一列中的两个 1 都变成 0。……如果每一列都有偶数个 1，我们就能把所有数都变成 0。……所以美丽子数组等价于：子数组的异或和等于 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把数写成二进制，每次能==成对==消掉同一列的两个 1 → 每列 1 的个数都得是偶数',
              '「一列有偶数个 1」就是该列异或为 0，所以==整个子数组异或和为 0==',
              '异或和加法一样可以做前缀：`s[l] == s[r]` ⇒ `nums[l..r-1]` 异或为 0，套 560 的哈希表（k = 0）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`cnt[0] = 1` 不能漏：空前缀 `s[0] = 0`，否则从开头开始的子数组算不到',
                 '==先 `ans += cnt[s]`，再 `cnt[s] += 1`==：反过来会自己和自己配对',
                 '异或的两个性质：`a ^ a = 0`，`a ^ b ^ b = a`，所以相同前缀之间的异或为 0',
                 '同类题：560 和为 K 的子数组、974 和可被 K 整除的子数组'],
    ),
)
