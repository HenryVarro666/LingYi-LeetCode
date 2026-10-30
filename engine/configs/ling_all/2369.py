def _case(S):
    i, x, nums, f = S['i'], S['x'], S['nums'], S['f']
    if i > 0 and f[i - 1] and x == nums[i - 1]:
        return '两个相等'
    if i > 1 and f[i - 2] and x == nums[i - 1] == nums[i - 2]:
        return '三个相等'
    if i > 1 and f[i - 2] and x == nums[i - 1] + 1 == nums[i - 2] + 2:
        return '三个连续递增'
    return None


def _if_cap(S, B, ret):
    i, x, nums, f = S.i, S.x, S.nums, S.f
    c = _case(S)
    if c == '两个相等':
        return f'`f[{i-1}]` 为真，且 `nums[{i}] = nums[{i-1}] = {x}`：最后两个数相等 → ==能划分=='
    if c == '三个相等':
        return f'`f[{i-2}]` 为真，且最后三个数都是 `{x}` → ==能划分=='
    if c == '三个连续递增':
        return f'`f[{i-2}]` 为真，且最后三个数是 `{nums[i-2]},{nums[i-1]},{x}` 连续递增 → ==能划分=='
    return f'`nums[{i}]` 结尾的三种划分都凑不出来：`f[{i+1}]` 保持 ==False=='


CONFIG = dict(
    num=2369, title='检查数组是否存在有效划分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（判定能否划分）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1780'],
    code='''
class Solution:
    def validPartition(self, nums: List[int]) -> bool:
        n = len(nums)
        f = [True] + [False] * n
        for i, x in enumerate(nums):
            if i > 0 and f[i - 1] and x == nums[i - 1] or \\
               i > 1 and f[i - 2] and (x == nums[i - 1] == nums[i - 2] or
                                       x == nums[i - 1] + 1 == nums[i - 2] + 2):
               f[i + 1] = True
        return f[n]
''',
    call='Solution().validPartition([4,4,4,5,6])',
    expect=True,
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (f"`f[{S['i']+1}]`：前 {S['i']+1} 个数能否有效划分？看最后 2 或 3 个数" if 'i' in S else '`f[k]` = 前 k 个数能否有效划分，`f[0] = True`')),
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             color=lambda S, k, v: ('yellow' if k == S['i'] else 'blue' if S['i'] - 2 <= k < S['i'] else None) if 'i' in S else None,
             pointers={'i': 'yellow'}),
        dict(type='array', var='f', label='f（f[k]：前 k 个数能否有效划分）', h=190, cell=96,
             color=lambda S, k, v: 'green' if v is True else ('yellow' if 'i' in S and k == S['i'] + 1 else None)),
    ],
    watch=['i', 'x', ('f[i+1]', "f[i+1] if 'i' in S else None", 'green')],
    skip=['n = len', 'i > 1 and f[i - 2]', 'x == nums[i - 1] + 1'],
    captions={
        'f = [True]': '`f[0] = True`：空数组算有效划分；其余先设为 `False`，`f` 长 {len(f)}',
        'for i, x in enumerate': lambda S, B, r: ('`nums` 枚举完了，答案看 `f[n]`' if 'i' in B and B.i == S.i else f'枚举 `nums[{S.i}] = {S.x}` 作为前 `{S.i+1}` 个数的最后一个数'),
        'if i > 0 and f[i - 1]': _if_cap,
        'f[i + 1] = True': '`f[{i+1}] = True`：前 {i+1} 个数可以有效划分',
        'return f[n]': '`f[{n}] = {f[n]}`：整个数组{"能" if f[n] else "不能"}有效划分',
    },
    cards=dict(
        one_liner='看最后 2 或 3 个数，去掉它们，问题变小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把数组切成若干连续段，每段只能是：`[a,a]`、`[a,a,a]`、`[a,a+1,a+2]`',
                 '示例：`[4,4,4,5,6]` → `true`（`[4,4]` + `[4,5,6]`）',
                 '示例：`[1,1,1,2]` → `false`'],
        quote='我们要解决的问题都形如「nums 的前 i 个数能否有效划分」。于是定义 f[0] = true，f[i+1] 表示能否有效划分 nums[0] 到 nums[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['看最后两个数相等：去掉它们，剩下 `i-1` 个数要能划分',
              '看最后三个数相等或连续递增：去掉它们，剩下 `i-2` 个数要能划分',
              '三种情况只要有一种成立，`f[i+1]` 就是 ==True==；答案 `f[n]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f[i+1]` 对应 `nums[i]`：下标差一位，别写错',
                 '注意 `i > 0`、`i > 1` 的边界判断，防止下标越界',
                 '思考题：改成统计划分方案数（模 `10^9+7`），把 `or` 改成相加'],
    ),
)
