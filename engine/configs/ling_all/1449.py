def _fmt(S):
    if 'i' not in S or 'c' not in S:
        return '`cost[i]` 是数位 `i+1` 的成本；`f[j]` = 总成本恰好为 j 时的最长长度（`-inf` 表示凑不出）'
    if S.get('_line', 0) <= 9:
        return f'物品 `c = {S["c"]}`：`f[j] = max(f[j], f[j − {S["c"]}] + 1)`'
    return f'当前数位 `{S["i"] + 1}`（成本 `{S["c"]}`），剩余成本 `j = {S["j"]}`'


CONFIG = dict(
    num=1449, title='数位成本和为目标值的最大数字', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='恰好装满完全背包 · 倒推构造',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1927'],
    code='''
class Solution:
    def largestNumber(self, cost: List[int], target: int) -> str:
        f = [0] + [-inf] * target  # 「恰好装满」型完全背包的初始值

        # 计算最长长度
        for c in cost:
            for j in range(c, target + 1):
                f[j] = max(f[j], f[j - c] + 1)

        if f[target] < 0:  # 无解
            return "0"

        ans = []
        j = target
        for i in range(8, -1, -1):  # 从大到小填 i+1
            c = cost[i]
            # f[j-c] + 1 == f[j] 说明上面 f[j] 取的 max 来自 f[j-c]，说明可以填 i+1
            while j >= c and f[j - c] + 1 == f[j]:
                ans.append(str(i + 1))
                j -= c

        return ''.join(ans)
''',
    call='Solution().largestNumber([4,3,2,5,6,7,2,5,5], 4)',
    expect='77',
    skip=['for j in range(c', 'c = cost[i]', 'for c in cost'],
    max_steps=90,
    views=[
        dict(type='text', fn=_fmt, size=24, h=50),
        dict(type='array', var='cost', label='cost（数位 1~9 的成本）', h=170, cell=64,
             color=lambda S, k, v: 'blue' if S.get('c') is not None and S.get('_line', 0) >= 14 and k == S.get('i') else None),
        dict(type='array', var='f', label='f[j]：成本恰好 j 的最长长度', h=190, cell=70, pointers={'j': 'pink'}),
        dict(type='array', var='ans', label='ans（已填的数位）', h=130, cell=70),
    ],
    watch=[('c', 'c', 'blue'), ('j', 'j', 'pink'), ('i', 'i', 'cyan'), ('f[target]', 'f[target]', 'green')],
    captions={
        'f = [0]': '`f[0] = 0`：成本 0 长度 0；其余 `-inf` 表示「恰好凑不出」',
        'f[j] = max': '物品成本 `{c}`：`f[{j}] = max({B.f[j]}, f[{j - c}] + 1)` = =={f[j]}==，成本 {j} 最多 {f[j]} 个数位',
        'if f[target] < 0': lambda S, B, r: ('`f[target] = %s`，凑不出 → 返回 "0"' % S.f[S.target] if S.f[S.target] < 0
                                             else '`f[target] = %s`：答案长度就是 %s' % (S.f[S.target], S.f[S.target])),
        'ans = []': '开始构造：长度已定，让字典序最大',
        'j = target': '`j` 是剩余未填的成本，从 `target` 开始',
        'for i in range(8': lambda S, B, r: ('数位都试完了，`j = 0` 刚好填满' if S.i == 0 and B.get('i') == 0 else f'尝试数位 `{S.i + 1}`（从大到小，大数位放高位）'),
        'while j >= c': lambda S, B, r: (
            f'`f[{S.j - S.c}] + 1 = {S.f[S.j - S.c] + 1}` == `f[{S.j}] = {S.f[S.j]}`：==f[j] 来自这个数位，可以填 {S.i + 1}=='
            if S.j >= S.c and S.f[S.j - S.c] + 1 == S.f[S.j]
            else (f'`j = {S.j} < {S.c}`：成本不够，不能再填 {S.i + 1}' if S.j < S.c
                  else f'`f[{S.j - S.c}] + 1 = {S.f[S.j - S.c] + 1}` ≠ `f[{S.j}] = {S.f[S.j]}`：填 {S.i + 1} 会让长度变短 → 换更小的数位')),
        'ans.append': '填入 `{i + 1}`：`ans = {ans}`',
        'j -= c': '剩余成本 `j` → {j}',
        'return \'\'.join': '拼成答案 `{ret}`',
    },
    cards=dict(
        one_liner='先求最长长度，再用 f 当地图，从大到小贪心填数位',
        complexity='时间 `O(9·target)`，空间 `O(target)`',
        problem=['数位 `i+1` 的成本是 `cost[i]`，总成本必须恰好等于 `target`，且不含 0',
                 '返回能得到的最大整数（字符串），做不到返回 `"0"`',
                 '示例：`cost=[4,3,2,5,6,7,2,5,5], target=9` → `"7772"`；视频用 `target=4` → `"77"`'],
        quote='首先要保证答案的长度尽量大。在此基础上，再保证答案的字典序尽量大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['恰好装满型完全背包：`f[j] = max(f[j], f[j-c]+1)` 求最长长度',
              '`f` 是「导航地图」：`f[j] == f[j-c]+1` 说明可以填这个数位',
              '倒序枚举 `i = 8..0`，每个数位能填就一直填，保证字典序最大'],
        summary=['时间 `O(9·target)`，空间 `O(target)`',
                 '初值 `f[0]=0`，其余为 `-inf`：区分「恰好」与「至多」',
                 '`f[target] < 0` 时无解，返回字符串 `"0"`',
                 '先比长度、再比字典序，所以构造时必须从大数位开始'],
    ),
)
