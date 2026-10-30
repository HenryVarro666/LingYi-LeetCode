def _fen_pic(cv, T, box, tree, old, vals, cur, title, vlabel='值'):
    """树状数组：上排 = 位置 1..m 的值，下面每根条 = tree[i] 管的关键区间 [i-lowbit+1, i]（按 lowbit 分层）；
    黄色 = 当前正在访问的 tree[i]，蓝色 = 它覆盖的位置，黄边 = 这一步刚改过"""
    x0, y0, x1, y1 = box
    m = len(tree) - 1
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    if m < 1:
        return
    cell = min(120, (x1 - x0 - 60) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    ty = y0 + 34
    nlev = max(i & -i for i in range(1, m + 1)).bit_length()
    rowh = min(60, (y1 - (ty + 76)) / nlev)
    lo = hi = None
    if cur is not None and 1 <= cur <= m:
        hi = cur
        lo = cur - (cur & -cur) + 1
    for i in range(1, m + 1):
        X = sx + (i - 1) * cell
        covered = lo is not None and lo <= i <= hi
        cv.rect((X + 2, ty, X + cell - 2, ty + 42), fill=T['blue'] if covered else T['panel2'], r=6, alpha=200 if covered else 255)
        v = vals[i - 1] if i - 1 < len(vals) else ''
        cv.text((X + cell / 2, ty + 21), v, 24, T['bg'] if covered else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 48), i, 18, T['dim'], anchor='mt', mono=True)
    by = ty + 72
    for i in range(1, m + 1):
        lb = i & -i
        lv = lb.bit_length() - 1
        xa, xb = sx + (i - lb) * cell + 3, sx + i * cell - 3
        ya = by + lv * rowh
        changed = old is not None and len(old) == len(tree) and old[i] != tree[i]
        if i == cur:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((xa, ya, xb, ya + rowh - 5), fill=fill, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1, r=6)
        lab = f't{i}={tree[i]}' if cell * lb > 150 else f'{tree[i]}'
        if lb > 1:
            lab = f't{i}={tree[i]}  [{i - lb + 1},{i}]' if cell * lb > 260 else f't{i}={tree[i]}'
        cv.text(((xa + xb) / 2, ya + (rowh - 5) / 2), lab, 20, tc, anchor='mm', bold=True)


def _lb_text(i):
    return f'`{i}` = `{i:b}`（二进制），lowbit = `{i & -i}`'
def _tree(S):
    t = S.get('self.tree')
    if t is None:
        o = S.get('t')
        t = o if isinstance(o, list) else getattr(o, 'tree', None)
    return t


def _draw(cv, S, B, box, T):
    t = _tree(S)
    sn = S.get('sorted_nums')
    if t is None or sn is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    cur = S.get('i')
    if 'self.tree' not in S:
        cur = None
    _fen_pic(cv, T, box, t, _tree(B), list(reversed(sn)), cur if cur and cur >= 1 else None,
             '上排 = 值（位置 1 = 最大值）；条 = 区间内 a 比 b 多的个数（黄 = 当前）')


def _info(S):
    if 'd' in S and 'x' in S:
        d = S['d']
        who = 'a 多' if d > 0 else ('b 多' if d < 0 else '一样多')
        return f"`x = {S['x']}`：比 x 大的元素 `a` 比 `b` 多 `d = {d}` 个（{who}）"
    if 'v' in S and 'x' in S:
        return f"`x = {S['x']}` 离散化成位置 `v = m − j = {S['v']}`（大的值位置靠前）"
    return ''


