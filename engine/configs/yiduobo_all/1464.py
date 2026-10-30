CONFIG = dict(
    num=1464, title='数组中两元素的最大乘积', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='一趟扫描找最大两个数', tags=[],
    code='''
class Solution(object):
    def maxProduct(self, nums):

        m1 = m2 = None
        for num in nums:
            if m1 is None:
                m1 = num
            elif num > m1:
                m2 = m1
                m1 = num
            elif m2 is None or num > m2:
                m2 = num

        return (m1 - 1) * (m2 - 1)
''',
    call='Solution().maxProduct([3,4,5,2])',
    expect=12,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260,
             index=True,
             color=lambda S, i, v: ('yellow' if S.get('m1') == v and i <= S.get('_k', 99) else None) if False else None),
        dict(type='text', fn=lambda S: f"最大 `m1 = {S.get('m1')}`，次大 `m2 = {S.get('m2')}`"),
    ],
    watch=[('num', 'num', 'blue'), ('m1', 'm1', 'green'), ('m2', 'm2', 'orange')],
    captions={
        'm1 = m2 = None': '`m1` 记最大数，`m2` 记次大数，一开始都还没有',
        'for num in nums': '看下一个数 `{num}`',
        'if m1 is None': lambda S, B, r: '`m1` 还是空 → 这是第一个数' if S.get('m1') is None else '`m1` 已有值 → 不是第一个数',
        'm1 = num\n': '第一个数先当最大：`m1 = {m1}`',
        'elif num > m1': lambda S, B, r: f"`{S['num']} > m1 = {S['m1']}` → " + ('成立：新的最大数' if S['num'] > S['m1'] else '不成立'),
        'm2 = m1': '原来的最大数降为次大：`m2 = {m2}`',
        'elif m2 is None or num > m2': lambda S, B, r: f"`m2 = {S['m2']}`，num = {S['num']}：" + ('次大还没有，或比次大更大 → 更新次大' if (S['m2'] is None or S['num'] > S['m2']) else '比次大还小 → 忽略'),
        'm2 = num': '更新次大：`m2 = {m2}`',
        'return': '最大的两个数 `{m1}` 和 `{m2}` → `({m1}-1) * ({m2}-1)` = =={ret}==',
    },
    cards=dict(
        one_liner='数都是正整数，越大越好，找最大的两个数就行',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选两个 ==不同下标== 的数，求 `(nums[i]-1) * (nums[j]-1)` 的最大值',
                 '示例：`[3,4,5,2]` → 选 4 和 5，`3 * 4 = 12`'],
        quote='比较基础的题目。由于这里的数都是整数，因此只需要找到最大的两个数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i] >= 1`，所以 `nums[i]-1 >= 0`，越大乘积越大',
              '一趟扫描维护最大 `m1` 和次大 `m2`',
              '新数比 `m1` 大：`m1` 退居次大；否则只可能刷新 `m2`'],
        summary=['时间 `O(n)`，空间 `O(1)`，不用排序',
                 '易错点：新数比 `m1` 大时，必须先 `m2 = m1` 再 `m1 = num`，顺序反了会丢数',
                 '易错点：`m2` 初始为 None，要写 `m2 is None or ...`',
                 '最大值重复（如 `[5,5]`）也成立：它走第三个分支'],
    ),
)
