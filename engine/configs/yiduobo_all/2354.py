CONFIG = dict(
    num=2354, title='优质数对的数目', difficulty='Hard', category='位运算',
    author='yiduobo', technique='数 1 的个数 · 后缀和 f',
    tags=['灵神题单·位运算', '位运算 · 六、恒等式', '难度分 2076'],
    code='''
class Solution(object):
    def countExcellentPairs(self, nums, k):

        nums = list(set(nums))

        cnt_list = []
        f = [0] * 31
        for num in nums:
            cnt = 0
            while num:
                cnt += 1
                num -= num & -num
            
            cnt_list.append(cnt)
            f[cnt] += 1
        
        for index in range(29, -1, -1):
            f[index] += f[index + 1]

        res = 0
        for cnt in cnt_list:
            if cnt >= k:
                res += f[0]
            elif k - cnt <= 30:
                res += f[k - cnt]
        
        return res
''',
    call='Solution().countExcellentPairs([1, 2, 3, 1], 3)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（去重）', h=150),
        dict(type='array', var='cnt_list', label='cnt_list：每个数二进制里 1 的个数', h=170),
        dict(type='array', var='f', label='f[i]：1 的个数 >= i 的数有几个', h=240,
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: i > 6 and v == 0),
        dict(type='text', size=28, h=110,
             fn=lambda S: (f"当前 `cnt = {S['cnt']}`，缺口 `k − cnt = {S['k'] - S['cnt']}` → 要找 `f[{S['k'] - S['cnt']}]` = =={S['f'][S['k'] - S['cnt']] if 0 <= S['k'] - S['cnt'] <= 30 else 0}==" if S['_line'] >= 22 and 'cnt' in S and 'res' in S else '')),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'nums = list(set(nums))': '先去重：相同数对只算一次，`nums = {nums}`',
        'f = [0] * 31': '`f[i]` 先记「恰好有 i 个 1 的数」的个数，后面再做后缀和',
        'num -= num & -num': '`num & -num` 是最低位的 1，减掉它 → `num = {num}`，`cnt = {cnt}`',
        'f[cnt] += 1': '这个数有 `{cnt}` 个 1：`f[{cnt}]` → =={f[cnt]}==',
        'f[index] += f[index + 1]': '后缀和：`f[{index}]` 加上 `f[{index + 1}]` → =={f[index]}==（1 的个数 >= {index} 的数）',
        'if cnt >= k': lambda S, B, r: (f"`cnt = {S.cnt} >= k = {S.k}`：自己已经够了，任何数都能配 → 加 `f[0] = {S.f[0]}`"
                                        if S.cnt >= S.k else f"`cnt = {S.cnt} < k = {S.k}`：还缺 `{S.k - S.cnt}` 个 1"),
        'res += f[0]': '去重后一共 `{f[0]}` 个数，全都能配 → `res` = =={res}==',
        'elif k - cnt <= 30': '缺口 `k - cnt = {k - cnt}`，不超过 30 才可能补上',
        'res += f[k - cnt]': '能补上缺口的数有 `f[{k - cnt}] = {f[k - cnt]}` 个 → `res` = =={res}==',
    },
    max_steps=66,
    cards=dict(
        one_liner='或与与的 1 总数 = 两数各自 1 的个数之和',
        complexity='时间 `O(n·log U)`，空间 `O(n)`',
        problem=['数对 `(a, b)` 都来自 `nums`，`a|b` 与 `a&b` 里 1 的个数之和 `>= k` 就是优质数对',
                 '同一个数可以和自己配，相同数对只算一次',
                 '示例：`nums = [1,2,3,1]`，`k = 3` → `5`'],
        quote='题目要找的1的数目恰好就是cnt1 + cnt2。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a|b` 的 1 的数目 = cnt1 + cnt2 − 两数都为 1 的位数，而减掉的恰是 `a&b` 的 1 的数目',
              '于是只需算每个数的 1 的个数 `cnt`，再对 `cnt` 做后缀和得到 `f`',
              '对每个数：缺口 `k - cnt` 由 `f[k - cnt]` 个数补上；`cnt >= k` 时配所有数'],
        summary=['时间 `O(n·log U)`，空间 `O(n)`',
                 '原文为 Python 2 写法，已删去类型说明；`num & -num` 逐个消去低位的 1 来数个数',
                 '易错点：先去重；`cnt >= k` 时加的是去重后总数 `f[0]`',
                 '对比灵神：灵神先按 1 的个数分组再配对；yiduobo 逐个数查后缀和'],
    ),
)
