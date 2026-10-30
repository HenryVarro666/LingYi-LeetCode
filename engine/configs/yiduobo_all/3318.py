def _heaps(S):
    sh, gh = S.get('s_heap'), S.get('g_heap')
    return sh, gh


def _draw_heap(cv, h, x0, y, x1, T, color, title, hl=None):
    cv.text((x0, y), title, 22, color, bold=True)
    if h is None:
        return
    items = list(zip(h.val, h.freq))
    cell = 92
    xs = x0
    yy = y + 40
    if not items:
        cv.text((xs, yy + 14), '（空）', 22, T['dim'])
    for k, (v, f) in enumerate(items):
        top = k == 0
        cv.rect((xs, yy, xs + cell - 8, yy + 60), fill=color, r=8, alpha=210,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + (cell - 8) / 2, yy + 30), f'{v}×{f}', 26, T['bg'], anchor='mm', bold=True)
        cv.text((xs + (cell - 8) / 2, yy + 66), k, 16, T['dim'], anchor='mt', mono=True)
        xs += cell
    cv.text((x1, y), f'和 s = {h.s}', 24, T['text'], anchor='rt', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sh, gh = _heaps(S)
    cv.text((x0 + 18, y0 + 2), '格子 = 值×频率；黄框 = 堆顶；下标是堆数组位置', 20, T['muted'])
    _draw_heap(cv, sh, x0 + 18, y0 + 44, x1 - 18, T, T['green'], '答案堆 s_heap（小顶：频率小的在顶，大小保持 x）')
    _draw_heap(cv, gh, x0 + 18, y0 + 190, x1 - 18, T, T['purple'], '备选堆 g_heap（大顶：频率大的在顶）')
    res = S.get('res')
    if res is not None:
        cv.text((x0 + 18, y0 + 340), '每个窗口的 x-sum：' + ('  '.join(str(r) for r in res) if res else '（还没有）'), 26, T['yellow'], bold=True)


CONFIG = dict(
    num=3318, title='计算子数组的 x-sum I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 + 两个手写堆',
    tags=[],
    code='''
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
        res = "val: {}\\nfreq: {}\\nindex: {}\\ns: {}\\nsize: {}".format(val_str, freq_str, index_str, self.s, self.size)
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
    call='Solution().findXSum([1,1,2,2], 3, 1)',
    expect=[2, 4],
    views=[
        dict(type='array', var='nums', h=240, pointers={'index': 'blue'}, label='nums',
             window=('index - k + 1', 'index')),
        dict(type='custom', draw=_draw, h=400),
    ],
    watch=[('index', 'index', 'blue'), ('s_heap.s', 's_heap.s', 'green'), ('g_heap.s', 'g_heap.s', 'purple'), ('res', 'res', 'yellow')],
    max_steps=140,
    skip=['self.val = []', 'self.freq = []', 'self.index = {}', 'self.s = 0', 'self.size = 0', 'self.cmp_func =',
          'self.root_type = root_type', 'self.size += 1', 'self.index[v] = self.size', 'self.freq.append(f)',
          'self.index[self.val[i]] = i', 'self.index[self.val[j]] = j', 'self.freq[i], self.freq[j]',
          'self.index.pop', 'self.freq.pop()', 'fa = (p - 1) // 2', 'left = p + p + 1', 'right = p + p + 2', 'child = left',
          'p = fa', 'p = child', 'return self.', 'return v in', 'return (None, None)', 'if self.root_type == 0', 'self.size -= 1', 'self.val.pop()', 'p = self.index[v]',
          'if self.size > 0', 'if not self.val', 'if res[0] is None', 'res = self.top()', 'if self.freq[i] == self.freq[j]', 'if p > 0', 'while p > 0', 'while p + p + 1',
          'self.s += v * f', 'self.s -= v', 'self.s -= self.val[-1]', 'return (self.val[0]', 106, 'self.up(self.index', 'self.down(self.index', 'self.swap(', 'self.down(0)', 'self.freq[self.index[v]] -= 1'],
    captions={
        'self.s += v * f': '堆内数值之和加上 `{v}×{f}`：`s = {self.s}`',
        'self.val.append(v)': '`{v}` 是新数 → 放到堆数组末尾（频率 {f}），再从末尾上移；堆内和 `s = {self.s}`',
        'self.freq[self.index[v]] += f': '`{v}` 已在这个堆里 → 频率 +{f}（和 `s = {self.s}`），小顶堆里频率变大要下沉、大顶堆要上移',
        'self.up(self.index[v])': '新节点从末尾向上调整',
        'self.down(self.index[v])': '小顶堆里频率变大了 → 往下沉',
        'self.up(self.index[v])\n': '',
        'self.s -= v': '`s` 减去 `{v}`',
        'self.freq[self.index[v]] -= 1': '`{v}` 的频率减 1',
        'if self.freq[self.index[v]] == 0': lambda S, B, r: (f'频率降到 0 → `{S.v}` 要从堆里删掉' if S.freq[S.index[S.v]] == 0 else f'`{S.v}` 频率还剩 `{S.freq[S.index[S.v]]}`，只调整堆序') if S.v in S.index else '',
        'self.swap(self.size - 1, p)': '把要删的节点和末尾节点交换，再弹出末尾',
        'self.val[i], self.val[j]': '交换堆数组的两个位置（值和频率一起换）',
        'if self.cmp_func[self.root_type](p, fa)': '和父节点比：谁更该靠近堆顶？（小顶堆频率小的在上，大顶堆频率大的在上，同频比数值）',
        'if self.cmp_func[self.root_type](child, p)': '和孩子比：孩子更该靠近堆顶吗？（规则同上）',
        'self.swap(fa, p)': '更该靠近堆顶 → 和父节点交换',
        'self.swap(child, p)': '孩子更该靠近堆顶 → 和孩子交换',
        'self.swap(self.size - 1, 0)': '弹出堆顶：先和末尾交换，再删掉末尾',
        'self.s -= self.val[-1] * self.freq[-1]': '`s` 减去被弹出的 `{self.val[-1]}×{self.freq[-1]}`',
        'self.down(0)': '换到堆顶的节点向下调整',
        's_heap = HeapWithFreq(0)': '答案堆：小顶堆，大小要保持 `x`（频率小的在顶）',
        'g_heap = HeapWithFreq(1)': '备选堆：大顶堆，频率大的在顶',
        'for index in range(k)': '先把前 k 个数全放进答案堆',
        's_heap.insert(nums[index])\n': '',
        'while s_heap.get_size() > x': '答案堆多于 `x` 种 → 把最弱的堆顶弹出，放进备选堆',
        'sv, sf = s_heap.pop()': '弹出答案堆顶 `{sv}×{sf}`（最弱的一种）',
        'g_heap.insert(sv, sf)': '放进备选堆',
        'res = [s_heap.get_sum()]': '第一个窗口的 x-sum = `{res[0]}`',
        'for index in range(k, len(nums))': lambda S, B, r: ('窗口都滑完了' if len(S.res) == len(S.nums) - S.k + 1 else f'窗口右移：新进 `nums[{S.index}] = {S.nums[S.index]}`，旧出 `nums[{S.index - S.k}] = {S.nums[S.index - S.k]}`'),
        'if g_heap.contained(nums[index])': '新数 `{nums[index]}` 已经在备选堆里吗？是就更新那边，否则先放答案堆',
        'g_heap.insert(nums[index])': '新数 `{nums[index]}` 在备选堆里 → 那边频率 +1',
        's_heap.insert(nums[index])': '新数 `{nums[index]}` 放进答案堆',
        'if s_heap.contained(nums[index - k])': '要移出窗口的 `{nums[index - k]}` 在答案堆吗？',
        's_heap.delete(nums[index - k])': '在答案堆 → 那边频率 -1',
        'g_heap.delete(nums[index - k])': '在备选堆 → 那边频率 -1',
        'if s_heap.get_size() > x': lambda S, B, r: f'答案堆有 `{S.s_heap.get_size()}` 种，x = `{S.x}`：' + ('多了 → 弹出最弱的放备选' if S.s_heap.get_size() > S.x else '没多'),
        'if s_heap.get_size() < x and': lambda S, B, r: f'答案堆 `{S.s_heap.get_size()}` 种 < x = `{S.x}`？{S.s_heap.get_size() < S.x}；备选堆非空？{S.g_heap.get_size() > 0}' + ('：从备选堆补一个最强的' if S.s_heap.get_size() < S.x and S.g_heap.get_size() > 0 else ''),
        'gv, gf = g_heap.pop()': '弹出备选堆顶 `{gv}×{gf}`（场外最强）',
        's_heap.insert(gv, gf)': '放进答案堆',
        'if g_heap.get_size() > 0:': '备选堆非空 → 还要比较两个堆顶，看是否该换位',
        'sv, sf = s_heap.top()': '取答案堆顶：答案堆里最弱的一种',
        'gv, gf = g_heap.top()': '取备选堆顶：场外最强的一种',
        'if sf < gf or': lambda S, B, r: (f'答案堆顶 `{S.sv}×{S.sf}` vs 备选堆顶 `{S.gv}×{S.gf}`：' + ('场外的更强（频率更大，或同频值更大）→ ==交换两个堆顶==' if (S.sf < S.gf or (S.sf == S.gf and S.sv < S.gv)) else '答案堆顶不弱于场外 → 不用换')),
        's_heap.pop()\n': '',
        'res.append(s_heap.get_sum())': '这个窗口的 x-sum = `{s_heap.get_sum()}`',
        169: '全部窗口的 x-sum：`{res}`',
    },
    cards=dict(
        one_liner='两个堆：一个存前 x 名，一个存其余，窗口滑动时在两堆之间搬',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['数组 `nums`，每个长为 `k` 的窗口只保留出现频率最高的前 `x` 种数（频率相同取值大的），求它们的和',
                 '示例：`[1,1,2,2,3,4,2,3], k=6, x=2` → `[6,10,12]`',
                 '本视频：`[1,1,2,2], k=3, x=1` → `[2,4]`'],
        quote='其中一个堆大小为x，其中储存的是频率最大的x种元素以及对应的频率，这个堆为小顶堆；另一个堆中则储存滑动窗口内其他的元素以及对应的频率，这个堆为大顶堆。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案堆（小顶）放前 x 名，堆顶是其中最弱的；备选堆（大顶）堆顶是场外最强的',
              '窗口滑动：新数频率 +1，旧数频率 -1，再把两堆的数量和堆顶==校正==回来',
              '为了能删除任意元素，手写堆并用 `index` 哈希表记住每个数在堆数组里的位置'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '易错：频率相同时比数值，`lt`/`gt` 要先比频率再比值',
                 '易错：`delete` 频率减到 0 要把该节点与末尾交换再弹出，交换后==上移下移都要试==',
                 '原文已是 Python 3 可运行写法，代码未做修改；`__str__` 仅调试用，不会被调用'],
    ),
)
