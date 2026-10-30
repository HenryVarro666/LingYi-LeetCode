CONFIG = dict(
    num=2910, title='合法分组的最少组数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='先枚举 k，再贪心',
    tags=['灵神题单', '交换论证法', '难度分 2132'],
    code='''
class Solution:
    def minGroupsForValidAssignment(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        for k in range(min(cnt.values()), 0, -1):
            ans = 0
            for c in cnt.values():
                q, r = divmod(c, k)
                if q < r:
                    break
                ans += (c + k) // (k + 1)
            else:
                return ans
''',
    call='Solution().minGroupsForValidAssignment([1,1,1,2,2,2,2,2,3,3,3])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=150, label='nums'),
        dict(type='map', var='cnt', h=200, label='cnt：每个数出现次数'),
        dict(type='text', h=90, fn=lambda S: (f"组大小为 `{S['k']}` 和 `{S['k']+1}`：`{S['c']} = {S['q']}×{S['k']} + {S['r']}`，" + ('==q < r 不行==' if S['q'] < S['r'] else '==q ≥ r 可以==')) if S['_line'] in (8, 9, 10) and all(x in S for x in ('k', 'c', 'q', 'r')) else (f"当前枚举 k = `{S['k']}`" if 'k' in S else '')),
    ],
    watch=['k', 'c', 'q', 'r', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '先数每个数出现几次：`cnt = {cnt}`',
        'for k in range': '从最小出现次数 `{min(cnt.values())}` 倒着枚举 `k`，==越大组数越少==，第一个可行的就是答案。现在 `k = {k}`',
        'ans = 0': '换一个 `k`，累计组数清零',
        'for c in cnt.values()': '检查数字出现次数 `c = {c}` 能否拆成 `{k}` 和 `{k+1}` 的组',
        'divmod': '`{c} = {q} × {k} + {r}`：先分出 {q} 组大小 {k}，余 {r} 个，每个余数分给一个组变成 {k+1}',
        'if q < r': lambda S, B, ret: (f"`q = {S.q} < r = {S.r}`：组数不够装余数 → ==这个 k 不行==，换更小的 k" if S.q < S.r else f"`q = {S.q} ≥ r = {S.r}`：每个余数都有组可加 → 可以"),
        'ans += ': '在可行前提下 `k+1` 越多组越少：`ceil({c}/{k+1}) = ({c}+{k})//{k+1}` = {(c+k)//(k+1)} 组，累计 `ans = {ans}`',
        'return ans': '所有数字都能分：`k = {k}` 可行，答案 =={ans}==（for-else：没 break 才走 else）',
    },
    cards=dict(
        one_liner='枚举组大小 k，每个数尽量多分出 k+1 的大组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['盒子里的球编号必须相同，最大盒子最多比最小盒子多 1 个球',
                 '求最少盒子数，例如 `[3,2,3,2,3]` → `2`',
                 '本视频：`[1,1,1,2,2,2,2,2,3,3,3]` → `4`'],
        quote='设 q = ⌊cnt[x]/k⌋，r = cnt[x] mod k。如果 q < r 则无法分成 k 和 k+1 组，否则一定可以分组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用哈希表数出现次数，假设所有组大小只能是 `k` 或 `k+1`',
              '余数 `r` 要靠 `q` 个组各加 1 吸收，所以 ==q ≥ r== 才行',
              '可行时尽量用 `k+1` 的大组：`ceil(c/(k+1))` 组；从大到小枚举 `k`，首个可行即最优'],
        summary=['时间 `O(n)`：哈希表大小 m、最小次数 k 满足 km ≤ n，循环至多 km 次',
                 '易错：`for-else` 里 `else` 只在没 `break` 时执行',
                 '`(c+k)//(k+1)` 是 `ceil(c/(k+1))` 的整数写法',
                 '与「先枚举，再贪心」同类：枚举一个量，再对其余部分贪心'],
    ),
)
