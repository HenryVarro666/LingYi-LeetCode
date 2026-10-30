ARR = 'f'
ROOT = 0
CH = lambda p: (p + p + 1, p + p + 2)


def _nodes(u, root, ch):
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            a, b = ch(o)
            go(a, l, m, d + 1)
            go(b, m + 1, r, d + 1)
    go(root, 1, u, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    arr = S.get(ARR)
    if arr is None:
        return
    u = max(S['nums'])
    nodes = _nodes(u, ROOT, CH)
    maxd = max(d for _, _, _, d in nodes) + 1
    W = x1 - x0 - 40
    slot = W / u
    dy = min(110, (y1 - y0 - 70) / maxd)
    bh = min(66, dy - 22)
    bw = min(150, slot * 2 - 14) if u > 1 else 140
    bw = max(70, min(bw, 150))
    inner = S.get('_inner') or {}
    kind = None
    qlo = qhi = tgt = None
    cur = None
    if 'p' in inner or 'o' in inner:
        cur = inner.get('p') if 'p' in inner else inner.get('o')
    if ('now' in inner and 'p' in inner) or 'val' in inner:
        kind = 'upd'
        tgt = inner.get('num') if 'num' in inner else inner.get('i')
    elif 'L' in inner or ('left' in inner and 'l' in inner):
        kind = 'qry'
        qlo = inner.get('L') if 'L' in inner else inner.get('left')
        qhi = inner.get('R') if 'R' in inner else inner.get('right')
    cx = {}
    for o, l, r, d in nodes:
        cx[o] = x0 + 20 + ((l - 1) + (r - l + 1) / 2) * slot
    cv.text((x0 + 18, y0 + 4), f'线段树：叶子 = 数值 1..{u}，节点值 = 区间最大 f（黄 = 当前）', 22, T['muted'], bold=True)
    pos = {}
    for o, l, r, d in nodes:
        pos[o] = (cx[o], y0 + 52 + d * dy)
    for o, l, r, d in nodes:
        if l < r:
            for c in CH(o):
                cv.line([(pos[o][0], pos[o][1] + bh), (pos[c][0], pos[c][1])], T['border'], 2)
    for o, l, r, d in nodes:
        X, Y = pos[o]
        fill = (50, 56, 68)
        outline = None
        if kind == 'qry' and qlo is not None and qlo <= l and r <= qhi:
            outline = T['blue']
        if kind == 'upd' and tgt is not None and l <= tgt <= r:
            outline = T['pink']
        if o == cur:
            fill = T['yellow']
        cv.rect((X - bw / 2, Y, X + bw / 2, Y + bh), fill=fill, r=8)
        if outline:
            cv.rect((X - bw / 2, Y, X + bw / 2, Y + bh), outline=outline, width=4, r=8)
        tc = T['bg'] if o == cur else T['text']
        v = arr[o]
        cv.text((X, Y + bh * 0.28), f'[{l},{r}]' if l < r else f'数值 {l}', 18, T['bg'] if o == cur else T['muted'], anchor='mm', bold=True)
        cv.text((X, Y + bh * 0.68), v, 30, tc, anchor='mm', bold=True)
    if kind == 'qry':
        cv.text((x0 + 20, y1 - 30), f'蓝框 = 完全落在 [{qlo},{qhi}] 内的节点', 20, T['blue'], bold=True)
    elif kind == 'upd':
        cv.text((x0 + 20, y1 - 30), f'粉框 = 含数值 {tgt} 的节点（从下往上更新）', 20, T['pink'], bold=True)


def _info(S):
    if 'num' not in S or S.get('k') is None:
        return '`f[v]`：以数值 `v` 结尾的最长上升子序列；线段树维护它的区间最大值'
    x, k = S['num'], S['k']
    if x == 1:
        return '`num = 1`：前面没有更小的数 → `now = 1`'
    return f'`num = {x}`：`f[{x}] = max(f[{max(1, x - k)}..{x - 1}]) + 1`（差 ≤ {k}）'


CONFIG = dict(
    num=2407, title='最长递增子序列 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='f[数值] + 线段树（区间最大值）',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2280'],
    code='''
class Solution(object):
    def lengthOfLIS(self, nums, k):

        max_n = max(nums)
        f = [0] * (max_n * 4)

        def find(f, p, l, r, left, right):
            if l == left and r == right:
                return f[p]
            else:
                mid = (l + r) >> 1
                if right <= mid:
                    return find(f, p + p + 1, l, mid, left, right)
                elif left > mid:
                    return find(f, p + p + 2, mid + 1, r, left, right)
                else:
                    return max(find(f, p + p + 1, l, mid, left, mid), find(f, p + p + 2, mid + 1, r, mid + 1, right))
        
        def insert(f, p, l, r, num, now):
            f[p] = max(f[p], now)
            if l < r:
                mid = (l + r) >> 1
                if num <= mid:
                    insert(f, p + p + 1, l, mid, num, now)
                else:
                    insert(f, p + p + 2, mid + 1, r, num, now)

        res = 0
        for num in nums:
            if num == 1:
                now = 1
            else:
                left = max(1, num - k)
                right = num - 1
                now = find(f, 0, 1, max_n, left, right) + 1
            
            res = max(res, now)
            insert(f, 0, 1, max_n, num, now)

        return res
''',
    call='Solution().lengthOfLIS([3,1,2,4], 2)',
    expect=3,
    skip=['mid = (l + r) >> 1', 'def find', 'def insert', 'if l < r', 'else:', 'return find(f, p + p', 'insert(f, p + p', 'return f[p]', 'elif left > mid', 'res = 0', 'right = num - 1', 'if num == 1', 'now = 1'],
    max_steps=160,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=200, hide=('f', 'nums')),
    ],
    watch=[('num', 'num', 'yellow'), ('now', 'now', 'green'), ('res', 'res', 'blue')],
    captions={
        'max_n = max(nums)': '数都不超过 `{max_n}`：把 `f` 开在==数值==上，而不是下标上',
        'f = [0] * (max_n * 4)': '`f[p]`：线段树节点 `p` 管的数值区间里，最长上升子序列的最大值',
        'res = 0': '`res` 记录答案',
        'for num in nums': lambda S, B, r: (f'处理 `num = {S.num}`：' + ('没有更小的数，只能自己成序列，`now = 1`' if S.num == 1 else '前一个数在 `[num−k, num−1]`，先查区间最大值') if S.get('num') != B.get('num') or B.get('num') is None else '`nums` 都处理完了'),
        'if num == 1': lambda S, B, r: ('`num = 1`：没有更小的数，只能自己成序列' if S.num == 1 else f'`num = {S.num} > 1`：先查区间最大值'),
                'left = max(1, num - k)': '区间左端 `max(1, num − k)` = `{left}`，右端取 `num − 1`（==严格==递增，不含自己）',
        'right = num - 1': '区间右端 `num − 1` = `{right}`：==严格==递增，不含 `num` 自己',
        'now = find': lambda S, B, r: f'查 `f[{B.left}..{B.right}]` 的最大值，`+1` 得 `now`',
        'res = max(res, now)': '`now` = {now}（区间最大值 + 1）；`res = max({B.res}, {now})` = =={res}==',
        'insert(f, 0, 1, max_n, num, now)': '把 `f[{num}]` 更新为 `{now}`：根节点 `f[0] = {f[0]}`',
        'if l == left and r == right': lambda S, B, r: (f'节点 `[{B.l},{B.r}]` ==正好等于== 查询区间 → 直接返回 `f[{B.p}] = {B.f[B.p]}`' if (B.l, B.r) == (B.left, B.right)
                                                       else f'节点 `[{B.l},{B.r}]` 与 `[{B.left},{B.right}]` 不完全一样 → 往下分'),
        'if right <= mid': lambda S, B, r: (f'`right = {B.right} <= mid = {(B.l + B.r) >> 1}`：整段在左半，只查左边' if B.right <= (B.l + B.r) >> 1
                                           else f'`left = {B.left} > mid = {(B.l + B.r) >> 1}`：整段在右半，只查右边' if B.left > (B.l + B.r) >> 1
                                           else f'`[{B.left},{B.right}]` 跨过 `mid = {(B.l + B.r) >> 1}`：左右两半都要查，再取 ==较大者=='),
        'f[p] = max(f[p], now)': '节点 `[{l},{r}]`：`f[{p}] = max(旧值, {now})` = =={f[p]}==（路径上每个节点都取最大）',
        'if num <= mid': lambda S, B, r: (f'`num = {B.num} <= mid = {(B.l + B.r) >> 1}`：往左子树走' if B.num <= (B.l + B.r) >> 1 else f'`num = {B.num} > mid = {(B.l + B.r) >> 1}`：往右子树走'),
        'return res': '最长子序列长度 =={ret}==',
    },
    cards=dict(
        one_liner='f 开在数值上，线段树负责「区间取最大」',
        complexity='时间 `O(n log U)`，空间 `O(U)`',
        problem=['最长==严格递增==子序列，相邻差 ==不超过== `k`',
                 '`n`、数值都到 `10^5`，`O(n^2)` 太慢',
                 '本视频：`[3,1,2,4], k=2` → `3`'],
        quote='注意到原数组中的每个数都不超过10^5，那么就可以换一种状态表示，令f[i]表示以数字i为结尾的最长上升子序列的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态换成「以数值 i 结尾」：`f[num] = max(f[num−k..num−1]) + 1`',
              '一趟遍历，每个数：==区间求最大 + 单点更新==，正是线段树的活',
              '`insert` 沿路径把每个节点都取 max，所以根节点始终是全局最大'],
        summary=['时间 `O(n log U)`，空间 `O(U)`',
                 '`num == 1` 单独处理：区间 `[1, 0]` 为空',
                 '这里的线段树根节点下标是 0，孩子是 `2p+1` / `2p+2`',
                 '`insert` 是「取 max」更新，不是覆盖；数值只增不减才成立',
                 '对比灵神：灵神用 `modify` 覆盖叶子再回溯合并，yiduobo 用 `insert` 一路取 max'],
    ),
)
