W = ["abcd", "cdef", "efab"]
N = len(W)


def _ft(S):
    f = S.get('f')
    if f is None:
        return [['·'] * N for _ in range(1 << N)]
    return [['·' if v is None else v for v in row] for row in f]


def _cm(S):
    c = S.get('common')
    if c is None:
        return [['·'] * N for _ in range(N)]
    return c


def _col(S, r, c, v):
    I = S['_inner']
    if 'state' not in I or 'last_word' not in I:
        return None
    if r == I['state'] and c == I['last_word']:
        return 'yellow'
    i = I.get('i')
    if S.get('_line') in (58, 59, 60) and i is not None and 'prev_state' in I and i != I['last_word'] and r == I['prev_state'] and c == i:
        return 'blue'
    return None


def _cc(S, r, c, v):
    I = S['_inner']
    if 'last_word' in I and S.get('_line') in (58, 59, 60) and I.get('i') is not None and r == I['i'] and c == I['last_word']:
        return 'yellow'
    return None


def _txt(S):
    I = S['_inner']
    if 'state' not in I or 'last_word' not in I:
        return '`common[i][j]`：词 i 的后缀 = 词 j 的前缀，最多重叠几个字符（对角线 = 词长）'
    st = I['state']
    used = '、'.join(W[k] for k in range(N) if st >> k & 1)
    return f'`state = {st:0{N}b}`：已用 {used}；以 =={W[I["last_word"]]}== 结尾'


