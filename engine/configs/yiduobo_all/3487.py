CONFIG = dict(
    num=3487, title='删除后的最大子数组元素和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 集合去重 + 记录最大值',
    code='''
class Solution(object):
    def maxSum(self, nums):
        
        vis = set()
        s = 0
        ma = None
        for v in nums:
            if ma is None or ma < v:
                ma = v
            if v > 0 and v not in vis:
                vis.add(v)
                s += v
        
        if ma <= 0:
            return ma
        return s
''',
    call='Solution().maxSum([1, 2, -1, -2, 1, 0, -1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=84,
             color=lambda S, i, v: 'green' if v > 0 else None, dim=lambda S, i, v: v <= 0),
        dict(type='set', var='vis', label='vis（已累加过的正数）', fmt=lambda x: str(x), h=130),
    ],
    watch=[('v', 'v', 'blue'), ('ma', 'ma', 'orange'), ('s', 's', 'green')],
    captions={
        'vis = set()': '`vis` 记录出现过（已累加）的正数',
        's = 0': '`s` 累加互不相同的正数',
        'ma = None': '`ma` 记录 nums 里的最大值，开始时还没有',
        'for v in nums': '取出 `v = {v}`',
        'if ma is None or ma < v': lambda S, B, r: (f'`ma` 还没有值 或 `ma = {B.ma} < v = {S.v}` → 要更新最大值' if (B.ma is None or B.ma < S.v)
                                                    else f'`ma = {S.ma}` ≥ `v = {S.v}`，最大值不变'),
        'ma = v': '最大值更新：`ma` = =={ma}==',
        'if v > 0 and v not in vis': lambda S, B, r: (f'`v = {S.v}` 是正数且没出现过 → 累加' if (S.v > 0 and S.v not in B.vis)
                                                      else (f'`v = {S.v}` 不是正数 → 删掉，不累加' if S.v <= 0 else f'`v = {S.v}` 已在 `vis` 中 → 重复，删掉')),
        'vis.add(v)': '`{v}` 加入 `vis`，以后再遇到就是重复',
        's += v': '`s += {v}` → =={s}==',
        'if ma <= 0': lambda S, B, r: (f'最大值 `ma = {S.ma}` ≤ 0：没有正数，只能留最大的那个' if S.ma <= 0
                                       else f'最大值 `ma = {S.ma}` > 0：有正数，答案是正数去重和'),
        'return ma': '全非正数：返回最大值 `{ma}`',
        'return s': '返回去重正数之和 =={s}==',
    },
    cards=dict(
        one_liner='一趟遍历：正数去重累加，同时记录最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['删掉任意个元素（不能删空）后，选一个元素互不相同的子数组',
                 '求最大元素和',
                 '示例：`[1,2,-1,-2,1,0,-1]` → `3`'],
        quote='若nums中没有正数，就应该将nums删得只剩下唯一一个最大的元素，反之则应该将nums中所有的非正数以及重复元素都删除。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `vis` 记录出现过的元素，`ma` 记录最大值',
              '遇到正数且没出现过就累加到 `s`',
              '遍历完：`ma` 非正说明没有正数，返回 `ma`；否则返回 `s`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`ma` 初始为 `None`，第一个元素一定会成为最大值',
                 '易错点：0 不是正数，不累加；全是 0 或负数时返回 `ma`',
                 '对比灵神：灵神先过滤非负数再 `sum(set)`；yiduobo 用手写循环一趟完成',
                 '原文为 Python 2 风格，该代码无需修改'],
    ),
)
