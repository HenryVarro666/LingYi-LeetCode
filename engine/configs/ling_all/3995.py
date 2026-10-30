SRC, TGT = 'cathe', 'dogwo'


def _cell_f(S, i, v):
    ii, r = S.get('i'), S.get('r')
    if ii is None:
        return None
    if r is not None and r <= len(S['f']) - 1 and i == r and S['f'][r] < inf and S['_line'] == 29:
        return 'yellow'
    if i == ii:
        return 'blue'
    return 'green' if v < inf and i < ii else None


def _fmt(S):
    ii = S.get('i')
    if ii is None:
        return '`f[i]` = 把 `source` 前 `i` 个字母变成 `target` 前 `i` 个字母的最小成本；`f[0] = 0`'
    return f'`f[{ii}] = {S["f"][ii]}`：前 {ii} 个字母已经对齐的最小成本，现在用它==往右刷表=='


def _if_match(S, B, ret):
    r, cost, pat, rep, i = S.r, S.cost, S.pattern, S.replacement, S.i
    seg = TGT[i:r]
    if r > len(S.source):
        return f'`r = {r}` 超出 `source` 长度 {len(S.source)}：这条规则放不下'
    if S.f[i] + cost >= S.f[r]:
        return f'`f[{i}] + {cost} = {S.f[i] + cost}` 不比 `f[{r}] = {S.f[r]}` 小：==不用再比字符串==，剪枝'
    if rep != seg:
        return f'`replacement = {rep}` ≠ `target[{i}:{r}] = {seg}`：替换结果对不上 target，规则不能用'
    return f'`replacement = {rep}` 恰好等于 `target[{i}:{r}]`，再看 `pattern = {pat}` 能不能匹配 `source`'


