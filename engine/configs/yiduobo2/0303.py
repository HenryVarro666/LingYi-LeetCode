NUMS = [-2, 0, 3, -5, 2, -1]
QUERIES = [(0, 2), (2, 5), (0, 5)]


def _q(S):
    return 'i' in S and 'j' in S


IM1 = lambda S: S['i'] - 1 if _q(S) and S['i'] > 0 else None              # noqa: E731
PREV = lambda S: S['index'] - 1 if 'index' in S and not _q(S) else None    # noqa: E731


def _sum_color(S, k, v):
    if _q(S):
        if k == S['j']:
            return 'green'
        if S['i'] > 0 and k == S['i'] - 1:
            return 'red'
        return None
    if 'index' in S:
        done = S['index'] - 1 + (S.get('_line') == 6)
        return 'cyan' if k <= done else None
    if 'self.sum_list' in S:
        return 'cyan' if k == 0 else None
    return None


def _formula(S):
    sl = S.get('self.sum_list')
    if sl is None:
        return ''
    if _q(S):
        i, j = S['i'], S['j']
        if i == 0:
            return f"`i = 0`：`[0, {j}]` 的和就是 `sum_list[{j}]` = =={sl[j]}=="
        return f"`sum_list[{j}] − sum_list[{i - 1}]` = `{sl[j]} − ({sl[i - 1]})` = =={sl[j] - sl[i - 1]}=="
    if 'index' in S:
        k = S['index']
        if S.get('_line') == 6:
            return f"`sum_list[{k}]` += `sum_list[{k - 1}]` → =={sl[k]}==（= nums[0] + … + nums[{k}]）"
        return f"`sum_list[{k}]` 现在还是 `nums[{k}] = {sl[k]}`，要加上前面的和 `sum_list[{k - 1}] = {sl[k - 1]}`"
    return '先复制一份：`sum_list = nums[:]`'


def _if(S, B, ret):
    if S.i == 0:
        return f'`i == 0`：前面没有 `sum_list[-1]`，==需要特别注意== → 直接返回 `sum_list[{S.j}]`'
    return f'`i = {S.i} ≠ 0` → 用两个前缀和相减'


CONFIG = dict(
    num=303, title='区域和检索 - 数组不可变', difficulty='Easy', category='子串',
    author='yiduobo', technique='原地前缀和 · i = 0 特判',
    tags=['字节30天'],
    code='''
class NumArray(object):

    def __init__(self, nums):
        self.sum_list = nums[:]
        for index in range(1, len(nums)):
            self.sum_list[index] += self.sum_list[index - 1]

    def sumRange(self, i, j):
        if i == 0:
            return self.sum_list[j]
        else:
            return self.sum_list[j] - self.sum_list[i - 1]
''',
    call=f'''na = NumArray({NUMS})
[na.sumRange(i, j) for i, j in {QUERIES}]''',
    expect=[1, -1, -3],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var=lambda S: NUMS, label='nums', cell=100, h=215, window=('i', 'j'),
             pointers={'index': 'blue', 'i': 'red', 'j': 'green'}),
        dict(type='array', var='self.sum_list', label='sum_list（sum_list[k] = nums[0] + … + nums[k]，青 = 已累加好）',
             cell=100, h=230, pointers={'index': 'blue', PREV: 'purple', IM1: 'red', 'j': 'green'},
             pointer_labels={PREV: 'index-1', IM1: 'i-1'}, color=_sum_color),
    ],
    watch=['index', ('i', 'i', 'red'), ('j', 'j', 'green')],
    captions={
        'self.sum_list = nums[:]': '`sum_list` 先复制 `nums`：`sum_list[0] = nums[0]` 已经是前缀和了',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：把前面的和累加到这一格'
                                               if 'index' not in B or B.index != S.index else '前缀和维护完毕'),
        'self.sum_list[index] +=': '`sum_list[{index}] += sum_list[{index - 1}]` → `{self.sum_list[index]}`',
        'if i == 0': _if,
        10: lambda S, B, r: f'`sum_list[{S.j}]` 就是 `nums[0..{S.j}]` 的和 → 返回 =={r}==',
        'return self.sum_list[j] - self.sum_list[i - 1]': lambda S, B, r: (
            f'`sum_list[{S.j}]` 减去 `sum_list[{S.i - 1}]`：`0..{S.i - 1}` 的部分==抵消掉==，剩下 `{S.i}..{S.j}` → 返回 =={r}=='),
    },
    cards=dict(
        one_liner='sum_list[y] − sum_list[x−1]，前面 0..x−1 的部分正好抵消',
        complexity='初始化 `O(n)`，`sumRange` `O(1)`；空间 `O(n)`',
        problem=['给定整数数组 `nums`，多次查询下标 `[i, j]`（闭区间）的元素和',
                 '实现 `NumArray(nums)` 和 `sumRange(i, j)`',
                 '示例：`nums = [-2,0,3,-5,2,-1]`',
                 '`sumRange(0,2) = 1`，`sumRange(2,5) = -1`，`sumRange(0,5) = -3`'],
        quote='两式相减，==0到x - 1的部分抵消掉之后剩下的就是x到y的和了==。需要特别注意x = 0的情况，此时直接返回sum_list[y]即可。',
        quote_src='—— yiduobo 题解',
        idea=['`sum_list[k] = nums[0] + … + nums[k]`（包含 `k` 自己），长度就是 `n`',
              '`sum_list[y] − sum_list[x−1]`：前面 `0..x−1` 抵消，剩 `x..y`',
              '`x = 0` 时没有 `sum_list[-1]`，要单独返回 `sum_list[y]`'],
        result='三次查询依次返回 `[1, -1, -3]` ✓（其中两次走了 `i == 0` 特判）',
        summary=['预处理 `O(n)`，每次查询 `O(1)`',
                 '易错：`i = 0` 时写 `sum_list[i − 1]` 会取到 `sum_list[-1]`，==错了也不报错==',
                 '对比灵神：前缀和多开一位、`s[0] = 0`，就不需要这个特判',
                 '原文为 Python 2 风格，只删去了文档字符串和 LeetCode 模板注释'],
    ),
)
