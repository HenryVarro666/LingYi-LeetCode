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
    ty = y0 + 38
    nlev = max(i & -i for i in range(1, m + 1)).bit_length()
    rowh = min(60, (y1 - (ty + 100)) / nlev)
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
    by = ty + 78
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
def _tv(S):
    return S.get('self.sum_list'), S.get('self.nums')


def _cur(S):
    c = S.get('pos')
    if c is None:
        c = S.get('now')
    return c if c is not None and c >= 1 else None


def _draw(cv, S, B, box, T):
    t, v = _tv(S)
    if t is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    tb, _ = _tv(B)
    _fen_pic(cv, T, box, t, tb, v or [], _cur(S), '上排 = nums；每根条 = sum_list[i] 管的区间（黄 = 当前，蓝 = 覆盖）')


def _info(S):
    c = _cur(S)
    if 'pos' in S and c is not None:
        return f"`add({c}, {S['delta']})`：下标 `{c}` = {c:b}（二进制），lowbit = `{c & -c}`，管 [{c - (c & -c) + 1}, {c}]"
    if 'now' in S and c is not None:
        return f"查询：`now = {c}` = {c:b}（二进制），lowbit = `{c & -c}`，管 [{c - (c & -c) + 1}, {c}]"
    if 'i' in S and 'j' in S:
        return f"`sumRange({S['i']}, {S['j']})` = 前缀 [1, {S['j'] + 1}] − 前缀 [1, {S['i']}]"
    return ''


CONFIG = dict(
    num=307, title='区域和检索 - 数组可修改', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='树状数组（下标二进制位）',
    tags=['常用数据结构', '树状数组和线段树'],
    code='''
class NumArray(object):

    def __init__(self, nums):
        self.nums = nums[:]
        self.sum_list = [0] * (len(nums) + 1)
        self.length = len(nums)
        for index, num in enumerate(nums):
            self.add(index + 1, num)

    def add(self, pos, delta):
        while pos <= self.length:
            self.sum_list[pos] += delta
            pos += pos & -pos

    def update(self, i, val):
        delta = val - self.nums[i]
        self.add(i + 1, delta)
        self.nums[i] = val

    def sumRange(self, i, j):
        res = 0
        now = j + 1
        while now > 0:
            res += self.sum_list[now]
            now -= now & -now

        now = i
        while now > 0:
            res -= self.sum_list[now]
            now -= now & -now

        return res
''',
    call='''o = NumArray([1, 3, 5])
r = [o.sumRange(0, 2)]
o.update(1, 2)
r.append(o.sumRange(0, 2))
r''',
    expect=[9, 8],
    skip=['self.length = len(nums)', 'self.nums[i] = val', 'res = 0'],
    views=[
        dict(type='text', fn=_info, h=70),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('pos', 'pos', 'blue'), ('now', 'now', 'blue'), ('delta', 'delta', 'yellow'), ('res', 'res', 'green')],
    captions={
        'self.nums = nums[:]': '先复制一份 `nums`：更新时要拿旧值算差',
        'self.sum_list = ': '`sum_list` 长度 `n + 1`：下标从 1 开始，0 号位不用',
        'self.add(index + 1, num)': '把 `nums[{index}]` = {num} 加进树：`add({index + 1}, {num})`（下标 +1）',
        'while pos <= self.length': lambda S, B, r: (f"`pos = {S.pos}` ≤ `length = {S['self'].length}`：`sum_list[{S.pos}]` 管的区间含这个位置 → 要加"
                                                      if S.pos <= S['self'].length else f"`pos = {S.pos}` > `length = {S['self'].length}`：越界，所有含它的区间都加好了"),
        'self.sum_list[pos] += delta': '`sum_list[{pos}]` 管 [{pos - (pos & -pos) + 1}, {pos}]，加上 `{delta}` → =={self.sum_list[pos]}=={""}',
        'pos += pos & -pos': '`lowbit({B.pos}) = {B.pos & -B.pos}`：加上最低位的 1，进位到下一个更大的区间 `{pos}`',
        'delta = val - self.nums[i]': '新值 `{val}` − 旧值 `{self.nums[i]}` = =={delta}==：树里存累加和，只需加上差值',
        'self.add(i + 1, delta)': '`add({i + 1}, {delta})`：下标 +1 对齐树状数组，所有含该位置的区间都加 `delta`',
        'res = 0': '`res` 先累加前缀 [1, j+1]，再减去前缀 [1, i]',
        'now = j + 1': '`now = j + 1 = {now}`：先算前缀 [1, {now}]',
        'while now > 0': lambda S, B, r: (f'`now = {S.now}` > 0：前缀 [1, {S.now}] 还没拆完' if S.now > 0 else '`now = 0`：这一段前缀拆完了'),
        'res += self.sum_list[now]': '`sum_list[{now}]` 管 [{now - (now & -now) + 1}, {now}]，整段加进 `res` → =={res}=={""}',
        'res -= self.sum_list[now]': '`sum_list[{now}]` 管 [{now - (now & -now) + 1}, {now}]，整段从 `res` 减去 → =={res}=={""}',
        'now -= now & -now': '逐位去掉最低位的 1：`{B.now}` → `{now}`（{B.now:b} → {now:b}）',
        'now = i': '再算前缀 [1, i]，要减掉：`now = {i}`',
        'return res': '大前缀 − 小前缀 = 区间和 ==`{ret}`==',
    },
    cards=dict(
        one_liner='下标的二进制位决定管多长：sum[i] 管 i 往前 lowbit(i) 个数',
        complexity='建树 `O(n log n)`，查询、更新 `O(log n)`；空间 `O(n)`',
        problem=['`update(i, val)` 改一个数，`sumRange(i, j)` 求下标 `i ~ j` 的和',
                 '示例：`[1,3,5]`，`sumRange(0,2)=9`，`update(1,2)` 后 `sumRange(0,2)=8`',
                 '数组可修改，前缀和数组每次更新要重算，太慢'],
        quote='可以发现，sum[index]等于index - 2^k + 1到index这一段的和，其中k为index末尾0的个数',
        quote_src='—— yiduobo 题解原文',
        idea=['用下标的二进制位表示区间：`sum[6]`（110）= `nums[5] + nums[6]`，`sum[8]`（1000）= 前 8 个数',
              '更新：`pos += pos & -pos`，沿着包含自己的区间一路加上差值',
              '查询：`now -= now & -now`，逐位分离最低位的 1，累加各段；例如前 7 个数 = `sum[4] + sum[6] + sum[7]`',
              '区间和 = 前缀 `[1, j+1]` − 前缀 `[1, i]`'],
        summary=['更新、查询都是 `O(log n)`；建树对每个数调一次 `add`，共 `O(n log n)`',
                 '易错：树状数组下标从 1 开始，`nums` 下标从 0，所以 `add(i + 1, …)`、`now = j + 1`',
                 '更新加的是差值 `val − nums[i]`，所以要留一份 `nums` 旧值',
                 '对比灵神：灵神把前缀拆成关键区间并推导出 `O(n)` 建树；这里直接用 `add` 逐个插入'],
    ),
)
