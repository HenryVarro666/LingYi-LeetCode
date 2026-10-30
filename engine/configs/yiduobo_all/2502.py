_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange', 'yellow', 'red']


def _mem_color(S, i, v):
    if v and v > 0:
        return _COLS[(v - 1) % len(_COLS)]
    return None


def _op_text(S):
    if 'left' in S and 'right' in S and 'size' in S:
        return f"allocate(size=`{S['size']}`, mID=`{S['mID']}`)：起点 left=`{S['left']}`，空闲段到 right=`{S['right']}`，长度 ==`{S['right'] - S['left']}`=="
    if 'left' in S and 'size' in S:
        return f"allocate(size=`{S['size']}`, mID=`{S['mID']}`)：先找一个空闲的起点 left=`{S['left']}`"
    if 'cnt' in S and 'mID' in S:
        return f"free(mID=`{S['mID']}`)：扫一趟，已释放 ==`{S['cnt']}`== 个"
    return '内存数组：0 = 空闲，非 0 = 已分配的块 id'


CONFIG = dict(
    num=2502, title='设计内存分配器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力枚举起点 + 向右延伸',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Allocator(object):

    def __init__(self, n):
        self.n = n
        self.mem = [0] * n

    def allocate(self, size, mID):
        left = 0
        while left < self.n:
            while left < self.n and self.mem[left] != 0:
                left += 1
            if left == self.n:
                break
            
            right = left + 1
            while right < self.n and right - left < size and self.mem[right] == 0:
                right += 1
            
            if right - left >= size:
                for index in range(left, right):
                    self.mem[index] = mID
                return left
            
            left = right
        
        return -1

    def free(self, mID):
        cnt = 0
        for index in range(self.n):
            if self.mem[index] == mID:
                self.mem[index] = 0
                cnt += 1
        
        return cnt
''',
    call='''loc = Allocator(6)
res = [loc.allocate(2, 1), loc.allocate(1, 2), loc.allocate(2, 3), loc.free(1), loc.allocate(3, 4)]
res''',
    expect=[0, 2, 3, 2, -1],
    views=[
        dict(type='text', fn=_op_text, size=26, h=70),
        dict(type='array', var='self.mem', label='mem（颜色 = 块 id，灰 0 = 空闲）', h=300, cell=100,
             pointers={'left': 'blue', 'right': 'pink'},
             window=('left', lambda S: S['right'] - 1 if 'right' in S and S['right'] > S['left'] else None),
             color=_mem_color,
             dim=lambda S, i, v: v == 0),
    ],
    watch=['size', 'mID', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cnt', 'cnt', 'green')],
    skip=['self.n = n', 'self.mem = [0] * n'],
    max_steps=76,
    captions={
        'left = 0': '从下标 `0` 开始，枚举分配区间的起点 `left`',
        'while left < self.n:': '`left = {left}`，还没越界，继续找起点',
        'while left < self.n and self.mem[left] != 0': lambda S, B, r: (f'`mem[{S.left}] = {S.self.mem[S.left]}` 已被占用 → 起点不能放这里' if S.left < S.self.n and S.self.mem[S.left] != 0
                                                                      else f'`left = {S.left}` 是空闲格，可以当起点'),
        'left += 1': '跳过已占用的格子，`left` → {left}',
        'if left == self.n': lambda S, B, r: ('`left` 走到了末尾：后面没有空闲格了 → 跳出循环' if S.left == S.self.n else f'`left = {S.left}` 还在范围内，继续'),
        'break': '没有空闲起点了，退出去返回 -1',
        'right = left + 1': '从 `left` 往右延伸，先让 `right = {right}`',
        'while right < self.n and right - left < size': lambda S, B, r: (
            f'空闲段长度 `{S.right - S.left}` 已够 `size = {S.size}`，或者撞到了边界/已占用的格子 → 停下'
            if not (S.right < S.self.n and S.right - S.left < S.size and S.self.mem[S.right] == 0)
            else f'`mem[{S.right}] = 0` 且长度 `{S.right - S.left} < {S.size}` → 继续延伸'),
        'right += 1': '空闲段又长了一格，`right` → {right}',
        'if right - left >= size': lambda S, B, r: (f'空闲段 `[{S.left}, {S.right})` 长 `{S.right - S.left} >= size = {S.size}` → 够用，就从 `left` 开始分配'
                                                    if S.right - S.left >= S.size else f'空闲段只有 `{S.right - S.left}` 个，不够 `{S.size}` → 放弃这一段'),
        'for index in range(left, right)': '把 `[{left}, {right})` 逐格赋值',
        'self.mem[index] = mID': '`mem[{index}] = {mID}`',
        'return left': '返回起点 ==`{left}`==：从左往右找，所以第一个够长的就是最左侧',
        'left = right': '这一段不够长，`left` 直接跳到 `right = {right}`（中间的格子都空闲但凑不够，不用再试）',
        'return -1': '所有起点都试过了，找不到 → ==-1==',
        'cnt = 0': '`cnt` 统计释放的格子数',
        'for index in range(self.n)': '`index = {index}`：扫描每个格子',
        'if self.mem[index] == mID': lambda S, B, r: (f'`mem[{S.index}] = {S.self.mem[S.index]}` 等于 `mID = {S.mID}` → 要释放' if S.self.mem[S.index] == S.mID
                                                     else f'`mem[{S.index}] = {S.self.mem[S.index]}` 不等于 `mID = {S.mID}` → 跳过'),
        'self.mem[index] = 0': '`mem[{index}]` 重新置 0',
        'cnt += 1': '释放计数 `cnt` → {cnt}',
        'return cnt': '一共释放 ==`{cnt}`== 个位置（不管分在几块里）',
    },
    cards=dict(
        one_liner='数据规模小，直接暴力：枚举起点，向右数空闲格',
        complexity='每次操作 `O(n)`，总共 `O(qn)`，空间 `O(n)`',
        problem=['`n` 个内存单元，`allocate(size, mID)` 在最左边找 `size` 个连续空闲格并标上 `mID`，返回起点，没有返回 `-1`',
                 '`free(mID)` 释放该 id 的所有格子，返回个数（视频里把 `freeMemory` 简写成 `free`，与原文一致）',
                 '本视频：`n = 6`，共 5 次操作'],
        quote='对于分配操作，从头部开始遍历分配区间的起点left，找出从left开始的连续空闲内存的终点right。若left到right之间空闲的位置大于等于申请的大小size，那么就从left开始划分size的空间给mID并返回left。',
        quote_src='—— yiduobo 题解原文',
        idea=['先跳过已占用的格子，找到一个空闲起点 `left`',
              '再向右延伸 `right`，直到凑够 `size` 或者碰到障碍',
              '不够长就让 `left = right` 换下一个起点；释放操作只需一趟遍历'],
        summary=['时间：每次操作 `O(n)`，空间 `O(n)`',
                 '延伸停止有三种情况：到末尾、遇到已占用格、长度已够 `size`',
                 '`left = right`：失败后直接跳到障碍位置，避免重复扫描',
                 '原文就是 Python 3 可运行的写法，仅 `class Allocator(object)` 为旧式写法，未改动',
                 '对比灵神：灵神一次遍历维护连续 0 的个数 `free`，yiduobo 枚举起点再向右延伸'],
    ),
)
