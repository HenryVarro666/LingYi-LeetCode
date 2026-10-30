import math

N0 = [2, 4, 8, 16]


def _info(S):
    if 'pre_gcd' in S:
        i = S['i']
        return (f"去掉 `nums[{i}]={S['x']}`：gcd(前 {S['pre_gcd']}, 后 {S['suf_gcd'][i + 1]}) × lcm(前 {S['pre_lcm']}, 后 {S['suf_lcm'][i + 1]})"
                f" = =={math.gcd(S['pre_gcd'], S['suf_gcd'][i + 1]) * math.lcm(S['pre_lcm'], S['suf_lcm'][i + 1])}==") if S.get('_line') == 13 else '`gcd(0, x) = x`、`lcm(1, x) = x`：空前缀/后缀用 0 和 1 占位'
    return '`gcd(0, x) = x`、`lcm(1, x) = x`：空前缀/后缀用 0 和 1 占位'


CONFIG = dict(
    num=3334, title='数组的最大因子得分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 GCD / LCM',
    tags=['动态规划', '数学算法', '专题：前后缀分解', '难度分 1519'],
    code='''
class Solution:
    def maxScore(self, nums: List[int]) -> int:
        n = len(nums)
        suf_gcd = [0] * (n + 1)
        suf_lcm = [0] * n + [1]
        for i in range(n - 1, -1, -1):
            suf_gcd[i] = gcd(suf_gcd[i + 1], nums[i])
            suf_lcm[i] = lcm(suf_lcm[i + 1], nums[i])

        ans = suf_gcd[0] * suf_lcm[0]  # 不移除元素
        pre_gcd, pre_lcm = 0, 1
        for i, x in enumerate(nums):  # 枚举移除 nums[i]
            ans = max(ans, gcd(pre_gcd, suf_gcd[i + 1]) * lcm(pre_lcm, suf_lcm[i + 1]))
            pre_gcd = gcd(pre_gcd, x)
            pre_lcm = lcm(pre_lcm, x)
        return ans
''',
    call=f'Solution().maxScore({N0!r})',
    expect=64,
    setup='from math import gcd, lcm',
    skip=['n = len', 'for i in range', 'for i, x in'],
    views=[
        dict(type='text', fn=_info, size=25, h=60),
        dict(type='array', var='nums', label='nums', h=150, cell=90,
             color=lambda S, i, v: ('pink' if i == S['i'] else None) if S.get('_line', 0) >= 13 and 'x' in S else ('blue' if i == S.get('i') else None)),
        dict(type='array', var='suf_gcd', label='suf_gcd[i]：nums[i..] 的 gcd', h=150, cell=90,
             color=lambda S, i, v: 'cyan' if i == S.get('i') and S.get('_line', 0) <= 9 else ('green' if S.get('_line', 0) >= 13 and 'x' in S and i == S['i'] + 1 else None)),
        dict(type='array', var='suf_lcm', label='suf_lcm[i]：nums[i..] 的 lcm', h=150, cell=90,
             color=lambda S, i, v: 'orange' if i == S.get('i') and S.get('_line', 0) <= 9 else ('green' if S.get('_line', 0) >= 13 and 'x' in S and i == S['i'] + 1 else None)),
    ],
    watch=[('i', 'i', 'blue'), ('pre_gcd', 'pre_gcd', 'cyan'), ('pre_lcm', 'pre_lcm', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'suf_gcd = [0]': '`suf_gcd[n]` = 0：因为 ==gcd(0, x) = x==，空后缀不影响结果',
        'suf_lcm = [0]': '`suf_lcm[n]` = 1：因为 ==lcm(1, x) = x==，空后缀不影响结果',
        'suf_gcd[i] = gcd': '`suf_gcd[{i}] = gcd({suf_gcd[i+1]}, {nums[i]})` = =={suf_gcd[i]}==：从右往左，`nums[{i}..]` 的最大公约数',
        'suf_lcm[i] = lcm': '`suf_lcm[{i}] = lcm({suf_lcm[i+1]}, {nums[i]})` = =={suf_lcm[i]}==：`nums[{i}..]` 的最小公倍数',
        'ans = suf_gcd[0]': '不移除元素：`gcd × lcm = {suf_gcd[0]} × {suf_lcm[0]}` = =={ans}==，先当作答案',
        'pre_gcd, pre_lcm = 0, 1': '前缀同样从「空」开始：`pre_gcd = 0`，`pre_lcm = 1`',
        'ans = max(': '枚举去掉 `nums[{i}] = {x}`：前后拼起来 `gcd({pre_gcd}, {suf_gcd[i+1]}) × lcm({pre_lcm}, {suf_lcm[i+1]})`，`ans` = {B.ans} → =={ans}==',
        'pre_gcd = gcd': '把 `{x}` 并进前缀：`pre_gcd` → {pre_gcd}（下一个位置用）',
        'pre_lcm = lcm': '把 `{x}` 并进前缀：`pre_lcm` → {pre_lcm}',
        'return ans': '最大因子得分 =={ret}==',
    },
    cards=dict(
        one_liner='去掉一个数 = 它左边的前缀 + 右边的后缀拼起来',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['因子得分 = 数组所有元素的 ==LCM × GCD==；最多移除一个元素，求最大因子得分',
                 '空数组得分为 0；单个数字 LCM、GCD 都是它自己',
                 '示例：`[2,4,8,16]` → `64`（移除 2，gcd 4 × lcm 16）'],
        quote='思路同 238. 除自身以外数组的乘积，本题维护前后缀的 GCD 和 LCM。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`suf_gcd`、`suf_lcm` 存每个后缀的 GCD、LCM',
              '正着枚举移除 `nums[i]`，前缀用变量 `pre_gcd`、`pre_lcm` 滚动',
              '去掉 `nums[i]` 后：`gcd(前缀, 后缀) × lcm(前缀, 后缀)`',
              '空的一侧用 `gcd(0,x)=x`、`lcm(1,x)=x` 当作单位元，不用特判'],
        summary=['时间 `O(n log U)`（`U` 是最大值），空间 `O(n)`',
                 '易错：`suf_gcd` 末尾要放 0，`suf_lcm` 末尾要放 1，别写反',
                 '==先用 pre 算答案，再把 nums[i] 并进 pre==，否则去掉的数还在前缀里',
                 '`math.lcm` 需要 Python 3.9+，已在 setup 里 import',
                 '同类：238. 除自身以外数组的乘积'],
    ),
)
