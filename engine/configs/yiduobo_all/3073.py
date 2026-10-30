NUMS = [2, 7, 3, 9, 5]


def _txt(S):
    ln = S.get('_line', 0)
    if 'index' not in S or 'mapping' not in S:
        return ''
    if 'left_ma' in S and 'res' in S and ln >= 33:
        j = S['index']
        nums, right = S['nums'], S['right']
        if S['left_ma'] != 0 and nums[j] < right[j + 1]:
            return f"枚举 `nums[j]={nums[j]}`：最优 i = =={S['left_ma']}==（比它小的最大值），最优 k = =={right[j + 1]}==（右侧最大值）→ `{S['left_ma']} − {nums[j]} + {right[j + 1]}` = =={S['left_ma'] - nums[j] + right[j + 1]}=="
        return f"枚举 `nums[j]={nums[j]}`：左侧比它小的最大 = {S['left_ma']}，右侧最大 = {right[j + 1]} → ==凑不出递增三元组=="
    return ''


CONFIG = dict(
    num=3073, title='最大递增三元组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间 j · 树状数组求前缀最大',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def maximumTripletValue(self, nums):
        mapping = {}
        rank = 1
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = rank
                rank += 1
        
        left = [0] * rank
        right = [nums[-1]]
        for index in range(len(nums) - 2, -1, -1):
            right.append(max(right[-1], nums[index]))
        right.reverse()

        def add(x, v):
            while x < rank:
                left[x] = max(left[x], v)
                x += x & -x
        
        def get(x):
            ma = 0
            while x > 0:
                ma = max(ma, left[x])
                x -= x & -x
            return ma

        add(mapping[nums[0]], nums[0])
        res = 0
        for index in range(1, len(nums) - 1):
            left_ma = get(mapping[nums[index]] - 1)
            if left_ma != 0 and nums[index] < right[index + 1]:
                res = max(res, left_ma - nums[index] + right[index + 1])
            add(mapping[nums[index]], nums[index])

        return res
''',
    call=f'Solution().maximumTripletValue({NUMS})',
    expect=8,
    skip=['for v in sorted', 'if v not in mapping', 'rank += 1', 'mapping = {}', 'rank = 1', 'while x < rank', 'while x > 0', 'ma = 0', 'res = 0', 'for index in range'],
    max_steps=90,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前中间元素 j）', cell=80, h=170,
             color=lambda S, i, v: 'blue' if i == S.get('index') and S.get('_line', 0) >= 12 else None),
        dict(type='array', var=lambda S: S.get('right') if S.get('_line', 0) >= 20 else None,
             label='right：从后往前追加，reverse 后 right[k] = nums[k:] 的最大值', cell=80, h=170),
        dict(type='array', var='left', label='left：树状数组（粉 = 当前 x），下标 = 排名，存前缀最大值', cell=80, h=170,
             color=lambda S, i, v: 'pink' if i == S.get('x') and 17 <= S.get('_line', 0) <= 25 else None),
        dict(type='map', var='mapping', label='mapping：数值 → 排名（离散化）', h=130, font=22),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('left_ma', 'left_ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        'mapping[v] = rank': '先排序，再把数值映射成排名（1, 2, 3…）：`{v}` 的排名是 `{rank}`，这样树状数组下标不会太大',
        'left = [0] * rank': '树状数组 `left`：按排名存“前缀最大值”，一开始全 0',
        'right = [nums[-1]]': '`right` 从最后一个数开始，从后往前记录“右侧最大值”',
        'right.append': '`nums[{index}] = {nums[index]}` 和已有的最大值取 max → `right` 末尾加入 `{right[-1]}`',
        'right.reverse()': '`right[k]` = `nums[k:]` 里的最大值：这就是==最优的 nums[k]==（越大越好又最容易 > nums[j]）',
        'left[x] = max': '树状数组位置 `{x}`：`left[{x}] = max(.., {v}) = {left[x]}`',
        'x += x & -x': '`x += x & -x` → {x}：沿树状数组往上更新',
        'ma = max': '`ma = max(.., left[{x}])` = {ma}：把管辖的区间并进来',
        'x -= x & -x': '`x -= x & -x` → {x}：沿树状数组往下查前缀最大',
        'return ma': '前缀最大值 =={ma}==：比 nums[j] 小的数里最大的那个',
        'add(mapping[nums[0]], nums[0])': '先把 `nums[0] = {nums[0]}` 放进树状数组，它是第一个候选的 i',
        'res = 0': '`res = 0`：找不到递增三元组就返回 0',
        'left_ma = get': '`get({mapping[nums[index]] - 1})`：查排名小于 `nums[{index}] = {nums[index]}` 的前缀最大值，也就是左边比它小的最大数',
        'if left_ma != 0': lambda S, B, r: (f'`left_ma = {S.left_ma} ≠ 0`（左边有更小的）且 `nums[{S.index}] = {S.nums[S.index]} < right[{S.index + 1}] = {S.right[S.index + 1]}`（右边有更大的）→ ==能凑成三元组=='
                                           if S.left_ma != 0 and S.nums[S.index] < S.right[S.index + 1] else
                                           f'左边没有更小的数，或右边没有更大的数（`left_ma = {S.left_ma}`，`right[{S.index + 1}] = {S.right[S.index + 1]}`）→ 这个 j 不行'),
        'res = max(res': '`res = max({B.res}, {left_ma} − {nums[index]} + {right[index + 1]}) = {res}`',
        'add(mapping[nums[index]]': '处理完 j，把 `nums[{index}] = {nums[index]}` 加进树状数组，留给后面的 j 当 i',
        'return res': '最大值 =={res}==',
    },
    cards=dict(
        one_liner='枚举中间 j：右边取最大，左边取小于它的最大',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['整数数组 `nums`，找 `i < j < k` 且 `nums[i] < nums[j] < nums[k]` 的三元组',
                 '要使 `nums[i] − nums[j] + nums[k]` ==最大==，找不到就返回 `0`',
                 '本视频：`[2,7,3,9,5]` → `8`（2 − 3 + 9）'],
        quote='对于这类三元组问题，常见的思路还是枚举中间元素nums[j]，然后分别找出最优的nums[i]以及nums[k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[k]` 越大越好：取 j 右侧最大值，一趟逆序遍历得到 `right`',
              '`nums[i]` 越大越好但必须 `< nums[j]`：前缀里 ==值小于 nums[j] 的最大值==',
              '这是动态的“前缀最大”问题 → 值域离散化成排名，用树状数组维护'],
        summary=['时间 `O(n log n)`（排序 + 树状数组），空间 `O(n)`',
                 '`right[j+1] <= nums[j]` 说明右边没有更大的数，不能当 k；`left_ma == 0` 说明左边没有更小的数',
                 '易错：先查询再 `add`，保证 i 严格在 j 左边；排名从 1 开始，树状数组下标不能为 0',
                 '原文为 Python 2 风格，只删去了 `:type` 说明文档字符串，代码未改',
                 '对比：也可以用前缀最小/有序集合，树状数组是因为值域太大 + 要“小于 nums[j]”的前缀最大'],
    ),
)
