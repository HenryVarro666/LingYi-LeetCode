CONFIG = dict(
    num=3678, title='大于平均值的最小未出现正整数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='下界 + 哈希集合',
    code='''
class Solution(object):
    def smallestAbsent(self, nums):
        
        s = sum(nums)
        target = max(1, s // len(nums) + 1)
        
        nums_set = set(nums)
        while target in nums_set:
            target += 1
        return target
''',
    call='Solution().smallestAbsent([4,-1,2,3])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"和 `{sum(S['nums'])}`，个数 `{len(S['nums'])}`" + (f"，target = =={S['target']}==" if 'target' in S else ''), h=60),
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'green' if 'target' in S and v == S['target'] else None),
        dict(type='set', var='nums_set', fmt=lambda x: str(x), h=200, label='nums_set'),
    ],
    watch=['s', ('target', 'target', 'green')],
    captions={
        's = sum': '先求元素和 `s = {s}`',
        'target = max': '平均值刚好整数时，`s // n + 1` 是平均值加 1；否则就是向上取整。负平均值时下界取 1：`target = {target}`',
        'nums_set = set': '把 `nums` 放进集合，便于快速判断是否出现',
        'while target': '`{target}` 在 nums 中吗？{"在，继续往上找" if target in nums_set else "不在，找到了"}',
        'target += 1': '`{B.target}` 已出现 → 向上遍历下一个：`target = {target}`',
        'return': '第一个没出现的正整数是 =={ret}==',
    },
    cards=dict(
        one_liner='确定下界 target，再向上找第一个没出现的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 取值 -100 到 100，求严格大于平均值的最小未出现正整数',
                 '示例：`[4,-1,2,3]` 平均值 2 → 答案 `5`'],
        quote='若平均值刚好为整数，那么target就相当于平均值加上1，否则target就代表了平均值向上取整。',
        quote_src='—— yiduobo 题解',
        idea=['平均值可能小于 1，此时下界就是 1', '否则下界取 `sum(nums) // len(nums) + 1`', '从下界起向上遍历，第一个不在集合里的就是答案'],
        after=[dict(heading='举例走一遍', lines=['`[3,5]` 平均值 4，target = 5，已出现，跳到 6', '关键是下界：向下取整的平均值加 1', '再用集合挡掉已出现的数，逐个加一', '数组至多 n 个数，所以最多加 n 次'])],
        summary=['时间 `O(n)`，空间 `O(n)`', '易错点：负平均值要用 `max(1, ...)` 兜底',
                 '原文为 Python 2 写法，已删去 `:type` 文档字符串；整数除法本来就是 `//`，无需改'],
    ),
)
