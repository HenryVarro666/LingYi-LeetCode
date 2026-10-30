def _k(S):
    """loop 2 里当前处理的 k（代码里没有下标变量，用差分数组重放推出）"""
    if 'd' not in S or 'sum_d' not in S or 'diff' not in S:
        return None
    diff, limit = S['diff'], S['limit']
    s, ans = S['n'], float('inf')
    for k in range(2, limit * 2 + 1):
        ps, pa = s, ans
        s += diff[k]
        ans = min(ans, s)
        want = {16: (ps, pa), 17: (s, pa), 18: (s, ans)}.get(S.get('_line'))
        if diff[k] == S['d'] and want and (S['sum_d'], S['ans']) == want:
            return k
    return None


def _a(S):
    if 'diff' not in S:
        return None
    if 'sum_d' not in S:
        return ['·'] * (S['limit'] * 2 + 2)
    s = S['n']
    out = ['·', '·']
    for k in range(2, S['limit'] * 2 + 1):
        s += S['diff'][k]
        out.append(s)
    return out + ['·']


def _txt(S):
    if 'sum_d' in S and 'd' in S and 'ans' in S:
        k = _k(S)
        a = f"到 k = `{k}` 为止，前缀和 `sum_d` = =={S['sum_d']}==（把所有对的和都变成 {k} 的操作次数），最小 `ans` = {S['ans']}" if k else ''
        return a
    if 'l' in S and 'y' in S:
        return (f"一对 `({S['x']}, {S['y']})`：和为 `{S['x']+S['y']}`；改 1 次能到的和 = `[{S['l']}, {S['r']}]`，"
                f"其余要改 2 次")
    return ''


CONFIG = dict(
    num=1674, title='使数组互补的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 枚举目标和 k',
    tags=['灵神题单·常用数据结构', '难度分 2333'],
    code='''
class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        diff = [0] * (limit * 2 + 2)
        for i in range(n // 2):
            x = nums[i]
            y = nums[n - 1 - i]
            l = min(x, y) + 1
            r = max(x, y) + limit
            diff[l] -= 1
            diff[x + y] -= 1
            diff[x + y + 1] += 1
            diff[r + 1] += 1
        ans = inf
        sum_d = n
        for d in diff[2 : limit * 2 + 1]:
            sum_d += d
            ans = min(ans, sum_d)
        return ans
''',
    call='Solution().minMoves([1,2,1,3], 4)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（成对：i 与 n-1-i）', h=190,
             pointers={'i if _line < 14 else None': 'blue', 'n - 1 - i if _line < 14 else None': 'pink'},
             pointer_labels={'i if _line < 14 else None': 'x', 'n - 1 - i if _line < 14 else None': 'y'}),
        dict(type='array', var='diff', label='diff（下标 = 目标和 k，范围 2 ~ 2·limit）', h=190,
             pointers={'l if _line < 14 else None': 'green'},
             pointer_labels={'l if _line < 14 else None': 'l'}),
        dict(type='array', var=_a, label='a[k]：把所有对的和变成 k 的操作次数', h=170,
             pointers={_k: 'orange'}, pointer_labels={_k: 'k'},
             color=lambda S, i, v: 'green' if isinstance(v, int) and v == S.get('ans') and i <= (_k(S) or 0) else None),
        dict(type='text', size=28, h=90, fn=_txt),
    ],
    watch=['x', 'y', 'l', 'r', 'sum_d', ('ans', 'ans', 'green')],
    captions={
        'diff = [0]': '`diff` 下标是目标和 `k`（最大 `2·limit`），多开一位给 `r+1`',
        'x = nums[i]': '取第 `{i}` 对：`x = nums[{i}] = {x}`',
        'y = nums[n': '`y = nums[{n-1-i}] = {y}`：和是 `{x+y}`',
        'l = min': '改一个数，和可落在 `[min+1, max+limit]` = `[{l}, {max(x,y)+limit}]`：左端点 `l = {l}`',
        'r = max': '右端点 `r = max + limit = {r}`：这段区间改 1 次就够',
        'diff[l] -= 1': '基线是每对都改 2 次（`sum_d = n`）；从 `l = {l}` 起只要 1 次：`diff[{l}] -= 1`',
        'diff[x + y] -= 1': '和恰好是 `{x+y}` 时一次都不用改：再减一，`diff[{x+y}] -= 1`',
        'diff[x + y + 1] += 1': '`{x+y}` 之后又回到改 1 次：`diff[{x+y+1}] += 1` 抵消',
        'diff[r + 1] += 1': '超过 `r = {r}` 又要改 2 次：`diff[{r+1}] += 1`',
        'ans = inf': '`ans` 取各个 k 的最小值',
        'sum_d = n': '`sum_d = n = {n}`：先假设 `n/2` 对每对都要改 2 次',
        'for d in': lambda S, B, ret: (f"枚举目标和 `k = {_k(S)}`" if _k(S) else '枚举目标和 `k = 2 .. 2·limit`') + f'，差分值 `d = {S.d}`' if 'd' in S else '枚举目标和 `k = 2 .. 2·limit`',
        'sum_d += d': '前缀和累加 `{d}` → `sum_d = {sum_d}`：这个 k 需要的总操作次数',
        'ans = min': '`ans = min({B.ans}, {sum_d}) = {ans}`',
        'return ans': '最少操作次数 `{ans}`',
    },
    cards=dict(
        one_liner='枚举目标和 k，每一对 (x, y) 对 k 贡献 0 / 1 / 2 次操作',
        complexity='时间 `O(n + limit)`，空间 `O(limit)`',
        problem=['偶数长数组，每次操作把任意数改成 `[1, limit]` 内的数',
                 '让所有 `nums[i] + nums[n-1-i]` 都相等，求最少操作数',
                 '本视频：`nums=[1,2,1,3], limit=4` → `1`；题目示例 1 同为 1'],
        quote='横看成岭侧成峰，单看 (nums[i], nums[n-1-i])，这对元素会如何影响数组 a？哪些 a[k] 需要增加 1，哪些 a[k] 需要增加 2？',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x + y = k`：不用改，贡献 `0`',
              'k 在 `[min+1, max+limit]` 内：改一个数就行，贡献 `1`',
              '其余 k：两个都改，贡献 `2`',
              '三段区间叠加用差分，`sum_d` 从 `n` 起（每对先算 2 次）'],
        summary=['时间 `O(n + limit)`，暴力枚举 k 再扫数组是 `O(n·limit)`',
                 '原文先给了「优化前」写法，视频用合并相同下标后的优化写法',
                 '`diff` 要开 `2·limit+2`，`r+1` 最大是 `2·limit+1`',
                 '最后只遍历 `diff[2 : 2·limit+1]`，k 的合法范围是 `[2, 2·limit]`',
                 '同类题：798 得分最高的最小轮调'],
    ),
)
