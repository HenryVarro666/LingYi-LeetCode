import math

NUMS = [0, 0, 2]
K = 3
SEGC = ['purple', 'green', 'blue', 'orange']
SEGN = ['① 套圈下降（经过 0）', '② 直接加到 t', '③ 直接减到 t', '④ 套圈上升（经过 k）']
COST = (41, 42, 43, 44)     # 四条 c 的行号
PHASE = range(41, 50)       # 算代价那一段（含 c 四行、更新最优 / 次优）


def _seg(i, p, index, q):
    return 0 if i < p else 1 if i < index else 2 if i < q else 3


def _ang(pos, k):
    return -math.pi / 2 + 2 * math.pi * (pos % k) / k


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    loc = S.get('_inner', {})
    k = S.get('k')
    cv.text((x0 + 18, y0 + 4), '环形公路（周长 k）：刻度 = 余数，圆点 = 一个数', 22, T['muted'], bold=True)
    if k is None:
        return
    line = S.get('_line', 0)
    in_calc = 'p' in loc and 'q' in loc
    nums = loc.get('nums') if in_calc else S.get('r')
    if not isinstance(nums, list):
        nums = []
    t = loc.get('t') if in_calc else None
    cx, cy, R = x0 + 220, y0 + 182, 104
    # 圆环和刻度
    pts = [(cx + R * math.cos(_ang(k * a / 120, k)), cy + R * math.sin(_ang(k * a / 120, k))) for a in range(121)]
    cv.line(pts, T['border'], 6)
    for r in range(k):
        a = _ang(r, k)
        cv.rect((cx + R * math.cos(a) - 5, cy + R * math.sin(a) - 5, cx + R * math.cos(a) + 5, cy + R * math.sin(a) + 5), fill=T['muted'], r=5)
        lab = f'{r}' if r else '0 = k'
        cv.text((cx + (R + 34) * math.cos(a), cy + (R + 34) * math.sin(a)), lab, 22, T['yellow'] if r == t else T['dim'],
                anchor='mm', bold=(r == t), mono=True)
    phase = in_calc and line in PHASE and t is not None
    p, index, q = loc.get('p', 0), loc.get('index', 0), loc.get('q', 0)
    # 每个人走向 t 的路线
    if phase:
        for i, v in enumerate(nums):
            sg = _seg(i, p, index, q)
            end = (t - k, t, t, t + k)[sg]
            if end == v:
                continue
            rad = R - 30 - 12 * i
            n_ = max(8, int(abs(end - v) * 30))
            path = []
            for s_ in range(n_ + 1):
                pos = v + (end - v) * s_ / n_
                a = _ang(pos, k)
                path.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
            cv.line(path, T[SEGC[sg]], 5)
            cv.arrow(path[-2], path[-1], T[SEGC[sg]], 5, 15)
    # 人
    seen = {}
    for i, v in enumerate(nums):
        m = seen.get(v, 0)
        seen[v] = m + 1
        a = _ang(v, k)
        rr = R + 0 + m * 40
        if in_calc:
            c = T[SEGC[_seg(i, p, index, q)]] if phase else T['blue']
        else:
            c = T['blue'] if i % 2 == 0 else T['pink']
        X, Y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        cv.rect((X - 17, Y - 17, X + 17, Y + 17), fill=c, r=17, outline=T['bg'], width=3)
        cv.text((X, Y), i, 20, T['bg'], anchor='mm', bold=True, mono=True)
    # 目标位置 t
    if t is not None:
        a = _ang(t, k)
        X, Y = cx + R * math.cos(a), cy + R * math.sin(a)
        cv.rect((X - 23, Y - 23, X + 23, Y + 23), outline=T['yellow'], width=5, r=23)
        cv.text((cx, cy), f't = {t}', 34, T['yellow'], anchor='mm', bold=True)
    # 图例
    lx, ly = x0 + 420, y0 + 56
    if in_calc:
        cnt = [p, index - p, q - index, len(nums) - q]
        for sgi in range(4):
            on = phase and cnt[sgi] > 0
            cv.rect((lx, ly + sgi * 56 + 6, lx + 22, ly + sgi * 56 + 28), fill=T[SEGC[sgi]] if on else (58, 64, 74), r=5)
            cv.text((lx + 36, ly + sgi * 56), SEGN[sgi], 24, T['text'] if on else T['dim'], bold=on)
            rng = ['[0, p)', '[p, index)', '[index, q)', '[q, n)'][sgi]
            cv.text((lx + 36, ly + sgi * 56 + 27), f'{rng}：{cnt[sgi]} 个' if phase else rng, 19, T['muted'] if on else T['dim'])
        cv.text((lx, ly + 4 * 56 + 6), '三个指针 p ≤ index ≤ q，t 增大时只会往右走', 19, T['dim'])
    else:
        cv.text((lx, ly), '蓝 = 偶数下标，粉 = 奇数下标', 22, T['muted'])
        cv.text((lx, ly + 36), '点里的数字 = 原下标', 19, T['dim'])


