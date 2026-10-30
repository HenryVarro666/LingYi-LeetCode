CONFIG = dict(
    num=1726, title='同积元组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表统计乘积 · 组合数',
    code='''
class Solution:
    def tupleSameProduct(self, nums):

        cnt_dict = {}
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                m = nums[i] * nums[j]
                cnt_dict[m] = cnt_dict.get(m, 0) + 1
        
        res = 0
        for cnt in cnt_dict.values():
            res += cnt * (cnt - 1) * 4
        
        return res
''',
    call='Solution().tupleSameProduct([2,3,4,6])',
    expect=8,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('i') and 'j' in S else ('pink' if i == S.get('j') else None)),
        dict(type='map', var='cnt_dict', label='cnt_dict：乘积 → 出现次数', h=200),
        dict(type='text', h=70, fn=lambda S: (f"`nums[{S['i']}] × nums[{S['j']}] = {S['nums'][S['i']]} × {S['nums'][S['j']]}` = =={S['m']}=="
                                              if 'm' in S and 'j' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('m', 'm', 'cyan'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '`cnt_dict` 记录每个乘积出现了几次',
        'for i in range': '`i` 当前枚举到 `{i}`',
        'for j in range': '`j` 取 `i` 后面的 `{j}`：保证 `i < j`，每一对只数一次',
        'm = nums[i]': '这一对的乘积：`{nums[i]} × {nums[j]}` = =={m}==',
        'cnt_dict[m] =': '乘积 `{m}` 出现次数 → =={cnt_dict[m]}==',
        'for cnt in': '这个乘积出现了 `{cnt}` 次',
        'res += cnt * (cnt - 1) * 4': '任选 2 对：`C({cnt},2)` 种，每种能排出 8 个元组，合起来 `{cnt}×({cnt}-1)×4 = {cnt*(cnt-1)*4}` → `res` = =={res}==',
        'return res': '一共 `{res}` 个元组',
    },
    cards=dict(
        one_liner='乘积相同的两对数，能排出 8 个元组：统计每个乘积出现几次',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`nums` 中元素互不相同，求满足 `a*b == c*d` 的元组 `(a,b,c,d)` 数量',
                 '`a,b,c,d` 取自 `nums` 且互不相同，顺序不同算不同的元组',
                 '示例：`[2,3,4,6]` → `8`（`2*6 == 3*4`）'],
        quote='若某个乘积一共出现了k次，那么从中任选两组数，就是C(k, 2)中选法，每种选法提供8种答案，那么这里就有k * (k - 1) * 4种答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先去重：保证 `i < j`，每一对数只算一次',
              '用哈希表数出每个乘积有几对',
              '选出两对，`(a,b)` 和 `(c,d)` 各自可交换、两对也可互换：2×2×2 = 8 种排法'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '`C(k,2)×8 = k(k-1)×4`，不用除法',
                 '`nums` 元素互不相同，所以同一乘积的两对一定没有公共元素',
                 '原文为 Python 2 风格，仅把 `Solution(object)` 改为 `Solution`'],
    ),
)
