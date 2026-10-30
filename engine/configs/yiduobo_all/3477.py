def _node(n, p):
    """线段树结点 p 对应的区间 [l, r]（n 个叶子，结点 p 的孩子是 2p+1、2p+2）"""
    path = []
    while p > 0:
        path.append((p - 1) % 2)
        p = (p - 1) // 2
    l, r = 0, n - 1
    for side in reversed(path):
        mid = (l + r) // 2
        l, r = (l, mid) if side == 0 else (mid + 1, r)
    return l, r


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ma = S.get('ma')
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), '线段树：每个结点 = 区间最大剩余容量 ma[p]（黄 = 当前结点）', 24, T['muted'], bold=True)
    if ma is None or n is None:
        return
    depth = 3 if n > 2 else 2
    W = x1 - x0 - 40
    nw, nh = 150, 70
    gap = (y1 - y0 - 90 - nh - 20) / max(1, depth - 1)
    ys = [y0 + 60 + nh / 2 + d * gap for d in range(depth)]
    pos = {}
    for d in range(depth):
        cnt = 2 ** d
        for k in range(cnt):
            p = (2 ** d - 1) + k
            if p < 2 * n - 1 + 2:
                pos[p] = (x0 + 20 + W * (k + 0.5) / cnt, ys[d])
    cur = S['_inner'].get('p') if isinstance(S.get('_inner'), dict) else None
    for p, (X, Y) in pos.items():
        for c in (2 * p + 1, 2 * p + 2):
            l, r = _node(n, p)
            if c in pos and l != r:
                cv.line([(X, Y + nh / 2), (pos[c][0], pos[c][1] - nh / 2)], T['border'], 2)
    for p, (X, Y) in pos.items():
        l, r = _node(n, p)
        if r < l or (p > 0 and _node(n, (p - 1) // 2)[0] == _node(n, (p - 1) // 2)[1]):
            continue
        hot = (p == cur)
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=T['yellow'] if hot else (36, 42, 52), r=10)
        cv.text((X, Y - 14), ma[p], 30, T['bg'] if hot else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 18), f'[{l},{r}]' if l != r else f'basket {l}', 20, T['bg'] if hot else T['muted'], anchor='mm', mono=True)


