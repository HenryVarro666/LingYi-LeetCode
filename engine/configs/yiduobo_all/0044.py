S0, P0 = 'adceb', '*a*b'


def _info(S):
    if 'i' not in S:
        return ''
    i, j, sp, pp = S['i'], S['j'], S.get('s_pos', -1), S.get('p_pos', -1)
    s, p = S['s'], S['p']
    if i < len(s) and j < len(p):
        cur = f"`s[{i}] = {s[i]}`  对  `p[{j}] = {p[j]}`"
    elif i >= len(s):
        cur = f'`s` 已经走完（`i = {i}`），只看 `p` 剩下的 `{p[j:]}`'
    else:
        cur = f"`s[{i}] = {s[i]}`，`p` 已走完（`j = {j}`）"
    star = f'；最近的 `*` 在 `p[{pp}]`，它目前吞到 `s[{sp}]` 之前' if pp >= 0 else '；还没遇到 `*`'
    return cur + star


def _ptr(S, name):
    v = S.get(name)
    return v


def _sc(S, k, v):
    if 'i' not in S:
        return None
    sp, i = S.get('s_pos', -1), S['i']
    if k == i:
        return 'blue'
    if sp >= 0 and sp <= k < i:
        return 'orange'
    return None


def _pc(S, k, v):
    if 'j' not in S:
        return None
    if k == S['j']:
        return 'pink'
    if k == S.get('p_pos', -1):
        return 'orange'
    return None


CONFIG = dict(
    num=44, title='通配符匹配', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贪心 + 回溯到最近的星号',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def isMatch(self, s, p):

        m = len(s)
        n = len(p)
        i = 0
        j = 0
        s_pos = -1
        p_pos = -1

        while i < m:
            if j < n and (p[j] == '?' or p[j] == s[i]):
                i += 1
                j += 1
            elif j < n and p[j] == '*':
                s_pos = i
                p_pos = j
                j += 1
            elif s_pos >= 0:
                s_pos += 1
                i = s_pos
                j = p_pos
            else:
                return False

        for index in range(j, n):
            if p[index] != '*':
                return False
        
        return True
''',
    call=f'Solution().isMatch({S0!r}, {P0!r})',
    expect=True,
    skip=['m = len', 'n = len', 'else:'],
    views=[
        dict(type='string', var='s', label='s（蓝 = i，橙 = 被 * 暂时吞掉的部分）', h=170, cell=64,
             pointers={'i': 'blue'}, color=_sc),
        dict(type='string', var='p', label='p（粉 = j，橙 = 最近的 *）', h=170, cell=64,
             pointers={'j': 'pink'}, color=_pc),
        dict(type='text', fn=_info, size=24, h=90),
    ],
    watch=['i', 'j', ('s_pos', 's_pos', 'orange'), ('p_pos', 'p_pos', 'orange')],
    captions={
        'i = 0': '`i` 指向 `s` 的开头',
        'j = 0': '`j` 指向 `p` 的开头',
        'p_pos = -1': '`p_pos = -1`：同上',
        's_pos = -1': '`s_pos`、`p_pos` 记下最近一个 `*` 的位置，-1 表示还没遇到',
        'while i < m': lambda S, B, r: (f'`i = {S.i} < m = {S.m}`：`s` 还没匹配完，继续' if S.i < S.m else f'`i = {S.i} = m`：`s` 已全部匹配，只剩检查 `p` 的尾巴'),
        "p[j] == '?' or": lambda S, B, r: (f"`p[{S.j}] = {S.p[S.j]}` 与 `s[{S.i}] = {S.s[S.i]}` 能配上 → 一一对应，两个指针一起走" if S.j < S.n and (S.p[S.j] == '?' or S.p[S.j] == S.s[S.i])
                                           else (f"`p[{S.j}] = {S.p[S.j]}` 配不上 `s[{S.i}] = {S.s[S.i]}`，再看是不是 `*`" if S.j < S.n else '`p` 已经用完，看能否回退到星号')),
        'i += 1': '`i` → {i}',
        'j += 1': '`j` → {j}',
        "p[j] == '*'": lambda S, B, r: (f'`p[{S.j}] = *` → ==先假设它匹配 0 个字符==，记下位置' if S.j < S.n and S.p[S.j] == '*' else f'`p[{S.j}] = {S.p[S.j]}` 也不是 `*`'),
        's_pos = i': '`s_pos = {s_pos}`：记住 `*` 此刻对应 `s` 的位置',
        'p_pos = j': '`p_pos = {p_pos}`：记住 `*` 在 `p` 里的位置',
        'elif s_pos >= 0': lambda S, B, r: (f'配不上，但前面有 `*`（`p_pos = {S.p_pos}`）→ ==回退==，让它多吞一个字符' if S.s_pos >= 0 else '配不上，前面也没有 `*` → 无解'),
        's_pos += 1': '`*` 多吞一个字符：`s_pos` → {s_pos}',
        'i = s_pos': '`s` 从 `{i}` 重新匹配',
        'j = p_pos': '`p` 回到星号位置 `{j}`，之后从 `*` 的下一格重新比',
        'return False': '没有任何办法匹配 → `False`',
        'for index in range': lambda S, B, r: ((f'`s` 已走完，检查 `p[{S.j}:]` = `{S.p[S.j:]}` 是不是只剩 `*`' if S.j < S.n else f'`s` 已走完，`j = {S.j} = n`：`p` 也恰好用完，没有多余字符要检查') if S.get('index') is None else f'检查 `p[{S.index}] = {S.p[S.index]}`'),
        'if p[index]': lambda S, B, r: (f'`p[{S.index}] = {S.p[S.index]}` 不是 `*`，没有字符可匹配 → 不行' if S.p[S.index] != '*' else f'`p[{S.index}]` 是 `*`，可以匹配空串'),
        'return True': '`s` 匹配完，`p` 剩下的都是 `*` → ==匹配成功==',
    },
    cards=dict(
        one_liner='星号先当空串用，配不上再让它多吞一个字符',
        complexity='最坏 `O(mn)`，空间 `O(1)`',
        problem=['`?` 匹配任意单个字符，`*` 匹配任意字符序列（含空）；`p` 要==完整匹配== `s`',
                 '示例：`s = "aa"`，`p = "*"` → `true`；`s = "cb"`，`p = "?a"` → `false`',
                 '本视频：`s = "adceb"`，`p = "*a*b"` → `true`'],
        quote='在遇到一个星号时，我们可以假设其匹配了零个字符，然后往后匹配。当匹配不了时，让星号往后兼容s中的一个字符，再从星号后面重新开始匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['平方 DP 会超时；星号太强，改用双指针 + 回退',
              '遇到 `*` 就记下 `s_pos`、`p_pos`，先让它吞 0 个字符继续比',
              '失败时只回退到最近的 `*`：它多吞一个字符，从其后重新匹配'],
        summary=['时间最坏 `O(mn)`（原文也说复杂度不好分析），空间 `O(1)`',
                 '易错：`s` 走完后，`p` 剩下的必须全是 `*`，要单独检查',
                 '易错：只需记最近一个 `*`，更早的星号不用回退（后面的星号已经能兼容）',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '同类题：10. 正则表达式匹配（那题 `*` 的含义不同，需要 DP）'],
    ),
)