CONFIG = dict(
    num=3072, title='将元素分配到两个数组中 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='值域树状数组（差值 + 离散化）',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2053'],
    code='''
# 模板来源 https://leetcode.cn/discuss/post/3583665/
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res += t[i]
            i &= i - 1
        return res

class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        sorted_nums = sorted(set(nums))
        m = len(sorted_nums)

        a = [nums[0]]
        b = [nums[1]]
        t = FenwickTree(m)
        t.update(m - bisect_left(sorted_nums, nums[0]), 1)
        t.update(m - bisect_left(sorted_nums, nums[1]), -1)

        for x in nums[2:]:
            v = m - bisect_left(sorted_nums, x)
            d = t.pre(v - 1)  # 转换成 < v 的元素个数之差
            if d > 0 or d == 0 and len(a) <= len(b):
                a.append(x)
                t.update(v, 1)
            else:
                b.append(x)
                t.update(v, -1)

        return a + b
''',
    call='Solution().resultArray([5, 14, 3, 1])',
    expect=[5, 3, 1, 14],
    max_steps=62,
    skip=['t = self.tree'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='custom', draw=_draw, h=270),
        dict(type='array', var='a', label='a（arr1）', h=130),
        dict(type='array', var='b', label='b（arr2）', h=130),
    ],
    watch=[('x', 'x', 'yellow'), ('v', 'v', 'blue'), ('d', 'd', 'pink'), ('i', 'i', 'blue'), ('res', 'res', 'green')],
    captions={
        'sorted_nums = sorted(set(nums))': '值太大不能直接当下标 → ==离散化==：去重排序得 `{sorted_nums}`，只关心相对大小',
        'm = len(sorted_nums)': '一共 `{m}` 个不同的值，树状数组开 `{m}` 格',
        'a = [nums[0]]': '第 1 次操作：`nums[0]` = {nums[0]} 进 `a`',
        'b = [nums[1]]': '第 2 次操作：`nums[1]` = {nums[1]} 进 `b`',
        't = FenwickTree(m)': '==一棵==树状数组就够：记录每个值在 `a` 里比在 `b` 里多出现几次（`a` 加 1，`b` 减 1）',
        't.update(m - bisect_left(sorted_nums, nums[0]), 1)': '`nums[0]` 在 `a` 里：位置 `m − 下标` = `{m - bisect_left(sorted_nums, nums[0])}`，加 `1`',
        't.update(m - bisect_left(sorted_nums, nums[1]), -1)': '`nums[1]` 在 `b` 里：位置 `{m - bisect_left(sorted_nums, nums[1])}`，减 `1`（==b 用负数==）',
        'for x in nums[2:]': '处理第 3 次及以后的操作',
        'v = m - bisect_left': '`x = {x}` 在去重数组里下标 `{bisect_left(sorted_nums, x)}`，位置 `v = m − 下标` = =={v}==：位置取反后，==比 x 大的值恰好在 v 前面==',
        'd = t.pre(v - 1)': 'greaterCount(a, x) − greaterCount(b, x) = 前缀 `[1, {v - 1}]` 的和 = =={d}==',
        'if d > 0 or d == 0': lambda S, B, r: (f'`d = {S.d}` > 0：a 里比 {S.x} 大的更多 → 放 `a`' if S.d > 0 else
                                                (f'`d = 0` 且 `len(a) = {len(S.a)} ≤ len(b) = {len(S.b)}` → 放 `a`' if len(S.a) <= len(S.b) and S.d == 0
                                                 else (f'`d = {S.d}` < 0：b 里比 {S.x} 大的更多 → 放 `b`' if S.d < 0 else f'`d = 0` 但 `len(a) = {len(S.a)} > len(b) = {len(S.b)}` → 放 `b`'))),
        'a.append(x)': '`x = {x}` 追加到 `a`：`a = {a}`',
        'b.append(x)': '`x = {x}` 追加到 `b`：`b = {b}`',
        't.update(v, 1)': '`a` 多了一个：位置 `{v}` 加 `1`',
        't.update(v, -1)': '`b` 多了一个：位置 `{v}` 减 `1`',
        'while i < len(t)': lambda S, B, r: (f'`i = {S.i}` < {len(S.t)}：`t[{S.i}]` 管的区间含这个位置 → 要改' if S.i < len(S.t) else f'`i = {S.i}` 越界：改完了'),
        't[i] += val': '`t[{i}]` 管 [{i - (i & -i) + 1}, {i}]，加 `{val}` → =={t[i]}==',
        'i += i & -i': '`i += lowbit` → `{i}`：下一个包含该位置的区间',
        'res = 0': '`res` 累加前缀 `[1, {i}]`',
        'while i > 0': lambda S, B, r: (f'`i = {S.i}` > 0：前缀还没拆完' if S.i > 0 else '`i = 0`：前缀拆完了'),
        'res += t[i]': '`t[{i}]` 管 [{i - (i & -i) + 1}, {i}]，加进 `res` → =={res}==',
        'i &= i - 1': '去掉最低位的 1：`{B.i}` → `{i}`',
        'return res': '前缀和 `{ret}`',
        'return a + b': '把 `a` 和 `b` 拼起来：`{a}` + `{b}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='树状数组存「a 比 b 多几个」，一次前缀和就比出 greaterCount',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['按规则把 `nums` 逐个分到 `arr1`、`arr2`：比较两边「严格大于 x 的个数」',
                 '`arr1` 里更多放 `arr1`，`arr2` 更多放 `arr2`；相等放元素少的，再相等放 `arr1`',
                 '最后返回 `arr1 + arr2`；示例：`[5,14,3,1,2]` → `[5,3,1,2,14]`；本视频：`[5,14,3,1]`'],
        quote='用两棵值域树状数组分别维护 a 和 b 中的每个元素的出现次数，即可快速计算 greaterCount。……把元素 v 添加到 t2 的操作，可以改成把元素 v 在 t1 中的出现次数减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['值域很大 → 先 ==离散化==（排序去重），只留相对大小',
              '写法一：两棵树，`greaterCount = len − pre(v)`；写法二：只关心两边的==差==，合并成一棵树',
              '`a` 的元素 +1、`b` 的元素 −1；位置取 `m − 下标`，让「比 x 大」变成「位置更小」，一次 `pre(v-1)` 就是差值 `d`'],
        summary=['时间 `O(n log n)`（离散化 + 每个数两次树状数组操作），空间 `O(n)`',
                 '易错：`d` 是 ==严格大于== x 的差，所以取 `pre(v - 1)`，不含 x 自己',
                 '`d == 0` 时要比较长度，再相等放 `a`；`<=` 不能写成 `<`',
                 '写法一：两棵树状数组 `t1`、`t2` 分别维护，`greaterCount = len(a) − t1.pre(v)`，本视频演示写法二'],
    ),
)
