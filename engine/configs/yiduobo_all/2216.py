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

NUMS = [1, 1, 2, 2, 3, 3, 3]


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _sim(S):
    """(配好的对, 等配对的下标, 被删除的下标集合, 当前下标是否已有结论)——只用于画图"""
    nums = S['nums']
    p = getattr(nums, 'pos', None)
    if p is None:
        return [], None, set(), False
    line = S.get('_line', 0)
    c = _cur(S)
    m = len(nums) if c is None else (c + 1 if line in (8, 10, 12, 13) else c)
    first, pairs, dele = None, [], set()
    for i in range(m):
        if first is None:
            first = i
        elif nums[first] == nums[i]:
            dele.add(i)
        else:
            pairs.append((first, i))
            first = None
    return pairs, first, dele, (c is None or m > c)


def _color(S, i, v):
    if 'nums' not in S or getattr(S['nums'], 'pos', None) is None:
        return None
    pairs, first, dele, decided = _sim(S)
    if i in dele:
        return 'red'
    if any(i in pr for pr in pairs):
        return 'green'
    if i == first:
        return 'orange'
    if i == _cur(S) and not decided:
        return 'blue'
    return None


def _kept(S):
    if getattr(S.get('nums'), 'pos', None) is None:
        return []
    return [S['nums'][i] for pr in _sim(S)[0] for i in pr]


def _note(S):
    if 'first' not in S:
        return '美丽数组 = 两两一对，每对两个数不相等；一趟扫描，用 `first` 记住“还在等搭档的左元素”'
    pairs, first, dele, _ = _sim(S)
    n = len(S['nums'])
    if _cur(S) is None and S.get('_line') == 15:
        tail = f'；落单的 `{S["nums"][first]}` 也要删' if first is not None else ''
        return f'`res = {n} − 2×{len(pairs)} = {S["res"]}`{tail}'
    f = 'None（下一个数当左元素）' if S['first'] is None else f"{S['first']}（等不同的数来配）"
    return f'`first = {f}`；已配成 {len(pairs)} 对，已删除 {len(dele)} 个'


def _if(S, B, ret):
    if S.first is None:
        return f'`first is None`：现在是偶数位，`{S.num}` 可以当左元素'
    return f'`first = {S.first}` 不是 None：已经有左元素了，`{S.num}` 要当右元素，先看看它们相不相等'


def _elif(S, B, ret):
    if S.first == S.num:
        return f'`first = {S.first}` == `num = {S.num}`：左右相等，不能成对 → ==删掉这个 {S.num}=='
    return f'`first = {S.first}` ≠ `num = {S.num}` → ==可以配成一对=='


def _none(S, B, ret):
    if S['_line'] == 4:
        return '`first` 记左元素；`None` = 现在轮到偶数位，下一个数可以随便放'
    return '这一对配好了，`first` 清空 → 下一个数又当新一对的左元素'


def _ret(S, B, ret):
    if S.first is not None:
        return f'遍历完，`first = {S.first}` 还落单 → 它要删，`len − 2×对数` 已经把它算进去了 → 返回 =={ret}=='
    return f'没有落单的数 → 返回 =={ret}=='


CONFIG = dict(
    num=2216, title='美化数组的最少删除数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 · 一趟遍历配对',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1510'],
    code='''
class Solution(object):
    def minDeletion(self, nums):

        first = None
        res = len(nums)
        for num in nums:
            if first is None:
                first = num
            elif first == num:
                continue
            else:
                res -= 2
                first = None
        
        return res
''',
    setup=SETUP,
    call=f'Solution().minDeletion(Nums({NUMS!r}))',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前；橙 = 等搭档的左元素；绿 = 已配成对；红 = 删掉）', cell=100, h=210,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'num'}, color=_color),
        dict(type='array', var=_kept, label='已配成对、保留下来的数（每 2 个一对，两数必须不同）', cell=100, h=170, index=False,
             color=lambda S, i, v: 'green'),
        dict(type='text', fn=_note, size=28, h=130),
    ],
    watch=[('num', 'num', 'blue'), ('first', 'first', 'orange'), ('res', 'res', 'green')],
    captions={
        'first = None': _none,
        'res = len(nums)': '`res` 先假设==全删==：`res = {res}`；每配成一对，就少删 2 个',
        'for num in nums': lambda S, B, ret: (f'取下一个数 `num = {S.num}`' if _cur(S) is not None else '`nums` 遍历完毕'),
        'if first is None': _if,
        'first = num': '`{num}` 做左元素，`first = {first}`，等一个不同的数来配对',
        'elif first == num': _elif,
        'continue': '删掉这个数，`first` ==不变==：继续等一个和 `first` 不同的数',
        'res -= 2': '配成一对 `({first}, {num})`，这两个都不用删 → `res = {res}`',
        'return res': _ret,
    },
    cards=dict(
        one_liner='贪心一趟遍历：遇到相同的数就删一个，不同的就配成一对',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['美丽数组：长度为偶数，且每一对 `nums[2i]`、`nums[2i+1]` 不相等',
                 '可以删任意个元素（右边的数左移补位），求最少删几个',
                 '示例：`[1,1,2,3,5]` → `1`；本视频：`[1,1,2,2,3,3,3]` → `3`'],
        quote='贪心法的题目，最直观的想法就是一趟遍历，如果遇到了相同的数那么就删去其中一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`first` 记当前这一对的左元素；遇到和它不同的数，就配成一对',
              '遇到相同的数：==保留一个==会让后面所有数的奇偶性翻转，但后面还能再删一个把它翻回来',
              '所以删一个比一次删两个更灵活；答案 = 总数 − 2 × 配成的对数'],
        result='配成 `(1,2)`、`(2,3)` 两对，`res = 7 − 4 = 3` ✓（删两个重复的 + 落单的 3）',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 从 `len(nums)` 倒着减：每配一对减 2；结尾落单的数（`first` 非 None）已经算在里面',
                 '易错：相等时 `continue`，==不要把 first 清空==，也不要 `res` 加减',
                 '和灵神的栈思路等价：`first` 非 None 就是“栈大小为奇数”',
                 '原文用 `class Solution(object)`，Python 3 下无需任何改动'],
    ),
)
