NUMS = [3, 1, 4, 2]


def _fmt(v, inf):
    return '∞' if v == inf else ('-' if v < 0 else str(v))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '节点：区间 / first / second ×个数（∞ = 可当左端点，- = 未激活）', 20, T['muted'], bold=True)
    first, second, fc = S.get('first'), S.get('second'), S.get('first_cnt')
    so = S.get('sorted_nums')
    if first is None or fc is None or second is None or so is None:
        return
    n = len(so)
    inf = so[-1] + 1
    bf = B.get('first') or first
    bs = B.get('second') or second
    inner = S.get('_inner') or {}
    cur = inner.get('p') if inner.get('left') is not None else None
    layout = {}
    leaves = [0]

    def lay(p, l, r, d):
        if l == r:
            layout[p] = (leaves[0], d, l, r)
            leaves[0] += 1
            return leaves[0] - 1
        m = (l + r) // 2
        a = lay(p * 2 + 1, l, m, d + 1)
        b = lay(p * 2 + 2, m + 1, r, d + 1)
        layout[p] = ((a + b) / 2, d, l, r)
        return (a + b) / 2
    lay(0, 0, n - 1, 0)
    maxd = max(v[1] for v in layout.values()) + 1
    cw = (x1 - x0 - 40) / n
    dy = min(150, (y1 - y0 - 130) / max(1, maxd - 1 or 1))
    bw, bh = min(168, cw * 0.92), 64

    def pos(p):
        i, d, l, r = layout[p]
        return x0 + 20 + (i + 0.5) * cw, y0 + 70 + d * dy
    for p, (i, d, l, r) in layout.items():
        if l != r:
            X, Y = pos(p)
            for c in (p * 2 + 1, p * 2 + 2):
                X2, Y2 = pos(c)
                cv.line([(X, Y + bh / 2), (X2, Y2 - bh / 2)], T['border'], 3)
    for p, (i, d, l, r) in layout.items():
        X, Y = pos(p)
        changed = first[p] != bf[p] or second[p] != bs[p]
        active = first[p] >= 0
        fill = T['panel2'] if not active else (70, 62, 34) if changed else (44, 56, 78)
        outline = T['pink'] if p == cur else (T['yellow'] if changed else T['border'])
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=fill, outline=outline, width=5 if p == cur else 2, r=10)
        cv.text((X, Y - 16), f'[{l},{r}]' if l != r else f'[{l}] = {so[l]}', 17, T['dim'] if not active else T['muted'], anchor='mm', mono=True)
        cv.text((X, Y + 12), f'{_fmt(first[p], inf)} / {_fmt(second[p], inf)} ×{fc[p]}', 21,
                T['dim'] if not active else T['text'], anchor='mm', mono=True, bold=True)
    cv.text((x0 + 18, y1 - 30), f'排序后 sorted_nums = {so}（叶子从左到右）；∞ = {inf}', 20, T['muted'])


def _cur(S):
    return S.get('v') if S.get('_inner', {}).get('left') is None else None


def _b(S, B, r):
    return ''


def _case(S, B, r):
    p = S.p
    f, s, v = B.first[p], B.second[p], S.v
    if f < v:
        return f'`first = {f} < v = {v}`：区间里没有比 {v} 大的上界，无事发生，返回 0'
    return f'`first = {f} ≥ {v}`：有上界要被压'


def _case2(S, B, r):
    p = S.p
    f, s, v = S.first[p] if False else B.first[p], B.second[p], S.v
    if s < v:
        return f'`second = {s} < v = {v} ≤ first = {f}`：只有最大值 `{f}` 要变成 `{v}`，打个标记 `first = {v}`，这 `{S.first_cnt[p]}` 个位置各成一个影子对'
    return f'`second = {s} ≥ v = {v}`：次大值也要被压平，必须往下递归'


