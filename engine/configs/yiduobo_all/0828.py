S0 = 'ABACB'


def _col(S, k, v):
    i = S.get('index')
    if i is None or 'prev_pos' not in S or S.get('_line', 0) < 31:
        return None
    if k == i:
        return 'blue'
    if k == S['prev_pos']:
        return 'orange'
    if 'next_pos' in S and k == S['next_pos']:
        return 'pink'
    return None


def _txt(S):
    if 'next_pos' not in S or 'index' not in S or 'res' not in S or S.get('_line', 0) < 31:
        return '字母 `s[index]` 的得分 = ==往左扩 × 往右扩== = `(index−prev) × (next−index)`'
    i, p, q = S['index'], S['prev_pos'], S['next_pos']
    return f'`s[{i}]` 得分 = `({i}−({p})) × ({q}−{i})` = =={(i - p) * (q - i)}==（`res` 累计 {S["res"]}）'


def _tabs(S):
    if 'prev' not in S or 'next' not in S or S.get('_line', 0) < 20:
        return '`prev[i]`：前缀里各字母最后出现的位置；`next[i]`：后缀里各字母最早出现的位置'
    i = S['index']
    p = S['prev'][i - 1] if i > 0 else {}
    q = S['next'][i + 1] if i + 1 < len(S['next']) else {}
    return f'`prev[{i - 1}]` = {p}\n`next[{i + 1}]` = {q}' if i > 0 else f'`next[{i + 1}]` = {q}'


CONFIG = dict(
    num=828, title='统计子串中的唯一字符', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换个角度：逐字母算贡献 · 前驱/后继位置',
    tags=['灵神题单', '动态规划', '难度分 2034'],
    code='''
class Solution(object):
    def uniqueLetterString(self, s):

        if not s:
            return 0

        mod = 10 ** 9 + 7
        n = len(s)
        prev = [{s[0] : 0}]
        for index in range(1, n):
            prev.append(prev[-1].copy())
            prev[-1][s[index]] = index
        next = [{s[n - 1] : n - 1}]
        for index in range(n - 2, -1, -1):
            next.append(next[-1].copy())
            next[-1][s[index]] = index
        next.reverse()
        
        res = 0
        for index, char in enumerate(s):
            if index == 0:
                prev_pos = -1
            else:
                prev_pos = prev[index - 1].get(char, -1)
            
            if index == n - 1:
                next_pos = n
            else:
                next_pos = next[index + 1].get(char, n)
            
            res += (index - prev_pos) * (next_pos - index)
            res %= mod

        return res
''',
    call=f'Solution().uniqueLetterString({S0!r})',
    expect=25,
    skip=['for index in range', 'prev.append', 'next.append', 'for index, char', 'next.reverse', 'prev[-1][', 'next[-1]['],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字母，橙 = 左边同字母，粉 = 右边同字母）', h=260, cell=90,
             pointers={'index': 'blue'}, color=_col),
        dict(type='text', fn=_txt, size=26, h=80),
        dict(type='text', size=24, h=120, fn=_tabs),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('prev_pos', 'prev_pos', 'orange'),
           ('next_pos', 'next_pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not s': '空串直接返回 0，本例不会进入',
        'mod = ': '结果取模，本例很小',
        'n = len(s)': '`n = {n}`',
        'prev = [': '`prev[i]` 是一张表：前缀 `s[0..i]` 里每个字母==最后一次出现==的位置',
        'next = [': '`next[i]` 是一张表：后缀 `s[i..]` 里每个字母==第一次出现==的位置（从右往左建，最后再反转）',
        'res = 0': '`res` 累计所有字母的得分',
        'prev_pos = -1': '第一个字符左边没有字母 → `prev_pos = -1`',
        'prev_pos = prev[': '`s[{index}] = {char}` 左边最近的同字母下标：`prev_pos = {prev_pos}`（没有就是 -1）',
        27: '最后一个字符右边没有字母 → `next_pos = n`',
        29: '`s[{index}] = {char}` 右边最近的同字母下标：`next_pos = {next_pos}`（没有就是 n）',
        'res += ': ('这个字母只在“左端点在 `prev_pos` 之后、右端点在 `next_pos` 之前”的子串里唯一：'
                    '`{index - prev_pos}` × `{next_pos - index}` → `res` = =={res}=='),
        'res %= mod': '取模，值不变：`res = {res}`',
        'return res': '全部字母的得分之和 = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='不数子串，数字母：每个字母的得分 = 左扩 × 右扩',
        complexity='时间 `O(n·|Σ|)`（每步复制字典），空间 `O(n·|Σ|)`',
        problem=['子串得分 = 其中只出现一次的字母个数',
                 '求 `s` 所有子串的得分之和',
                 '示例：`"ABC"` → `10`；本视频：`"ABACB"` → `25`'],
        quote='对于位于index的字母，我们可以先计算出其该字母上一次出现的位置prev，以及下一次出现的位置next，那么该字符可以往左侧扩展的长度就是index - prev，可以往右扩展的长度则为next - index。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目从子串出发，yiduobo 改从单个字母出发：它在哪些子串里是唯一的',
              '左端点只能在 `prev` 之后，右端点只能在 `next` 之前 → ==左扩 × 右扩==',
              '`prev` / `next` 用正反两趟扫描的 DP 预处理'],
        summary=['时间 `O(n·26)`，因为每一步复制一份字典；空间同阶',
                 '易错：没有前驱记 `-1`、没有后继记 `n`',
                 '边界下标 0 和 n-1 要单独处理，避免越界',
                 '对比灵神：灵神按右端点分组维护 `total`，yiduobo 按字母算贡献'],
    ),
)
