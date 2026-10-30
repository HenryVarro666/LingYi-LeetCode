CONFIG = dict(
    num=2908, title='元素和最小的山形三元组 I', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间 + 前后缀最小值',
    tags=[],
    code='''
class Solution:
    def minimumSum(self, nums: List[int]) -> int:
        n = len(nums)
        suf = [0] * n
        suf[-1] = nums[-1]  # 后缀最小值
        for i in range(n - 2, 1, -1):
            suf[i] = min(suf[i + 1], nums[i])

        ans = inf
        pre = nums[0]  # 前缀最小值
        for j in range(1, n - 1):
            if pre < nums[j] > suf[j + 1]:  # 山形
                ans = min(ans, pre + nums[j] + suf[j + 1])  # 更新答案
            pre = min(pre, nums[j])
        return ans if ans < inf else -1
''',
    call='Solution().minimumSum([8,6,1,5,3])',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"山顶 `nums[{S['j']}]` = =={S['nums'][S['j']]}==，左边最小 `{S['pre']}`，右边最小 `{S['suf'][S['j']+1]}`" if 'j' in S and 'pre' in S and S['j'] + 1 < len(S['nums']) and S['_line'] >= 11 else '先从右往左算后缀最小值 `suf`'), size=34, h=60),
        dict(type='array', var='nums', label='nums', pointers={'j': 'pink'}, h=170,
             color=lambda S, i, v: 'pink' if 'j' in S and S['_line'] >= 11 and i == S['j'] else None),
        dict(type='array', var='suf', label='suf（nums[i..] 的最小值）', h=170,
             color=lambda S, i, v: 'cyan' if S['_line'] < 9 and i == S.get('i') else 'green' if 'j' in S and S['_line'] >= 11 and i == S['j'] + 1 else None),
    ],
    watch=['i', ('j', 'j', 'pink'), ('pre', 'pre', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'suf[-1] = ': '最右边的后缀最小值就是它自己：`suf[{n-1}] = {nums[-1]}`',
        'suf[i] = min': '`suf[{i}] = min(suf[{i+1}], nums[{i}])` = `min({suf[i+1]}, {nums[i]})` = =={suf[i]}==',
        'pre = nums[0]': '前缀最小值先取 `nums[0] = {pre}`，j 从 1 开始枚举',
        'if pre < nums[j]': lambda S, B, ret: f"山形判断：`{S['pre']} < {S['nums'][S['j']]} > {S['suf'][S['j']+1]}` → " + ('==成立==，j 左右各有一个更小的数' if S['pre'] < S['nums'][S['j']] > S['suf'][S['j']+1] else '不成立，j 不是山顶'),
        'ans = min': '三元组和 `{pre} + {nums[j]} + {suf[j+1]}` = {pre + nums[j] + suf[j+1]}，`ans` 取小 → =={ans}==',
        'pre = min(pre': '把 `nums[{j}]` 并入前缀：`pre = min({B.pre}, {nums[j]})` = {pre}',
        'return ans': '`ans` 还是 inf 说明没有山形，返回 -1；否则返回 =={ans}==',
    },
    cards=dict(
        one_liner='三元组题枚举中间数，左右各取最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找 `i<j<k` 且 `nums[i]<nums[j]>nums[k]` 的山形三元组，求元素和最小值',
                 '没有山形返回 `-1`',
                 '示例：`[8,6,1,5,3]` → `9`（下标 2,3,4）'],
        quote='这种三元组的题目，通常是枚举中间的数。枚举 nums[j]，我们需要求出 j 左边所有元素的最小值和右边所有元素的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['固定山顶 j 后，左右两边各选最小的数，和一定最小',
              '后缀最小值 `suf[i] = min(suf[i+1], nums[i])` 递推',
              '前缀最小值边枚举边更新，只要一个变量 `pre`'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suf` 数组）',
                 '==先判断山形再更新 pre==：`pre` 只能包含 j 左边的数',
                 '`suf` 只需算到下标 2，因为 j 最小为 1，要用 `suf[j+1]`',
                 '数据更大的 II 题（2909）同一套做法，同类题：2874、42'],
    ),
)
