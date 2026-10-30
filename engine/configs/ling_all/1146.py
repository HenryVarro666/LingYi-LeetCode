def _hist(k, v):
    return f'[{k}] ' + ('  '.join(f'({a},{b})' for a, b in v) if v else '（空）')


def _info(S):
    if 'self.cur_snap_id' not in S:
        return '不复制数组：只给每个下标记「在哪个快照编号下改成了什么」'
    return f'当前快照编号 `cur_snap_id = {S["self.cur_snap_id"]}`；每条记录 = (快照编号, 值)，编号==有序=='


CONFIG = dict(
    num=1146, title='快照数组', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='历史修改记录 + 二分',
    tags=['灵神题单·二分算法', '难度分 1771'],
    code='''
class SnapshotArray:
    def __init__(self, _: int):
        self.cur_snap_id = 0
        self.history = defaultdict(list)  # 每个 index 的历史修改记录

    def set(self, index: int, val: int) -> None:
        self.history[index].append((self.cur_snap_id, val))

    def snap(self) -> int:
        self.cur_snap_id += 1
        return self.cur_snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        # 找快照编号 <= snap_id 的最后一次修改记录
        # 等价于找快照编号 >= snap_id+1 的第一个修改记录，它的上一个就是答案
        j = bisect_left(self.history[index], (snap_id + 1,)) - 1
        return self.history[index][j][1] if j >= 0 else 0
''',
    call='''a = SnapshotArray(3)
out = []
a.set(0, 5)
out.append(a.snap())
a.set(0, 6)
a.set(0, 7)
out.append(a.snap())
a.set(1, 4)
out.append(a.snap())
out.append(a.get(0, 1))
out.append(a.get(1, 1))
out.append(a.get(0, 0))
out''',
    expect=[0, 1, 2, 7, 0, 5],
    views=[
        dict(type='text', h=70, size=28, fn=_info),
        dict(type='map', var='self.history', label='history[index]：(快照编号, 值) 的修改记录', fmt=_hist, h=230, font=30),
        dict(type='text', h=110, size=30, fn=lambda S: (
            f'`snap_id + 1 = {S["snap_id"] + 1}`：第一条编号 ≥ {S["snap_id"] + 1} 的记录下标 −1 → `j = {S["j"]}`'
            + (f'，值 ==`{S["self.history"][S["index"]][S["j"]][1]}`==' if S['j'] >= 0 else '，没有记录 → ==0==')
            if 'j' in S and 'snap_id' in S else '')),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('cur_snap_id', 'self.cur_snap_id', 'blue'), 'index', 'val', 'snap_id', ('j', 'j', 'green')],
    captions={
        'self.cur_snap_id = 0': '快照编号从 `0` 开始',
        'self.history = defaultdict(list)': '每个下标一个列表，只记==被改过==的位置，省内存',
        'self.history[index].append': '不改数组：往 `history[{index}]` 末尾追加 `(快照编号 {self.cur_snap_id}, 值 {val})`',
        'self.cur_snap_id += 1': '`snap()` 只把编号加一：`{B.self.cur_snap_id}` → `{self.cur_snap_id}`，O(1)，不复制数组',
        'return self.cur_snap_id - 1': '返回加一前的编号 `{ret}`',
        'j = bisect_left': '二分找第一个编号 `>= {snap_id + 1}` 的记录，减一就是编号 `<= {snap_id}` 的最后一条：`j = {j}`',
        'return self.history[index][j][1]': lambda S, B, ret: (
            f'`j = {S.j}` 有记录 → 取它的值 `{ret}`' if S.j >= 0 else f'`j = {S.j} < 0`：这之前没改过 → 返回初始值 `0`'),
    },
    cards=dict(
        one_liner='不复制数组，只记每个下标的历史修改记录，get 时二分',
        complexity='`set`、`snap` 为 `O(1)`，`get` 为 `O(log q)`；空间 `O(q)`',
        problem=['`set(i, v)` 改元素，`snap()` 拍快照并返回编号，`get(i, id)` 读编号为 `id` 的快照',
                 '数组长度和操作数都到 `50000`，不能每次 `snap` 都复制数组',
                 '示例：`set(0,5) snap set(0,6) get(0,0)` → `5`'],
        quote='能否**不复制数组**呢？换个视角，调用 set(index, val) 时，不去修改数组，而是往 index 的历史修改记录末尾添加一条数据：此时的快照编号和 val。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`snap()` 只让编号加一；`set` 把 `(当前编号, val)` 追加到 `history[index]`',
              '记录里的快照编号==天然有序==，所以 `get` 可以二分',
              '找编号 `<= snap_id` 的最后一条，等价于找编号 `>= snap_id+1` 的第一条再减一'],
        summary=['`get` 用 `bisect_left(记录, (snap_id+1,)) - 1`：元组比较，`(x,)` 比任何 `(x, 值)` 都小',
                 '`j < 0` 说明那个快照之前没改过，返回初始值 `0`',
                 '同一编号下多次 `set` 都会追加，最后一条生效（`bisect` 保证取最后一条）',
                 '同类题：981. 基于时间的键值存储'],
    ),
)
