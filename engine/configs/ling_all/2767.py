S0 = '10111'


def _tl(S):
    t = S.get('t')
    return len(t) if t else 0


def _sc(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    line = S.get('_line')
    t = S.get('t')
    if line == 8:
        return 'pink' if k == i and v == '0' else ('blue' if k == i else None)
    if t and line in (10, 11, 12, 13) and i <= k < i + len(t):
        return 'green' if line == 13 else 'yellow'
    if k == i:
        return 'blue'
    return None


def _fc(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    if k == i:
        return 'yellow'
    if S.get('_line') == 13 and S.get('t') and k == i + len(S['t']):
        return 'green'
    return None


def _formula(S):
    i, t = S.get('i'), S.get('t')
    if i is None:
        return '`f[i]` = 后缀 `s[i:]` 最少分几段（`inf` = 分不了）；`f[n] = 0`，从后往前算'
    s, line = S['s'], S.get('_line')
    if line == 8 and s[i] == '0':
        return f'`s[{i}] = 0` 会让美丽子串带前导 0 → `f[{i}]` 保持 `inf`'
    if t and line >= 12:
        seg = s[i:i + len(t)]
        if seg == t:
            return f'`s[{i}:{i + len(t)}] = "{seg}"` = 5 的幂 `{t}` → 候选 `f[{i + len(t)}] + 1`'
        return f'`s[{i}:{i + len(t)}] = "{seg}"` ≠ `{t}`'
    return f'从 `s[{i}]` 开始，逐个试 5 的幂的二进制串 `t`'


CONFIG = dict(
    num=2767, title='将字符串分割为最少的美丽子字符串', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（预处理 5 的幂 + 倒序递推）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1865'],
    code='''
# 预处理 2**15 以内的 5 的幂
pow5 = [bin(5 ** i)[2:] for i in range(7)]
class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        n = len(s)
        f = [inf] * n + [0]
        for i in range(n - 1, -1, -1):
            if s[i] == '0': continue
            for t in pow5:
                if i + len(t) > n:
                    break
                if s[i: i + len(t)] == t:  # 忽略切片的时间，这里的比较视作均摊 O(1)
                    f[i] = min(f[i], f[i + len(t)] + 1)
        return f[0] if f[0] < inf else -1
''',
    call=f'Solution().minimumBeautifulSubstrings({S0!r})',
    expect=3,
    skip=['for t in pow5'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = 起点 i，黄 = 正在比的片段，绿 = 匹配成功）', h=150, cell=70, pointers={'i': 'blue'}, color=_sc),
        dict(type='array', var=lambda S: [bin(5 ** k)[2:] for k in range(7)], label='pow5：5 的幂的二进制', h=120, cell=100, index=False,
             color=lambda S, k, v: 'yellow' if S.get('t') == v and S.get('_line') in (10, 11, 12, 13) else None),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f[i]：后缀 s[i:] 的最少段数（黄 = 正在算，绿 = 依赖的 f[i+len(t)]）', h=170, cell=70, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('t', 't', 'yellow'), ('f[0]', 'f[0]', 'green')],
    captions={
        'pow5 = [': '`s` 最长 15，值小于 `2^15`，所以只需 5 的前 7 次幂的二进制串：`1, 101, 11001, ...`',
        'n = len(s)': '`n = {n}`',
        'f = [inf] * n': '`f[n] = 0`：空后缀不用分；其余先设成 `inf`，表示还没找到分法',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算后缀 `s[{S.i}:]`；它依赖更靠右的 `f`，所以==倒着==枚举，也方便判断前导 0' if S.get('i') != B.get('i')
                                           else '所有起点都算完了'),
        "if s[i] == '0'": lambda S, B, r: (f'`s[{S.i}] = 0`：美丽子串不能有前导 0 → 这个位置作不了起点，`f[{S.i}]` 留着 `inf`' if S.s[S.i] == '0'
                                            else f'`s[{S.i}] = 1`：可以作为一个美丽子串的开头'),
        'if i + len(t) > n': lambda S, B, r: (f'`t = {S.t}` 长 {len(S.t)}，从 `{S.i}` 开始会超出 `s` → 后面的 `t` 更长，直接 `break`' if S.i + len(S.t) > S.n
                                              else f'`t = {S.t}` 放得下：`{S.i} + {len(S.t)} <= {S.n}`'),
        'if s[i: i + len(t)] == t': lambda S, B, r: (f'`s[{S.i}:{S.i+len(S.t)}] = "{S.s[S.i:S.i+len(S.t)]}"` ==等于== `{S.t}`，是 5 的幂 → 可以切下这一段'
                                                     if S.s[S.i:S.i+len(S.t)] == S.t else f'`s[{S.i}:{S.i+len(S.t)}] = "{S.s[S.i:S.i+len(S.t)]}"` ≠ `{S.t}`，这个 `t` 不行'),
        'break': '`break`：`pow5` 按长度递增，后面的 `t` 只会更长，更放不下',
        'f[i] = min': '切下 `{t}` 后剩 `f[{i+len(t)}]` = {f[i+len(t)]} 段，再 +1：`f[{i}] = min({B.f[i]}, {f[i+len(t)]} + 1)` = =={f[i]}==',
        'return f[0]': '整串最少分成 `f[0]` = =={ret}== 段',
    },
    cards=dict(
        one_liner='先预处理 5 的幂，再倒着做划分型 DP',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把二进制串 `s` 切成若干段，每段都是「美丽」的：无前导 0，且是 5 的幂的二进制',
                 '求最少切几段；切不了返回 `-1`',
                 '示例：`"1011"` → `2`（`"101"`、`"1"`）；视频用 `"10111"` → `3`'],
        quote='所有情况取最小值。如果 s[i]=0，或者不存在这样的 t，那么 dfs(i)=∞。……倒着遍历的好处是方便判断是否有前导零。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度 ≤ 15，值 < `2^15`，5 的幂只有 7 个，预处理成二进制串 `pow5`',
              '`dfs(i)` 表示划分后缀 `s[i:]` 的最少段数：枚举 `t`，匹配就 `dfs(i+m)+1`',
              '`s[i] = 0` 或没有匹配 → `inf`；递归边界 `dfs(n) = 0`，再 1:1 翻译成倒序递推'],
        summary=['时间 `O(n^2)`：状态 `O(n)`，每个状态只有匹配成功那次是 `O(n)`，其余失配很快',
                 '易错：`f` 开 `n+1` 格，`f[n] = 0`；`f[0] = inf` 时答案是 `-1`',
                 '`i + len(t) > n` 时可以直接 `break`：`pow5` 按长度递增',
                 '题解先给了 `@cache` 记忆化搜索写法，这里是它 1:1 翻译出的递推'],
    ),
)
