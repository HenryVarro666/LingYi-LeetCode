# setup 里的 Nums 只是普通 list，额外记下 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
class Nums(list):
    def __init__(self, it):
        super().__init__(it)
        self.live = True
    def __iter__(self):
        return self._walk() if self.live else list.__iter__(self)
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Nums(list.__iter__(self))
        c.__dict__.update(self.__dict__)
        c.live = False
        return c
'''

NUMS = [2, 2, 4, 3, 3, 6, 12]


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    p = getattr(S.get('nums'), 'pos', None)
    return -1 if p is None else p


def _note(S):
    if 'v' not in S or _cur(S) is None:
        if S.get('_line') == 12:
            return '遍历结束，栈里存的就是合并完的数组'
        return '栈里存==已经合并好、位于 v 左边的数组==；v 是正在处理的数'
    v, st = S['v'], S['stack']
    if not st:
        return f'`v = {v}`，栈空：左边没有可合并的数 → 直接压入'
    t = st[-1]
    if t == v:
        return f'`v = {v}` 与栈顶 `{t}` 相等 → 是最左的相等相邻对 → ==合并成 {v + v}=='
    return f'`v = {v}` 与栈顶 `{t}` 不等 → 无法再合并 → 压入'


def _while(S, B, ret):
    v, st = S.v, S.stack
    if not st:
        return f'栈空，`v = {v}` 左边没有数了 → 退出 while'
    if st[-1] == v:
        return f'栈顶 `{st[-1]}` == `v = {v}` → ==相等，要合并=='
    return f'栈顶 `{st[-1]}` ≠ `v = {v}` → 无法再合并，退出 while'


CONFIG = dict(
    num=3834, title='合并相邻且相等的元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 先弹后压，v 翻倍',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1429'],
    code='''
class Solution(object):
    def mergeAdjacent(self, nums):
        
        stack = []
        for v in nums:
            while stack and stack[-1] == v:
                stack.pop()
                v += v
            
            stack.append(v)
        
        return stack
''',
    setup=SETUP,
    call=f'Solution().mergeAdjacent(Nums({NUMS!r}))',
    expect=[8, 24],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在处理的元素，灰 = 已处理）', cell=96, h=190,
             pointers={_cur: 'blue'}, pointer_labels={_cur: '当前'},
             dim=lambda S, i, v: i < _done(S) or (i == _done(S) and _cur(S) is None),
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='stack', var='stack', label='stack（已合并的数组，栈顶在右）', h=160, font=36),
        dict(type='text', fn=_note, size=28, h=110),
    ],
    watch=[('v', 'v', 'blue'), ('stack', 'stack', 'green'), ('栈顶', 'stack[-1] if stack else None', 'orange')],
    captions={
        'stack = []': '用栈存==遍历并合并后得到的数组==，右边的元素暂时不用管',
        'for v in nums': lambda S, B, ret: (f'取下一个数 `v = {S.v}`' if _cur(S) is not None else '`nums` 遍历完毕'),
        'while stack and': _while,
        'stack.pop()': '弹出栈顶 `{B.stack[-1]}`，它和 `v` 合并',
        'v += v': '合并：`v = {B.v} + {B.v} = {v}`，合并后的 v 回头继续和新的栈顶比（对应 nums[p-2]）',
        'stack.append(v)': '`v = {v}` 不能再合并 → 压栈，栈 = `{stack}`',
        'return stack': '栈里储存的就是最终的数组 `{ret}`',
    },
    cards=dict(
        one_liner='合并后的数要先和左边比，比完了才轮到右边：栈顶比 v',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组里有相邻且相等的数，选==最左边==的一对，用它们的和替换，直到没有为止',
                 '示例：`[3,1,1,2]` → `[3,4]`；`[2,2,4]` → `[8]`',
                 '本视频：`[2,2,4,3,3,6,12]` → `[8,24]`'],
        quote='在这二者合并为nums[p] * 2之后，其需要先尝试与nums[p - 2]进行合并，当无法合并时，再继续往后考虑nums[p + 1]以及之后的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['最左一对 `nums[p-1]`、`nums[p]` 合并后，先看能不能和 `nums[p-2]` 合并，再看右边',
              '左边剩下的元素 + 先进后出的合并顺序 → 用栈',
              '遍历到 `v`：栈顶等于 `v` 就弹出、`v` 翻倍，重复；最后压入 `v`'],
        result='最终栈 `[8, 24]`，没有相邻相等的元素 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`：每个数最多进栈、出栈各一次',
                 '`v += v` 改的是循环变量，所以要 ==先比较再压栈==，压栈的是合并后的 `v`',
                 '`while` 先判断 `stack` 非空，再取 `stack[-1]`',
                 '对比灵神写法一：灵神先入栈再用栈顶两个比较，这里是先弹出再压入合并后的值'],
    ),
)
