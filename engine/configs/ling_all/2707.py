S0 = 'leetsco'
D0 = ['leet', 'co', 'leetco']


def _hit(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (9, 10):
        return None
    return S['s'][j:i + 1] in S['d']


def _sc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if j is not None and j <= k <= i and S.get('_line') in (9, 10):
        return 'green' if _hit(S) else 'yellow'
    if k == i:
        return 'blue'
    return None


def _fc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if k == i + 1:
        return 'yellow'
    if j is not None and k == j and _hit(S):
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return '`f[i]` = 前 `i` 个字符里，最少剩下几个额外字符；`f[0] = 0`'
    if j is not None and S.get('_line') in (9, 10):
        sub = S['s'][j:i + 1]
        if sub in S['d']:
            return f'`s[{j}:{i + 1}] = "{sub}"` 在字典里 → 候选 `f[{j}]` = =={S["f"][j]}=='
        return f'`s[{j}:{i + 1}] = "{sub}"` 不在字典里'
    return f'算 `f[{i + 1}]`：先假设 `s[{i}]` 是额外字符，再枚举最后一个单词'


CONFIG = dict(
    num=2707, title='字符串中的额外字符', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（记忆化搜索 1:1 翻译成递推）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1736'],
    code='''
class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        d = set(dictionary)
        n = len(s)
        f = [0] * (n + 1)
        for i in range(n):
            f[i + 1] = f[i] + 1  # 不选
            for j in range(i + 1):  # 枚举选哪个
                if s[j:i + 1] in d:
                    f[i + 1] = min(f[i + 1], f[j])
        return f[n]
''',
    call=f'Solution().minExtraChar({S0!r}, {D0!r})',
    expect=1,
    skip=['for j in range'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符 i，黄/绿 = 正在检查的子串 s[j..i]）', h=150, cell=70,
             pointers={'j': 'pink', 'i': 'blue'}, color=_sc),
        dict(type='set', var='d', label='dictionary', h=90, fmt=lambda x: f'"{x}"'),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f[k]：前 k 个字符的最少额外字符数（黄 = 正在算）', h=170, cell=70, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[n]', 'f[-1]', 'green')],
    captions={
        'd = set': '字典放进集合，查一个子串在不在是 `O(1)`（忽略哈希长度）',
        'n = len(s)': '`n = {n}`',
        'f = [0] * (n + 1)': '`f[0] = 0`：空串没有额外字符，这就是递归边界 `dfs(-1) = 0`',
        'for i in range(n)': lambda S, B, r: (f'`i = {S.i}`：计算前缀 `s[0..{S.i}]`，结果存进 `f[{S.i+1}]`' if S.get('i') != B.get('i')
                                              else '`i` 已经枚举完所有位置，循环结束'),
        'f[i + 1] = f[i] + 1': '先假设 `s[{i}]` 不属于任何单词：`f[{i+1}] = f[{i}] + 1` = =={f[i+1]}==，它是额外字符',
        'if s[j:i + 1] in d': lambda S, B, r: (f'子串 `s[{S.j}:{S.i+1}] = "{S.s[S.j:S.i+1]}"` ==在==字典里 → 可以把它整段用掉，前面剩 `f[{S.j}]`' if S.s[S.j:S.i+1] in S.d
                                              else f'子串 `s[{S.j}:{S.i+1}] = "{S.s[S.j:S.i+1]}"` 不在字典里 → 跳过'),
        'f[i + 1] = min': '`f[{i+1}] = min({B.f[i+1]}, f[{j}])` = =={f[i+1]}==：用这个单词，更少就更新',
        'return f[n]': '整串 `s[0..{n-1}]` 最少剩 `f[{n}]` = =={ret}== 个额外字符',
    },
    cards=dict(
        one_liner='枚举最后一个单词从哪开始，不用的字符算额外',
        complexity='时间 `O(L + n^3)`，空间 `O(n + L)`',
        problem=['把 `s` 切成若干不重叠、且都在 `dictionary` 里的子串',
                 '没被覆盖的字符就是==额外字符==，求最少有几个',
                 '示例：`s = "leetscode"`，字典 `["leet","code","leetcode"]` → `1`（本视频用更短的 `"leetsco"`）'],
        quote='考虑「枚举选哪个」，如果 s 的子串 [j,i] 在 dictionary 中，那么问题变成 s 的前缀 [0,j-1] 的子问题。',
        quote_src='—— 灵茶山艾府题解（二、记忆化搜索）',
        idea=['`dfs(i)`：前缀 `[0,i]` 最少剩多少额外字符；跳过 `s[i]` 就是 `dfs(i-1)+1`',
              '或者枚举 `j`，`s[j..i]` 在字典里就接上 `dfs(j-1)`，两者取小',
              '1:1 翻译成递推：给 `f` 左边多插一格表示 `dfs(-1)`，所以下标整体右移一位'],
        summary=['时间：状态 `O(n)` × 转移 `O(n^2)`（枚举 `j` 再切片比较），共 `O(n^3)`',
                 '易错：`f` 要开 `n+1` 格，`f[i+1]` 对应前缀 `[0,i]`，别写成 `f[i]`',
                 '题解先写了 `@cache` 记忆化搜索，再 1:1 翻译成这份递推；还可用字典树优化枚举',
                 '同类划分型 DP：139. 单词拆分、2767. 最少美丽子串'],
    ),
)
