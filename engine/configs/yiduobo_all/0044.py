def _t(S):
    if 'i' not in S:
        return ''
    s, p, i, j = S['s'], S['p'], S['i'], S['j']
    a = f"`s[{i}]`" if i < len(s) else 's 已用完'
    b = f"`p[{j}] = {p[j]}`" if j < len(p) else 'p 已用完'
    return f"看 {a} 和 {b}；记住的星号位置：s_pos = ==`{S['s_pos']}`==，p_pos = ==`{S['p_pos']}`=="


CONFIG = dict(
    num=44, title='通配符匹配', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贪心双指针 + 星号回退',
    tags=['灵神题单·动态规划'],
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
    call='Solution().isMatch("adceb", "*a*b")',
    expect=True,
    skip=['m = len', 'n = len', 'i = 0', 'j = 0', 'for index in range'],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = i；紫格 = 星号吞到的位置 s_pos）', cell=84, h=190,
             pointers={'i': 'blue'},
             color=lambda S, k, v: 'purple' if k == S.get('s_pos') else None),
        dict(type='string', var='p', label='p（粉箭头 = j；橙格 = 回退用的星号 p_pos）', cell=84, h=190,
             pointers={'j': 'pink'},
             color=lambda S, k, v: 'orange' if k == S.get('p_pos') else ('purple' if v == '*' else None)),
        dict(type='text', fn=_t, size=26, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s_pos', 's_pos', 'purple'), ('p_pos', 'p_pos', 'purple')],
    captions={
        's_pos = -1': '`s_pos`、`p_pos` 记录最近一个星号的位置，`-1` 表示还没遇到星号',
        'while i < m': lambda S, B, r: (f'`i = {B.i} < m = {B.m}`：s 还没匹配完，继续' if B.i < B.m else f'`i = {B.i} == m`：s 全部用完，看 p 剩下什么'),
        "p[j] == '?' or p[j] == s[i]": lambda S, B, r: (f"`p[{B.j}] = {B.p[B.j]}` 能匹配 `s[{B.i}] = {B.s[B.i]}`（`?` 或字符相同）→ ==两个指针一起前进=="
            if B.j < B.n and (B.p[B.j] in '?' or B.p[B.j] == B.s[B.i]) else
            f"`p[{B.j}]` 不能直接匹配 `s[{B.i}] = {B.s[B.i]}`"),
        13: '匹配成功：`i` → {i}，`j` 随后也加一',
        14: '`j` → {j}：两个指针都往后走了一格',
        15: lambda S, B, r: ('遇到星号 `*`：先假设它==匹配 0 个字符==，往后继续比' if B.j < B.n and B.p[B.j] == '*'
                             else '也不是星号，这一步只能靠回退了'),
        16: '记下星号对应的 s 位置：`s_pos = {s_pos}`',
        17: '`p_pos = {p_pos}`：以后失败了就回到这个星号',
        18: '`j` → {j}：越过星号，从星号后面开始比',
        'elif s_pos >= 0': lambda S, B, r: (f'当前无法匹配，但前面有星号（`s_pos = {B.s_pos}`）→ 可以让它多吞一个字符' if B.s_pos >= 0
                                           else '当前无法匹配，前面也没有星号可以回退'),
        's_pos += 1': '星号==多吞一个字符==：`s_pos` → {s_pos}',
        'i = s_pos': '`i` 回到星号吞完之后的位置 `{i}`',
        'j = p_pos': '`j` 回到星号 `{j}`，之后会再次走星号分支、从它后面重新匹配',
        24: '没有星号可回退，匹配失败 → `False`',
        27: '`p[{index}] = {p[index]}`：s 已用完，p 剩下的必须全是 `*` 才能匹配空串',
        28: '剩下的有非星号字符 → 不匹配 → `False`',
        'return True': 's 用完，p 剩余的全是 `*`（都能匹配空串）→ ==匹配成功== `True`',
    },
    cards=dict(
        one_liner='遇到星号先当空串，失败了就让星号多吞一个字符',
        complexity='最坏 `O(mn)`，空间 `O(1)`',
        problem=['`s` 是字符串，`p` 是含 `?` 和 `*` 的模式，要求整串匹配',
                 '`?` 匹配任意单个字符，`*` 匹配任意长度（含 0）的字符串',
                 '示例：`s = "adceb"`，`p = "*a*b"` → `true`'],
        quote='遇到一个星号时，我们可以假设其匹配了零个字符，然后往后匹配。当匹配不了时，让星号往后兼容s中的一个字符，再从星号后面重新开始匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['平方 DP 会超时，所以改用贪心双指针',
              '星号先匹配 0 个字符；记下 `s_pos`、`p_pos` 作为回退点',
              '后面失败就让星号多吞一个字符，`i`、`j` 回到回退点重新比'],
        summary=['时间最坏 `O(mn)`，空间 `O(1)`（原文也说复杂度不好分析）',
                 '易错：循环结束后要检查 `p` 剩下的部分是否全是 `*`',
                 '只记==最近一个==星号就够了：前面的星号已经足够灵活，不需要回退',
                 '原文本身就是 Python 3 可运行的写法，代码未改'],
    ),
)
