def _brk(S, B, ret):
    d, n, i = S.d, S.n, S.i
    if d * d > n:
        return f'`d² = {d * d} > n = {n}`：下一个数必须 ≥ d，乘起来会超过 n → 后面的因子都不用看，==break=='
    if i > 0 and d - S.path[0] >= S.min_diff:
        return f'`d − path[0] = {d - S.path[0]} ≥ min_diff = {S.min_diff}`：最大值至少是 d，差值已经不可能更小 → ==最优性剪枝 break=='
    return f'`d = {d}`：`d² = {d * d} ≤ {n}`，也没触发最优性剪枝 → 往下试'


def _fill(S, B, ret):
    d, i = S.d, S.i
    if i == 0 or d >= S.path[i - 1]:
        return f'`d = {d}` 不小于上一个数 → 合法，填入 `path[{i}] = {d}`'
    return f'`d = {d} < path[{i - 1}] = {S.path[i - 1]}`：违反「不降」 → 跳过（等效冗余）'


CONFIG = dict(
    num=3669, title='K 因数分解', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='回溯：不降序枚举因子 + 剪枝',
    tags=['难度分 1917'],
    setup='''
# 预处理每个数的因子（原文放在 class 外面；这里放进 setup 不追踪）
MX = 100_001
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i, MX, i):  # 枚举 i 的倍数 j
        divisors[j].append(i)  # i 是 j 的因子
''',
    code='''
class Solution:
    def minDifference(self, n: int, k: int) -> List[int]:
        min_diff = inf
        path = [0] * k
        ans = None

        def dfs(i: int, n: int) -> None:
            if i == k - 1:
                nonlocal min_diff, ans
                # path[0] 最小，n 最大
                if n - path[0] < min_diff:
                    min_diff = n - path[0]
                    path[i] = n
                    ans = path.copy()  # path[:]
                return
            for d in divisors[n]:  # 枚举 n 的因子 d
                if d * d > n or i > 0 and d - path[0] >= min_diff:
                    break
                if i == 0 or d >= path[i - 1]:
                    path[i] = d  # 直接覆盖，无需恢复现场
                    dfs(i + 1, n // d)

        dfs(0, n)
        return ans
''',
    call='Solution().minDifference(8, 3)',
    expect=[2, 2, 2],
    views=[
        dict(type='array', var='path', label='path（蓝 = 正在填的位置）', cell=90, h=150, pointers={'i': 'blue'},
             dim=lambda S, i, v: i > S['_inner'].get('i', 0)),
        dict(type='text', fn=lambda S: f"当前最优：`min_diff = {S['_inner'].get('min_diff', S.get('min_diff'))}`，`ans = {S['_inner'].get('ans', S.get('ans'))}`", size=24, h=60),
        dict(type='calls', h=230),
    ],
    watch=['k', ('i', lambda S: S['_inner'].get('i'), 'blue'), ('n', lambda S: S['_inner'].get('n'), 'pink'),
           ('d', lambda S: S['_inner'].get('d'), 'yellow'), ('min_diff', lambda S: S['_inner'].get('min_diff', S.get('min_diff')), 'green')],
    skip=['min_diff = inf', 'path = [0] * k', 'ans = None', 'nonlocal'],
    captions={
        'dfs(0, n)': '从 `dfs(0, n)` 开始：`i` 是正在填的位置，`n` 是还没拆掉的剩余乘积',
        'if i == k - 1': lambda S, B, ret: (f'`i = {S.i} = k−1`：最后一个数 ==只能是剩余的 n==，即 `{S.n}`' if S.i == S.k - 1
                                             else f'`i = {S.i} < k−1`：还要继续拆，枚举 `n = {S.n}` 的因子'),
        'for d in divisors[n]': lambda S, B, ret: f'枚举 `{S.n}` 的因子 `d`（从小到大）：当前 `d = {S.d}`',
        'if d * d > n': _brk,
        'if i == 0 or d >= path[i - 1]': _fill,
        'path[i] = d': '`path[{i}] = {d}`：直接覆盖，==不用恢复现场==',
        'dfs(i + 1': '递归填下一个位置，剩余乘积 `{B.n} // {B.d} = {B.n // B.d}`',
        'if n - path[0] < min_diff': lambda S, B, ret: (f'`path` 递增 → 最小是 `path[0] = {S.path[0]}`，最大是 `n = {S.n}`：差 `{S.n - S.path[0]}`'
                                                       f' {"<" if S.n - S.path[0] < S.min_diff else "≥"} 当前最优 `{S.min_diff}`'),
        'min_diff = n - path[0]': '更新最小差值：`min_diff = {min_diff}`',
        'path[i] = n': '最后一个数就是 `n`：`path[{i}] = {n}`',
        'ans = path.copy()': '记录答案 `{ans}`（==拷贝==，不然会被后面的搜索覆盖）',
        'break': '跳出这一层的循环，回到上一层',
        'return ans': '搜索结束，最优方案 `{ret}`',
        '                return': '这一层结束，回到上一层',
    },
    max_steps=110,
    cards=dict(
        one_liner='因子从小到大不降地填，最后一个数就是剩下的积',
        complexity='时间 `O(D^{k/2})`，空间 `O(k)`',
        problem=['把 `n` 恰好拆成 `k` 个正整数，乘积等于 `n`',
                 '要使这些数的 ==最大值 − 最小值== 最小，返回任一方案',
                 '示例：`n = 44, k = 3` → `[2,2,11]`；本视频取 `n = 8, k = 3` → `[2,2,2]`'],
        quote='排除等效冗余。比如先填 2 再填 3，和先填 3 再填 2，二者是等效的。不妨规定所填数字必须大于等于上一个填的数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k ≤ 5`，搜索树很小：先预处理每个数的因子，回溯枚举',
              '规定 `path` 不降 → 最小值是 `path[0]`，最大值是最后一个数 `n`，不用维护 mn/mx',
              '`d*d > n` 就 break（下一个数会比 d 小，不合法）；`d − path[0] ≥ min_diff` 就 break（最优性剪枝）'],
        after=[dict(heading='与原文的两处差别', lines=[
            '原文「预处理因子」写在 class 外面，这里放进 `setup` 不追踪（循环太长）',
            '灵神还给了「优化前」写法：每层都维护 `mn`、`mx`，不剪枝；本视频用优化后的写法'])],
        summary=['时间 `O(D^{k/2})`，`D ≤ 128` 是因子个数；空间 `O(k)`',
                 '易错点：保存答案要 `path.copy()`，`path` 会被反复覆盖',
                 '`path` 无需恢复现场：每层固定覆盖 `path[i]`',
                 '最后一层不枚举，直接取 `n`，所以 `i == k-1` 是递归边界'],
    ),
)
