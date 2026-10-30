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

NUMS = [1, 2, 3, 1, 2, 3]
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
class Solution(object):
    def beautifulSubarrays(self, nums):

        cnt = {0 : 1}
        now = 0
        res = 0
        for v in nums:
            now ^= v
            res += cnt.get(now, 0)
            cnt[now] = cnt.get(now, 0) + 1

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_X, L_ANS, L_INC = _ln('now ^= v'), _ln('res += cnt.get'), _ln('cnt[now] = ')


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
    cv.text((x0 + 18, y0 + 4), '每个数的二进制 和 前缀异或 now[j]（同色 = 值相同，下划线 = 已记进 cnt）', 22, T['muted'], bold=True)
    ya, yb = y0 + 70, y0 + 178
    ch = 78
    cv.text((sx - 16, ya + ch / 2), 'nums', 24, T['muted'], anchor='rm', bold=True)
    cv.text((sx - 16, yb + ch / 2), 'now', 24, T['muted'], anchor='rm', bold=True)
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
        return '一位上 1 的个数全是偶数 ⇔ 异或值为 0 ⇔ 前缀异或相等'
    D = _done(S)
    if L == L_X:
        return f"`now = {_b(XS[D - 1])} ^ {_b(NUMS[D - 1])} = {_b(XS[D])}`：现在的前缀异或是 `{XS[D]}`"
    if L == L_ANS:
        hs = _hits(S)
        if hs:
            return (f"`{_b(XS[D])}` 以前出现过 `{len(hs)}` 次（前缀 {'、'.join(str(j) for j in hs)}）→ "
                    f"==新增 {len(hs)} 个==美丽子数组")
        return f"`{_b(XS[D])}` 以前没出现过 → 新增 ==0 个=="
    return '把前缀异或 `now` 记进 `cnt`，留给后面的前缀配对'


CONFIG = dict(
    num=2588, title='统计美丽子数组数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀异或 · 哈希表计数',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1697'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().beautifulSubarrays(Nums({NUMS}))',
    expect=5,
    views=[
        dict(type='text', fn=_fx, h=84, size=26),
        dict(type='custom', draw=_draw, h=340),
        dict(type='map', var='cnt', label='cnt：前缀异或值 → 出现次数', fmt=lambda a, b: f'now={a}（{a:0{BITS}b}）有 {b} 个', h=110, font=26),
    ],
    watch=['v', ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = {0 : 1}': '`cnt` 记每种前缀异或出现的次数；一开始 `{{0: 1}}`：==空前缀的异或值是 0==，算 1 次',
        'now = 0': '`now` 是当前的前缀异或',
        'res = 0': '`res` 累计美丽子数组的个数',
        'for v in nums': lambda S, B, ret: (f'往右遍历：取下一个数 `v = {S.v}`（二进制 `{_b(S.v)}`）' if _p(S) is not None
                                            else '`nums` 遍历完了'),
        'now ^= v': lambda S, B, ret: f'`now = {B.now} ^ {S.v} = {S.now}`（`{_b(S.now)}`）：把 `v` 异或进前缀',
        'res += cnt.get': lambda S, B, ret: (
            f'`cnt[{S.now}] = {S.cnt[S.now]}`：有 `{S.cnt[S.now]}` 个前缀和现在异或值相同，中间那段异或为 0 → `res = {B.res} + {S.cnt[S.now]} = {S.res}`'
            if S.now in S.cnt else f'`now = {S.now}` 还没出现过，`get` 返回 0 → `res` 不变，仍是 `{S.res}`'),
        'cnt[now] = ': '==先用 cnt 更新答案，再把 now 的次数加 1==：`cnt[{now}] = {cnt[now]}`',
        'return res': '一共有 =={res}== 个美丽子数组',
    },
    cards=dict(
        one_liner='美丽子数组 = 每一位 1 都成对 = 异或值为 0，转成前缀异或配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一次操作要选两个数，把它们==同一位上的 1 一起减掉==；能把整个子数组变成全 0，就是美丽子数组',
                 '统计 `nums` 中美丽子数组的个数',
                 '示例：`[4,3,1,2,4]` → `2`；本视频：`[1,2,3,1,2,3]` → `5`'],
        quote='对于一个美丽子数组而言，其包含的所有数的二进制表示中，每一位出现的次数必然都是偶数。更进一步的，子数组中的数的异或值也同样为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['减去 `2^k` 要两个数的第 `k` 位都是 1，所以每一位的 1 都是==成对==消掉的',
              '每一位的 1 都是偶数个 ⇒ 所有数的异或值为 0；于是问题变成找异或为 0 的子数组',
              '前缀异或 `now`：`nums[:l]` 与 `nums[:r+1]` 的异或相同 ⇒ 中间一段异或为 0'],
        result='返回 `5`：`[1,2,3]` 出现两次、`[2,3,1]`、`[3,1,2]` 以及整个数组',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`cnt = {0: 1}` 不能漏：空前缀的异或值为 0，从头开始的子数组才能配上对',
                 '==先 `res += cnt.get(now, 0)`，后 `cnt[now] += 1`==，顺序反了会和自己配对',
                 '这里用 `cnt.get(now, 0)` 避免 KeyError；也可以换成 `defaultdict`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
