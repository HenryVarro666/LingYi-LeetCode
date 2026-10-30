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
def _draw(cv, S, B, box, T):
    t = S.get('f')
    peek = S.get('peek')
    if t is None or peek is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    x = S.get('x')
    cur = x if (x is not None and 'index' in S and S.get('new_val') is not None) or (x is not None and 'index' not in S) else None
    if cur is not None and cur < 1:
        cur = None
    _fen_pic(cv, T, box, t, B.get('f'), list(peek), cur, '上排 = peek[index]（该位置是不是峰值）；位置 = index + 1；条 = f[x]（黄 = 当前）')


def _isp(a, i):
    return 0 < i < len(a) - 1 and a[i - 1] < a[i] > a[i + 1]


def _info(S):
    q = S.get('q')
    if q is None:
        return ''
    if q[0] == 1:
        return f"查询 `[1,{q[1]},{q[2]}]`：峰值只可能在下标 `{q[1] + 1} ~ {q[2] - 1}`（首尾不算）"
    return f"修改 `[2,{q[1]},{q[2]}]`：`nums[{q[1]}]` 改成 {q[2]}，要重算它和左右邻居的 `peek`"


CONFIG = dict(
    num=3187, title='数组中的峰值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='peek 数组 + 树状数组（动态前缀和）',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2154'],
    code='''
class Solution(object):
    def countOfPeaks(self, nums, queries):

        n = len(nums)
        peek = [0] * n
        f = [0] * (n + 1)

        def update(index):
            if index == 0 or index == n - 1:
                return
            
            new_val = 0
            if nums[index] > nums[index - 1] and nums[index] > nums[index + 1]:
                new_val = 1
            
            if peek[index] == new_val:
                return
            
            x = index + 1
            while x <= n:
                f[x] += new_val - peek[index]
                x += x & -x
            
            peek[index] = new_val

        def get(x):
            s = 0
            while x:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n - 1):
            update(index)

        res = []
        for q in queries:
            if q[0] == 1:
                if q[1] + 1 <= q[2] - 1:
                    res.append(get(q[2]) - get(q[1] + 1))
                else:
                    res.append(0)
            else:
                nums[q[1]] = q[2]
                update(q[1])
                if q[1] > 0:
                    update(q[1] - 1)
                if q[1] < n - 1:
                    update(q[1] + 1)
        
        return res
''',
    call='Solution().countOfPeaks([1, 3, 2, 1], [[1, 0, 3], [2, 2, 4], [1, 0, 2]])',
    expect=[1, 0],
    max_steps=66,
    skip=['n = len(nums)', 'res = []', 'new_val = 0', 'x = index + 1', 'while x <= n', 'while x:', 's = 0', 'if index == 0 or index == n - 1'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='nums', label='nums（绿 = 当前峰值）', h=150,
             color=lambda S, i, v: 'green' if _isp(S['nums'], i) else None),
        dict(type='array', var='res', label='res', cell=64, h=100),
    ],
    watch=[('index', 'index', 'blue'), ('new_val', 'new_val', 'yellow'), ('x', 'x', 'pink'), ('s', 's', 'green')],
    captions={
        'peek = [0] * n': '`peek[index]` = 1 表示 `nums[index]` 是峰值，0 表示不是',
        'f = [0] * (n + 1)': '树状数组 `f`，下标从 1 开始（位置 = index + 1），维护 `peek` 的前缀和',
        'if nums[index] > nums[index - 1] and': lambda S, B, r: (
            f'`nums[{S.index}] = {S.nums[S.index]}`，左 `{S.nums[S.index - 1]}`，右 `{S.nums[S.index + 1]}`：'
            + ('比两边都大 → ==峰值=='  if S.nums[S.index] > S.nums[S.index - 1] and S.nums[S.index] > S.nums[S.index + 1] else '不是峰值')),
        'new_val = 1': '`new_val = 1`：峰值',
        'if peek[index] == new_val': lambda S, B, r: (f'`peek[{S.index}] = {S.peek[S.index]}` == `new_val = {S.new_val}`：状态没变，树不用动 → 直接返回'
                                                      if S.peek[S.index] == S.new_val else f'`peek[{S.index}] = {S.peek[S.index]}` ≠ `new_val = {S.new_val}`：状态变了，要把差值加进树'),
        10: '首尾不可能是峰值（`index == 0` 或 `n - 1`）→ 直接返回',
        17: '没有变化，返回，树不用动',
        'f[x] += new_val - peek[index]': '`f[{x}]` 管 [{x - (x & -x) + 1}, {x}]，加上差值 `{new_val} − {peek[index]}` = `{new_val - peek[index]}` → =={f[x]}==',
        'x += x & -x': '`x += lowbit` → `{x}`：下一个包含该位置的区间',
        'peek[index] = new_val': '记下新状态 `peek[{index}] = {new_val}`',
        's += f[x]': '`f[{x}]` 管 [{x - (x & -x) + 1}, {x}]，整段加进 `s` → =={s}==',
        'x -= x & -x': '去掉最低位的 1：`{B.x}` → `{x}`',
        'return s': '前缀和 `{ret}`',
        'for index in range(1, n - 1)': lambda S, B, r: ('每个位置都判断过了，树建好' if ('index' in B and B['index'] == S.index) else f'建树：首尾不可能是峰值，从 `index = {S.index}` 开始判断'),
        'update(index)': '`update({index})`：重新判断 `nums[{index}]` 是不是峰值',
        'for q in queries': lambda S, B, r: ('所有查询处理完了' if ('q' in B and B['q'] == S.q) else f'处理查询 `q = {S.q}`'),
        'if q[0] == 1': lambda S, B, r: ('`q[0] == 1`：==查询==' if S.q[0] == 1 else '`q[0] == 2`：==修改=='),
        'if q[1] + 1 <= q[2] - 1': lambda S, B, r: (f'峰值只可能在 `[{S.q[1] + 1}, {S.q[2] - 1}]`：区间不空 → 用前缀和' if S.q[1] + 1 <= S.q[2] - 1 else '首尾都不算，区间是空的 → 答案 0'),
        'res.append(get(q[2]) - get(q[1] + 1))': '前缀 `get({q[2]})` − 前缀 `get({q[1] + 1})`：位置从 `{q[1] + 2}` 到 `{q[2]}`，也就是下标 `{q[1] + 1} ~ {q[2] - 1}`',
        'res.append(0)': '区间为空：`res` 加 `0`',
        'nums[q[1]] = q[2]': '先改 `nums[{q[1]}] = {q[2]}`',
        'update(q[1])': '重算 `nums[{q[1]}]` 自己是不是峰值',
        'update(q[1] - 1)': '它的==左邻居==也变了：重算下标 `{q[1] - 1}`',
        'update(q[1] + 1)': '它的==右邻居==也变了：重算下标 `{q[1] + 1}`',
        'if q[1] > 0': '左边还有邻居吗？`q[1] = {q[1]}` > 0 才需要重算',
        'if q[1] < n - 1': '右边还有邻居吗？`q[1] = {q[1]}` < `n - 1 = {n - 1}` 才需要重算',
        'return res': '所有查询 1 的答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='peek 记成 0/1，区间峰值数 = 区间和；改一个数只重算它和左右邻居',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['峰值：严格大于左右邻居的元素；==区间首尾不算峰值==',
                 '操作 1：求 `nums[l..r]` 里峰值个数；操作 2：把 `nums[index]` 改成 `val`',
                 '本视频：`nums=[1,3,2,1]`，`[[1,0,3],[2,2,4],[1,0,2]]` → `[1,0]`'],
        quote='令peek[index]表示nums[index]是否为峰值元素，若nums[index]是峰值元素，那么peek[index]就等于1，否则peek[index]就等于0。这样一来，nums[l]到nums[r]之间峰值元素的数目，就相当于peek[l]到peek[r]这一段的区间和',
        quote_src='—— yiduobo 题解原文',
        idea=['「区间里满足条件的个数」→ 新开 `peek` 数组，满足记 1，不满足记 0，再求和',
              'peek 会变 → 动态前缀和 → 树状数组，查询用 `get(r) − get(l)`',
              '修改：只更新 `peek[index]` 与更新前的差值：`new_val − peek[index]` 加进树',
              '改 `nums[index]` 会影响 `index − 1, index, index + 1` 三个位置'],
        summary=['时间 `O((n + q) log n)`，空间 `O(n)`',
                 '易错：首尾不可能是峰值（`update` 里直接返回）；查询区间要缩成 `[l+1, r-1]`，空了答 0',
                 '`update` 先比较新旧 `peek`：没变化就不碰树；变了才加差值',
                 '对比灵神：灵神每次先「去掉旧峰值」再「加回新峰值」；这里直接加新旧差值，省一轮'],
    ),
)
