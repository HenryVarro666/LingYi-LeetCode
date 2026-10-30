FULL = 100000
LO = FULL - 7          # 画出 99993 ~ 100000 这 8 个位置
OPS = '`append(2)` → `addAll(3)` → `append(7)` → `multAll(2)` → `getIndex(1)`'


def _lowbit(i):
    return i & -i


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    im, ia = S.get('self.index_m'), S.get('self.index_a')
    if im is None or ia is None:
        cv.text((x0 + 18, y0 + 10), '树状数组尚未创建（两个长为 100001 的数组）', 24, T['dim'])
        return
    bim, bia = B.get('self.index_m'), B.get('self.index_a')
    nums = S.get('self.nums') or []
    cv.text((x0 + 18, y0 + 4), '树状数组的末尾（倒着存：第 k 个数在位置 100000 − k + 1）', 22, T['muted'], bold=True)
    far_w = 150
    n = FULL - LO + 1
    w = (x1 - x0 - 40 - far_w) / n
    sx = x0 + 20 + far_w
    top = y0 + 60
    idx = S.get('index') if S.get('_line', 0) in range(14, 19) or S.get('_line', 0) in range(21, 28) \
        or S.get('_line', 0) in range(34, 43) else None
    for k in range(n):
        p = LO + k
        X = sx + k * w
        m, a = im[p], ia[p]
        touched = m != 1 or a != 0
        ch = bim is not None and (bim[p] != m or bia[p] != a)
        hot = idx == p
        fill = (60, 52, 30) if hot else (T['panel2'] if touched else T['panel'])
        oc = T['yellow'] if (ch or hot) else T['border']
        cv.rect((X + 3, top, X + w - 3, top + 150), fill=fill, r=10, outline=oc, width=4 if (ch or hot) else 1)
        cv.text((X + w / 2, top + 18), p, 15, T['muted'], anchor='mm', mono=True)
        cv.text((X + w / 2, top + 58), f'm={m}', 22, T['orange'] if m != 1 else T['dim'], anchor='mm', mono=True, bold=m != 1)
        cv.text((X + w / 2, top + 98), f'a={a}', 22, T['cyan'] if a != 0 else T['dim'], anchor='mm', mono=True, bold=a != 0)
        lb = _lowbit(p)
        cv.text((X + w / 2, top + 134), f'管{lb}个', 15, T['dim'], anchor='mm')
        kth = FULL - p  # nums 下标
        if 0 <= kth < len(nums):
            cv.text((X + w / 2, top + 170), f'nums[{kth}]', 17, T['green'], anchor='mm', mono=True)
            cv.text((X + w / 2, top + 196), nums[kth], 26, T['green'], anchor='mm', bold=True)
        if hot:
            cv.tri_up(X + w / 2, top + 218, 10, T['yellow'])
            cv.text((X + w / 2, top + 236), 'index', 19, T['yellow'], anchor='mt', bold=True)
    # 左边：更小的位置（都没被改过）
    cv.rect((x0 + 20, top, x0 + 20 + far_w - 10, top + 150), fill=T['panel'], r=10, outline=T['border'], width=1)
    cv.text((x0 + 20 + (far_w - 10) / 2, top + 50), '1 ~ 99992', 17, T['dim'], anchor='mm', mono=True)
    cv.text((x0 + 20 + (far_w - 10) / 2, top + 84), 'm=1, a=0', 17, T['dim'], anchor='mm', mono=True)
    if idx is not None and idx < LO:
        X = x0 + 20 + (far_w - 10) / 2
        cv.rect((x0 + 20, top, x0 + 20 + far_w - 10, top + 150), outline=T['yellow'], width=4, r=10)
        cv.text((X, top + 120), str(idx), 19, T['yellow'], anchor='mm', mono=True, bold=True)
        cv.tri_up(X, top + 218, 10, T['yellow'])
        cv.text((X, top + 236), 'index', 19, T['yellow'], anchor='mt', bold=True)
    if idx is not None and 0 < idx <= FULL:
        lb = _lowbit(idx)
        cv.rich(x0 + 22, top + 280, f'`index = {idx}`，`lowbit = {lb}`：这个节点管 `({idx - lb}, {idx}]` 这 {lb} 个位置',
                x1 - x0 - 44, size=24, accent=T['yellow'])


