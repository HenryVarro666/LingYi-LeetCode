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
    o = S.get('self')
    t = S.get('tree')
    if t is None:
        t = getattr(o, 'tree', None)
    v = getattr(o, 'nums', None)
    if v is None:
        v = S.get('nums')
    return t, v


def _draw(cv, S, B, box, T):
    t, v = _tv(S)
    if t is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    tb, _ = _tv(B)
    cur = S.get('i')
    if cur is not None and cur < 1:
        cur = None
    _fen_pic(cv, T, box, t, tb, v or [], cur, '上排 = 数组；每根条 = 关键区间 tree[i]（黄 = 当前，蓝 = 覆盖）')


def _info(S):
    i = S.get('i')
    if 'index' in S and 'val' in S:
        s = f"`update({S['index']}, {S['val']})`：下标 `{S['index'] + 1}` 所在的所有关键区间都要改"
        if i is not None and i >= 1:
            s += f"；当前 `i = {i}`（{i:b}），lowbit = `{i & -i}`，管 [{i - (i & -i) + 1}, {i}]"
        return s
    if 'left' in S and 'right' in S and 's' not in S:
        return f"`sumRange({S['left']}, {S['right']})` = 前缀 [1, {S['right'] + 1}] − 前缀 [1, {S['left']}]"
    if 'left' in S and 'right' in S and 'i' in S:
        return f"计算前缀 [1, {S.get('_orig', i)}] 的和"
    if i is not None and 's' in S:
        return f"拆分前缀：`i = {i}`（{i:b}），lowbit = `{i & -i}`" if i else '`i = 0`：前缀拆完了'
    if i is not None and 'nxt' in S:
        return f"建树：`i = {i}`（{i:b}），lowbit = `{i & -i}`，下一个关键区间右端点 = `{i} + {i & -i}` = `{S['nxt']}`"
    return ''


