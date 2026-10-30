NUMS = [7, 1, 5, 4, 9, 2]


def _color(S, i, v):
    if 'index' not in S:
        return 'green' if 'mi' in S and i == 0 else None
    if i == S['index']:
        return 'blue'
    if i == S.get('p'):
        return 'green'
    return None


def _dim(S, i, v):
    return 'index' in S and i > S['index']


def _txt(S):
    if 'mi' not in S:
        return '枚举 j；nums[i] 选 ==nums[0..j−1] 的最小值== 最好'
    if 'index' not in S:
        return f"先把 `nums[0] = {S['mi']}` 当作前缀最小值 `mi`"
    j = S['index']
    v = S['nums'][j]
    if S.get('_line') in (8, 9) and v > S['mi']:
        return f"`nums[{j}] − mi = {v} − {S['mi']} = {v - S['mi']}`"
    return f"前缀 `nums[0..{j - 1}]` 的最小值 `mi = {S['mi']}`（在下标 `p = {S['p']}`）"


def _if(S, B, r):
    v, mi = S.nums[S.index], S.mi
    if v > mi:
        return f'`nums[{S.index}] = {v} > mi = {mi}`：==严格更大==，可以配成一对'
    return f'`nums[{S.index}] = {v}` 不大于 `mi = {mi}`，配不成'


CONFIG = dict(
    num=2016, title='增量元素之间的最大差值', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 维护前缀最小值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1246'],
    code='''
class Solution(object):
    def maximumDifference(self, nums):

        mi = nums[0]
        p = 0
        res = -1
        for index in range(1, len(nums)):
            if nums[index] > mi:
                res = max(res, nums[index] - mi)
            elif nums[index] < mi:
                mi = nums[index]
                p = index

        return res
''',
    call=f'Solution().maximumDifference({NUMS})',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='nums', h=320, cell=110, pointers={'index': 'blue', 'p': 'green'},
             color=_color, dim=_dim, label='nums（蓝 = 当前 j，绿 = 前缀最小值所在位置 p）'),
    ],
    watch=[('index', 'index', 'blue'), ('mi', 'mi', 'green'), 'p', ('res', 'res', 'orange')],
    captions={
        'mi = nums[0]': '`mi`：已遍历前缀的最小值，先取 `nums[0] = {mi}`',
        'p = 0': '`p` 记录最小值的位置',
        'res = -1': '`res = -1`：没找到合法的一对就返回它',
        'for index in range': lambda S, B, r: (f'枚举 `j = {S.index}`，`nums[j] = {S.nums[S.index]}`'
                                            if B.get('index') != S.index else '所有 j 都枚举完了，循环结束'),
        'if nums[index] > mi': _if,
        'res = max': lambda S, B, r: (f'用 `{S.nums[S.index]} − {S.mi} = {S.nums[S.index] - S.mi}` 更新：'
                                      + (f'==res = {S.res}==' if S.res != B.res else f'不超过 `{S.res}`，不变')),
        'elif nums[index] < mi': lambda S, B, r: (f'`{S.nums[S.index]} < mi = {S.mi}`：发现==更小==的数'
                                                  if S.nums[S.index] < S.mi else f'`{S.nums[S.index]} == mi`：什么都不做'),
        'mi = nums[index]': '前缀最小值更新为 `mi = {mi}`',
        'p = index': '它在下标 `p = {p}`',
        'return res': '返回最大差值 =={res}==',
    },
    cards=dict(
        one_liner='nums[j] 固定时，nums[i] 越小越好：只记前缀最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums[j] − nums[i]` 的最大值，要求 `i < j` 且 ==`nums[i] < nums[j]`==',
                 '不存在就返回 `-1`',
                 '示例：`[7,1,5,4]` → `4`；本视频：`[7,1,5,4,9,2]` → `8`'],
        quote='为了使得nums[j] - nums[i]尽可能大，那么就需要让选择的nums[i]==尽可能小==，也就是说应该找出nums[0]到nums[j - 1]之间的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据小可以暴力枚举 `(i, j)`，但有个常见小优化',
              '`nums[0..j−1]` 的最小值 = ==`nums[0..j−2]` 的最小值和 `nums[j−1]` 取小==',
              '只有 `nums[j] > mi` 才更新答案，所以 `res = -1` 初始化没问题'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`>` 严格大于：相等的数不算，自然保证 `nums[i] < nums[j]`',
                 '变量 `p` 记录最小值下标，求答案时其实用不到',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未作改动'],
    ),
)