def _seg_cells(S, i, v):
    loc = S.get('_inner', {})
    if 'p' in loc and 'q' in loc and S.get('_line', 0) in PHASE:
        return SEGC[_seg(i, loc['p'], loc['index'], loc['q'])]
    return None


def _n(v):
    return '空' if v is None else v


def _formula(S):
    loc = S.get('_inner', {})
    line = S.get('_line', 0)
    if 'p' not in loc or 't' not in loc:
        return '`r` 是余数；偶数、奇数下标互相独立：各自在环上找最优、次优的目标位置'
    k, t, p, index, q, n = S['k'], loc['t'], loc['p'], loc['index'], loc['q'], len(loc['nums'])
    s = loc['s']
    if line == 41:
        return f'① 前 {p} 个：先减到 0 共 `s[{p}]` = {s[p]}，再从 `k` 绕下来到 `t`，每个 `k − t` = {k - t}：{s[p]} + {k - t}×{p} = =={loc["c"]}=='
    if line == 42:
        return f'② `[{p},{index})` 加到 t：`t×{index - p} − ({s[index]} − {s[p]})` = {t * (index - p) - (s[index] - s[p])}　累计 `c` = =={loc["c"]}=='
    if line == 43:
        return f'③ `[{index},{q})` 减到 t：`({s[q]} − {s[index]}) − t×{q - index}` = {s[q] - s[index] - t * (q - index)}　累计 `c` = =={loc["c"]}=='
    if line == 44:
        return f'④ 后 {n - q} 个：先加到 `k`，再从 0 上到 `t`：`{n - q}×(k+t) − ({s[-1]} − {s[q]})` = {(n - q) * (k + t) - (s[-1] - s[q])}　`c` = =={loc["c"]}=='
    if 'c' in loc and line >= 46:
        return (f'`t = {t}` 的总代价 `c = {loc["c"]}`；目前最优 `c1 = {_n(loc.get("c1"))}`（t1 = {_n(loc.get("t1"))}），'
                f'次优 `c2 = {_n(loc.get("c2"))}`（t2 = {_n(loc.get("t2"))}）')
    return f'目标 `t = {t}`：指针 `p = {p}`、`index = {index}`、`q = {q}`，把 {n} 个数分成四段'


def _is_even(S):
    return 'et1' not in S


def _long(S):
    return _is_even(S)


