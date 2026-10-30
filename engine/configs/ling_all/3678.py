CONFIG = dict(
    num=3678, title='大于平均值的最小未出现正整数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 + 从下界枚举',
    code='''
class Solution:
    def smallestAbsent(self, nums: List[int]) -> int:
        st = set(nums)
        ans = max(sum(nums) // len(nums) + 1, 1)  # 答案必须是正整数
        while ans in st:
            ans += 1
        return ans
''',
    call='Solution().smallestAbsent([-1,1,2])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"元素和 `{sum(S['nums'])}`，个数 `{len(S['nums'])}`，下界 = max(和 // 个数 + 1, 1)" + (f" → 当前 ans = =={S['ans']}==" if 'ans' in S else ''), h=60),
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'green' if 'ans' in S and v == S['ans'] else None),
        dict(type='set', var='st', fmt=lambda x: str(x), h=200, label='st'),
    ],
    watch=[('ans', 'ans', 'green')],
    captions={
        'st = set': '转成哈希集合 `st = {st}`，之后判断「是否出现」只要 O(1)',
        'ans = max': '平均值向下取整再加 1，就是严格大于平均值的最小整数；与 1 取最大保证为正：`ans = {ans}`',
        'while ans in st': '`{ans}` 在集合里吗？{"在，已经出现过，不能当答案，继续加一" if ans in st else "不在，它就是答案"}',
        'ans += 1': '`ans` 已出现 → 加一，试下一个：`ans = {ans}`',
        'return': '`{ans}` 严格大于平均值且没出现过，返回 =={ret}==',
    },
    cards=dict(
        one_liner='先算出答案下界，再往上跳过已出现的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求严格大于 `nums` 平均值、且不在 `nums` 里的最小正整数',
                 '示例：`[-1,1,2]` 平均值 0.667 → 答案 `3`'],
        quote='答案至少为 max(floor(s/n)+1, 1)。从上式开始枚举，如果答案在 nums 中，则把答案加一，继续判断，直到答案不在 nums 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`sum // len + 1` 是严格大于平均值的最小整数', '平均值可能为负，所以和 1 取最大',
              '用哈希集合判断是否出现，答案至多增大 n 次'],
        after=[dict(heading='举例走一遍', lines=['`[3,5]` 平均值 4，下界 5，5 已出现，跳到 6', '关键是下界：向下取整的平均值加 1', '再用集合挡掉已出现的数，逐个加一', '数组至多 n 个数，所以最多加 n 次'])],
        summary=['时间 `O(n)`：集合里至多 n 个数，`ans` 最多加 n 次',
                 '易错点：Python 的 `//` 向下取整，负数也正确；别忘了与 1 取最大',
                 '「是否出现」类问题，先转哈希集合'],
    ),
)