CONFIG = dict(
    num=3995, title='转换字符串的最小成本 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='线性 DP · 正序刷表',
    tags=['其他线性 DP', '难度分 2101'],
    code='''
class Solution:
    def minCost(self, source: str, target: str, rules: list[list[str]], costs: list[int]) -> int:
        # 把成本加上 '*' 的个数，这样在 DP 中无需反复统计 '*' 的个数
        for i, rule in enumerate(rules):
            costs[i] += rule[0].count('*')

        # pattern 是否匹配 s[left: left+len(pattern)]
        def is_match(pattern: str, s: str, left: int) -> bool:
            for j, ch in enumerate(pattern):
                if ch != '*' and ch != s[left + j]:
                    return False
            return True

        n = len(source)
        f = [0] + [inf] * n

        for i in range(n):
            if f[i] == inf:
                continue

            # 不替换下标 i
            if source[i] == target[i]:
                f[i + 1] = min(f[i + 1], f[i])

            # 替换子串 [i, i+len(pattern)-1]
            for (pattern, replacement), cost in zip(rules, costs):
                r = i + len(pattern)
                if r <= n and f[i] + cost < f[r] and replacement == target[i:r] and is_match(pattern, source, i):
                    f[r] = f[i] + cost

        return f[n] if f[n] < inf else -1
''',
    call=f"Solution().minCost({SRC!r}, {TGT!r}, [['he','wo'],['c*t','dog'],['h*','wx']], [3,2,5])",
    expect=6,
    skip=['for j, ch in enumerate', "if ch != '*'", 'return False', 'return True'],
    max_steps=80,
    views=[
        dict(type='string', var=lambda S: SRC, label='source', h=130, cell=70,
             color=lambda S, k, v: ('blue' if k == S['i'] else None) if 'i' in S and 'f' in S else None),
        dict(type='string', var=lambda S: TGT, label='target', h=130, cell=70,
             color=lambda S, k, v: ('blue' if k == S['i'] else None) if 'i' in S and 'f' in S else None),
        dict(type='text', fn=_fmt, size=26, h=60),
        dict(type='array', var='f', label='f[i]（蓝 = 当前 i，绿 = 已可达，黄 = 刚更新的 f[r]）', h=220, cell=76,
             color=_cell_f),
    ],
    watch=[('i', 'i', 'blue'), ('r', 'r', 'pink'), 'pattern', 'replacement', ('cost', 'cost', 'orange')],
    captions={
        'costs[i] += rule[0].count': '`costs[{i}]` 加上 `{rule[0]}` 里 `*` 的个数 → =={costs[i]}==，之后不用再数星号',
        'n = len(source)': '`n = {n}`',
        'f = [0] + [inf] * n': '`f[0] = 0`：空串不用花钱；其余先设为 ==inf==（还没有办法到达）',
        'for i in range(n)': '`i = {i}`：从 `f[{i}]` 出发，往右更新别的状态（==刷表法==）',
        'if f[i] == inf': lambda S, B, r: (f'`f[{S.i}] = inf`：前 {S.i} 个字母根本对不齐 → 不能从它出发，==跳过==' if S.f[S.i] == inf
                                           else f'`f[{S.i}] = {S.f[S.i]}`，可达，继续往右转移'),
        'continue': '`f[{i}]` 是 inf，这个起点没有用，直接看下一个 i',
        'if source[i] == target[i]': lambda S, B, r: (f"`source[{S.i}] = {S.source[S.i]}` == `target[{S.i}]`：这个字母==不用改==，成本不变" if S.source[S.i] == S.target[S.i]
                                                      else f"`source[{S.i}] = {S.source[S.i]}` ≠ `target[{S.i}] = {S.target[S.i]}`：必须靠规则替换"),
        'f[i + 1] = min': '不替换下标 {i}：`f[{i + 1}] = min(旧值, f[{i}])` = =={f[i + 1]}=='  ,
        'for (pattern, replacement), cost': '试规则 `{pattern} → {replacement}`，成本（含星号）`{cost}`',
        'r = i + len(pattern)': '这条规则覆盖 `[{i}, {r - 1}]`，右端点 `r = {r}`',
        'if r <= n and': _if_match,
        'f[r] = f[i] + cost': '规则可用：`f[{r}] = f[{i}] + {cost}` = =={f[r]}==',
        'return f[n]': lambda S, B, ret: f'`f[{S.n}] = {ret}`' + ('' if ret != -1 else '，是 inf → 返回 -1') + '：整个 `source` 变成了 `target` 的最小成本',
    },
    cards=dict(
        one_liner='f[i] 去刷新右边：不改就白走一格，规则能匹配就整段跳过去',
        complexity='时间 `O(nL)`，空间 `O(n)`',
        problem=['`source` 要变成 `target`，每条规则 `pattern → replacement` 一次替换一段，`*` 可匹配任意字母',
                 '成本 = `costs[i]` + `pattern` 里 `*` 的个数，每个位置至多被替换一次',
                 '本视频：`cathe → dogwo`，答案 `6`'],
        quote='如果 f[i] = inf（从未被更新过），那么不需要用 f[i] 更新右边的状态。',
        quote_src='—— 灵茶山艾府题解（写法三：正序 DP）',
        idea=['从最后一个字母想：不替换要求两边字母相同，替换要求 `pattern` 匹配、`replacement` 等于 `target` 子串',
              '`f[i]` = 前 `i` 个字母变成 `target` 前 `i` 个的最小成本，`f[0] = 0`',
              '正序刷表：`f[i]` 更新 `f[i+1]` 和 `f[i+len(pattern)]`，`inf` 的状态直接跳过'],
        summary=['时间 `O(nL)`，`L` 是所有 `pattern` 长度之和；空间 `O(n)`',
                 '先把 `*` 的个数加进 `costs`，DP 里不用再数',
                 '==先比成本，再比字符串==：`f[i] + cost < f[r]` 不成立就不用判断匹配',
                 '写法一是记忆化搜索，写法二是倒序查表 DP，都是同一个状态；`replacement` 无通配符，还可用 AC 自动机加速',
                 '题目没保证两串等长，实测数据都等长'],
    ),
)
