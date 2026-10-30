def _inf(v):
    return '∞' if v == float('inf') else str(v)


def _cand(S):
    m = S['min_s']
    return min(m.get(S['x'] - S['k'], float('inf')), m.get(S['x'] + S['k'], float('inf')))


def _txt(S):
    if 'x' not in S:
        return '好子数组 `a[i..j]` 的和 = `s[j+1] − s[i]`：枚举 j，让 `s[i]` 尽量小'
    c = _cand(S)
    ctext = '无' if c == float('inf') else str(c)
    return f"当前 `x = {S['x']}`：要找的开头是 `{S['x'] - S['k']}` 或 `{S['x'] + S['k']}`，其中最小前缀和 = =={ctext}=="


CONFIG = dict(
    num=3026, title='最大好子数组和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表',
    tags=['难度分 1817'],
    code='''
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        min_s = defaultdict(lambda: inf)
        s = 0
        ans = -inf
        for x in nums:
            ans = max(ans, s + x - min(min_s[x - k], min_s[x + k]))
            min_s[x] = min(min_s[x], s)
            s += x
        return ans if ans > -inf else 0
''',
    call='Solution().maximumSubarraySum([-1,3,2,4,5], 3)',
    expect=11,
    views=[
        dict(type='array', var='nums', h=200, label='nums（蓝色 = 当前右端点 j）',
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] and i == S['nums'].index(S['x']) else None),
        dict(type='map', var=lambda S: {k: v for k, v in S['min_s'].items() if v != float('inf')}, label='min_s：键 = a[i]，值 = 它之前出现位置的最小前缀和 s[i]',
             fmt=lambda k, v: f'{k}: {_inf(v)}', h=250, font=28),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('x', 'x', 'blue'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'min_s = defaultdict': '`min_s` 记录每个值 `a[i]` 对应的最小 `s[i]`，缺省为 `inf`（视图里只画有值的键）',
        's = 0': '`s` 是 `x` 之前所有数的和，也就是 `s[j]`',
        'ans = -inf': '`ans` 初始为 `-inf`，最后没有好子数组就返回 0',
        'ans = max': lambda S, B, r: (f"以 `{S.x}` 结尾：开头只能是 `{S.x - S.k}` 或 `{S.x + S.k}`，最小前缀和 `{'无' if _cand(S) == float('inf') else _cand(S)}`"
                                      + ('，没有这样的开头 → ans 不变' if _cand(S) == float('inf') else f"；子数组和 = `{B.s} + {S.x} − {_cand(S)}` = =={B.s + S.x - _cand(S)}== → `ans = {S.ans}`")),
        'min_s[x] = min': lambda S, B, r: (f"把 `{S.x}` 登记为以后的开头：`min_s[{S.x}] = min({_inf(B.min_s.get(S.x, float('inf')))}, {S.s}) = {S.min_s[S.x]}`"
                                           + ('（取更小的前缀和）' if B.min_s.get(S.x, float('inf')) <= S.s else '（第一次出现，直接记下）')),
        's += x': '`s` 加上 `x`，变成 `{s}`，给下一个数当前缀和',
        'return ans': lambda S, B, r: f'最大好子数组和 = =={r}==' if S.ans > -float('inf') else '没有好子数组，返回 0',
    },
    cards=dict(
        one_liner='枚举右端点 j，在哈希表里找“值差为 k”的最小前缀和当左端点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 和正整数 `k`，子数组首尾元素之差的绝对值恰好为 `k` 就是“好”的',
                 '求所有好子数组的最大和，没有则返回 `0`',
                 '示例：`[-1,3,2,4,5]`，`k = 3` → `11`（子数组 `[2,4,5]`）'],
        quote='枚举 j，我们需要找到最小的 s[i]，满足 |a[i]-a[j]|=k，即 a[i] = a[j]-k 或 a[i]=a[j]+k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组和 = `s[j+1] − s[i]`，右端点固定后要让 `s[i]` ==尽量小==',
              '哈希表 `min_s[v]`：值为 `v` 的开头里，最小的前缀和',
              '每个 `x` 查两次：`x−k` 与 `x+k`；查完再把自己登记进去'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：==先用 `s` 算答案，再登记 `min_s[x]`，最后才 `s += x`==，顺序反了前缀和会错位',
                 '`defaultdict(lambda: inf)` 读取缺失键会插入 `inf`，不影响结果',
                 '答案可能为负（示例 3 是 `-6`），所以 `ans` 初始值用 `-inf` 而不是 0',
                 '同类：974 和可被 K 整除的子数组'],
    ),
)
