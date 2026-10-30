NUMS = [4, 1, 3, 3, 6, 5, 9]


def _txt(S):
    if 'index' not in S:
        return '好数对：`j − i = nums[j] − nums[i]` ⇔ ==`nums[j] − j = nums[i] − i`=='
    k = S['num'] - S['index']
    return f"`num − index = {S['num']} − {S['index']}` = =={k}==，哈希表里同权重的下标都和它组成好数对"


CONFIG = dict(
    num=2364, title='统计坏数对的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='总数减好数对 · 哈希计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1622'],
    code='''
class Solution(object):
    def countBadPairs(self, nums):

        cnt_dict = {}
        res = len(nums) * (len(nums) - 1) // 2
        for index, num in enumerate(nums):
            res -= cnt_dict.get(num - index, 0)
            cnt_dict[num - index] = cnt_dict.get(num - index, 0) + 1
        
        return res
''',
    call=f'Solution().countBadPairs({NUMS})',
    expect=18,
    views=[
        dict(type='array', var='nums', label='nums（下方是 nums[index] − index）', h=190, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='array', var=lambda S: [v - k for k, v in enumerate(S['nums'])], label='权重 nums[index] − index（绿 = 与当前相同 → 好数对）', h=190,
             color=lambda S, i, v: ('blue' if i == S['index'] else 'green' if i < S['index'] and v == S['num'] - S['index'] else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='map', var='cnt_dict', label='cnt_dict（权重 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=140, font=34),
        dict(type='text', h=80, size=27, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '`cnt_dict` 统计每种 `nums[j] − j` 出现的次数',
        'res = len(nums)': '一共 `n(n − 1)/2` = =={res}== 组数对；==统计相等比统计不等容易==，所以减去好数对',
        'for index, num in': lambda S, B, r: (f'遍历到 `nums[{S.index}] = {S.num}`' if B.get('index') != S.index else '遍历完成'),
        'res -= cnt_dict.get': lambda S, B, r: (f'之前有 `{B.res - S.res}` 个下标的 `nums[j] − j` 也等于 `{S.num - S.index}` → 好数对，`res` 减到 {S.res}' if B.res != S.res
                                               else f'之前没有 `nums[j] − j = {S.num - S.index}` 的下标，没有新的好数对'),
        'cnt_dict[num - index] =': '`{num - index}` 的权重加 1 → `{cnt_dict[num - index]}`',
        'return res': '总数减去好数对，坏数对 `{res}` 个',
    },
    cards=dict(
        one_liner='坏数对 = 总数对 − 好数对；好数对用 nums[j] − j 哈希',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`i < j` 且 `j − i ≠ nums[j] − nums[i]` 的 `(i, j)` 是==坏数对==，求个数',
                 '示例：`[4,1,3,3]` → `5`',
                 f'本视频：`{NUMS}` → `18`'],
        quote='可以先将问题从统计坏数对变为统计好数对，然后使用这个总数减去好数对得到题目要求的坏数对。这样做的理由是一般来说，==统计相等比统计不等还是容易点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`j − i = nums[j] − nums[i]` 移项 → `nums[j] − j = nums[i] − i`',
              '式子两边各只与一个下标有关 → 哈希表记录每种 `nums[j] − j` 的次数',
              '一趟遍历：先用旧权重扣掉好数对，再把自己的权重加 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`n * (n − 1) / 2` 的整数除法已改为 `//`',
                 '先减 `res` 再更新哈希表，否则会把自己算成好数对',
                 '“不等”转“相等”是计数题常用的补集思路'],
    ),
)
