
def _pairs(S, name):
    h = S.get(name)
    if h is None:
        return []
    try:
        return list(zip(h.val, h.freq))
    except Exception:
        return []


def _fmt(p):
    return f'{p[0]}×{p[1]}'


def _txt(S):
    if 's_heap' not in S:
        return 's_heap 小顶堆：存前 x 种（按 次数、值 比），堆顶最弱；g_heap 大顶堆：存其余，堆顶最强'
    a, b = S['s_heap'], S['g_heap']
    return f'`s_heap` {a.size} 种，和 `{a.s}`　`g_heap` {b.size} 种　（格子 = 值×次数）'


CONFIG = dict(
    num=3321, title='计算子数组的 x-sum II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='滑动窗口 · 手写带频率的可删除堆',
    tags=['常用数据结构', '难度分 2598'],
    code=r'''

class HeapWithFreq(object):
    def __init__(self, root_type = 0):
        self.val = []
        self.freq = []
        self.index = {}
        self.s = 0
        self.size = 0
        self.cmp_func = [self.lt, self.gt]
        self.root_type = root_type

    def insert(self, v, f=1):
        self.s += v * f
        if v not in self.index:
            self.index[v] = self.size
            self.size += 1
            self.val.append(v)
            self.freq.append(f)
            self.up(self.index[v])
        else:
            self.freq[self.index[v]] += f
            if self.root_type == 0:
                self.down(self.index[v])
            else:
                self.up(self.index[v])
    
    def delete(self, v):
        self.s -= v
        self.freq[self.index[v]] -= 1
        if self.freq[self.index[v]] == 0:
            p = self.index[v]
            self.swap(self.size - 1, p)
            self.size -= 1
            self.index.pop(v)
            self.val.pop()
            self.freq.pop()
            if p < self.size:
                self.down(p)
                self.up(p)
        else:
            if self.root_type == 0:
                self.up(self.index[v])
            else:
                self.down(self.index[v])

    def swap(self, i, j):
        self.val[i], self.val[j] = self.val[j], self.val[i]
        self.freq[i], self.freq[j] = self.freq[j], self.freq[i]
        self.index[self.val[i]] = i
        self.index[self.val[j]] = j

    def lt(self, i, j):
        if self.freq[i] == self.freq[j]:
            return self.val[i] < self.val[j]
        return self.freq[i] < self.freq[j]
    
    def gt(self, i, j):
        if self.freq[i] == self.freq[j]:
            return self.val[i] > self.val[j]
        return self.freq[i] > self.freq[j]

    def up(self, p):
        while p > 0:
            fa = (p - 1) // 2
            if self.cmp_func[self.root_type](p, fa):
                self.swap(fa, p)
                p = fa
            else:
                break

    def down(self, p):
        while p + p + 1 < self.size:
            left = p + p + 1
            right = p + p + 2

            child = left
            if right < self.size and self.cmp_func[self.root_type](right, left):
                child = right
            
            if self.cmp_func[self.root_type](child, p):
                self.swap(child, p)
                p = child
            else:
                break
    
    def top(self):
        if not self.val:
            return (None, None)
        return (self.val[0], self.freq[0])
    
    def pop(self):
        res = self.top()
        if res[0] is None:
            return res

        self.swap(self.size - 1, 0)
        self.size -= 1
        self.s -= self.val[-1] * self.freq[-1]

        self.index.pop(self.val[-1])
        self.val.pop()
        self.freq.pop()

        if self.size > 0:
            self.down(0)
        
        return res

    def get_size(self):
        return self.size
    
    def get_sum(self):
        return self.s

    def contained(self, v):
        return v in self.index

    def __str__(self):
        val_str = ', '.join([str(x) for x in self.val])
        freq_str = ', '.join([str(x) for x in self.freq])
        index_str = ', '.join(["{}: {}".format(key, value) for key, value in self.index.items()])
        res = "val: {}\nfreq: {}\nindex: {}\ns: {}\nsize: {}".format(val_str, freq_str, index_str, self.s, self.size)
        return res

class Solution(object):
    def findXSum(self, nums, k, x):
        
        s_heap = HeapWithFreq(0)
        g_heap = HeapWithFreq(1)

        for index in range(k):
            s_heap.insert(nums[index])

        while s_heap.get_size() > x:
            sv, sf = s_heap.pop()
            g_heap.insert(sv, sf)

        res = [s_heap.get_sum()]

        for index in range(k, len(nums)):
            if g_heap.contained(nums[index]):
                g_heap.insert(nums[index])
            else:
                s_heap.insert(nums[index])

            if s_heap.contained(nums[index - k]):
                s_heap.delete(nums[index - k])
            else:
                g_heap.delete(nums[index - k])

            if s_heap.get_size() > x:
                sv, sf = s_heap.pop()
                g_heap.insert(sv, sf)
            
            if s_heap.get_size() < x and g_heap.get_size() > 0:
                gv, gf = g_heap.pop()
                s_heap.insert(gv, gf)

            if g_heap.get_size() > 0:    
                sv, sf = s_heap.top()
                gv, gf = g_heap.top()
                if sf < gf or (sf == gf and sv < gv):
                    s_heap.pop()
                    s_heap.insert(gv, gf)
                    g_heap.pop()
                    g_heap.insert(sv, sf)

            res.append(s_heap.get_sum())
    
        return res
''',
    call='Solution().findXSum([1,1,2,3], 3, 2)',
    expect=[4, 5],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口）', h=215,
             pointers={'index': 'blue'},
             window=(lambda S: max(0, S['index'] - 3 + 1) if 'index' in S else None, 'index')),
        dict(type='queue', var=lambda S: _pairs(S, 's_heap'), label='s_heap 前 x 种（值×次数）', fmt=_fmt, h=105),
        dict(type='queue', var=lambda S: _pairs(S, 'g_heap'), label='g_heap 其余', fmt=_fmt, h=105),
        dict(type='array', var='res', label='res', h=150),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'orange'), ('f', 'f', 'orange'), ('p', 'p', 'pink')],
    skip=['self.val = []', 'self.freq = []', 'self.index = {}', 'self.s = 0', 'self.size = 0', 'self.cmp_func =', 'self.root_type = root_type', 'self.val[i], self.val[j]', 'self.freq[i], self.freq[j]', 'self.index[self.val[i]]', 'self.index[self.val[j]]', 'self.index[v] = self.size', 'self.size += 1', 'self.val.append(v)', 'self.freq.append(f)', 'if self.freq[i] == self.freq[j]', 'return self.val[i] <', 'return self.freq[i] <', 'return self.val[i] >', 'return self.freq[i] >', 'fa = (p', 'left = p + p', 'right = p + p', 'child = left', 'return self.size', 'return self.s', 'return v in self.index', 'return (self.val[0]', 'self.s += v * f', 'self.index.pop(', 'self.val.pop()', 'self.freq.pop()', 'if not self.val', 'if res[0] is None', 'for index in range(k)', 'p = fa', 'p = child', 'sv, sf = s_heap.top()', 'gv, gf = g_heap.top()', 'return res'],
    captions={
        127: '`s_heap`：小顶堆，存前 x 种（堆顶 = 其中最弱的）',
        128: '`g_heap`：大顶堆，存其余种类（堆顶 = 其中最强的）',
        131: '先把窗口前 `k` 个数放进 `s_heap`：`{nums[index]}`，频率 1',
        13: lambda S, B, r: (f'`{S.v}` 不在堆里 → 新增节点' if S.v not in S.self.index else f'`{S.v}` 已在堆里 → 只加频率'),
        18: '新节点放到末尾，向上调整（`up`）',
        20: '频率 `+{f}`，不用新增节点',
        21: '小顶堆里频率变大 → 要下沉（大顶堆则上浮）',
        22: '`down`：和孩子比较强弱',
        62: lambda S, B, r: ('到根节点了，调整结束' if S.p <= 0 else '有父节点：比较强弱'),
        64: '比较强弱：先比频率，频率相同比数值',
        65: '比父节点更弱 → 交换，==同时更新 `index` 里的位置==',
        68: '不比父节点更弱，停止上浮',
        71: lambda S, B, r: ('没有孩子了，调整结束' if not (S.p + S.p + 1 < S.self.size) else '有孩子：选更弱的那个比较'),
        76: '选出两个孩子里更弱的 `child`',
        79: '`child` 比 `p` 更弱吗？',
        80: '更弱 → 交换，继续下沉',
        133: lambda S, B, r: (f'`s_heap` 有 {S.s_heap.size} 种，超过 x={S.x} → 把堆顶挪去 g_heap' if S.s_heap.size > S.x else f'`s_heap` 有 {S.s_heap.size} 种，已经不超过 x={S.x}，不用挪'),
        137: '第一个窗口的 x-sum = `s_heap.s` = =={s_heap.s}==',
        139: lambda S, B, r: ('遍历结束' if S.index == len(S.nums) - 1 and B.get('index') == S.index else f'窗口右移：`nums[{S.index}] = {S.nums[S.index]}` 进入，`nums[{S.index - S.k}] = {S.nums[S.index - S.k]}` 离开'),
        140: '新数在 `g_heap` 里吗？在就累加频率，否则放进 `s_heap`',
        143: '不在 `g_heap` → 放进 `s_heap`',
        145: '离开的数在 `s_heap` 里吗？',
        146: '在 `s_heap` → 删一次（频率 −1）',
        27: '`s` 先减去 `{v}`',
        28: '频率减一',
        29: '频率变成 0 才删节点；否则只要调整位置',
        40: '小顶堆里频率变小 → 要上浮（大顶堆则下沉）',
        41: '`up`',
        150: lambda S, B, r: ('`s_heap` 超过 x 种 → 弹出最弱的挪去 g_heap' if S.s_heap.size > S.x else f'`s_heap` 有 {S.s_heap.size} 种，不超过 x'),
        151: '弹出 `s_heap` 的堆顶（最弱的一种）',
        91: '先取出堆顶',
        95: '堆顶与末尾交换，再删掉末尾',
        96: '大小减一',
        97: '`s` 减去被弹走的 值×频率',
        104: '对交换上来的新堆顶 `down`',
        152: '弹出的这一种放进 `g_heap`',
        154: lambda S, B, r: ('`s_heap` 不足 x 种且 g_heap 非空 → 补一个' if (S.s_heap.size < S.x and S.g_heap.size > 0) else '`s_heap` 已有 x 种，不用补'),
        158: '`g_heap` 非空：比较两个堆顶谁更强',
        161: lambda S, B, r: (f'`s_heap` 堆顶 {S.sv}×{S.sf} 比 `g_heap` 堆顶 {S.gv}×{S.gf} 更弱 → 交换两个堆顶' if (S.sf < S.gf or (S.sf == S.gf and S.sv < S.gv)) else f'`s_heap` 堆顶 {S.sv}×{S.sf} 不弱于 `g_heap` 堆顶 {S.gv}×{S.gf} → 不换'),
        167: '本窗口 x-sum = `s_heap.s` = =={s_heap.s}==',
        169: '所有窗口的 x-sum：`{res}`',
    },
    max_steps=140,
    cards=dict(
        one_liner='自己写一个「带频率、能删任意元素」的堆，两个堆对顶',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['窗口内每种数按出现次数排序，次数相同数值大的优先，保留前 `x` 种求和',
                 '对每个长为 `k` 的子数组求 x-sum',
                 '本视频：`[1,1,2,3]`，`k=3`，`x=2` → `[4,5]`'],
        quote='其中一个堆大小为x，其中储存的是频率最大的x种元素以及对应的频率，这个堆为小顶堆，其中元素与频率乘积累加起来就是当前窗口的x-sum；另一个堆中则储存滑动窗口内其他的元素以及对应的频率，这个堆为大顶堆。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s_heap`（小顶堆）存前 `x` 种 `(值, 频率)`，`s` 记 值×频率 之和；`g_heap`（大顶堆）存其余',
              '窗口滑动时频率会变，延迟删除不好用 → ==手写堆，用 `index` 哈希表记录每个值的位置，随时删==',
              '每步先入后出，再按大小和堆顶强弱做挪动、交换'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '易错点：频率变化后要上移或下移（小顶堆与大顶堆方向相反）；删除节点要先与末尾交换',
                 '比较规则：先比频率，频率相同比数值 `val`',
                 '原文本身可在 Python 3 运行（已使用 `//`），未做修改',
                 '对照灵神：灵神用 SortedList 对顶，这里要手写堆才能删任意位置'],
    ),
)
