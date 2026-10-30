CONFIG = dict(
    num=2541, title='使数组中所有元素相等的最小操作数 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='先判 k=0 · 倍数与总和判定',
    tags=['灵神题单', '数学算法', '难度分 1620'],
    code='''
class Solution(object):
    def minOperations(self, nums1, nums2, k):

        if k == 0:
            if nums1 == nums2:
                return 0
            return -1

        n = len(nums1)
        diff = []
        res = 0
        s = 0
        for index in range(n):
            diff = nums1[index] - nums2[index]
            s += diff
            if diff % k != 0:
                return -1
            elif diff > 0:
                res += diff // k
        
        if s == 0:
            return res
        
        return -1
''',
    call='Solution().minOperations([4,3,1,4], [1,3,7,1], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums1', pointers={'index': 'blue'}, label='nums1', h=210),
        dict(type='array', var='nums2', pointers={'index': 'blue'}, label='nums2', h=230),
        dict(type='text', fn=lambda S: (f'`diff = {S["nums1"][S["index"]]} − {S["nums2"][S["index"]]}` = =={S["nums1"][S["index"]] - S["nums2"][S["index"]]}==，累计差之和 `s = {S["s"]}`，已需 `res = {S["res"]}` 次'
                                         if 'index' in S and 'diff' in S and isinstance(S['diff'], int) else '')
             , size=30, h=130),
    ],
    watch=['index', 'diff', ('s', 's', 'yellow'), ('res', 'res', 'green'), 'k'],
    captions={
        'if k == 0': '先考虑特殊情况：`k = {k}`，{"数组根本无法变动" if k == 0 else "可以操作，继续"}',
        'if nums1 == nums2': '`k = 0` 时只有两数组一开始就相同才有解 → 相同返回 0',
        'diff = nums1': '第 `{index}` 位的差 `diff = nums1[{index}] − nums2[{index}]` = =={diff}==',
        15: '操作不改变 nums1 的总和，所以把差累加起来，最后必须为 0：`s` = =={s}==',
        'if diff % k': '每次变化都是 `k` 的倍数：`{diff} % {k} = {diff % k}` → {"不能整除，返回 -1" if diff % k else "通过"}',
        'elif diff > 0': '只统计大于 0 的差：`{diff} > 0` → {"成立，要补 `" + str(diff // k) + "` 次" if diff > 0 else "不成立，跳过"}',
        19: '`res` += `{diff} // {k}` → =={res}==',
        'if s == 0': '总和 `s = {s}`：{"相等，答案就是 res" if s == 0 else "不为 0，无解"}',
    },
    cards=dict(
        one_liner='先排除 k=0，再用 倍数 + 总和 两条件判有无解',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作：`nums1[i] += k`，`nums1[j] -= k`',
                 '求最少操作数让 `nums1 == nums2`，不可能返回 `-1`',
                 '示例：`[4,3,1,4]`、`[1,3,7,1]`、`k=3` → `2`'],
        quote='首先考虑特殊情况。当k = 0时，数组是无法发生任何变动的，在这种情况下，若一开始num1就和nums2相同，那么答案就为0，否则答案为-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k = 0`：能不能相等一眼就能看出',
              '`k > 0`：每个位置的差必须是 `k` 的倍数；操作不改变总和，所以差之和必须为 0',
              '满足后，统计所有正的差，每个要 `diff / k` 次操作'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`k = 0` 必须先判，否则取模会除零',
                 '原文为 Python 2 写法，`res += diff / k` 的整数除法已改为 `//`',
                 '对比灵神：灵神把 k=0 判断放进循环里；yiduobo 先单独处理'],
    ),
)
