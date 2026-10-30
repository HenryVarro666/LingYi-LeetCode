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

ARR = [1, 2, 3, 4, 5, 6]
N = len(ARR)
RAW = [0]
for _x in ARR:
    RAW.append(RAW[-1] + _x)

CODE = '''
class Solution(object):
    def numOfSubarrays(self, arr):

        now = 0
        odd = even= 0
        res = 0
        mod = 10 ** 9 + 7
        for num in arr:
            now += num
            if now & 1:
                res += even + 1
                odd += 1
            else:
                res += odd
                even += 1
            if res >= mod:
                res -= mod
        
        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_ADD, L_ODD, L_EVEN = _ln('now += num'), _ln('res += even + 1'), _ln('res += odd')
L_OI, L_EI = _ln('odd += 1'), _ln('even += 1')


def _p(S):
    a = S.get('arr')
    p = getattr(a, 'pos', None)
    return p if p is not None and p < len(a) else None


def _done(S):
    a = S.get('arr')
    p = getattr(a, 'pos', None)
    if p is None:
        return 0
    if p >= N:
        return N
    return p if S.get('_line') == _ln('for num in arr') else p + 1


def _stored(S):
    return S.get('odd', 0) + S.get('even', 0) if 'odd' in S and 'even' in S else 0


def _hits(S):
    L = S.get('_line')
    if L not in (L_ODD, L_EVEN) or _p(S) is None:
        return []
    D = _done(S)
    want = 0 if L == L_ODD else 1  # 当前奇 → 配前面的偶；当前偶 → 配前面的奇
    return [j for j in range(1, D) if RAW[j] % 2 == want]


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
    L = S.get('_line')
    live = L in (L_ADD, L_ODD, L_EVEN, L_OI, L_EI, _ln('if now & 1'))
    plus1 = L == L_ODD and _p(S) is not None
    cv.text((x0 + 18, y0 + 4), '前缀和 now[j] 的奇偶（粉 = 奇，青 = 偶，下划线 = 已计入 odd / even）', 22, T['muted'], bold=True)
    ya, yb = y0 + 70, y0 + 170
    ch = 70
    cv.text((sx - 16, ya + ch / 2), 'arr', 24, T['muted'], anchor='rm', bold=True)
    cv.text((sx - 16, yb + ch / 2), '前缀和', 24, T['muted'], anchor='rm', bold=True)
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
            cv.text((xc, ya + ch / 2), ARR[j - 1], 30, T['pink'] if cur else T['text'], anchor='mm', bold=True)
        have = j <= D
        newest = live and have and j == D and j > 0
        odd = RAW[j] % 2 == 1
        c = T['pink'] if odd else T['cyan']
        special0 = plus1 and j == 0
        cv.rect((xc - bw / 2, yb, xc + bw / 2, yb + ch), fill=c if have else None,
                outline=T['orange'] if special0 else (T['text'] if (j in hits or newest) else T['border']),
                width=4 if (j in hits or newest or special0) else 1, r=10)
        if have:
            cv.text((xc, yb + 26), RAW[j], 30, T['bg'], anchor='mm', bold=True)
            cv.text((xc, yb + 54), '奇' if odd else ('偶（空）' if j == 0 else '偶'), 20, T['bg'], anchor='mm', bold=True)
        else:
            cv.text((xc, yb + ch / 2), '?', 30, T['dim'], anchor='mm', bold=True)
        if have and 1 <= j <= st:
            cv.rect((xc - bw / 2, yb + ch + 6, xc + bw / 2, yb + ch + 12), fill=c, r=3)
    for j in hits:
        _arc_dn(cv, (X(D), yb + ch + 20), (X(j), yb + ch + 20), 24 + 8 * (D - j), T['green'], 4)
    if plus1:
        _arc_dn(cv, (X(D), yb + ch + 20), (X(0), yb + ch + 20), 24 + 8 * D, T['orange'], 4)
        cv.text((X(0) - cw / 2 + 6, yb + ch + 66), '橙色弧线 = +1（now 自己成一段，等价于配空前缀）', 20, T['orange'], anchor='lt', bold=True)


def _fx(S, B):
    L = S.get('_line')
    if _p(S) is None:
        return '奇 − 偶 = 奇，偶 − 奇 = 奇 → 看==前缀和的奇偶==，找奇偶不同的两个前缀'
    D = _done(S)
    if L == L_ODD:
        return f"`now = {RAW[D]}` 是奇数：前面 `{S['even']}` 个偶数前缀各配一个，再加上 now 自己 → ==新增 {S['even'] + 1} 个=="
    if L == L_EVEN:
        return f"`now = {RAW[D]}` 是偶数：前面 `{S['odd']}` 个奇数前缀各配一个 → ==新增 {S['odd']} 个=="
    if L == _ln('if now & 1'):
        return f"`{RAW[D]} & 1 = {RAW[D] & 1}`：{'奇数' if RAW[D] & 1 else '偶数'}"
    return '奇 − 偶 = 奇，偶 − 奇 = 奇 → 看==前缀和的奇偶==，找奇偶不同的两个前缀'


CONFIG = dict(
    num=1524, title='和为奇数的子数组数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和奇偶 · 计数配对',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().numOfSubarrays(Nums({ARR}))',
    expect=12,
    skip=['if res >= mod', 'res -= mod'],
    views=[
        dict(type='text', fn=_fx, h=84, size=26),
        dict(type='custom', draw=_draw, h=370),
        dict(type='map', var=lambda S: {'odd': S['odd'], 'even': S['even']} if 'odd' in S and 'even' in S else None,
             label='已经出现过的前缀和（不含空前缀）', fmt=lambda k, v: (f'奇数前缀 odd = {v} 个' if k == 'odd' else f'偶数前缀 even = {v} 个'),
             h=110, font=28),
    ],
    watch=['num', ('now', 'now', 'blue'), ('odd', 'odd', 'pink'), ('even', 'even', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now`：当前的前缀和，只关心它是奇还是偶',
        'odd = even': '`odd` / `even`：之前出现过的前缀和里，奇数、偶数各有几个',
        'res = 0': '`res` 累计和为奇数的子数组个数',
        'mod = ': '答案可能很大，要对 `10^9 + 7` 取模；本例数很小，用不到',
        'for num in arr': lambda S, B, ret: (f'往右扫：取下一个数 `num = {S.num}`' if _p(S) is not None else '`arr` 扫完了'),
        'now += num': lambda S, B, ret: f'`now = {B.now} + {S.num} = {S.now}`：这是 `now[{_done(S)}]`',
        'if now & 1': lambda S, B, ret: f'`now & 1` 看最低位：`{S.now}` 是' + ('==奇数==' if S.now & 1 else '==偶数=='),
        'res += even + 1': lambda S, B, ret: (f'奇 − 偶 = 奇：前面 `{S.even}` 个偶数前缀各配一段，再 `+1`（now 自己成一段）'
                                              f'→ `res = {B.res} + {S.even} + 1 = {S.res}`'),
        'odd += 1': '把这个奇数前缀记下来：`odd = {odd}`',
        'res += odd': lambda S, B, ret: (f'偶 − 奇 = 奇：前面 `{S.odd}` 个奇数前缀各配一段；now 是偶数，自己不算'
                                         f' → `res = {B.res} + {S.odd} = {S.res}`'),
        'even += 1': '把这个偶数前缀记下来：`even = {even}`',
        'return res': '和为奇数的子数组一共 =={res}== 个',
    },
    cards=dict(
        one_liner='和为奇数 ⇔ 两个前缀和奇偶不同，数一数前面有多少个异奇偶的前缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `arr`，统计==元素和为奇数==的子数组个数；答案对 `10^9 + 7` 取余',
                 '示例：`[1,3,5]` → `4`',
                 f'本视频：`{ARR}` → `12`'],
        quote='若s[index]为奇数，那么在index之前有多少个偶数的前缀和，那么就可以形成多少个和为奇数的子数组。……若当前前缀和为奇数，那么直接将这个前缀和拎出来也是一种合法答案，因此此时还需要将答案额外加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['子数组和 = 两个前缀和之差；差为奇数 ⇔ 两个前缀和==奇偶不同==',
              '当前前缀是奇数：前面每个偶数前缀配一个；当前是偶数：前面每个奇数前缀配一个',
              '当前前缀是奇数时，==整段前缀本身==（相当于空前缀 0 是偶数）也算一个，所以多加 1'],
        result='返回 `12`',
        summary=['时间 `O(n)`，空间 `O(1)`：只用 `odd`、`even` 两个计数器，不用存前缀和数组',
                 '`now` 是奇数时 `res += even + 1`，别漏掉这个 `+1`（空前缀的偶数）',
                 '`odd`、`even` 不含空前缀；空前缀的贡献就是那个 `+1`',
                 '每步后判断 `res >= mod` 再减，避免整数过大；本例太小，没有触发',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
