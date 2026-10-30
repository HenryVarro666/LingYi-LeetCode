_CODE = '''
class Solution(object):
    def longestBalanced(self, nums):
        
        n = len(nums)
        ma = [0] * ((n + 1) * 4)
        mi = [0] * ((n + 1) * 4)
        f = [0] * ((n + 1) * 4)
        pre = {}
        res = 0

        def update(now, left, right, start, end, delta):
            if left == start and right == end:
                f[now] += delta
                return
            
            mid = (left + right) // 2
            if end <= mid:
                update(now + now + 1, left, mid, start, end, delta)
            elif start > mid:
                update(now + now + 2, mid + 1, right, start, end, delta)
            else:
                update(now + now + 1, left, mid, start, mid, delta)
                update(now + now + 2, mid + 1, right, mid + 1, end, delta)

            ma[now] = max(ma[now + now + 1] + f[now + now + 1], ma[now + now + 2] + f[now + now + 2])
            mi[now] = min(mi[now + now + 1] + f[now + now + 1], mi[now + now + 2] + f[now + now + 2])
        
        def get(now, left, right, v):
            if left == right:
                if mi[now] <= v <= ma[now]:
                    return left
                return None
            
            mid = (left + right) // 2
            if mi[now + now + 1] <= v - f[now + now + 1] <= ma[now + now + 1]:
                return get(now + now + 1, left, mid, v - f[now + now + 1])
            else:
                return get(now + now + 2, mid + 1, right, v - f[now + now + 2])

        s = 0
        for index, v in enumerate(nums):
            if v % 2 == 0:
                delta = 1
            else:
                delta = -1

            if v not in pre:
                update(0, 0, n, index + 1, n, delta)
                s += delta
            else:
                update(0, 0, n, pre[v], index, -delta)

            pre[v] = index + 1
            p = get(0, 0, n, s)
            if p is not None:
                res = max(res, index + 1 - p)
        
        return res
'''
_LN = _CODE.strip('\n').split('\n')
_s = next(i for i, l in enumerate(_LN, 1) if 'def update' in l)
_e = next(i for i, l in enumerate(_LN, 1) if l.strip() == 's = 0')
_keep = {'f[now] += delta', 'if mi[now] <= v <= ma[now]:', 'return left'}
_SKIP = [i for i in range(_s, _e) if _LN[i - 1].strip() and _LN[i - 1].strip() not in _keep]


def _sums(S):
    f, n = S.get('f'), S.get('n')
    if f is None or not n:
        return []
    out = [0] * (n + 1)

    def go(p, l, r, add):
        if l == r:
            out[l] = f[p] + add
            return
        m = (l + r) // 2
        go(p + p + 1, l, m, add + f[p])
        go(p + p + 2, m + 1, r, add + f[p])
    try:
        go(0, 0, n, 0)
    except Exception:
        pass
    return out


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, ma, mi, n = S.get('f'), S.get('ma'), S.get('mi'), S.get('n')
    cv.text((x0 + 18, y0 + 4), '线段树：min,max / f（整段加的量，不下传）；黄框 = 本步改动', 22, T['muted'], bold=True)
    if f is None or ma is None or mi is None or not n or 'pre' not in S:
        return
    Bf, Bma, Bmi = B.get('f'), B.get('ma'), B.get('mi')
    pos = {}
    depth = n.bit_length()
    gap = min(90, (y1 - y0 - 100) / max(1, depth))

    def lay(p, l, r, d, lo, hi):
        pos[p] = ((lo + hi) / 2, y0 + 64 + d * gap, l, r, hi - lo)
        if l == r:
            return
        m = (l + r) // 2
        c = (lo + hi) / 2
        lay(p + p + 1, l, m, d + 1, lo, c)
        lay(p + p + 2, m + 1, r, d + 1, c, hi)

    lay(0, 0, n, 0, x0 + 6, x1 - 6)
    for p, (cx, cy, l, r, ww) in pos.items():
        for c in (p + p + 1, p + p + 2):
            if c in pos:
                cv.line([(cx, cy + 24), (pos[c][0], pos[c][1] - 24)], T['border'], 2)
    for p, (cx, cy, l, r, ww) in pos.items():
        ch = Bf is not None and p < len(Bf) and (Bf[p], Bma[p], Bmi[p]) != (f[p], ma[p], mi[p])
        w = min(120, ww * 0.92)
        cv.rect((cx - w / 2, cy - 24, cx + w / 2, cy + 24), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=6)
        cv.text((cx, cy - 22), f'[{l},{r}]', 14, T['dim'], anchor='mt', mono=True)
        cv.text((cx, cy - 4), f'{mi[p]},{ma[p]}/{f[p]}', 18, T['text'], anchor='mt', bold=True, mono=True)


def _star(S, k, v):
    index, pre = S.get('index'), S.get('pre')
    if index is None or pre is None:
        return False
    if k > index:
        return True
    return k != index and pre.get(v) != k + 1


def _txt(S):
    if 's' not in S:
        return '奇数 −1、偶数 +1；重复的数只留最近一次，其余当作 0'
    return f"当前前缀的 `s` = ==`{S['s']}`==；找最小的下标 `p`，使 `sum[p] == s`，区间 `(p, index+1]` 就平衡"


