def _top(S):
    if 'flag' not in S or S['_line'] in (4, 5, 6, 7, 8, 9):
        return f"已统计有效单词 `res = {S.get('res', 0)}`"
    return (f"当前 token 还可能有效，`hyphen_flag = {S['hyphen_flag']}`" if S['flag'] else '当前 token 已经==无效==，后面字符直接跳过')


def _col(S, i, v):
    p = S.get('p')
    if p is None:
        return None
    if i == p:
        return 'blue'
    return None


def _dim(S, i, v):
    p = S.get('p')
    return p is not None and i < p and v == ' '


def _chk(S, B, ret):
    s, p = S['sentence'], S['p']
    c = s[p]
    pre = s[p - 1] if p > 0 else '无'
    nxt = s[p + 1] if p + 1 < len(s) else '无'
    return c, pre, nxt


CONFIG = dict(
    num=2047, title='句子中的有效单词数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='手写遍历 · 两个标记 flag / hyphen_flag',
    code='''
class Solution(object):
    def countValidWords(self, sentence):

        res = 0
        p = 0
        n = len(sentence)
        while p < n:
            while p < n and sentence[p] == ' ':
                p += 1
            
            if p == n:
                break

            flag = True
            hyphen_flag = False

            while p < n and sentence[p] != ' ':
                if not flag:
                    pass
                elif sentence[p] >= '0' and sentence[p] <= '9':
                    flag = False

                elif sentence[p] == '-':
                    if hyphen_flag:
                        flag = False
                    elif p > 0 and sentence[p - 1] >= 'a' and sentence[p - 1] <= 'z' and p + 1 < n and sentence[p + 1] >= 'a' and sentence[p + 1] <= 'z':
                        hyphen_flag = True
                    else:
                        flag = False

                elif sentence[p] == '!' or sentence[p] == '.' or sentence[p] == ',':
                    if p + 1 < n and sentence[p + 1] != ' ':
                        flag = False
                
                p += 1

            if flag:
                res += 1
        
        return res
''',
    call='Solution().countValidWords("cat  b8 a-b!")',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='sentence', label='sentence（蓝 = 当前位置 p，空格也占一格）', cell=84,
             pointers={'p': 'blue'}, color=_col, dim=_dim, h=220),
    ],
    watch=[('p', 'p', 'blue'), ('flag', 'flag', 'orange'), ('hyphen_flag', 'hyphen_flag', 'cyan'), ('res', 'res', 'green')],
    max_steps=90,
    captions={
        'res = 0': '`res` 统计有效单词数',
        'p = 0': '`p` 是当前扫描的位置',
        'n = len(sentence)': '`n = {n}`',
        'while p < n:': lambda S, B, ret: (f'`p = {S.p} < n = {S.n}`，还有字符没处理，开始找下一个 token' if S.p < S.n else f'`p = {S.p} == n`，句子扫完了'),
        'while p < n and sentence[p] == ': lambda S, B, ret: (f"`sentence[{S.p}]` 是空格吗？是 → 跳过" if S.p < S.n and S.sentence[S.p] == ' ' else '不是空格了：这里就是 token 的开头'),
        'p += 1': lambda S, B, ret: f'`p` → {S.p}',
        'if p == n': lambda S, B, ret: ('`p == n`：后面全是空格，没有 token 了 → 结束' if S.p == S.n else f'`p = {S.p} != n`，找到了一个 token'),
        14: '新 token：`flag = True`，先假设它是有效单词',
        15: '`hyphen_flag = False`：还没出现过合法连字符',
        'while p < n and sentence[p] != ': lambda S, B, ret: (f"token 还没结束：`sentence[{S.p}] = '{S.sentence[S.p]}'`" if S.p < S.n and S.sentence[S.p] != ' ' else 'token 到头了（遇到空格或句尾）'),
        'if not flag': lambda S, B, ret: ('`flag` 已经是 False：这个 token 无效了，字符不用再处理' if not S.flag else '`flag` 还是 True，继续检查这个字符'),
        'pass': '什么都不做，只往后走',
        'elif sentence[p] >= \'0\'': lambda S, B, ret: (f"`'{S.sentence[S.p]}'` 是数字 → ==token 含数字，无效==" if '0' <= S.sentence[S.p] <= '9' else f"`'{S.sentence[S.p]}'` 不是数字"),
        'flag = False': '`flag = False`：这个 token 无效，后面的字符都不用看了',
        'elif sentence[p] == \'-\'': lambda S, B, ret: (f"`'{S.sentence[S.p]}'` 是连字符，要看是不是第一个、两边是不是小写字母" if S.sentence[S.p] == '-' else f"`'{S.sentence[S.p]}'` 不是连字符"),
        'if hyphen_flag': lambda S, B, ret: ('`hyphen_flag = True`：已经有一个合法连字符，这是第二个 → ==无效==' if S.hyphen_flag else '`hyphen_flag = False`：这是第一个连字符，继续看两边'),
        'elif p > 0 and': lambda S, B, ret: ('连字符两边都是小写字母吗？' + ('是 → 这是合法连字符' if (S.p > 0 and 'a' <= S.sentence[S.p - 1] <= 'z' and S.p + 1 < S.n and 'a' <= S.sentence[S.p + 1] <= 'z') else '不是 → 无效')),
        27: '`hyphen_flag = True`：记下已经用过一个连字符',
        'elif sentence[p] == \'!\'': lambda S, B, ret: (f"`'{S.sentence[S.p]}'` 是标点：必须在 token 末尾" if S.sentence[S.p] in '!.,' else f"`'{S.sentence[S.p]}'` 是小写字母，没有问题"),
        'if p + 1 < n and sentence[p + 1] != ': lambda S, B, ret: ('标点后面还有字符（不是空格）→ ==标点不在末尾，无效==' if (S.p + 1 < S.n and S.sentence[S.p + 1] != ' ') else '标点后面是空格或句尾 → 位置合法'),
        'if flag:': lambda S, B, ret: ('token 结束时 `flag = True` → ==有效单词==，`res` 加一' if S.flag else 'token 结束时 `flag = False` → 无效，不计数'),
        'res += 1': '`res` → {res}',
        'return res': '一共 `{res}` 个有效单词',
    },
    cards=dict(
        one_liner='一趟遍历：找 token，用两个标记边走边判',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['句子里 token 之间有一个或多个空格；有效单词：不含数字、至多一个连字符（两侧是小写字母）、至多一个标点（只能在末尾）',
                 '返回有效单词的数目',
                 '本视频：`"cat  b8 a-b!"` → `2`（`b8` 含数字）'],
        quote='空格的数量不定，因此如果想用split就必须靠正则来匹配，否则就需要一趟遍历来做。我在这里采取的遍历的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先跳过空格，找到 token 开头；再扫到下一个空格或句尾',
              '`flag`：这个 token 还可能有效；`hyphen_flag`：已经出现过合法连字符',
              '数字 → 无效；连字符要是第一个且两侧是小写字母；标点后面必须是空格或句尾'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：连字符要检查 `p > 0` 和 `p + 1 < n`，避免越界',
                 '易错：标点只能出现在末尾，所以看后一个字符是不是空格或句尾',
                 '易错：空格数量不定，不能直接 `split(\' \')`',
                 '本题代码无需 Python 3 改动；视频里用了较短的句子'],
    ),
)
