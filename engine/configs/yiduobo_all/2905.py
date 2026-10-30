CONFIG = dict(
    num=2905, title='找出满足差值条件的下标 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀最值下标 · 一趟扫描',
    tags=['灵神题单', '难度分 1764'],
    code='''
class Solution(object):
    def findIndices(self, nums, indexDifference, valueDifference):

        ma = mi = None
        for index, v in enumerate(nums[indexDifference:]):
            if ma is None or nums[ma] < nums[index]:
                ma = index
            if mi is None or nums[mi] > nums[index]:
                mi = index
            
            if nums[ma] - v >= valueDifference:
                return [ma, index + indexDifference]
            if v - nums[mi] >= valueDifference:
                return [mi, index + indexDifference]
        
        return [-1, -1]
''',
    call='Solution().findIndices([3,5,2,4,1,9], 2, 6)',
    expect=[2, 5],
    views=[
        dict(type='array', var='nums', label='nums（粉 = ma，青 = mi，蓝 = 当前 j = index + indexDifference）', h=230, cell=100,
             pointers={'ma': 'pink', 'mi': 'cyan', 'index + indexDifference': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and S['index'] + S['indexDifference'] == i else None),
        dict(type='text', size=28, h=130,
             fn=lambda S: (f"`nums[ma]` = {S['nums'][S['ma']]}，`nums[mi]` = {S['nums'][S['mi']]}，当前 `v` = {S['v']}，"
                           f"要 ≥ =={S['valueDifference']}==：`{S['nums'][S['ma']] - S['v']}` 或 `{S['v'] - S['nums'][S['mi']]}`"
                           if S.get('ma') is not None and 'v' in S else '只检测两种情况：前缀最大值 − v，或 v − 前缀最小值')),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v'), ('ma', 'ma', 'pink'), ('mi', 'mi', 'cyan')],
    captions={
        'ma = mi = None': '`ma`、`mi` 分别存前缀 `0 ~ j−indexDifference` 里最大、最小值的下标，一开始都没有',
        'for index, v in enumerate': lambda S, B, r: (f'`index = {S.index}`：当前 `v = nums[{S.index + S.indexDifference}] = {S.v}`，前缀范围到下标 `{S.index}`' if 'index' in S and ('index' not in B or S.index != B.index) else '遍历结束，没有可行解'),
        'if ma is None or nums[ma] < nums[index]': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` 比当前最大值大（或还没有最大值）→ 它成为新的 `ma`' if (S.ma is None or S.nums[S.ma] < S.nums[S.index]) else f'`nums[{S.index}] = {S.nums[S.index]}` 没超过最大值 `{S.nums[S.ma]}`，`ma` 不变'),
        'ma = index': '`ma = {ma}`：最大值下标更新',
        'if mi is None or nums[mi] > nums[index]': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` 比当前最小值小（或还没有最小值）→ 它成为新的 `mi`' if (S.mi is None or S.nums[S.mi] > S.nums[S.index]) else f'`nums[{S.index}] = {S.nums[S.index]}` 没低于最小值 `{S.nums[S.mi]}`，`mi` 不变'),
        'mi = index': '`mi = {mi}`：最小值下标更新',
        'if nums[ma] - v': lambda S, B, r: (f'最大值减当前：`{S.nums[S.ma]} − {S.v} = {S.nums[S.ma] - S.v}` ≥ {S.valueDifference} → ==成立=={chr(65292)}`[ma, j]` 可行' if S.nums[S.ma] - S.v >= S.valueDifference else f'最大值减当前：`{S.nums[S.ma]} − {S.v} = {S.nums[S.ma] - S.v}` < {S.valueDifference}，不够'),
        'return [ma': '`[ma, index + indexDifference]` = `[{ma}, {index + indexDifference}]`',
        'if v - nums[mi]': lambda S, B, r: (f'当前减最小值：`{S.v} − {S.nums[S.mi]} = {S.v - S.nums[S.mi]}` ≥ {S.valueDifference} → ==成立=={chr(65292)}`[mi, j]` 可行' if S.v - S.nums[S.mi] >= S.valueDifference else f'当前减最小值：`{S.v} − {S.nums[S.mi]} = {S.v - S.nums[S.mi]}` < {S.valueDifference}，不够'),
        'return [mi': '`[mi, index + indexDifference]` = `[{mi}, {index + indexDifference}]`',
        'return [-1, -1]': '遍历完仍没找到，返回 `[-1, -1]`',
    },
    cards=dict(
        one_liner='对每个 j，只试前缀最大值和最小值两个候选',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找下标 `i, j`：`|i − j| ≥ indexDifference` 且 `|nums[i] − nums[j]| ≥ valueDifference`',
                 '有解返回 `[i, j]`，否则 `[-1, -1]`；是 2903 题的加强版（`n` 到 `10^5`）',
                 '本视频：`nums=[3,5,2,4,1,9]`，`indexDifference=2`，`valueDifference=6` → `[2,5]`'],
        quote='对于后面这个绝对值之差，则只需检测两种情况，即0到j - indexDifference中的最大值减去nums[j]，以及nums[j]减去0到indexDifference中的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`O(n²)` 暴力不行：每个 j 只需要看前缀的最大、最小',
              '从 `indexDifference` 往后遍历 j，两个变量 `ma`、`mi` 记下标',
              '`index` 是切片后的下标，对应原数组前缀的末位 `j − indexDifference`'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片 `nums[indexDifference:]` 会多占 `O(n)`）',
                 '返回时要把 `index` 加回 `indexDifference` 才是原下标 j',
                 '`ma`、`mi` 用 `None` 表示“还没有”，第一轮必须先赋值',
                 '对比灵神：灵神 `max_idx` 从 0 开始、用 `elif`；yiduobo 两个 if 并列、从 None 开始',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
