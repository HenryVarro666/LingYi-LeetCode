S0 = 'abba'


def _inner(S):
    return S.get('_inner') or S


def _tcolor(S, r, c, v):
    I = _inner(S)
    l, r_ = I.get('l'), I.get('r')
    if l is None or r_ is None:
        return None
    if (r, c) == (l, r_):
        return 'yellow'
    return None


def _scolor(S, k, v):
    I = _inner(S)
    l, r = I.get('l'), I.get('r')
    if l is None or r is None:
        return None
    if l <= k <= r:
        return 'blue'
    return None


def _fml(S):
    I = _inner(S)
    ch, npos, ppos = I.get('char'), I.get('next_pos'), I.get('prev_pos')
    if 'l' not in I or 'f' not in I:
        return '`f[l][r]` = `s[l..r]` 里不同回文子序列的个数（空串也算 1 个）'
    if ch is None:
        return f'区间 `[{I["l"]}, {I["r"]}]`：对 a、b、c、d 各找最左、最右出现位置'
    return f'字符 `{ch}`：最左 `next_pos = {npos}`，最右 `prev_pos = {ppos}`'


CONFIG = dict(
    num=730, title='统计不同回文子序列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 枚举两端字符去重',
    tags=[],
    code='''
class Solution(object):
    def countPalindromicSubsequences(self, S):

        mod = 10 ** 9 + 7
        n = len(S)

        pos_dict = {}
        prev_pos_list = []
        for index in range(n):
            pos_dict[S[index]] = index
            prev_pos_list.append(pos_dict.copy())
        
        pos_dict = {}
        next_pos_list = []
        for index in range(n - 1, -1, -1):
            pos_dict[S[index]] = index
            next_pos_list.append(pos_dict.copy())
        next_pos_list.reverse()
        
        f = [[None] * n for _ in range(n)]

        res = self.dfs(0, n - 1, f, next_pos_list, prev_pos_list, mod)
        if res == 0:
            return mod - 1
        else:
            return res - 1
        
    
    def dfs(self, l, r, f, next_pos_list, prev_pos_list, mod):
        if l > r:
            return 1
        if l == r:
            return 2

        if f[l][r] is None:
            f[l][r] = 1
            for char in ['a', 'b', 'c', 'd']:
                next_pos = next_pos_list[l].get(char, None)
                prev_pos = prev_pos_list[r].get(char, None)
                if next_pos is not None and l <= next_pos and next_pos <= r:
                    f[l][r] += 1
                if next_pos is not None and next_pos < prev_pos:
                    f[l][r] += self.dfs(next_pos + 1, prev_pos - 1, f, next_pos_list, prev_pos_list, mod)
                f[l][r] %= mod

        return f[l][r]
''',
    call=f'Solution().countPalindromicSubsequences({S0!r})',
    expect=6,
    skip=['mod = 10', 'n = len', 'pos_dict = {}', 'prev_pos_list = []', 'next_pos_list = []', 'for index in range',
          'pos_dict[S[index]]', 'prev_pos_list.append', 'next_pos_list.append', 'next_pos_list.reverse'],
    views=[
        dict(type='string', var='S', label='S（蓝 = 当前区间 [l, r]）', cell=80, h=150, color=_scolor),
        dict(type='text', fn=_fml, size=24, h=56),
        dict(type='table', var='f', label='f[l][r]（黄 = 当前区间；空 = 还没算）', cell=64, h=330,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_tcolor),
        dict(type='calls', h=200, hide=('f', 'next_pos_list', 'prev_pos_list', 'mod')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'char', 'next_pos', 'prev_pos'],
    captions={
        'for char in': lambda S, B, r: (f'依次试 a、b、c、d 作为端点字符：先 `{S.char}`' if 'char' not in (B.get('_inner') or B)
                                        else (f'换下一个端点字符：`{S.char}`' if S.get('char') != B.get('char') else f'a、b、c、d 都试过了，区间 `[{S.l},{S.r}]` 算完')),
        'f = [[None]': '预处理完成：`prev_pos_list[i][c]` = i 及左边最后一个 c，`next_pos_list[i][c]` = i 及右边第一个 c；`f` 是记忆化表',
        'res = self.dfs(0': '求整个串 `[0, {n-1}]` 的 `f[0][{n-1}]`，空串也算 1 个，最后再减掉',
        'if l > r': lambda S, B, r: ('`l > r`：空区间，只有空串 → 返回 1' if S.l > S.r else '`l <= r`：区间非空，继续'),
        'if l == r': lambda S, B, r: ('`l == r`：单个字符 → 本身 + 空串 = 2' if S.l == S.r else '`l < r`：区间里至少两个字符'),
        'if f[l][r] is None': lambda S, B, r: ('`f[{0}][{1}]` 还没算 → 开始算'.format(S.l, S.r) if S.f[S.l][S.r] is None else '`f[{0}][{1}]` 算过了 → 直接用'.format(S.l, S.r)),
        'f[l][r] = 1': '先把空串记上：`f[{l}][{r}] = 1`',
        'next_pos = next_pos_list': lambda S, B, r: (
            f'区间 `[{S.l},{S.r}]` 里字符 `{S.char}` ==最左==出现的位置：`next_pos = {S.next_pos}`' if S.next_pos is not None and S.l <= S.next_pos <= S.r
            else f'字符 `{S.char}`：`next_pos = {S.next_pos}`，不在区间 `[{S.l},{S.r}]` 内'),
        'prev_pos = prev_pos_list': lambda S, B, r: (
            f'区间 `[{S.l},{S.r}]` 里字符 `{S.char}` ==最右==出现的位置：`prev_pos = {S.prev_pos}`' if S.prev_pos is not None and S.l <= S.prev_pos <= S.r
            else f'字符 `{S.char}`：`prev_pos = {S.prev_pos}`，不在区间内 → 区间里没有 `{S.char}`'),
        'if next_pos is not None and l <=': lambda S, B, r: (f'区间里有 `{S.char}` → 单独一个 `{S.char}` 是回文，==+1==' if (S.next_pos is not None and S.l <= S.next_pos <= S.r) else f'区间里没有 `{S.char}` → 跳过'),
        'f[l][r] += 1': '`f[{l}][{r}]` = =={f[l][r]}==（算上单独的 `{char}`）',
        'if next_pos is not None and next_pos < prev_pos': lambda S, B, r: (
            f'`{S.next_pos} < {S.prev_pos}`：有两个不同位置的 `{S.char}` → 可作回文==两端==' if (S.next_pos is not None and S.next_pos < S.prev_pos)
            else (f'`{S.char}` 只有一个位置 → 只能单取；中间那些 `{S.char}` 不当端点，==这就是去重==' if (S.next_pos is not None and S.l <= S.next_pos <= S.r) else f'没有 `{S.char}`，换下一个字符')),
        'f[l][r] += self.dfs': '最左、最右各取一个 `{char}`：中间 {"空区间" if next_pos+1 > prev_pos-1 else f"`[{next_pos+1},{prev_pos-1}]`"} 的每个回文都能套上这对端点 → 递归',
        'f[l][r] %= mod': '累加完、取模：`f[{l}][{r}]` = =={f[l][r]}==',
        'return f[l][r]': '区间 `[{l},{r}]` 共 `{f[l][r]}` 个（含空串）',
        'return 1': '空区间返回 1',
        'return 2': '单字符返回 2',
        'if res == 0': '`res = {res}`：含空串的总数；取模后为 0 的话答案要 `mod − 1`',
        'return res - 1': '减去空串：答案 = =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='看两端字符 a/b/c/d：最左、最右各取一个，中间的重复字符不当端点',
        complexity='时间 `O(n^2 · 4)`，空间 `O(n^2)`',
        problem=['字符串 `s` 只含 `a b c d`，求==不同的非空回文子序列==个数，对 `10^9+7` 取模',
                 '子序列内容相同就算同一个（和位置无关）',
                 '示例：`bccb` → `6`；本视频：`abba`'],
        quote='对于所有形如X...X...X的字符串，中间的这个X不能作为当前字符串的回文子序列的端点',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[l][r]` = 区间里不同回文子序列数，空串也算一个',
              '去重：枚举端点字符 `c`，只取区间内==最左和最右的 c==',
              '单取 `c` 算 1 个；左右都取则加 `f[next+1][prev-1]`（外面套上 c 两端）'],
        summary=['时间 `O(4n^2)`，空间 `O(n^2)`（记忆化 + 预处理 next/prev）',
                 '易错：`f` 把空串算进去了，最后要 `res - 1`；取模后为 0 时答案是 `mod - 1`',
                 '易错：`next_pos == prev_pos` 时只有一个 c，只能单取，不能当两端',
                 '预处理：正扫、反扫各一遍，得到每个位置之后最近 / 之前最近的 a-d 下标'],
    ),
)
