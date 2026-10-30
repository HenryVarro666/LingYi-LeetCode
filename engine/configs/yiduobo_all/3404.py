from math import gcd as _g

NUMS = [1, 2, 3, 4, 3, 6, 1, 2]


def _k(k, v):
    return f'{k[0]}/{k[1]}: {v}'


def _region(S, i, v):
    r = S.get('r')
    if r is None:
        return None
    if i == r:
        return 'pink'
    if i == r - 2:
        return 'blue'
    if i < r - 3:
        return 'cyan'
    if i >= r + 2:
        return 'orange'
    return None


def _txt(S):
    r = S.get('r')
    if r is None:
        return '`nums[p]*nums[r] = nums[q]*nums[s]` 变形成 `nums[p]/nums[q] = nums[s]/nums[r]`'
    nums = S['nums']
    q = r - 2
    base = f'q = r-2 = {q}（值 {nums[q]}），r = {r}（值 {nums[r]}）'
    ln = S.get('_line')
    if ln in (17, 18, 19, 20, 21, 22, 23) and 'p' in S:
        return base + f"；左边比值 `{nums[S['p']]}/{nums[q]}`"
    if ln in (25, 26, 27, 28, 29, 30, 31) and 's' in S:
        return base + f"；右边比值 `{nums[S['s']]}/{nums[r]}`，已累计 `res = {S['res']}`"
    return base


CONFIG = dict(
    num=3404, title='统计特殊子序列的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='变形成比值 · 约分后哈希表计数',
    tags=['动态规划', '难度分 2445'],
    code='''
class Solution(object):
    def numberOfSubsequences(self, nums):
        
        n = len(nums)

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        prefix = {}
        res = 0
        for r in range(4, n - 2):
            q = r - 2
            for p in range(q - 1):
                x, y = nums[p], nums[q]
                g = gcd(x, y)
                x //= g
                y //= g
                key = (x, y)
                prefix[key] = prefix.get(key, 0) + 1
        
            for s in range(r + 2, n):
                x = nums[s]
                y = nums[r]
                g = gcd(x, y)
                x //= g
                y //= g
                key = (x, y)
                res += prefix.get(key, 0)
        
        return res
''',
    call=f'Solution().numberOfSubsequences({NUMS})',
    expect=2,
    skip=['for p in range', 'for s in range', 'while y', 'x, y = y', 'return x', 'x, y = nums', 'x = nums[s]', 'y = nums[r]',
          'def gcd', 'x //= g', 'y //= g'],
    views=[
        dict(type='array', var='nums', label='nums（青 = p 的范围，蓝 = q，粉 = r，橙 = s 的范围）', h=220, cell=90,
             color=_region),
        dict(type='map', var='prefix', label='prefix：左边每个约分后的 nums[p]/nums[q] 出现次数', fmt=_k, h=260, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('r', 'r', 'pink'), ('p', 'p', 'blue'), ('s', 's', 'orange'), 'x', 'y', ('res', 'res', 'green')],
    captions={
        'prefix = {}': '`prefix`：键是约分后的 `(分子, 分母)`，值是出现次数',
        'res = 0': '`res` 累计答案',
        'for r in range': lambda S, B, ret: (f'枚举 r = `{S.r}`（值 {S.nums[S.r]}），s 在它右边隔一个以上' if 'r' not in B or S.r != B.r else '`r` 枚举完了'),
        'q = r - 2': '`r` 后移一格时，新增的 q 只有 `r - 2 = {q}`（更前面的 q 早已统计过）',
        'g = gcd': lambda S, B, ret: (f'`gcd({S.x}, {S.y}) = {_g(S.x, S.y)}`：约分后 `{S.x // _g(S.x, S.y)}/{S.y // _g(S.x, S.y)}`'
                                      + ('，用 ==整数对== 当 key，避开浮点误差' if S.get('_line') < 25 else '')),
        'key = (x, y)': '约分后的比值 `key = {key}`',
        'prefix[key] = prefix.get': '左边比值 `{key[0]}/{key[1]}` 又出现一次 → `prefix[{key}] = {prefix[key]}`',
        'res += prefix.get': lambda S, B, ret: (f'右边 `{S.key[0]}/{S.key[1]}` 在左边出现过 `{S.prefix.get(S.key, 0)}` 次 → `res` = =={S.res}=='
                                                 if S.prefix.get(S.key, 0) else f'右边 `{S.key[0]}/{S.key[1]}` 左边没有 → `res` 不变，仍是 {S.res}'),
        'return res': '一共 `{res}` 个特殊子序列',
    },
    max_steps=90,
    cards=dict(
        one_liner='先变形 a/b = d/c，再约分，用整数对当哈希键',
        complexity='时间 `O(n^2 log U)`，空间 `O(n^2)`',
        problem=['找 `p<q<r<s`，三段间隔都大于 1，且 `nums[p]*nums[r] == nums[q]*nums[s]` 的子序列个数',
                 '全是正整数，所以可以做除法',
                 '本视频：`[1,2,3,4,3,6,1,2]` → `2`'],
        quote='由于题目中的除法是实数除法，为了能使用哈希表，因此需要先计算分子分母的最大公约数然后约分，以分子分母对为key的方式来使用哈希表。',
        quote_src='—— yiduobo 题解原文',
        idea=['等式两边错开了，先变形：`nums[p]/nums[q] = nums[s]/nums[r]`',
              '枚举靠右的 r、s；左边的 p、q 比值放哈希表，r 每右移一格只新增 `q = r - 2`',
              '比值先除以 gcd 约分，`(分子, 分母)` 作为键，避免小数误差'],
        summary=['时间 `O(n^2 log U)`，空间 `O(n^2)`',
                 '键的方向：左边存 `(p/q)`，右边查 `(s/r)`，不能反过来',
                 '间隔限制：`p` 取 `range(q-1)`，`s` 从 `r+2` 起',
                 '原文已是 Python 3 可运行写法，无需改动',
                 '对比灵神：灵神用浮点 `a/b` 当键，yiduobo 用约分后的整数对'],
    ),
)
