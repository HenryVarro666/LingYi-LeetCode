def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '`f` 全部算完：`f = [' + ','.join('T' if x else 'F' for x in S.f) + ']`'
    pre = ''
    if 'i' in B and not S.f[B.i]:
        pre = f'所有 j 都不行 → `f[{B.i}]` 保持 F。'
    return pre + f'算 `f[{S.i}]`：前缀 `"{S.s[:S.i]}"` 能拆吗？==枚举最后一段== `s[j:{S.i}]`'


def _cap_if(S, B, ret):
    head = f'`"{S.s[:S.j]}"`' if S.j else '空串'
    if not S.f[S.j]:
        return f'`f[{S.j}] = F`：前缀 {head} 拆不开 → 跳过'
    if S.s[S.j:S.i] in S.words:
        return f'`f[{S.j}] = T` 且 `"{S.s[S.j:S.i]}"` ==在字典里== → 成立！'
    return f'`f[{S.j}] = T`，但 `"{S.s[S.j:S.i]}"` 不在字典里 → 不行'


def _text(S):
    if 'j' not in S or 'i' not in S:
        return '`f[i]` = 前缀 `s[:i]` 能否拆分（`f[0]` 是空串）'
    i, j, s = S['i'], S['j'], S['s']
    ok = s[j:i] in S['words']
    return (f"`f[{i}]` ⇐ `f[{j}]`={'T' if S['f'][j] else 'F'}  且  "
            f"`s[{j}:{i}]`=\"{s[j:i]}\" {'==∈ words==' if ok else '∉ words'}")


CONFIG = dict(
    num=139, title='单词拆分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（递推）',
    code='''
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        max_len = max(map(len, wordDict))  # 用于限制下面 j 的循环次数
        words = set(wordDict)  # 便于快速判断 s[j:i] in words

        n = len(s)
        f = [True] + [False] * n
        for i in range(1, n + 1):
            for j in range(i - 1, max(i - max_len - 1, -1), -1):
                if f[j] and s[j:i] in words:
                    f[i] = True
                    break
        return f[n]
''',
    call='Solution().wordBreak("catsand", ["cat", "cats", "and", "sand"])',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', label='s', cell=84, min_slots=8,
             window=('j', 'i-1')),
        dict(type='array', var='f', label='f[i]：前缀 s[:i] 能否拆分（黄 = 正在算，蓝 = 依赖的 f[j]）',
             cell=84, pointers={'j': 'blue', 'i': 'yellow'},
             color=lambda S, i, v: 'yellow' if i == S.get('i') else
                                   ('blue' if i == S.get('j') else ('green' if v else None))),
        dict(type='set', var='words', label='words（哈希集合）', h=110),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), 'max_len', ('f[n]', 'f[n]', 'green')],
    skip=['for j in range'],
    captions={
        'max_len = max': '最长单词 `{max_len}` 个字母 → 最后一段最长 `{max_len}`，==枚举长度而不是枚举单词==',
        'words = set': '转成哈希集合，`s[j:i] in words` 查得快',
        'f = [True]': '`f` 长 `n+1 = {n + 1}`；`f[0] = True`：==空串算拆分成功==（翻译自递归边界 `dfs(0)`）',
        'for i in range': _cap_for_i,
        'if f[j] and': _cap_if,
        'f[i] = True': lambda S, B, ret: (f'`"{S.s[:S.j]}"`' if S.j else '空串') + f' 能拆 + `"{S.s[S.j:S.i]}"` 是单词 → `f[{S.i}] = True`',
        'break': '找到一个 j 就够了，不用再试别的 j',
        'return f[n]': '答案就是 `f[{n}]`（翻译自递归入口 `dfs(n)`）→ =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一个单词，问题缩成更短的前缀',
        complexity='时间 `O(mL + nL²)`，空间 `O(mL + n)`（`L` 为最长单词长）',
        problem=['给字符串 `s` 和字典 `wordDict`，问 `s` 能否拆成若干个字典里的单词',
                 '单词可以==重复使用==，也不必全部用上',
                 '示例：`"catsand"`，`["cat","cats","and","sand"]` → `true`'],
        before=[dict(heading='第一步：寻找子问题', lines=[
            '例如 `s = "leetcode"`，==枚举最后一段的长度==：`e`、`de`、`ode`、`code`…',
            '若 `code` 在字典里，问题变成：`leet` 能否拆分？',
            '这是==和原问题相似、规模更小的子问题== → 可以递归',
        ])],
        quote='枚举 j=i−1,i−2,…,max(i−maxLen,0)，只要其中一个 j 满足 ==s[j:i] 在 wordDict 中且 f[j]=true==，那么 f[i] 就是 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]`：前缀 `s[:i]` 能否拆分；初始 `f[0] = True`，答案 `f[n]`',
              '最后一段 `s[j:i]` 长度 ≤ `max_len`，所以 `j` 只需倒着枚举 `L` 个',
              '字典多达 1000 个词，但长度最多 20 种 → ==枚举长度，不枚举单词=='],
        after=[dict(heading='从记忆化搜索到递推', lines=[
            '灵神先写 `dfs(i)` + `@cache` 记忆化搜索：边界 `dfs(0)`，入口 `dfs(n)`',
            '去掉「递」只留「归」：`dfs(i)` → `f[i]`，边界 → `f[0]`，入口 → `f[n]`',
            '答疑：==不能==像完全背包那样外层枚举单词——本题单词可以交替选（ABA）',
        ])],
        summary=['`n` 个状态 × 枚举 `L` 个 j × 切片查哈希 `O(L)` → `O(nL²)`',
                 '易错：`f` 长 `n + 1`，`f[i]` 管的是 `s[:i]`，==不含== `s[i]`',
                 '易错：j 下界 `max(i - max_len, 0)`；更长的串可用==字典树==优化'],
    ),
)