def _ops_text(S):
    return f'操作：{OPS}'


def _acc(S):
    if 'a' in S and 'm' in S and S.get('_line', 0) >= 35 and isinstance(S.get('a'), int):
        return f'查询累计：`m = {S["m"]}`，`a = {S["a"]}`　→ 答案 = `nums[idx−1] × m + a`'
    return '修改：`index += lowbit` 往大走；查询：`index -= lowbit` 往小走'


def _w15(S, B, ret):
    if S.index <= S.self.full_size:
        return f'`index = {S.index} ≤ 100000` → 更新这个节点'
    return f'`index = {S.index}` 超过 100000 → 更新结束'


def _w22(S, B, ret):
    if S.index <= S.self.full_size:
        return f'`index = {S.index}` → 这个节点的变换也要乘上 `{S.m}`'
    return f'`index = {S.index}` 超过 100000 → 更新结束'


def _w37(S, B, ret):
    if S.index > 0:
        p = S.index
        tag = '（被修改过）' if S.self.index_m[p] != 1 or S.self.index_a[p] != 0 else '（没被修改过，m=1, a=0）'
        return f'`index = {p}` → 合并这个节点{tag}'
    return '`index = 0` → 查询结束'


CONFIG = dict(
    num=1622, title='奇妙序列', difficulty='Hard', category='设计',
    author='yiduobo', technique='倒序存储 + 树状数组维护 (乘, 加)',
    tags=['字节30天'],
    code='''
class Fancy(object):

    def __init__(self):
        self.full_size = 100000
        self.index_m = [1] * (self.full_size + 1)
        self.index_a = [0] * (self.full_size + 1)
        self.nums = []
        self.mod = 10 ** 9 + 7

    def append(self, val):
        self.nums.append(val)

    def addAll(self, inc):
        index = self.full_size - len(self.nums) + 1
        while index <= self.full_size:
            self.index_a[index] += inc
            self.index_a[index] %= self.mod
            index += index & -index

    def multAll(self, m):
        index = self.full_size - len(self.nums) + 1
        while index <= self.full_size:
            self.index_m[index] *= m
            self.index_m[index] %= self.mod
            self.index_a[index] *= m
            self.index_a[index] %= self.mod
            index += index & -index

    def getIndex(self, idx):
        idx += 1
        if idx > len(self.nums):
            return -1

        index = self.full_size - idx + 1
        m = 1
        a = 0
        while index > 0:
            m *= self.index_m[index]
            m %= self.mod
            a = a * self.index_m[index] + self.index_a[index]
            a %= self.mod
            index -= index & -index

        return (self.nums[idx - 1] * m + a) % self.mod
''',
    call='''f = Fancy()
f.append(2); f.addAll(3); f.append(7); f.multAll(2)
f.getIndex(1)''',
    expect=14,
    skip=['%= self.mod'],
    views=[
        dict(type='text', size=24, h=60, fn=_ops_text),
        dict(type='custom', draw=_draw, h=480),
        dict(type='text', size=24, h=60, fn=_acc),
    ],
    watch=[('index', 'index', 'yellow'), ('m', 'm', 'orange'), ('a', 'a', 'cyan'), ('idx', 'idx', 'green')],
    captions={
        'self.full_size = 100000': 'append 最多 100000 次 → 直接开大小 100000 的树状数组',
        'self.index_m = [1]': '`index_m`：每个节点记录的“乘多少”，初始 1',
        'self.index_a = [0]': '`index_a`：每个节点记录的“加多少”，初始 0（节点表示变换 `x → x·m + a`）',
        'self.nums = []': '`nums` 原样存 append 进来的数',
        'self.mod = 10 ** 9 + 7': '答案对 `10^9+7` 取模',
        'self.nums.append(val)': '`append({val})`：第 {len(self.nums)} 个数，对应树状数组位置 `{100000 - len(self.nums) + 1}`',
        14: '`addAll({inc})`：当前有 {len(self.nums)} 个数 → 从位置 `100000 − {len(self.nums)} + 1 = {index}` 开始更新',
        15: _w15,
        'self.index_a[index] += inc': '节点 `{index}` 的加数 `a` += {inc} → `{self.index_a[index]}`',
        18: lambda S, B, r: f'`index += lowbit({B.index}) = {B.index & -B.index}` → `{S.index}`：去更新==更大的==位置',
        21: '`multAll({m})`：当前有 {len(self.nums)} 个数 → 从位置 `{index}` 开始更新',
        22: _w22,
        'self.index_m[index] *= m': '节点 `{index}`：`m` 乘 {m} → `{self.index_m[index]}`',
        'self.index_a[index] *= m': '`(x·m + a)·{m} = x·({m}m) + {m}a`：所以 `a` 也乘 {m} → `{self.index_a[index]}`',
        27: lambda S, B, r: f'`index += lowbit({B.index}) = {B.index & -B.index}` → `{S.index}`',
        'idx += 1': '`getIndex({idx - 1})`：换成从 1 开始的第 `{idx}` 个数',
        'if idx > len(self.nums)': lambda S, B, r: (f'`{S.idx} > {len(S.self.nums)}` → 越界' if S.idx > len(S.self.nums)
                                                    else f'`{S.idx} ≤ {len(S.self.nums)}`，下标合法'),
        'return -1': '返回 -1',
        'index = self.full_size - idx + 1': '第 {idx} 个数存在位置 `100000 − {idx} + 1 = {index}`',
        'm = 1': '`m`、`a` 累计查到的变换，从恒等变换 `x → x·1 + 0` 开始',
        'a = 0': '`a = 0`',
        37: _w37,
        'm *= self.index_m[index]': '`m` 乘上节点的 `{self.index_m[index]}` → `{m}`',
        'a = a * self.index_m[index]': lambda S, B, r: (f'`a = {B.a} × {S.self.index_m[S.index]} + {S.self.index_a[S.index]} = {S.a}`：'
                                                        '先做前面的变换，再做这个节点的'),
        42: lambda S, B, r: f'`index -= lowbit({B.index}) = {B.index & -B.index}` → `{S.index}`：往==更小==的位置查',
        'return (self.nums[idx - 1] * m + a)': '`nums[{idx - 1}] × m + a = {self.nums[idx - 1]} × {m} + {a}` = =={ret}==',
    },
    max_steps=46,
    cards=dict(
        one_liner='把序列倒过来存，前缀操作就变成树状数组的后缀更新',
        complexity='每个操作 `O(log N)`，`N = 100000`；空间 `O(N)`',
        problem=['`append(val)` 追加；`addAll(inc)` 所有数加 inc；`multAll(m)` 所有数乘 m',
                 '`getIndex(idx)` 返回下标 idx 的值（模 `10^9+7`），越界返回 `-1`',
                 '本视频：append 2、addAll 3、append 7、multAll 2 → `[10, 14]`，查 `getIndex(1) = 14`'],
        quote='无论之前经历过什么样的操作，最后都可以将答案写成==multi * x + add==的形式。……一般的树状数组是操作完x这个位置后会对大于等于x的所有位置产生影响，而本题……那么一个自然的想法就是==直接倒过来存储序列==。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个 addAll/multAll 只影响==已经存在==的数，即一段前缀',
              '倒着存：第 k 个数放在位置 `100000 − k + 1`，操作就变成“影响 ≥ 某位置的所有数”',
              '树状数组节点存变换 `x → x·m + a`；查询时把路径上的变换依次复合'],
        summary=['每个操作 `O(log N)`；空间 `O(N)`（两个长为 100001 的数组）',
                 '为什么复合顺序对：越晚的操作起点越小，查询从大下标往小下标走，正好按时间先后复合',
                 '本例中 `getIndex(1)` 只经过 `99999` 等节点，不会碰到 `addAll(3)` 存在 `100000` 的标记 → `7×2 = 14`',
                 '原文为 Python 2 写法：只删去了文档字符串和 LeetCode 模板注释；演示中省略了取模行的单独步骤'],
    ),
)