CONFIG = dict(
    num=3721, title='最长平衡子数组 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 区间修正 + 线段树（最值判定首个位置）',
    tags=['灵神题单', '常用数据结构', '难度分 2724'],
    code=_CODE,
    call='Solution().longestBalanced([1, 2, 3, 2])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='nums', label='nums（灰 = 不是最近一次出现，视作 0）', h=170, cell=80,
             window=(lambda S: 0 if 'index' in S else None, lambda S: S['index'] if 'index' in S else None),
             dim=lambda S, k, v: _star(S, k, v)),
        dict(type='array', var=_sums, label='sum（前缀和，线段树维护）', h=170, cell=80,
             color=lambda S, k, v: ('pink' if S.get('p') is not None and k == S['p'] and S.get('_line', 0) >= 54 else 'green' if 's' in S and v == S['s'] else None)),
        dict(type='custom', draw=_draw_tree, h=260),
    ],
    watch=['index', 'v', ('delta', 'delta'), ('s', 's', 'cyan'), ('p', 'p', 'pink'), ('res', 'res', 'green'), ('pre', 'pre')],
    skip=_SKIP + ['n = len(nums)', 'ma = [0]', 'mi = [0]', 'f = [0]', 'pre = {}', 'res = 0', 'def update', 'def get', 's = 0', 'mid = (left + right) // 2',
          'ma[now] = max', 'delta = 1', 'delta = -1', 'if v % 2 == 0'],
    max_steps=60,
    captions={
        'for index, v in enumerate(nums)': lambda S, B, r: (f'遍历结束，`res = {S.res}`' if B.get('index') == S.index and B.get('v') == S.v else f'处理第 `{S.index + 1}` 个数 `nums[{S.index}] = {S.v}`'),
        'if v not in pre': lambda S, B, r: (f'`{S.v}` 没出现过 → 首次，它要被计入' if S.v not in S.pre else f'`{S.v}` 之前在位置 `{S.pre[S.v]}` 出现过 → 不能重复计数'),
        'update(0, 0, n, index + 1, n, delta)': '首次出现：所有包含它的前缀（下标 `[{index + 1}, {n}]`）都要加上 `{delta}`（偶 +1，奇 −1）',
        's += delta': '当前前缀的和 `s` 同步变化 → =={s}==',
        'update(0, 0, n, pre[v], index, -delta)': '再次出现：旧位置 `{pre[v]}` 变成 0、它搬到了新位置，所以 `[{pre[v]}, {index}]` 这段前缀要反向修正 `{-delta}`',
        'pre[v] = index + 1': '记下 `{v}` 最近一次出现在前缀位置 `{index + 1}`',
        'p = get(0, 0, n, s)': '在前缀和数组里找第一个等于 `s = {s}` 的位置 `p`（相邻差 ≤ 1，所以区间 `min ≤ s ≤ max` 就一定有）',
        'if p is not None': lambda S, B, r: ((f'找到 `p = {S.p}`，就是自己：空区间，不算' if S.p == S.index + 1 else f'找到 `p = {S.p}`：`sum[{S.p}] = sum[{S.index + 1}]`，`({S.p}, {S.index + 1}]` 里偶、奇数个数相同') if S.p is not None else '没找到，这个右端点没有平衡子数组'),
        'res = max(res, index + 1 - p)': '长度 `{index + 1} − {p}` = {index + 1 - p}，更新 `res` → =={res}==',
        'return res': '最长平衡子数组长度 =={res}==',
        'f[now] += delta': '整段命中：只在这个节点记 `f += {delta}`，不往下传（查询时再扣）',
        'mi[now] = min': '回溯：`mi` / `ma` = 两个儿子「自身值 + 它的 f」的最小 / 最大',
        'if mi[now + now + 1] <= v - f[now + now + 1] <= ma[now + now + 1]': lambda S, B, r: (
            f'`{S.v}` 去掉左子树的 `f` 后，若落在左子树 `[min, max]` 里 → 往左找（保证首个位置）；否则去右边'),
        'if mi[now] <= v <= ma[now]': '到叶子：确认 `v` 就是这个位置的值，返回下标',
    },
    cards=dict(
        one_liner='重复的数只留最近一次，转成「找最长和为 0 的子数组」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组里「不同偶数个数 = 不同奇数个数」就算平衡，求最长平衡子数组的长度',
                 '同一个数出现多次只算一种',
                 '本视频：`[1,2,3,2]` → `3`（子数组 `[2,3,2]`）'],
        quote='若v是首次出现，那么所有包含其的前缀都应该将其计算进去，反之，若其上次出现的位置为p，由于v在s中没有被计数，那么此时只能让作为被减数的一方，也就是从p开始的所有前缀和都反向计数当前元素一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数 +1、奇数 −1；当前前缀的 `s` 只让每个数首次出现时计一次',
              '被减掉的前缀和不好直接算，反过来修正已存的前缀和：首次出现给 `[index+1, n]` 加，再次出现给 `[旧位置, index]` 减',
              '前缀和相邻差 ≤ 1，只存区间最大/最小值就能判断「`s` 在不在区间里」，从而找到最左的位置'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '线段树里区间修改只打 `f` 标记、不下传：查询时一路扣掉经过节点的 `f`',
                 '`get` 优先走左子树，所以找到的是最小的 `p`，区间最长',
                 '原文是 Python 2 风格写法，在 Python 3 中可直接运行（`//` 本来就是整除），未做改动',
                 '对比灵神：灵神用 Lazy 线段树（标准下传）+ `find_first` 带范围限制 `i-1-ans`；yiduobo 用不下传的 `f` 标记，每次从全范围里找'],
    ),
)
