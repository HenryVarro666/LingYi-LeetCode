_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange', 'yellow', 'red']


def _mem_color(S, i, v):
    if v and v > 0:
        return _COLS[(v - 1) % len(_COLS)]
    return None


def _op_text(S):
    line = S.get('_line', 0)
    if 'size' in S and 'free' in S:
        return f"allocate(size=`{S['size']}`, mID=`{S['mID']}`)：找最左边连续 `{S['size']}` 个 0；已连续空闲 ==`{S['free']}`== 个"
    if 'ans' in S and 'mID' in S:
        return f"freeMemory(mID=`{S['mID']}`)：把等于 `{S['mID']}` 的格子清零，已释放 ==`{S['ans']}`== 个"
    return '内存数组：0 = 空闲，非 0 = 已分配的块 id'


CONFIG = dict(
    num=2502, title='设计内存分配器', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='直接模拟（数组 + 连续 0 计数）',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Allocator:
    def __init__(self, n: int):
        self.memory = [0] * n

    def allocate(self, size: int, mID: int) -> int:
        free = 0
        for i, id in enumerate(self.memory):
            if id > 0:  # 已分配
                free = 0  # 重新计数
                continue
            free += 1
            if free == size:  # 找到了
                self.memory[i - size + 1: i + 1] = [mID] * size
                return i - size + 1
        return -1  # 无法分配内存

    def freeMemory(self, mID: int) -> int:
        ans = 0
        for i, id in enumerate(self.memory):
            if id == mID:
                ans += 1
                self.memory[i] = 0  # 标记为空闲内存
        return ans
''',
    call='''loc = Allocator(6)
res = [loc.allocate(2, 1), loc.allocate(1, 2), loc.allocate(2, 3), loc.freeMemory(1), loc.allocate(3, 4)]
res''',
    expect=[0, 2, 3, 2, -1],
    views=[
        dict(type='text', fn=_op_text, size=26, h=70),
        dict(type='array', var='self.memory', label='memory（颜色 = 块 id，灰 0 = 空闲）', h=300, cell=100,
             pointers={'i': 'blue'},
             window=(lambda S: S['i'] - S['free'] + 1 if 'free' in S and S['free'] > 0 and 'i' in S else None, 'i'),
             color=_mem_color,
             dim=lambda S, i, v: v == 0),
    ],
    watch=['size', 'mID', 'free', 'i', ('id', 'id'), ('ans', 'ans', 'green')],
    skip=['self.memory = [0] * n'],
    max_steps=84,
    captions={
        'for i, id in enumerate': '`i = {i}`，`id = {id}`：逐格检查',
        'if id > 0': '`memory[{i}] = {id}` → ' + '{"已被占用" if id > 0 else "空闲"}',
        'free = 0  #': '遇到已分配的格子，连续空闲被打断 → `free` 清零重新数',
        'free += 1': '这格空闲，连续空闲 `free` → =={free}==',
        'if free == size': lambda S, B, r: (f'`free = {S.free} == size = {S.size}`：找到了，最左边的块是 `[{S.i - S.size + 1}, {S.i}]`'
                                              if S.free == S.size else f'`free = {S.free} < size = {S.size}`：还不够长，继续往右'),
        'self.memory[i - size + 1': '把 `[{i - size + 1}, {i}]` 整段赋值为 `mID = {mID}`',
        'return i - size + 1': '返回块的第一个下标 ==`{i - size + 1}`==；因为从左往右扫，第一个凑够的一定最靠左',
        'return -1': '扫完也没凑够 `size` 个连续空闲 → 返回 ==-1==',
        'ans = 0': '`ans` 统计释放的格子数',
        'if id == mID': lambda S, B, r: (f'`memory[{S.i}] = {S.id}` 等于 `mID = {S.mID}` → 要释放' if S.id == S.mID
                                         else f'`memory[{S.i}] = {S.id}` 不等于 `mID = {S.mID}` → 跳过'),
        'ans += 1': '释放计数 `ans` → {ans}',
        'self.memory[i] = 0': '`memory[{i}]` 置 0，标记为空闲',
        'return ans': '一共释放了 ==`{ans}`== 个格子（同一个 mID 可能分在多块里，都要清）',
    },
    cards=dict(
        one_liner='n 很小：用一个数组直接模拟，找连续的 0',
        complexity='每次操作 `O(n)`，总共 `O(qn)`，空间 `O(n)`',
        problem=['`n` 个内存单元，`allocate(size, mID)` 在最左边找 `size` 个连续空闲格，标上 `mID`，返回起点，找不到返回 `-1`',
                 '`freeMemory(mID)` 释放该 id 的所有格子，返回释放个数',
                 '本视频：`n = 6`，依次 allocate / free 共 5 次操作，最后一次分配不下'],
        quote='可以在遍历 a 的过程中，维护连续为 0 的元素个数 free。遇到非 0 数字就把 free 置为 0，否则把 free 加一。如果遍历到 a[i] 发现 free=size，则要找的区间为 [i-size+1, i]。',
        quote_src='—— 灵茶山艾府题解 · 方法一',
        idea=['初始数组全 0；注意题目保证 `mID > 0`，所以 0 就代表空闲',
              '从左往右数连续的 0，数到 `size` 就收工，起点自然是最左边的',
              '释放：整个数组扫一遍，等于 `mID` 的全部清零并计数'],
        summary=['每次操作 `O(n)`，总时间 `O(qn)`，空间 `O(n)`',
                 '易错：`free == size` 时区间是 `[i-size+1, i]`，别写成 `[i, i+size-1]`',
                 '同一个 `mID` 可以分配多次，释放时必须全部清掉',
                 '题解还给了方法二：Lazy 线段树 + 线段树二分，单次操作 `O(log n)`，数据大时才需要'],
    ),
)
