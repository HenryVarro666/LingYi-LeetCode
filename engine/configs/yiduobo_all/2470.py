def _row(S):
    if 'i' not in S:
        return ''
    if 'j' not in S:
        return f"枚举左端点 `i = {S['i']}`，`now = 1`（空数组的 LCM）"
    return f"子数组 `nums[{S['i']}..{S['j']}]`，当前 `now = {S.get('now', 1)}`，`k = {S['k']}`"


CONFIG = dict(
    num=2470, title='最小公倍数等于 K 的子数组数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举左右端点 + 增量求 LCM',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def subarrayLCM(self, nums, k):

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        res = 0
        for i in range(len(nums)):
            now = 1
            for j in range(i, len(nums)):
                g = gcd(now, nums[j])
                now = now * nums[j] // g
                if now == k:
                    res += 1
        
        return res
''',
    call='Solution().subarrayLCM([3, 6, 2], 6)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 左端点 i，粉 = 右端点 j，框 = 当前子数组）', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=190,
             color=lambda S, i, v: 'green' if 'now' in S and S['now'] == S['k'] and 'j' in S and S['i'] <= i <= S['j'] else None),
        dict(type='text', fn=_row, size=32, h=90),
        dict(type='text', fn=lambda S: (f"`lcm(a, b) = a × b ÷ gcd(a, b)`　`now = {S['now']}`" if 'now' in S else '`lcm(a, b) = a × b ÷ gcd(a, b)`'), size=32, h=80),
    ],
    watch=['i', 'j', ('now', 'now', 'cyan'), ('g', 'g', 'purple'), ('res', 'res', 'green')],
    captions={
        'while y': lambda S, B, r: (f'`y = {S.y}` 不为 0，继续辗转相除' if S.y else '`y = 0`，gcd 求完'),
        'x, y = y, x % y': '`x, y = {x}, {y}`',
        'return x': 'gcd = `{x}`',
        'res = 0': '`res` 统计 LCM 恰为 k 的子数组数',
        'for i in range': '枚举子数组左端点 `i = {i}`',
        'now = 1': '`now` 记录当前子数组的 LCM，从 1 开始（对 LCM 是单位元）',
        'for j in range': '向右扩展右端点 `j = {j}`，子数组 `nums[{i}..{j}]`',
        'g = gcd': '求 `gcd(now, nums[j]) = gcd({now}, {nums[j]})`：进入 gcd 辗转相除',
        'now = now': '新 LCM = `{B.now} × {nums[j]} ÷ {g} = {now}`（不能直接滑窗，所以暴力增量算）',
        'if now == k': lambda S, B, r: (f'`now = {S.now}` == `k = {S.k}` → 这个子数组满足' if S.now == S.k else f'`now = {S.now}` ≠ `k = {S.k}`，不计数'),
        'res += 1': '找到一个：`res` → {res}',
        'return res': '一共 `{res}` 个子数组',
    },
    cards=dict(
        one_liner='窗口左端移动时 LCM 没法撤销，干脆暴力：左端固定，右端增量求 LCM',
        complexity='时间 `O(n^2 log U)`，空间 `O(1)`',
        problem=['统计 `nums` 中 ==最小公倍数恰为 k== 的非空连续子数组个数',
                 '示例：`[3,6,2,7,1]`，`k = 6` → `4`',
                 '本视频：`[3,6,2]`，`k = 6` → `4`'],
        quote='虽然看上去可以用滑动窗口，但是在窗口左边界移动向右移动时，很难直接得出新的子数组的最小公倍数是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['滑窗要求左端点右移时能“撤销”一个数，LCM 做不到',
              '分解质因数统计次数可行，但麻烦',
              '所以枚举左端点 `i`，向右枚举 `j`，用 `lcm = a×b÷gcd` 增量更新 `now`',
              '`now == k` 就计数'],
        summary=['时间 `O(n^2 log U)`，空间 `O(1)`',
                 '`now` 从 1 开始，1 与任何数的 LCM 都是该数',
                 '不剪枝：LCM 超过 k 后仍会继续（灵神用 `k % res` 剪枝）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（否则 now 会变成浮点数）'],
    ),
)
