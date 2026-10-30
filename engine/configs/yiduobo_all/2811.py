NUMS = [3, 1, 2, 1, 4, 2]
M = 5


def _cell(S, i, v):
    if 'index' not in S:
        return None
    k = S['index']
    if S['nums'][k] + S['nums'][k - 1] >= S['m'] and i in (k, k - 1):
        return 'green'
    if i in (k, k - 1):
        return 'blue'
    return None


def _sum_txt(S):
    if 'index' not in S:
        return f'`m = {S["m"]}`：找相邻两数之和 `>= m` 的一对'
    k = S['index']
    a, b = S['nums'][k - 1], S['nums'][k]
    return f'`nums[{k - 1}] + nums[{k}] = {a} + {b} = ` ==`{a + b}`==' + (f' ≥ {S["m"]}' if a + b >= S['m'] else f' < {S["m"]}')


CONFIG = dict(
    num=2811, title='判断是否能拆分数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='脑筋急转弯 · 一趟找相邻和',
    tags=['灵神题单·贪心与思维', '难度分 1543'],
    code='''
class Solution(object):
    def canSplitArray(self, nums, m):

        if len(nums) <= 2:
            return True

        for index in range(1, len(nums)):
            if nums[index] + nums[index - 1] >= m:
                return True
        
        return False
''',
    call=f'Solution().canSplitArray({NUMS}, {M})',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 正在比较的相邻两数，绿 = 和 ≥ m）', cell=96, h=240,
             color=_cell, pointers={'index': 'blue'}),
        dict(type='text', h=90, size=32, fn=_sum_txt),
    ],
    watch=[('m', 'm', 'yellow'), ('index', 'index', 'blue')],
    captions={
        'if len(nums) <= 2': lambda S, B, r: (f'`len(nums) = {len(S.nums)} <= 2`：一刀就拆成单个元素，直接 `True`' if len(S.nums) <= 2
                                              else f'`len(nums) = {len(S.nums)} > 2`：一定会出现「长为 2 的子数组被切开」的那一刀，往下找'),
        'return True': lambda S, B, r: ('长度不超过 2，直接满足' if len(S.nums) <= 2 or 'index' not in S
                                        else f'`{S.nums[S.index - 1]} + {S.nums[S.index]} >= {S.m}`：找到这对相邻元素，从两侧一个个剥离 → ==`True`=='),
        'for index in range': '下标 `{index}`：看相邻两数 `nums[{index - 1}] = {nums[index - 1]}` 和 `nums[{index}] = {nums[index]}`',
        'if nums[index] + nums[index - 1] >= m': lambda S, B, r: (
            f'`{S.nums[S.index]} + {S.nums[S.index - 1]} = {S.nums[S.index] + S.nums[S.index - 1]}`，'
            + ('==≥ m==，这对相邻元素可以当核心' if S.nums[S.index] + S.nums[S.index - 1] >= S.m else f'小于 `m = {S.m}`，不行，看下一对')),
        'return False': '所有相邻对的和都 `< m`：最后一次「长为 2 → 两个 1」的切分一定不合法 → `False`',
    },
    cards=dict(
        one_liner='最终必有一次把长为 2 的数组切成两个单元素，所以必须有相邻两数之和 ≥ m',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把长度为 `n` 的数组不断一分为二，直到都是长度 1 的数组',
                 '每次切出的两部分都要「好」：长度为 1，或元素和 `>= m`',
                 '示例：`nums=[2,3,3,2,3]`，`m=6` → `true`',
                 '本视频：`[3,1,2,1,4,2]`，`m=5`'],
        quote='无论怎么切分，一定会至少执行一次下面的操作：将一个长度为2的子数组切分成两个长度为1的子数组。这也就意味着这个长度为2的子数组之和必须大于等于m。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，可以想区间记忆化搜索，但太复杂',
              '必有一刀把长 2 的数组切开 → 必须有相邻两数之和 `>= m`',
              '反过来：数组元素都是正数，以这两个数为中心不断剥离两侧单个元素',
              '每次剩下的部分和都 `>= m`，所以充分',
              '一趟遍历找相邻两数之和即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`len(nums) <= 2` 要先特判，否则范围 `range(1, len)` 里没有合法的一对也会返回 False',
                 '充分性依赖「元素都是正数」：剥离元素后和只增不减，不会跌破 `m`',
                 '对比灵神：灵神用 `any(x + y >= m for x, y in pairwise(nums))` 一行写完，思路相同',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