CONFIG = dict(
    num=943, title='最短超级串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 后缀/前缀重叠 + prev 还原',
    tags=['状压 DP', '输出具体方案'],
    code='''
class Solution(object):
    def shortestSuperstring(self, words):

        n = len(words)

        suffix_set_list = []
        for i in range(n):
            suffix_set_list.append(set())
            for j in range(len(words[i]) - 1, 0, -1):
                suffix_set_list[-1].add(words[i][j:])

        common = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    for p in range(len(words[j]) - 1, 0, -1):
                        if words[j][:p] in suffix_set_list[i]:
                            common[i][j] = p
                            break
            common[i][i] = len(words[i])

        f = [[None] * n for _ in range(1 << n)]
        prev = [[None] * n for _ in range(1 << n)]

        min_len, last_word = None, None
        state = (1 << n) - 1

        for i in range(n):
            if min_len is None or self.dfs(state, i, n, f, common, prev) < min_len:
                min_len = self.dfs(state, i, n, f, common, prev)
                last_word = i
        
        res = ''
        while last_word is not None:
            prev_word = prev[state][last_word]
            if prev_word is None:
                common_len = 0
            else:
                common_len = common[prev_word][last_word]
            res = words[last_word][common_len:] + res
            state -= (1 << last_word)
            last_word = prev_word
        
        return res

    def dfs(self, state, last_word, n, f, common, prev):
        if f[state][last_word] is None:
            used = set()
            for i in range(n):
                if state & (1 << i):
                    used.add(i)

            if len(used) == 1:
                f[state][last_word] = common[last_word][last_word]
            else:
                prev_state = state - (1 << last_word)
                for i in used:
                    if i != last_word and (f[state][last_word] is None or f[state][last_word] > self.dfs(prev_state, i, n, f, common, prev) + common[last_word][last_word] - common[i][last_word]):
                        f[state][last_word] = self.dfs(prev_state, i, n, f, common, prev) + common[last_word][last_word] - common[i][last_word]
                        prev[state][last_word] = i
            
        return f[state][last_word]
''',
    call=f'Solution().shortestSuperstring({W})',
    expect='cdefabcd',
    skip=[4, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 19, 20, 25, 26, 47, 48, 49, 50, 51, 56, 57],
    views=[
        dict(type='text', fn=_txt, size=22, h=64),
        dict(type='table', var=_cm, label='common[i][j]：i 的后缀 = j 的前缀，最长几位（0 abcd，1 cdef，2 efab）', h=220, cell=64,
             rows=lambda S: [f'{k}' for k in range(N)], cols=lambda S: [f'{k}' for k in range(N)], color=_cc),
        dict(type='table', var=_ft, label='f[state][i]：行 = 已用词集合，列 = 结尾词，值 = 最短长度', h=330, cell=60,
             rows=lambda S: [format(x, f'0{N}b') for x in range(1 << N)], cols=lambda S: [str(x) for x in range(N)], color=_col),
        dict(type='calls', h=140, hide=('f', 'common', 'prev', 'n')),
        dict(type='text', fn=lambda S: f'答案拼接中：`res = {S["res"]!r}`' if 'res' in S else '', size=24, h=50),
    ],
    watch=[('state', lambda S: format(S['_inner']['state'], f'0{N}b') if 'state' in S['_inner'] else '', 'cyan'),
           ('last_word', lambda S: S['_inner'].get('last_word'), 'blue'), ('i', lambda S: S['_inner'].get('i'), 'pink'),
           ('min_len', lambda S: S.get('min_len'), 'green')],
    captions={
        'common = [[0]': '`common[i][j]` 初始为 0；先用「后缀集合」两两求出重叠长度',
        'common[i][j] = p': '`common[{i}][{j}] = {p}`：`{words[i]}` 的后缀 = `{words[j]}` 的前缀，重叠 {p} 个字符',
        'f = [[None]': '`f[state][i]`：用了 state 里的词、以词 i 结尾的最短长度；`None` = 没算过',
        'prev = [[None]': '`prev[state][i]`：这个最优解里，词 i 前面的那个词，用来还原方案',
        'if min_len is None or self.dfs': '枚举最后一个词 `i = {i}`：算 `f[全集][{i}]`，和当前最短 `min_len = {min_len}` 比',
        'min_len = self.dfs': '更短（或第一次）→ 把 `f[全集][{i}]` 记为新的 `min_len`',
        'last_word = i': '最后一个词暂定为 `{words[i]}`',
        53: lambda S, B, r: ('`state` 里只有一个词 → 长度就是这个词的长度' if len(S.used) == 1 else f'`state` 里有 {len(S.used)} 个词 → 枚举倒数第二个词 `i`'),
        54: lambda S, B, r: f'只有一个词：`f[{S.state:0{N}b}][{S.last_word}]` = 词长 =={S.common[S.last_word][S.last_word]}==',
        58: lambda S, B, r: (f'`i = {S.i}` 就是 last_word 自己 → 跳过' if S.i == S.last_word else
                             f'倒数第二个词试 `{S.i}`：`f[{S.prev_state:0{N}b}][{S.i}] + 词长 {S.common[S.last_word][S.last_word]} − 重叠 {S.common[S.i][S.last_word]}`，比当前 f 更小才采用'),
        59: '采用这个选择：`f[state][last_word] = f[prev_state][i] + 词长 − 重叠`（再次递归取值，已记忆化，直接返回）',
        60: lambda S, B, r: f'`prev[{S.state:0{N}b}][{S.last_word}] = {S.i}`：记下前一个词',
        62: lambda S, B, r: f'`f[{S.state:0{N}b}][{S.last_word}]` = =={r}==',
        'while last_word is not None': lambda S, B, r: ('`last_word` 为 None：所有词都拼完了' if S.last_word is None else f'还原：当前最后一个词是 `{S.words[S.last_word]}`'),
        'prev_word = prev': '`prev_word = {prev_word}`：它前面的词',
        'if prev_word is None': lambda S, B, r: ('没有前一个词 → 整个词都要接上' if S.prev_word is None else f'有前一个词 → 和它重叠 `common[{S.prev_word}][{S.last_word}]` = {S.common[S.prev_word][S.last_word]} 个字符'),
        'common_len = 0': '没有重叠',
        'common_len = common[': '重叠 `common_len = {common_len}`',
        'res = words[last_word][common_len:] + res': '把 `{words[last_word]}` 去掉重叠的前 `{common_len}` 个字符，接到最前面：`res = {res}`',
        'state -= ': '`state` 去掉这个词：`{state:0{N}b}`',
        'last_word = prev_word': '回到前一个词 `{last_word}`',
        'return res': '最短超级串：`{ret}`（长度 {len(ret)}）',
    },
    max_steps=60,
    cards=dict(
        one_liner='字符串两两重叠 + 状压：f[已用词集合][最后一个词]',
        complexity='时间 `O(n^2 2^n + n^2 L^2)`，空间 `O(n 2^n)`',
        problem=['给定一组互不包含的字符串 `words`，求包含所有词作为子串的==最短字符串==',
                 '本视频：`["abcd","cdef","efab"]` → `cdefabcd`（长度 8）',
                 '（题目保证没有词是另一个词的子串；答案可能不唯一）'],
        quote='所有共用字符的情况就只可能是某个串的后缀能匹配上另一个串的前缀。……串的个数比较少，最多只有12个，那么可以使用状态压缩来表示当前使用了哪些串。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理 `common[i][j]`：i 的后缀和 j 的前缀最多能重叠几位',
              '`f[state][i]`：用了 state 里的词、以 i 结尾的最短长度；新加入 i 就是 `f[state - i][last] + len(i) - common[last][i]`',
              '用 `prev[state][i]` 记下倒数第二个词，最后从答案往回倒推拼出字符串'],
        summary=['时间 `O(n^2 2^n)`（再加预处理重叠 `O(n^2 L^2)`），空间 `O(n 2^n)`',
                 '不能贪心：一个串可能和多个串重叠，要用状压 DP 试所有顺序',
                 '还原时每次拼接的是 `words[i][common_len:]`（去掉与前一个词重叠的部分）',
                 '题面库里没有，题意按 LeetCode 943 补写；原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
