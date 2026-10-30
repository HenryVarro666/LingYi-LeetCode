CONFIG = dict(
    num=3584, title='子序列首尾元素的最大乘积', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举尾元素 · 前缀最大最小值',
    tags=['灵神题单', '难度分 1763'],
    code='''
class Solution(object):
    def maximumProduct(self, nums, m):
        
        res = None
        mi = nums[0]
        ma = nums[0]
        for index, v in enumerate(nums[m - 1:], m - 1):
            mi = min(mi, nums[index - m + 1])
            ma = max(ma, nums[index - m + 1])
            
            best = max(v * ma, v * mi)
            if res is None or res < best:
                res = best
        
        return res
''',
    call='Solution().maximumProduct([2,-1,2,-6,5,2,-5,7], 2)',
    expect=35,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 尾元素 v，黄 = 刚并入的 index−m+1，其余 [0, index−m+1] 是起点候选）', h=230, cell=96,
             pointers={'index': 'blue'},
             dim=lambda S, i, v: 'index' in S and i > S['index'] - S['m'] + 1 and i != S['index'],
             color=lambda S, i, v: ('blue' if S.get('index') == i else 'yellow' if 'index' in S and i == S['index'] - S['m'] + 1 else None)),
        dict(type='text', size=28, h=130,
             fn=lambda S: (f"起点候选：最小 `mi = {S['mi']}`，最大 `ma = {S['ma']}`；`v = {S['v']}`：`v·ma` = {S['v'] * S['ma']}，`v·mi` = {S['v'] * S['mi']}"
                           if 'index' in S and 'v' in S else 'v 为正选最大值做起点，v 为负选最小值做起点')),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v'), ('mi', 'mi', 'cyan'), ('ma', 'ma', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = None': '`res` 记录最大乘积，先用 `None` 表示还没有结果（答案可能为负，不能用 0）',
        'mi = nums[0]': '`mi` 记录起点候选里的最小值，先放入 `nums[0]` = {mi}',
        'ma = nums[0]': '`ma` 记录起点候选里的最大值，先放入 `nums[0]` = {ma}',
        'for index, v in': lambda S, B, r: (f'尾元素 `index = {S.index}`，`v = {S.v}`：尾下标从 `m − 1` 起，才凑得出 m 个元素' if 'index' in S and ('index' not in B or S.index != B.index) else '遍历结束'),
        'mi = min': '起点下标最大到 `index − m + 1 = {index - m + 1}`，把 `nums[{index - m + 1}]` 并入：`mi = {mi}`',
        'ma = max': '同样并入最大值：`ma = {ma}`',
        'best = max': '`v·ma = {v * ma}`，`v·mi = {v * mi}`：v 为正选 ma，为负选 mi → `best = {best}`',
        'if res is None': lambda S, B, r: ('`res` 还是空，直接采用 `best`' if S.res is None else (f'`res = {S.res} < best = {S.best}` → 更新' if S.res < S.best else f'`res = {S.res} ≥ best = {S.best}`，不更新')),
        'res = best': '`res = {res}`',
        'return res': '最大乘积 `{res}`',
    },
    cards=dict(
        one_liner='尾元素 v 定了：正数配最大起点，负数配最小起点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在长为 `m` 的子序列里，求首尾元素乘积的最大值',
                 '尾元素下标 `index` 在 `m − 1 ~ n − 1` 之间',
                 '本视频：`nums=[2,-1,2,-6,5,2,-5,7]`，`m=2` → `35`'],
        quote='当nums[index]为正数时，就应该选择nums[0]到nums[index - m + 1]之间的最大值作为起点，反之则应该选择nums[0]到nums[index - m + 1]之间的最小值作为起点。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举子序列最后一个元素的下标 `index`',
              '起点下标 `p ≤ index − m + 1`，才保证至少有 m 个元素',
              '用 `mi`、`ma` 维护起点候选的最小、最大值，一趟搞定'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先用 `nums[index − m + 1]` 更新 `ma`、`mi`，再算乘积',
                 '`res` 用 `None` 起步，因为乘积可能为负',
                 '对比灵神：灵神用 `±inf` 起步并只在起点处并入；yiduobo 先放入 `nums[0]` 并用 `None` 记结果',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
