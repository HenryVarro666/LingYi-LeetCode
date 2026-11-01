NUMS = ['777', '7', '77', '77']
TARGET = '7777'


def _tc(S, i, v):
    k = S.get('i')
    if k is None or 'p' not in S:
        return None
    return 'green' if i < k else 'pink'


def _txt(S):
    if 'p' not in S or 's' not in S or 'i' not in S:
        return '把 `target` 劈成「前缀 p + 后缀 s」，看 `nums` 里各有几个 p、几个 s'
    p, s = S['p'], S['s']
    c = S['cnt']
    if p != s:
        return f"`cnt['{p}'] × cnt['{s}']` = {c.get(p, 0)} × {c.get(s, 0)} = =={c.get(p, 0) * c.get(s, 0)}=="
    return f"p = s：`cnt['{p}'] × (cnt['{p}'] − 1)` = {c.get(p, 0)} × {c.get(p, 0) - 1} = =={c.get(p, 0) * (c.get(p, 0) - 1)}=="


CONFIG = dict(
    num=2023, title='连接后等于目标字符串的字符串对', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='哈希计数 · 枚举前后缀（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def numOfPairs(self, nums: List[str], target: str) -> int:
        cnt = defaultdict(int)
        for s in nums:
            cnt[s] += 1
        ans = 0
        n = len(target)
        for i in range(1, n):
            p, s = target[:i], target[i:]  # 枚举所有前缀+后缀
            if p != s:
                ans += cnt[p] * cnt[s]
            else:
                ans += cnt[p] * (cnt[p] - 1)  # 前后缀相同时，相当于从 cnt[p] 个下标中选择两个不同下标的排列数，即 A(cnt[p], 2)
        return ans
''',
    call=f'Solution().numOfPairs({NUMS}, {TARGET!r})',
    expect=4,
    skip=['ans = 0'],
    views=[
        dict(type='array', var='nums', label='nums', cell=110, h=200, font=26,
             color=lambda S, i, v: 'blue' if S.get('s') == v and 'i' not in S else None),
        dict(type='string', var='target', label='target（绿 = 前缀 p，粉 = 后缀 s）', cell=80, h=170, color=_tc),
        dict(type='map', var='cnt', label='cnt（每个字符串在 nums 里出现几次）', h=200,
             fmt=lambda k, v: f"'{k}' : {v}"),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('i', 'i', 'yellow'), ('p', 'p', 'green'), ('s', 's', 'pink'), ('ans', 'ans', 'blue')],
    captions={
        'cnt = defaultdict': '`cnt` 记录 `nums` 里每个字符串出现几次',
        'for s in nums': lambda S, B, r: ('`nums` 全部数完了' if sum(S.cnt.values()) == len(S.nums) else
                                          f"取 `nums` 里的下一个字符串" + (f" `'{S.s}'`" if 's' in S and sum(S.cnt.values()) > 0 or 's' in S else '')),
        'cnt[s] += 1': "`cnt['{s}']` = {cnt[s]}",
        'n = len(target)': '`target = {target}`，长度 `n = {n}`；切点 `i` 从 1 到 `n - 1`',
        'for i in range(1, n)': lambda S, B, r: ('所有切点都试完了' if 'i' in B and S.i == B.i and 'p' in B and 'ans' in B and S.i == S.n - 1 and B.ans == S.ans
                                                 else f'切点 `i = {S.i}`：`target` 劈成前缀和后缀两段'),
        'p, s = target[:i]': '前缀 `p = {p}`，后缀 `s = {s}`：要从 `nums` 里各挑一个，拼起来正好是 `target`',
        'if p != s': lambda S, B, r: (f"`p = '{S.p}'` ≠ `s = '{S.s}'`：前缀、后缀是不同的字符串 → 各选一个，互不冲突" if S.p != S.s
                                      else f"`p = s = '{S.p}'`：前后缀是同一个字符串 → 要小心不能选同一个下标"),
        'ans += cnt[p] * cnt[s]': "`cnt['{p}'] × cnt['{s}']` = {cnt[p]} × {cnt[s]}，`ans` → =={ans}==",
        'ans += cnt[p] * (cnt[p] - 1)': "同一个字符串选两个不同下标：`{cnt[p]} × ({cnt[p]} − 1)` = =={cnt[p] * (cnt[p] - 1)}=={\"，ans → \"}{ans}",
        'return ans': '所有切法加起来，一共 =={ans}== 对',
    },
    cards=dict(
        one_liner='枚举 target 的每个切点，前缀数 × 后缀数',
        complexity='时间 `O(nL + L^2)`（n 个串、target 长 L），空间 `O(n L)`',
        problem=['给你数字字符串数组 `nums` 和 `target`，数 `(i, j)`（`i ≠ j`）使得 `nums[i] + nums[j] == target`',
                 '注意 `(i, j)` 和 `(j, i)` 算两对（顺序不同，拼出来的串不同）',
                 '示例：`["777","7","77","77"]`，`"7777"` → `4`'],
        quote='func numOfPairs(nums []string, target string) (ans int)；p, s := target[:i], target[i:] // 枚举所有前缀+后缀；前后缀相同时，相当于从 cnt[p] 个下标中选择两个不同下标的排列数，即 A(cnt[p], 2)',
        quote_src='—— 灵茶山艾府题解（Go 原文代码注释）',
        idea=['先用 `cnt` 数出每个字符串出现几次',
              '枚举切点：`target = p + s`，满足条件的下标对数 = `cnt[p] × cnt[s]`',
              '`p == s` 时不能选同一个下标：排列数 `cnt[p] × (cnt[p] − 1)`'],
        summary=['时间 `O(nL + L^2)`，空间 `O(nL)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python（`map[string]int{}` → `defaultdict(int)`，`cnt[s]++` → `cnt[s] += 1`）',
                 '易错：`p == s` 时要用 `cnt[p] * (cnt[p] - 1)`，否则会把同一个下标算成一对',
                 '顺序不同算不同的对，所以 `p` 和 `s` 各枚举一次就不用再乘 2'],
    ),
)
