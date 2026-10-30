CONFIG = dict(
    num=2475, title='数组中不等三元组的数目', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逆向思维 · 总数减去不合法',
    tags=[],
    code='''
class Solution(object):
    def unequalTriplets(self, nums):

        n = len(nums)
        cnt = {}
        for num in nums:
            cnt[num] = cnt.get(num, 0) + 1
        
        res = n * (n - 1) * (n - 2) // 6
        for num in cnt:
            if cnt[num] >= 2:
                res -= (cnt[num] * (cnt[num] - 1) // 2) * (n - cnt[num])
                if cnt[num] >= 3:
                    res -= (cnt[num] * (cnt[num] - 1) * (cnt[num] - 2) // 6)
        
        return res
''',
    call='Solution().unequalTriplets([4,4,2,4,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=160),
        dict(type='map', var='cnt', label='cnt：每种数出现次数', fmt=lambda k, v: f'{k}: {v}', h=170),
        dict(type='text', h=130, size=30,
             fn=lambda S: f"`C({S['n']},3)` 共有 `{S['n']*(S['n']-1)*(S['n']-2)//6}` 个三元组，`res` 还剩 ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('num', 'num', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`，三元组总数是 `C(n, 3)`',
        'cnt[num] = cnt.get': '`cnt[{num}]` 变成 `{cnt[num]}`',
        'res = n *': '先算所有三元组 `C({n}, 3) = {res}`，接着减去不合法的',
        'if cnt[num] >= 2': '`cnt[{num}] = {cnt[num]}`：{"至少两个相同，可能有不合法三元组" if cnt[num] >= 2 else "只有一个，不会产生相等的对 → 跳过"}',
        'res -= (cnt[num] * (cnt[num] - 1) // 2)': '恰好两个 `{num}` + 一个别的数：`C({cnt[num]},2) × ({n} − {cnt[num]})` = `{B.res - res}`，`res` → =={res}==',
        'if cnt[num] >= 3': '`cnt[{num}] = {cnt[num]}`：{"三个都是 num 的也不合法，再减 C(cnt,3)" if cnt[num] >= 3 else "凑不出三个相同"}',
        'res -= (cnt[num] * (cnt[num] - 1) * (cnt[num] - 2)': '三个全是 `{num}`：`C({cnt[num]},3) = {B.res - res}`，`res` → =={res}==',
        'return res': '剩下的就是合法三元组：`{res}`',
    },
    cards=dict(
        one_liner='正难则反：总数减去“有两个数相等”的三元组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums`，数 `(i, j, k)` 满足 `i<j<k` 且 `nums` 三个值两两不同',
                 '示例：`[4,4,2,4,3]` → `3`',
                 '数据规模很小，暴力也能过，这里用逆向思维'],
        quote='考虑有多少不符合条件的三元组。一共有C(n, 3)个三元组，其中不符合条件的三元组可以分成其中只有两个数相等以及三个数都相等这两种情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表 `cnt` 统计每种数出现次数',
              '某数出现 `c` 次：恰好两个相等 `C(c,2) × (n−c)`，三个全相等 `C(c,3)`',
              '总数 `C(n,3)` 减去所有这些，就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '两种不合法情况互不重叠，所以可以直接相减',
                 '对比灵神：灵神正面按 `a·b·c` 累加，yiduobo 用总数减不合法'],
    ),
)