CONFIG = dict(
    num=307, title='区域和检索 - 数组可修改', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='树状数组（O(n) 建树）',
    tags=['常用数据结构', '树状数组和线段树'],
    code='''
class NumArray:
    __slots__ = 'nums', 'tree'

    def __init__(self, nums: List[int]):
        n = len(nums)
        tree = [0] * (n + 1)
        for i, x in enumerate(nums, 1):  # i 从 1 开始
            tree[i] += x
            nxt = i + (i & -i)  # 下一个关键区间的右端点
            if nxt <= n:
                tree[nxt] += tree[i]
        self.nums = nums
        self.tree = tree

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        i = index + 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefixSum(self, i: int) -> int:
        s = 0
        while i:
            s += self.tree[i]
            i &= i - 1  # i -= i & -i 的另一种写法
        return s

    def sumRange(self, left: int, right: int) -> int:
        return self.prefixSum(right + 1) - self.prefixSum(left)
''',
    call='''o = NumArray([1, 3, 5, 2])
r = [o.sumRange(0, 2)]
o.update(1, 2)
r.append(o.sumRange(0, 2))
r''',
    expect=[9, 8],
    max_steps=52,
    skip=['if nxt <= n', 'self.nums = nums', 'self.tree = tree', 'self.nums[index] = val', 's = 0'],
    views=[
        dict(type='text', fn=_info, h=70),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'green'), ('delta', 'delta', 'yellow')],
    captions={
        'tree = [0] * (n + 1)': '`tree` 用下标 `1 ~ {n}`，多开一格：`tree[i]` 存==右端点为 i 的关键区间==的和',
        'tree[i] += x': '`tree[{i}]` 加上 `nums[{i - 1}]` = {x} → `tree[{i}]` = =={tree[i]}==：这个关键区间算完了',
        'nxt = i + (i & -i)': lambda S, B, r: (f'`lowbit({S.i}) = {S.i & -S.i}`，下一个关键区间右端点 `nxt = {S.nxt}`' +
                                                (f' ≤ `n`：它也包含 `tree[{S.i}]` 管的范围，待会儿汇入' if S.nxt <= S.n else f' > `n = {S.n}`：没有更大的区间了，不用汇入')),
        'tree[nxt] += tree[i]': '把算好的 `tree[{i}]` = {tree[i]} 汇入更大的区间：`tree[{nxt}]` → =={tree[nxt]}==（刷表，不用再逐个 update）',
        'self.nums = nums': '保存 `nums`，建树 `O(n)` 完成',
        'self.tree = tree': '保存 `tree` = {tree}',
        'delta = val - self.nums[index]': '新值 `{val}` 减旧值 `{self.nums[index]}`：`delta` = =={delta}==。树状数组只存累加和，更新就是给每个相关区间==加上 delta==',
        'self.nums[index] = val': '`nums[{index}]` 改成 `{val}`',
        'i = index + 1': '树状数组下标从 1 开始：`i = {index} + 1` = =={i}==',
        'while i < len(self.tree)': lambda S, B, r: (f'`i = {S.i}` < {len(S.tree) if "tree" in S else len(S["self"].tree)}：`tree[{S.i}]` 管的区间包含被改的位置 → 要更新'
                                                     if S.i < len(S['self'].tree) else f'`i = {S.i}` 越界：包含该位置的关键区间都改完了'),
        'self.tree[i] += delta': '`tree[{i}]` 管 [{i - (i & -i) + 1}, {i}]，包含下标 {index + 1} → 加上 `{delta}` → =={self.tree[i]}=={""}',
        'i += i & -i': '`i += lowbit({B.i})`（+{B.i & -B.i}）：跳到下一个包含该位置的更大区间 `{i}`',
        's = 0': '`s` 累加前缀 [1, {i}] 拆出来的关键区间',
        'while i:': lambda S, B, r: (f'`i = {S.i}`（{S.i:b}）≠ 0：前缀 [1, {S.i}] 还没拆完' if S.i else '`i = 0`：前缀拆完了'),
        's += self.tree[i]': '`tree[{i}]` 管 [{i - (i & -i) + 1}, {i}]，整段加进 `s` → =={s}=={""}',
        'i &= i - 1': '去掉最低位的 1：`{B.i}` → `{i}`（{B.i:b} → {i:b}），剩下的前缀 [1, {i}] 继续拆',
        'return s': '前缀和 = ==`{ret}`==',
        'return self.prefixSum(right + 1)': lambda S, B, ret: (f'区间和 = 前缀 [1,{S.right + 1}] − 前缀 [1,{S.left}]，先分别算两个前缀和' if ret is None
                                                              else f'大前缀 − 小前缀 = 区间和 ==`{ret}`=='),
    },
    cards=dict(
        one_liner='把前缀拆成 lowbit 长度的关键区间：查询和更新都只走 log n 步',
        complexity='建树 `O(n)`，查询、更新 `O(log n)`；空间 `O(n)`',
        problem=['`NumArray(nums)`：初始化；`update(index, val)`：把 `nums[index]` 改成 `val`',
                 '`sumRange(left, right)`：返回下标 `left ~ right` 的元素和',
                 '`n ≤ 3·10^4`，查询和更新各最多 `3·10^4` 次',
                 '本视频：`[1,3,5,2]`，`sumRange(0,2)=9`，`update(1,2)` 后 `8`'],
        quote='如果你之前学过树状数组，请把它忘了，我将带你重新发明树状数组。',
        quote_src='—— 灵茶山艾府题解《带你发明树状数组》',
        idea=['前缀和查询快但更新慢；逐个存又查询慢 → 折中：把前缀 [1,i] 拆成 ==log 段关键区间==',
              '`i` 的二进制从低位往高位拆：区间 `[i-lowbit(i)+1, i]` 的和存在 `tree[i]`，共 `n` 个',
              '改一个数 = 给所有包含它的区间加 `delta`：`i += i & -i`；查前缀 = `i &= i - 1` 逐段累加',
              '建树可以「刷表」：算好 `tree[i]` 就加到 `tree[i + lowbit(i)]`，`O(n)`'],
        summary=['查询、更新各 `O(log n)`，建树 `O(n)`；`tree` 要多开一格，因为下标从 1 开始',
                 '易错：`nums` 下标从 0，树状数组下标从 1，`sumRange` 要用 `prefixSum(right+1) − prefixSum(left)`',
                 '更新存的是==差值 delta==，不是新值；`self.nums` 要同步改，下次才能算 delta',
                 '原文另有 `O(n log n)` 建树：对每个 `nums[i]` 调一次 `update`；结果相同'],
    ),
)