CONFIG = dict(
    num=3477, title='水果成篮 II', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='线段树 · 区间最大值上二分',
    code='''
class Solution(object):
    def numOfUnplacedFruits(self, fruits, baskets):
        
        n = len(baskets)
        ma = [0] * (n * 4)

        def update(p, left, right, index, v):
            if left == right:
                ma[p] = v
                return

            mid = (left + right) // 2
            if index <= mid:
                update(p * 2 + 1, left, mid, index, v)
            else:
                update(p * 2 + 2, mid + 1, right, index, v)
            ma[p] = max(ma[p * 2 + 1], ma[p * 2 + 2])

        def find(p, left, right, v):
            if left == right:
                return left
            mid = (left + right) // 2
            if ma[p * 2 + 1] >= v:
                return find(p * 2 + 1, left, mid, v)
            else:
                return find(p * 2 + 2, mid + 1, right, v)

        for index, b in enumerate(baskets):
            update(0, 0, n - 1, index, b)
        
        res = 0
        for index, f in enumerate(fruits):
            if ma[0] < f:
                res += 1
            else:
                p = find(0, 0, n - 1, f)
                update(0, 0, n - 1, p, 0)
        
        return res
''',
    call='Solution().numOfUnplacedFruits([4, 2, 5], [3, 5, 4])',
    expect=1,
    views=[
        dict(type='array', var='fruits', label='fruits（从左到右依次放）', h=130, cell=80,
             color=lambda S, i, v: 'blue' if 'f' in S and v == S['f'] else None),
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', label='递归调用栈', h=150),
    ],
    watch=['f', 'v', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len(baskets)': '`n = {n}` 个篮子，线段树的叶子就是这些篮子',
        'ma = [0] * (n * 4)': '`ma[p]` 存线段树结点 `p` 所管区间的==最大剩余容量==，开 `4n` 个位置',
        'ma[p] = v': '到了叶子 `[{left}]`：把这个篮子的容量设为 `{v}`',
        'mid = (left + right)': '区间 `[{left}, {right}]` 的中点 `mid = {mid}`',
        'if index <= mid': lambda S, B, r: (f'要改的下标 `{S.index}` ≤ `mid = {S.mid}` → 去左半区间' if S.index <= S.mid
                                            else f'要改的下标 `{S.index}` > `mid = {S.mid}` → 去右半区间'),
        'update(p * 2 + 1': '进入左孩子 `[{left}, {mid}]`',
        'update(p * 2 + 2': '进入右孩子 `[{mid + 1}, {right}]`',
        'ma[p] = max(': '回溯：`ma[{p}] = max(左孩子, 右孩子)` = =={ma[p]}==，父结点跟着更新',
        'for index, b in enumerate(baskets)': '第一步建树：取篮子 `{index}`，容量 `{b}`',
        'update(0, 0, n - 1, index, b)': '调用 `update` 把容量 `{b}` 写到下标 `{index}`，从根 `[0, {n - 1}]` 往下找叶子',
        'for index, f in enumerate(fruits)': '第二步：按顺序放水果，当前水果 `fruits[{index}] = {f}`',
        'if ma[0] < f': lambda S, B, r: (f'整棵树最大容量 `ma[0] = {S.ma[0]}` < `{S.f}` → 没有任何篮子装得下，水果未放置'
                                         if S.ma[0] < S.f else f'整棵树最大容量 `ma[0] = {S.ma[0]}` ≥ `{S.f}` → ==至少有一个篮子能装==，去找最左的'),
        'res += 1': '放不下，未放置数 `res` → {res}',
        'if left == right': lambda S, B, r: (f'`left == right = {S.left}`：到叶子了' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 还没缩到一个篮子，继续'),
        'return': '返回上一层',
        'return left': '找到了最左的可用篮子，下标 `{left}`',
        'if ma[p * 2 + 1] >= v': lambda S, B, r: (f'左孩子最大值 `{S.ma[S.p * 2 + 1]}` ≥ `{S.v}` → ==左边就有可用的==，只走左边'
                                                  if S.ma[S.p * 2 + 1] >= S.v else f'左孩子最大值 `{S.ma[S.p * 2 + 1]}` < `{S.v}` → 左边没有，答案一定在右边'),
        'return find(p * 2 + 1': '往左半区间继续二分',
        'return find(p * 2 + 2': '往右半区间继续二分',
        'p = find(0, 0, n - 1, f)': '调用 `find`：从根开始二分，找最左的、容量 ≥ `{f}` 的篮子',
        'update(0, 0, n - 1, p, 0)': '水果 `{f}` 放进找到的篮子；它用掉了：容量改成 0，==这样它不会再被找到==，最大值自动重算',
        'return res': '剩下 `{res}` 种水果没放置',
    },
    skip=['mid = (left + right) // 2'],
    max_steps=80,
    cards=dict(
        one_liner='线段树维护区间最大容量，找最左的够大的篮子',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`fruits[i]` 是水果数量，`baskets[j]` 是篮子容量',
                 '水果从左到右，放进==最左边容量够的空篮子==，一个篮子只放一种',
                 '求最后有几种水果没放上。示例 `[4,2,5]`、`[3,5,4]` → `1`'],
        quote='若区间最大值ma大于等于指定值v，说明区间中至少存在一处可用的下标。现在要求找出最左侧的可用下标，那么在这里可以先递归求解左半区间中的最左侧的可用下标，若不存在，再递归求解右半区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间最大值 ≥ v，才说明里面有篮子装得下',
              '左半区间最大值够大就只走左边，否则走右边 → 一次 `O(log n)` 二分',
              '篮子用掉后把容量改成 0，不影响最大值的逻辑 → 单点修改'],
        summary=['本题 `n ≤ 100`，暴力也行；原文为 3479（`n ≤ 10^5`）准备，用线段树',
                 '时间 `O(n log n)`，空间 `O(n)`；线段树数组开 `4n`',
                 '放不下的判断：先看根 `ma[0] < f`，成立就不用往下找',
                 '易错点：用掉的篮子要 `update(..., 0)`，否则会被重复使用',
                 '原文为 Python 2 风格，该代码无需修改（`//` 本来就是整除）'],
    ),
)
