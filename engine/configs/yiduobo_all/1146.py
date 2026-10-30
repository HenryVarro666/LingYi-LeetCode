def _row(i):
    def fn(S):
        if 'self.s' not in S:
            return '`s[i]`：下标 i 改变过的快照编号；`v[i]`：对应时刻的值' if i == 0 else ''
        return f'下标 {i}：`s[{i}] = {S["self.s"][i]}`　`v[{i}] = {S["self.v"][i]}`'
    return fn


def _bs(S):
    if 'tmp' not in S or 'self.snap_id' not in S:
        return ''
    if 'r' in S and 'l' in S:
        return f'在 `s[index]` 里找 `<= {S["snap_id"]}` 的最右位置：`l = {S["l"]}`，`r = {S["r"]}`'
    return f'`tmp = s[index] = {S["tmp"]}`，查询快照 `{S["snap_id"]}`'


CONFIG = dict(
    num=1146, title='快照数组', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='s / v 两个数组记变化点 + 二分',
    tags=['灵神题单·二分算法', '难度分 1771'],
    code='''
class SnapshotArray(object):

    def __init__(self, length):
        self.s = [[0] for _ in range(length)]
        self.v = [[0] for _ in range(length)]
        self.snap_id = 0

    def set(self, index, val):
        if self.snap_id == self.s[index][-1]:
            self.v[index][-1] = val
        else:
            self.s[index].append(self.snap_id)
            self.v[index].append(val)

    def snap(self):
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        tmp = self.s[index]
        if tmp[-1] <= snap_id:
            return self.v[index][-1]
        else:
            l = 0
            r = len(tmp) - 1
            while l < r:
                mid = (l + r + 1) >> 1
                if tmp[mid] <= snap_id:
                    l = mid
                else:
                    r = mid - 1
            return self.v[index][r]
''',
    call='''a = SnapshotArray(2)
out = []
a.set(0, 5)
out.append(a.snap())
a.set(0, 6)
a.set(0, 7)
out.append(a.snap())
a.set(0, 9)
out.append(a.snap())
out.append(a.get(0, 1))
out.append(a.get(0, 5))
out''',
    expect=[0, 1, 2, 7, 9],
    views=[
        dict(type='text', h=64, size=28, fn=_row(0)),
        dict(type='text', h=64, size=28, fn=_row(1)),
        dict(type='array', var='tmp', label='tmp = s[index]（升序的快照编号）', cell=100, h=260,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r')),
        dict(type='text', h=100, size=28, fn=_bs),
        dict(type='calls', label='正在执行', h=90),
    ],
    watch=[('snap_id', 'self.snap_id', 'blue'), 'index', 'val', 'l', 'r', 'mid'],
    captions={
        'self.s = ': '`s[i]` 记录下标 `i` 在哪些快照编号下改变过，初始 `[0]`',
        'self.snap_id = 0': '全局快照编号 `snap_id` 从 0 开始',
        'self.v = ': '`v[i]` 记录对应时刻的值，和 `s[i]` 一一对应',
        'if self.snap_id == self.s[index][-1]': lambda S, B, ret: (
            f'`snap_id = {S["self.snap_id"]}` 等于 `s[{S.index}][-1] = {S["self.s"][S.index][-1]}`：这个编号已经在记录里 → 直接覆盖'
            if S["self.snap_id"] == S["self.s"][S.index][-1] else
            f'`snap_id = {S["self.snap_id"]}` 不等于 `s[{S.index}][-1] = {S["self.s"][S.index][-1]}`：本轮第一次改 → 追加'),
        'self.v[index][-1] = val': '覆盖：同一编号下多次 `set` 只留最后一次，`v[{index}][-1] = {val}`',
        'self.s[index].append': '记下编号 `{self.snap_id}`',
        'self.v[index].append': '记下值 `{val}`，下标 `{index}` 的变化点又多一个',
        'self.snap_id += 1': '`snap()` 只把全局编号加一：`{B.self.snap_id}` → `{self.snap_id}`',
        'return self.snap_id - 1': '返回加一前的编号 `{ret}`',
        'tmp = self.s[index]': '取出下标 `{index}` 的变化点 `{tmp}`',
        'if tmp[-1] <= snap_id': lambda S, B, ret: (
            f'最后一个变化点 `{S.tmp[-1]} <= {S.snap_id}`：之后没再改过 → 直接取最后一个值'
            if S.tmp[-1] <= S.snap_id else f'最后一个变化点 `{S.tmp[-1]} > {S.snap_id}`：要在中间找，二分'),
        'return self.v[index][-1]': '返回最后一个值 `{ret}`',
        'l = 0': '二分区间 `[0, {len(tmp)-1}]`，找最右的 `tmp[p] <= snap_id`',
        'mid = (l + r + 1) >> 1': '取右中位数 `mid = {mid}`（`l = mid` 的分支必须上取整，否则死循环）',
        'if tmp[mid] <= snap_id': lambda S, B, ret: (
            f'`tmp[{S.mid}] = {S.tmp[S.mid]} <= {S.snap_id}`：mid 可能是答案 → `l = mid`'
            if S.tmp[S.mid] <= S.snap_id else f'`tmp[{S.mid}] = {S.tmp[S.mid]} > {S.snap_id}`：太晚了 → `r = mid - 1`'),
        'l = mid': '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'return self.v[index][r]': '`l = r = {r}`：`s[{index}][{r}] <= snap_id < s[{index}][{r}+1]`，取 `v[{index}][{r}]` = =={ret}=='
    },
    cards=dict(
        one_liner='只存发生变化的位置：s 记快照编号，v 记对应的值',
        complexity='`set`、`snap` 为 `O(1)`，`get` 为 `O(log q)`；空间 `O(n + q)`',
        problem=['`set` 改元素、`snap` 拍快照并返回编号、`get(index, snap_id)` 读历史快照',
                 '长度和操作数都很大，不可能每次 `snap` 都存一份数组',
                 '示例：`set(0,5) snap set(0,6) get(0,0)` → `5`'],
        quote='一个自然的想法就是我们只储存本轮snap之前产生变化的位置和数值，那么我们需要维护两个二维数组s和v，其中s[index]表示下标为index的数产生改变的snap_id组成的list，而v[index]则表示与s[index]中对应snap_id时刻在index上的数值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`set`：若 `s[index][-1]` 就是当前编号，说明本轮改过，直接覆盖 `v`；否则两个数组各追加一项',
              '`snap`：全局编号加一就行',
              '`get`：`s[index][p] <= snap_id < s[index][p+1]` 时，答案就是 `v[index][p]`，在 `s[index]` 里二分'],
        summary=['与灵神对比：灵神把 `(编号, 值)` 全追加后用 `bisect`；yiduobo 同编号只保留一条，手写二分',
                 '初值 `[0]` 保证每个下标至少有一个变化点，不用单独判空',
                 '`l = mid` 配 `mid = (l+r+1)>>1`：区间收缩到一个点时不会死循环',
                 '原文本身是 Python 3 可运行的写法，未做修改'],
    ),
)
