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

NUMS = [4, 2, 2, 1, 1, 2, 4, 3]


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return -1 if p is None else p


def _note(S):
    st = S.get('st')
    if st is None:
        return '从左到右扫：栈 = ==左侧还没被合并走的元素==，栈顶就是“左侧剩余最近元素”'
    if len(st) > 1 and st[-1] == st[-2]:
        return f'栈顶两个都是 `{st[-1]}` → 相邻相等 → ==合并成 {2 * st[-1]}=='
    return '栈里相邻元素各不相同 ✓，新元素只需要和==栈顶==比'


def _while(S, B, ret):
    st = S.st
    if len(st) <= 1:
        return '栈里只有 1 个元素，没有可比的左邻居 → 本轮合并结束'
    if st[-1] == st[-2]:
        return f'栈顶两个 `{st[-1]}` == `{st[-2]}` → ==要合并==（合并后可能又和左边相等，所以用 while）'
    return f'栈顶 `{st[-1]}` ≠ 左邻 `{st[-2]}` → 本轮合并结束，处理下一个元素'


CONFIG = dict(
    num=3834, title='合并相邻且相等的元素', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 先入栈再合并',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1429'],
    code='''
class Solution:
    def mergeAdjacent(self, nums: List[int]) -> List[int]:
        st = []
        for x in nums:
            st.append(x)
            while len(st) > 1 and st[-1] == st[-2]:
                st.pop()
                st[-1] *= 2
        return st
''',
    setup=SETUP,
    call=f'Solution().mergeAdjacent(Nums({NUMS!r}))',
    expect=[16, 3],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 x，灰 = 已处理）', cell=96, h=190,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'x'},
             dim=lambda S, i, v: i < _done(S) or (i == _done(S) and _cur(S) is None),
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='stack', var='st', label='st（栈顶在右）', h=160, font=36),
        dict(type='text', fn=_note, size=28, h=110),
    ],
    watch=[('x', 'x', 'blue'), ('st', 'st', 'green'), ('len(st)', 'len(st)', 'purple')],
    captions={
        'st = []': '栈里放“左侧剩余的元素”，栈顶就是离新元素最近的那个',
        'for x in nums': lambda S, B, ret: (f'取下一个元素 `x = {S.x}`' if _cur(S) is not None else '`nums` 遍历完毕'),
        'st.append(x)': '`{x}` 先入栈：栈 = `{st}`',
        'while len(st) > 1': _while,
        'st.pop()': '弹出栈顶 `{B.st[-1]}`（相等的那一对里右边的）',
        'st[-1] *= 2': '左边的翻倍：`{B.st[-1]} × 2 = {st[-1]}`（就是两数之和）；它可能又和更左边的相等，回去再比',
        'return st': '全部合并完，返回栈 `{ret}`',
    },
    cards=dict(
        one_liner='每次都合并最左边的一对 = 从左到右扫，用栈接住“左侧剩余最近元素”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有相邻相等的元素，就取==最左边==那一对，换成它们的和；重复到没有相邻相等为止',
                 '示例：`[3,1,1,2]` → `[3,4]`；`[2,2,4]` → `[8]`',
                 '本视频：`[4,2,2,1,1,2,4,3]` → `[16,3]`（会连环合并）'],
        quote='一旦发现 nums[i] 和左侧剩余最近元素相等，就执行合并操作。如果合并后，新元素与左侧剩余最近元素相等，就继续执行合并操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最左边的一对先合并 → 从左到右处理，左边永远已经“稳定”',
              '要频繁看、删“左侧剩余最近元素” → 后进先出的数据结构：栈',
              '写法一：先把 `x` 入栈，只要栈顶两个相等就弹出一个、另一个翻倍'],
        result='最终栈 `[16, 3]`，没有相邻相等的元素 ✓',
        summary=['时间 `O(n)`：虽然是二重循环，但每个元素最多入栈、出栈各一次',
                 '易错：合并后的新元素可能又和左边相等 → 必须用 ==while==，不能用 if',
                 '易错：`len(st) > 1` 在前，栈里只有一个元素时不能访问 `st[-2]`',
                 '写法二是“先出栈再入栈”：`while st and st[-1] == x: st.pop(); x *= 2`，最后再 `append(x)`',
                 '邻项消除类型题（栈）：20、1047、1209 等'],
    ),
)
