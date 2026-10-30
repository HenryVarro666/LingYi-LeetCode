def _need(S):
    if 'x' not in S or 's' not in S or 'p' not in S:
        return ''
    if 'i' not in S:
        return f"目标：移除的子数组和 ≡ `x = {S['x']}`（mod {S['p']}）"
    return (f"前缀和 `s = {S['s']}`，`s % p = {S['s'] % S['p']}`；要找的余数 `(s − x) % p` = =={(S['s'] - S['x']) % S['p']}==，"
            f"目标 `x = {S['x']}`")


CONFIG = dict(
    num=1590, title='使数组和能被 P 整除', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表 · 同余',
    tags=['前缀和与哈希表', '同余', '难度分 2039'],
    code='''
class Solution:
    def minSubarray(self, nums: List[int], p: int) -> int:
        x = sum(nums) % p
        if x == 0:
            return 0  # 移除空子数组（这行可以不要）

        ans = n = len(nums)
        s = 0
        last = {s: -1}  # 由于下面 i 是从 0 开始的，前缀和下标就要从 -1 开始了
        for i, v in enumerate(nums):
            s += v
            last[s % p] = i
            j = last.get((s - x) % p, -n)  # 如果不存在，-n 可以保证 i-j >= n
            ans = min(ans, i - j)  # 改成手写 min 会再快一些
        return ans if ans < n else -1
''',
    call='Solution().minSubarray([6,3,5,2], 9)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=200, cell=110,
             color=lambda S, i, v: 'green' if 'i' in S and 'j' in S and S['j'] < i <= S['i'] and S['i'] - S['j'] == S['ans'] and S['ans'] < S['n'] else None),
        dict(type='map', var='last', label='last：余数 → 最近一次出现的前缀下标', fmt=lambda k, v: f'{k}: {v}', h=210, font=32),
        dict(type='text', h=110, size=28, fn=_need),
    ],
    watch=[('x', 'x', 'orange'), ('i', 'i', 'blue'), ('s', 's', 'cyan'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'x = sum(nums) % p': '总和 `{sum(nums)}`，`x = {sum(nums)} % {p} = {x}`：要移除的子数组和必须 ≡ `{x}`（模 `{p}`）',
        'if x == 0': lambda S, B, r: ('`x = 0`：总和已经能被 p 整除，不用移除' if S.x == 0 else f'`x = {S.x} ≠ 0`：必须移除一段和 ≡ {S.x} 的子数组'),
        'return 0': '移除空子数组，长度 `0`',
        'ans = n = len': '`n = {n}`：答案先设成 n（不允许全部移除，最后等于 n 就是无解）',
        's = 0': '前缀和 `s` 从 0 开始',
        'last = {s: -1}': '空前缀（下标 -1）的余数是 0：`last = {last}`',
        'for i, v in enumerate': lambda S, B, r: (f'枚举 `nums[{S.i}] = {S.v}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        's += v': '前缀和 `s = {B.s} + {v} = {s}`',
        'last[s % p] = i': '==先更新 last==（可以移除空子数组）：余数 `{s % p}` 最近出现在下标 `{i}`',
        'j = last.get': lambda S, B, r: (f'要找的余数 `(s − x) % p = ({S.s} − {S.x}) % {S.p} = {(S.s - S.x) % S.p}`，'
                                         + (f'它最近在下标 `{S.j}` → 移除 `({S.j}, {S.i}]`，长 `{S.i - S.j}`' if S.j > -S.n
                                            else '`last` 里没有 → j = -n，保证长度 ≥ n，不会更新答案')),
        'ans = min': '`ans = min({B.ans}, i−j={i - j}) = {ans}`',
        'return ans if': lambda S, B, r: (f'`ans = {S.ans} < n = {S.n}` → 返回 `{S.ans}`' if S.ans < S.n else f'`ans = n` → 无解，返回 `-1`'),
    },
    cards=dict(
        one_liner='移走的子数组和 ≡ 总和（模 p）：前缀和余数查哈希表',
        complexity='时间 `O(n)`，空间 `O(min(n, p))`',
        problem=['删去一段最短的连续子数组（可为空，不能删光），让剩余元素和能被 `p` 整除',
                 '示例：`nums = [6,3,5,2], p = 9` → `2`（删去 `[5,2]`，剩 `6+3 = 9`）'],
        quote='设 nums 的元素和为 x，去掉的子数组和为 y。x−y 能被 p 整除……等价于 y ≡ x (mod p)',
        quote_src='—— 灵茶山艾府题解 · 提示 1',
        idea=['总和余数 `x`，删去的子数组和余数必须也是 `x`（同余）',
              '子数组和 = 两个前缀和之差 → 移项：`(s − x) % p` 要等于左端前缀的余数',
              '用哈希表 `last` 记每个余数最近出现的下标，越近越短'],
        summary=['时间 `O(n)`，空间 `O(min(n, p))`',
                 '易错：可以删空子数组，所以==先更新 last，再查==',
                 '`x % p` 的差要用 `(s - x) % p`，Python 的取模结果已非负',
                 '答案初始为 n：不允许删光，最后等于 n 说明无解返回 -1',
                 '另一种写法：先用 `accumulate` 求前缀和数组，思路相同'],
    ),
)
