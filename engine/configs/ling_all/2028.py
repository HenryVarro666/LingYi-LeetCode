CONFIG = dict(
    num=2028, title='找出缺失的观测数据', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='总和相减 + 平均分配',
    tags=[],
    code='''
class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        rem = mean * (n + len(rolls)) - sum(rolls)
        if not n <= rem <= n * 6:
            return []
        avg, extra = divmod(rem, n)
        return [avg + 1] * extra + [avg] * (n - extra)
''',
    call='Solution().missingRolls([1, 5, 6], 3, 4)',
    expect=[3, 2, 2, 2],
    views=[
        dict(type='text', fn=lambda S: (f"总和 `mean × (n + m)` = `{S['mean']} × {S['n'] + len(S['rolls'])}` = {S['mean'] * (S['n'] + len(S['rolls']))}，已知 `sum(rolls)` = {sum(S['rolls'])}" + (f"，缺的 `rem` = =={S['rem']}==" if 'rem' in S else '')), size=26, h=60),
        dict(type='array', var='rolls', label='rolls（已知的 m 次投掷）', cell=84, h=190),
        dict(type='text', fn=lambda S: (f"合法范围：`n ≤ rem ≤ 6n`，即 `{S['n']} ≤ {S['rem']} ≤ {6 * S['n']}`" if 'rem' in S else ''), size=26, h=60),
        dict(type='array', var='[avg + 1] * extra + [avg] * (n - extra)', label='构造：extra 个 avg+1（绿），其余 avg', cell=84, h=190,
             color=lambda S, i, v: 'green' if i < S.get('extra', 0) else None),
    ],
    watch=['rem', 'avg', 'extra'],
    captions={
        'rem = mean': '`rem = {mean} × ({n} + {len(rolls)}) − {sum(rolls)}` = =={rem}==：缺失的 `{n}` 次投掷的总和',
        'if not n <= rem <= n * 6': lambda S, B, r: f"每次投掷在 `[1, 6]`，`{S.n}` 次的和只能在 `[{S.n}, {6 * S.n}]`；`rem = {S.rem}` " + ('==在范围内== → 一定有解' if S.n <= S.rem <= S.n * 6 else '超出范围 → 无解'),
        'return []': 'rem 不在 `[n, 6n]` → 无解，返回空数组',
        'avg, extra = divmod': '`divmod({rem}, {n})`：每次先平均分 `avg = {avg}`，还剩 `extra = {extra}` 没分出去',
        'return [avg + 1]': '把多出的 `{extra}` 分给前 `{extra}` 个：它们取 `avg+1 = {avg + 1}`，其余 `{n - extra}` 个取 `{avg}` → `{ret}`',
    },
    max_steps=40,
    cards=dict(
        one_liner='总和减去已知，剩下的平均分给缺失的 n 次',
        complexity='时间 `O(m+n)`，空间 `O(1)`（返回值不计）',
        problem=['已知 `n+m` 次骰子投掷的平均值 `mean`，只剩 `m` 次记录 `rolls`',
                 '构造缺失的 `n` 次（每次 1~6），使总平均数恰好是 `mean`；无解返回空数组',
                 '示例：`rolls=[1,5,6]`，`mean=3`，`n=4` → 任意合法答案，如 `[3,2,2,2]`'],
        quote='如果 rem 不在区间 [n, 6n] 中，则答案不存在，否则答案一定存在。答案中有 extra 个 avg+1 以及 n-extra 个 avg。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总和 = `mean * (n + m)`，减去已知和得到缺失总和 `rem`',
              '每次投掷 1~6，所以 `rem` 必须落在 `[n, 6n]`，否则无解',
              '有解时一定能构造：`rem` 除以 `n` 取整得 `avg`，余数 `extra` 个位置多加 1'],
        summary=['时间 `O(m+n)`，空间 `O(1)`（不计返回值）',
                 '易错：别漏掉 `rem < n` 的情况（每次至少是 1）',
                 '`divmod` 一次得到商和余数，`avg + 1` 与 `avg` 都不会超过 6',
                 '思考题：若 `rolls` 有序，可用二分/前缀和更快求和；方案数需用 DP 计数'],
    ),
)
