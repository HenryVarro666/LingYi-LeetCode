N = 5
PAIRS = [[1, 2], [2, 5], [3, 5]]   # 示例 2 → 12


def _show(S):
    if 'b0' not in S:
        return ''
    i = S.get('i')
    s = f"`b0 = {S['b0']}`（最小 b），`b1 = {S['b1']}`（次小 b）"
    if i is not None and S.get('_line', 0) >= 20:
        s += f"\n左端点 `i = {i}` 的合法子数组：`b0 − i = {S['b0'] - i}` 个；`ans = {S['ans']}`"
        s += f"\n连续相同 b0 的增量 `extra = {S['extra']}`，最大 `max_extra = {S['max_extra']}`"
    return s


CONFIG = dict(
    num=3480, title='删除一个冲突对后最大子数组数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='倒序枚举左端点，维护最小/次小 b',
    tags=['枚举右，维护左', '难度分 2764'],
    code='''
class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # 更快写法见【Python3 写法二】
        groups = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            groups[a].append(b)

        ans = max_extra = extra = 0
        b0 = b1 = n + 1
        for i in range(n, 0, -1):
            pre_b0 = b0
            for b in groups[i]:
                if b < b0:
                    b0, b1 = b, b0
                elif b < b1:
                    b1 = b

            ans += b0 - i
            if b0 != pre_b0:  # 重新统计连续相同 b0 的 extra
                extra = 0
            extra += b1 - b0
            max_extra = max(max_extra, extra)

        return ans + max_extra
''',
    call=f'Solution().maxSubarrays({N}, {PAIRS!r})',
    expect=12,
    skip=['pre_b0 = b0'],
    views=[
        dict(type='array', var='groups', label='groups[a]：左端点 a 对应的所有 b（下标 = a）', cell=130,
             pointers={'i': 'blue'}, h=300),
        dict(type='text', fn=_show, size=28, h=230),
    ],
    watch=[('i', 'i', 'blue'), ('b0', 'b0', 'pink'), ('b1', 'b1', 'purple'), ('ans', 'ans', 'green'),
           ('extra', 'extra', 'yellow'), ('max_extra', 'max_extra', 'orange')],
    captions={
        'groups = ': '按 `a` 分组：`groups[a]` 存所有以 `a` 为较小端点的冲突对的 `b`',
        'a, b = b, a': '`a > b` 就交换，保证 `a ≤ b`',
        'groups[a].append': '冲突对 `({a}, {b})` 放进 `groups[{a}]`',
        'ans = max_extra': '`ans`：不删冲突对时的合法子数组数；`extra / max_extra` 记删一个多出来的',
        'b0 = b1 = n + 1': '`b0` 最小 b、`b1` 次小 b，初值 `n+1`：右端点不能出界（相当于两个虚拟冲突对）',
        'for i in range': '倒着枚举左端点 `i = {i}`：`groups` 里 `a ≥ i` 的是后缀，所以从后往前',
        'for b in groups[i]': lambda S, B, r: (f'逐个用 `groups[{S.i}] = {S.groups[S.i]}` 里的 `b` 更新最小、次小' if S.groups[S.i]
                                                else f'`groups[{S.i}]` 是空的 → `b0`、`b1` 都不变'),
        'if b < b0': lambda S, B, r: (f'`{S.b} < b0 = {S.b0}` 成立：`b` 成为新的最小，原最小退为次小' if S.b < S.b0
                                       else f'`{S.b} ≥ b0 = {S.b0}`，不是最小，看看能不能当次小'),
        'b0, b1 = b, b0': '`b0 = {b0}`，`b1 = {b1}`',
        'elif b < b1': lambda S, B, r: (f'`{S.b} < b1 = {S.b1}`：成为新的次小' if S.b < S.b1
                                         else f'`{S.b} ≥ b1 = {S.b1}`：比次小还大，忽略'),
        'b1 = b': '`b1 = {b1}`',
        'ans += b0 - i': '左端点 `{i}` 的右端点可取 `{i}..{b0 - 1}`，共 `{b0} − {i}` = {b0 - i} 个 → `ans = {ans}`',
        'if b0 != pre_b0': lambda S, B, r: (f'`b0` 从 `{S.pre_b0}` 变成 `{S.b0}`：换了一段 → ==重新统计 extra=='
                                             if S.b0 != S.pre_b0 else f'`b0` 仍是 `{S.b0}`：同一段，extra 接着累加'),
        'extra = 0': '`extra` 清零',
        'extra += b1 - b0': '删掉 `b = {b0}` 的冲突对，左端点 `{i}` 多 `b1 − b0 = {b1} − {b0}` = {b1 - b0} 个 → `extra = {extra}`',
        'max_extra = max': '`max_extra = max({B.max_extra}, {extra}) = {max_extra}`',
        'return ans + max_extra': '不删的答案 `{ans}` + 删一个最多多出的 `{max_extra}` = =={ret}==',
    },
    cards=dict(
        one_liner='先算不删的答案，再加上"删哪个冲突对最赚"的最大增量',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums = [1..n]`，给若干冲突对 `[a, b]`，删去 ==恰好一个==',
                 '数有多少非空子数组不同时包含任何剩余冲突对的 `a` 和 `b`',
                 '示例：`n = 5, [[1,2],[2,5],[3,5]]` → `12`（删 `[1,2]`）',
                 '本视频用示例 2'],
        quote='枚举子数组左端点，统计有多少个合法的右端点。……左端点为 i 时，满足 a≥i 的冲突对中 b 的最小值为 b0，右端点可以是 i, i+1, …, b0−1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒着枚举左端点 `i`，维护 `a ≥ i` 的冲突对里 ==最小 b0 和次小 b1==',
              '不删：左端点 `i` 有 `b0 − i` 个合法右端点，累加得 `ans`',
              '删掉 `b = b0` 的那个对，`b0` 变成 `b1`，==多出 `b1 − b0` 个==；同一个 `b0` 的各个 `i` 一起受益，要累加',
              '答案 = `ans` + 最大的累加增量'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`b0 = b1 = n + 1` 的虚拟冲突对，让没有冲突对时也不越界',
                 '易错：增量要按相同 `b0` 累加（`extra`），不能只取单个 `b1 − b0` 的最大',
                 '`b0` 倒着枚举时只减不增 → 相同 `b0` 连续出现，一个变量代替 `extra` 数组',
                 '另有"优化前"（每次排序取前二小）与更快的 g0/g1 写法，这里选主推的优化版'],
    ),
)