CONFIG = dict(
    num=4055, title='统计影子数对 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='吉司机线段树（区间取 min）',
    tags=['灵神题单·常用数据结构', '难度分 2631'],
    code='''
class Solution(object):
    def shadowPairs(self, nums):
        
        n = len(nums)
        sorted_nums = sorted(nums)
        order = {}
        cnt = {}
        for index, v in enumerate(sorted_nums):
            cnt[v] = cnt.get(v, 0) + 1
            order[(v, cnt[v])] = index
        
        first = [-1] * (n * 4)
        first_cnt = [0] * (n * 4)
        second = [-1] * (n * 4)

        def update_first(p):
            if first[p * 2 + 1] > first[p * 2 + 2]:
                first[p] = first[p * 2 + 1]
                first_cnt[p] = first_cnt[p * 2 + 1]
                second[p] = max(first[p * 2 + 2], second[p * 2 + 1])
            
            elif first[p * 2 + 1] < first[p * 2 + 2]:
                first[p] = first[p * 2 + 2]
                first_cnt[p] = first_cnt[p * 2 + 2]
                second[p] = max(first[p * 2 + 1], second[p * 2 + 2])
            
            else:
                first[p] = first[p * 2 + 1]
                first_cnt[p] = first_cnt[p * 2 + 1] + first_cnt[p * 2 + 2]
                second[p] = max(second[p * 2 + 1], second[p * 2 + 2])

        def ch_min(p, left, right, start, end, v):
            if left == start and right == end:
                if first[p] < v:
                    return 0
                if second[p] < v:
                    first[p] = v
                    return first_cnt[p]
            
            first[p * 2 + 1] = min(first[p * 2 + 1], first[p])
            first[p * 2 + 2] = min(first[p * 2 + 2], first[p])
            mid = (left + right) // 2
            if end <= mid:
                pair = ch_min(p * 2 + 1, left, mid, start, end, v)
            elif start > mid:
                pair = ch_min(p * 2 + 2, mid + 1, right, start, end, v)
            else:
                pair = ch_min(p * 2 + 1, left, mid, start, mid, v) + ch_min(p * 2 + 2, mid + 1, right, mid + 1, end, v)
            
            update_first(p)
            return pair

        def update_point(p, left, right, index, v):
            if left == right:
                first[p] = v
                first_cnt[p] = 1
                second[p] = -1
                return
            
            first[p * 2 + 1] = min(first[p * 2 + 1], first[p])
            first[p * 2 + 2] = min(first[p * 2 + 2], first[p])
            mid = (left + right) // 2
            if index <= mid:
                update_point(p * 2 + 1, left, mid, index, v)
            else:
                update_point(p * 2 + 2, mid + 1, right, index, v)
            
            update_first(p)

        cnt = {}
        res = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            o = order[(v, cnt[v])]
            bound = o - cnt[v]
            if bound >= 0:
                res += ch_min(0, 0, n - 1, 0, bound, v)
            
            update_point(0, 0, n - 1, o, sorted_nums[-1] + 1)

        return res
''',
    call=f'Solution().shadowPairs({NUMS})',
    expect=3,
    max_steps=46,
    skip=[54, 55, 58, 63, 64, 66, 17, 18, 19, 20, 22, 23, 24, 25, 28, 29, 30, 'first[p * 2 + 2] = min', 56, 57, 60, 61, 62, 68, 'n = len(nums)', 'order = {}', 'cnt = {}', 'cnt[v] = cnt.get', 'order[(v', 'for index, v in enumerate', 'first_cnt = [0]',
          'second = [-1]', 'mid = (left + right)', 'return pair', 'cnt = {}'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在处理的 v）', cell=76, h=170, 
             color=lambda S, i, v: 'blue' if S.get('v') == v and S['_inner'].get('left') is None else None),
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', h=130, hide=('start', 'end')),
    ],
    watch=[('v', 'v', 'blue'), ('o', 'o'), ('bound', 'bound', 'pink'), ('res', 'res', 'green')],
    captions={
        'sorted_nums = sorted': '排序：`{sorted_nums}`；线段树的叶子按“值从小到大”排，下标 `o` 就是排名',
        'first = [-1]': '`first[p]` = 区间里“上界”最大值，`-1` 表示这个位置还没遍历到，不能当左端点',
        'second = [-1]': '`second` 次大值，`first_cnt` = 最大值出现的次数',
        'for v in nums': '依次遍历 `nums`，当前 `v = {v}`：先找已经遍历过且比它小的左端点，再让 v 自己变成左端点',
        'o = order': '`v = {v}` 在排序数组中的位置 `o = {o}`（相同值按出现顺序排）',
        'bound = o - cnt[v]': '严格比 `{v}` 小的数在叶子 `[0, {bound}]` 内：`bound = o - cnt[v] = {bound}`',
        'if bound >= 0': lambda S, B, r: (f'`bound = {S.bound} ≥ 0`：有更小的数，去 `[0, {S.bound}]` 里找 upper ≥ v 的左端点' if S.bound >= 0 else '`bound < 0`：没有比它小的数，不会产生影子对'),
        'res += ch_min': '去 `[0, {bound}]` 把 upper ≥ `{B.v}` 的全压成 `{B.v}`，压掉几个，就多几个影子对',
        'update_point(0, 0': '`v = {B.v}` 自己也成为左端点：叶子 `{B.o}` 的 upper 设为 `∞`（= {sorted_nums[-1] + 1}）',
        'if left == start and right == end': lambda S, B, r: ('区间 `[{},{}]` 正好是要操作的 `[{},{}]`'.format(S.left, S.right, S.start, S.end) if (S.left == S.start and S.right == S.end) else '区间 `[{},{}]` 比要操作的 `[{},{}]` 大，需要拆开'.format(S.left, S.right, S.start, S.end)),
        'if first[p] < v': _case,
        'if second[p] < v': _case2,
        'return first_cnt[p]': '返回最大值个数 `{ret}`：这些左端点和 v 组成影子对',
        'first[p * 2 + 1] = min': '先把本节点的 first 标记下放给左儿子：`min(儿子first, first[p])`（懒更新）',
        'first[p * 2 + 2] = min': '同样下放给右儿子',
        'if end <= mid': '`end = {end} ≤ mid = {mid}`？操作区间只在左半 → {"是" if end <= mid else "否"}',
        'elif start > mid': '`start = {start} > mid = {mid}`？操作区间只在右半 → {"是" if start > mid else "否"}',
        'pair = ch_min(p * 2 + 1, left, mid, start, mid': '横跨两半：左半 `[{B.start},{B.mid}]` 和右半 `[{B.mid + 1},{B.end}]` 各递归，个数相加',
        'update_first(p)': '回溯：用两个儿子重新算本节点的 `first / second / first_cnt`',
        'first[p] = v': lambda S, B, r: ('叶子：upper 设为 `∞`（{}）'.format(S.v) if S._inner.get('index') is not None else '`first[p] = {}`：只有最大值被压成 v，打懒标记，不用往下走'.format(S.v)),
        'first_cnt[p] = 1': '叶子最大值只有 1 个',
        'index <= mid': '`index = {index}` 在 {"左" if index <= mid else "右"}半，往下找叶子',
        'return res': '全部遍历完，影子对共 =={ret}== 个',
    },
    cards=dict(
        one_liner='给每个左端点记一个“上界”，用吉司机线段树整段压平',
        complexity='时间 `O(n log n)` 均摊，空间 `O(n)`',
        problem=['`i < j` 且 `nums[i] < nums[j]`，且中间没有 `k` 使 `nums[i] < nums[k] < nums[j]`',
                 '数出这样的“影子对” `(i, j)` 的个数',
                 '示例：`[3,1,4,2,5]` → `5`',
                 '本视频：`[3,1,4,2]` → `3`'],
        quote='对于每个左边界值nums[i]，其对应的右边界值必然是单调不增的，因为一旦出现了递增的关系，前面这个较小的右边界值就会成为破坏影子对成立的k。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个已遍历的 `i` 维护上界 `upper[i]`：`nums[i] < nums[j] ≤ upper[i]` 才配成对，配完上界压成 `nums[j]`',
              '左端点按值排序后，“比 v 小的数”正好是一段前缀 `[0, bound]`',
              '前缀里 upper ≥ v 的全部压成 v、并计数 → 区间 chmin，吉司机线段树：维护最大值、次大值、最大值个数',
              '`v` 处理完再把它自己的上界设成 `∞`，成为新的左端点'],
        summary=['时间 `O(n log n)` 均摊（势能：每棵子树里不同值的个数之和），空间 `O(n)`',
                 '`first = -1` 表示还没遍历到：upper 比任何 v 都小，天然不会被统计',
                 '易错：相同的值要按出现顺序排名，`bound = o - cnt[v]`，才不会把相等的数算进“更小”',
                 '原文本身可直接在 Python 3 运行，代码未改',
                 '对比灵神：灵神用值域分治 + 两个单调栈，不用吉司机树'],
    ),
)