CONFIG = dict(
    num=3937, title='使数组变为模交替数组的最少操作次数 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='环形公路 · 枚举目标位置，三个指针分四段算代价',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):

        r = [v % k for v in nums]
        odd = []
        even = []
        for index, v in enumerate(r):
            if index % 2 == 0:
                even.append(v)
            else:
                odd.append(v)

        even.sort()
        odd.sort()

        def calc(nums):
            if not nums:
                return None, 0, None, None

            s = [0]
            for v in nums:
                s.append(s[-1] + v)

            n = len(nums)
            index = 0
            p = 0
            q = 0
            c1, t1, c2, t2 = None, None, None, None
            for t in range(k):
                while index < n and nums[index] <= t:
                    index += 1

                while p < index and t - nums[p] > nums[p] + k - t:
                    p += 1

                if q < index:
                    q = index
                while q < n and nums[q] - t < k - nums[q] + t:
                    q += 1

                c = s[p] + (k - t) * p
                c += t * (index - p) - (s[index] - s[p])
                c += s[q] - s[index] - t * (q - index)
                c += (n - q) * (k + t) - (s[-1] - s[q])

                if c1 is None or c < c1:
                    t1, c1, t2, c2 = t, c, t1, c1
                elif c2 is None or c < c2:
                    t2, c2 = t, c

            return t1, c1, t2, c2

        et1, ec1, et2, ec2 = calc(even)
        ot1, oc1, ot2, oc2 = calc(odd)

        if et1 != ot1:
            return ec1 + oc1

        return min(ec1 + oc2, ec2 + oc1)
''',
    call=f'Solution().minOperations({NUMS}, {K})',
    expect=1,
    skip=['odd = []', 'even = []', 'for index, v in enumerate(r)', 'if index % 2 == 0', 'even.sort()', 'odd.sort()',
          'if not nums', 's = [0]', 'for v in nums', 's.append(s[-1] + v)', 'n = len(nums)', 'index = 0', 'p = 0', 'q = 0',
          'while index < n', 'while p < index', 'if q < index', 'while q < n'],
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var=lambda S: S['_inner'].get('nums') if 'p' in S['_inner'] else None,
             label='排好序的余数（calc 里：这一组下标的数）；指针 p ≤ index ≤ q', h=270, cell=90,
             pointers={'p': 'purple', 'index': 'green', 'q': 'orange'}, color=_seg_cells, min_slots=3),
        dict(type='text', fn=_formula, size=23, h=84),
    ],
    watch=[('t', lambda S: S['_inner'].get('t'), 'yellow'), ('c', lambda S: S['_inner'].get('c'), 'cyan'),
           ('c1', lambda S: S['_inner'].get('c1') if 't' in S['_inner'] else None, 'green'),
           ('t1', lambda S: S['_inner'].get('t1') if 't' in S['_inner'] else None, 'green'),
           ('c2', lambda S: S['_inner'].get('c2') if 't' in S['_inner'] else None, 'orange'),
           ('t2', lambda S: S['_inner'].get('t2') if 't' in S['_inner'] else None, 'orange')],
    captions={
        'r = [v % k for v in nums]': '先对 `k` 取模：只关心余数。把余数想成一条==环形公路==（周长 `k`）上的点',
        'even.append(v)': lambda S, B, r: '下标 `{}` 是偶数 → 余数 `{}` 放进 `even`'.format(S.index, S.v),
        'odd.append(v)': lambda S, B, r: '下标 `{}` 是奇数 → 余数 `{}` 放进 `odd`'.format(S.index, S.v),
        'calc(even)': '偶数下标先算：排好序的 `even` 就是 `calc` 里的 `nums`',
        'calc(odd)': lambda S, B, r: '偶数下标算完了：最优位置 `{}`，次优位置 `{}`；奇数下标同理'.format(S.et1, S.et2) if 'et1' in S
                                  else '奇数下标同理',
        'c1, t1, c2, t2 = None': '`c1, t1`：最优代价和位置；`c2, t2`：次优。先空着',
        'for t in range(k)': lambda S, B, r: ('`t` 枚举完了，返回最优和次优' if ('t' in B['_inner'] and S['_inner'].get('t') == B['_inner']['t'])
                                              else ('枚举目标位置 `t = {}`：直接把 0 到 `k − 1` 都试一遍'.format(S['_inner']['t']) if _long(S) and S['_inner']['t'] == 0
                                                    else '`t = {}`'.format(S['_inner']['t']))),
        'index += 1': lambda S, B, r: ('`nums[{}] = {}` ≤ `t = {}` → 它在 t 的左边（含 t），`index` 右移 → {}'.format(
            S['_inner']['index'] - 1, S['_inner']['nums'][S['_inner']['index'] - 1], S['_inner']['t'], S['_inner']['index'])),
        'p += 1': lambda S, B, r: ('`nums[{}] = {}`：减到 0 再绕下来（`{} + {}`）比直接加到 t（`{}`）近 → `p` 右移 → {}'.format(
            S['_inner']['p'] - 1, S['_inner']['nums'][S['_inner']['p'] - 1], S['_inner']['nums'][S['_inner']['p'] - 1], S.k - S['_inner']['t'],
            S['_inner']['t'] - S['_inner']['nums'][S['_inner']['p'] - 1], S['_inner']['p'])),
        'q = index': lambda S, B, r: '`q` 不能落在 `index` 左边：`q = index` = {}'.format(S['_inner']['q']),
        'q += 1': lambda S, B, r: ('`nums[{}] = {}`：直接减到 t（`{}`）比加到 k 再绕上来（`{}`）近 → `q` 右移 → {}'.format(
            S['_inner']['q'] - 1, S['_inner']['nums'][S['_inner']['q'] - 1], S['_inner']['nums'][S['_inner']['q'] - 1] - S['_inner']['t'],
            S.k - S['_inner']['nums'][S['_inner']['q'] - 1] + S['_inner']['t'], S['_inner']['q'])),
        41: lambda S, B, r: ('分四段算代价。① `[0, p)`：先减到 0，再套圈从 `k` 下降到 `t`'
                             if _long(S) and S['_inner']['t'] == 0 else '第一段 `[0, p)`：`p` = {}'.format(S['_inner']['p'])),
        42: lambda S, B, r: ('② `[p, index)`：在 t 左边，直接加到 `t`' if _long(S) and S['_inner']['t'] == 0
                             else '第二段 `[p, index)` = {} 个'.format(S['_inner']['index'] - S['_inner']['p'])),
        43: lambda S, B, r: ('③ `[index, q)`：在 t 右边，直接减到 `t`' if _long(S) and S['_inner']['t'] == 0
                             else '第三段 `[index, q)` = {} 个'.format(S['_inner']['q'] - S['_inner']['index'])),
        44: lambda S, B, r: ('④ `[q, n)`：先加到 `k`（≡ 0），再套圈上升到 `t`' if _long(S) and S['_inner']['t'] == 0
                             else '第四段 `[q, n)` = {} 个：`c` = =={}=='.format(len(S['_inner']['nums']) - S['_inner']['q'], S['_inner']['c'])),
        'if c1 is None or c < c1': lambda S, B, r: ('`c = {}`，`c1` 还是空 → 它就是目前最优'.format(S['_inner']['c']) if B['_inner'].get('c1') is None
                                                    else ('`c = {} < c1 = {}` → 刷新最优'.format(S['_inner']['c'], B['_inner']['c1']) if S['_inner']['c'] < B['_inner']['c1']
                                                          else '`c = {}` 不比 `c1 = {}` 小 → 看看能不能当次优'.format(S['_inner']['c'], B['_inner']['c1']))),
        't1, c1, t2, c2 = t, c, t1, c1': lambda S, B, r: ('最优换成 `t = {}`；原来的最优 `{}` 降为次优'.format(S['_inner']['t1'], S['_inner']['t2'])
                                                          if S['_inner']['t2'] is not None else '最优 = `t = {}`；还没有旧的最优，次优仍空'.format(S['_inner']['t1'])),
        'elif c2 is None or c < c2': lambda S, B, r: ('`c = {}`，`c2` 还是空 → 先当次优'.format(S['_inner']['c']) if B['_inner'].get('c2') is None
                                                      else ('`c = {} < c2 = {}` → 刷新次优'.format(S['_inner']['c'], B['_inner']['c2']) if S['_inner']['c'] < B['_inner']['c2']
                                                            else '`c = {}` 也不比 `c2 = {}` 小 → 不更新'.format(S['_inner']['c'], B['_inner']['c2']))),
        't2, c2 = t, c': '次优换成 `t = {t}`：`c2 = {c2}`',
        'return t1, c1, t2, c2': lambda S, B, r: '最优位置 `{}`（代价 `{}`），次优位置 `{}`（代价 `{}`）'.format(r[0], r[1], r[2], r[3]),
        'if et1 != ot1': lambda S, B, r: ('最优位置相同（都是 `{}`），但要求 `x ≠ y`，必须一边取次优'.format(S.et1) if S.et1 == S.ot1
                                          else '偶数、奇数的最优位置不同，各取最优'),
        'return ec1 + oc1': '最优位置不同：直接 `ec1 + oc1`',
        'return min(ec1 + oc2, ec2 + oc1)': '`min({ec1}+{oc2}, {ec2}+{oc1})` = =={ret}==：一边最优、另一边次优，取小的',
    },
    cards=dict(
        one_liner='把余数放到环形公路上，枚举目标位置，用三个指针分四段算代价',
        complexity='本题数据下暴力枚举 `t`：时间 `O(n log n + k)`，空间 `O(n)`',
        problem=['每步把任意数 `±1`；偶数下标的数模 `k` 都等于 `x`，奇数下标的都等于 `y`，且 `x ≠ y`',
                 '求最少操作次数',
                 '示例：`nums=[1,4,2,8]`，`k=3` → `2`',
                 f'本视频：`nums={NUMS}`，`k={K}` → `1`（偶数、奇数最优位置撞车的情形）'],
        quote='接下来的问题就可以认为是对于一条环形公路，上面有若干点，找出最优与次优的两个位置，使得所有点到这两个位置的距离之和最小/次小。',
        quote_src='—— yiduobo 题解原文',
        idea=['先对 `k` 取模，按奇偶下标分成 `even`、`odd` 两组并排序',
              '枚举目标位置 `t`（0 到 `k−1`）：点分四段——套圈下降、直接加、直接减、套圈上升',
              '`p`、`index`、`q` 是四段的分界，随 `t` 增大==只会右移==，均摊 `O(1)`；段内用前缀和求代价',
              '记最优和次优；偶奇最优位置相同就一边取次优'],
        summary=['枚举 `t` 共 `k` 次，每次指针均摊 `O(1)`；排序 `O(n log n)`',
                 '易错：次优位置不一定在已有的点上，所以要枚举 `0 ~ k−1`',
                 '易错：`x ≠ y`——最优位置相同时才取次优',
                 '原文是 Python 3 也能直接运行的写法，代码未改动',
                 '对比灵神：灵神断环 + 二分 + 前缀和，只试 `a[i]` 与 `best_x ± 1`'],
    ),
)
