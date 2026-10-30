def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'left' not in S:
        return
    cv.text((x0 + 18, y0 + 4), '计数器', 24, T['muted'], bold=True)
    l, r = S['left'], S['right']
    maxv = max(4, l, r)
    bx, bw = x0 + 210, x1 - x0 - 300
    for k, (name, v, c) in enumerate([('left  (', l, T['blue']), ('right )', r, T['pink'])]):
        y = y0 + 52 + k * 72
        cv.text((x0 + 40, y + 24), name, 28, c, anchor='lm', bold=True, mono=True)
        cv.rect((bx, y, bx + bw, y + 48), fill=T['panel2'], r=10)
        if v:
            cv.rect((bx, y, bx + bw * v / maxv, y + 48), fill=c, r=10)
        cv.text((bx + bw + 20, y + 24), str(v), 34, c, anchor='lm', bold=True)
    if l == r and l > 0:
        msg, c = f'left == right → 当前串匹配上了，长度 {l + r}', T['green']
    elif l == r == 0:
        msg, c = '两个计数器都是 0（刚开始 / 刚清零）', T['muted']
    else:
        msg, c = f'差 {abs(l - r)} 个，还不相等', T['muted']
    cv.text((x0 + 40, y0 + 210), msg, 26, c, anchor='lt', bold=True)


def _cap_eq(S, B, ret):
    if S.left == S.right:
        return f'`left == right == {S.left}` → ==当前串是匹配上的=='
    return f'`left = {S.left}`，`right = {S.right}`，不相等'


CONFIG = dict(
    num=32, title='最长有效括号', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='左右括号计数 + 正反两次扫描',
    code='''
class Solution(object):
    def longestValidParentheses(self, s):
        res = 0
        left = right = 0
        for index in range(len(s)):
            if s[index] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                res = max(res, left + right)
            elif left < right:
                left = right = 0

        left = right = 0
        for index in range(len(s) - 1, -1, -1):
            if s[index] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                res = max(res, left + right)
            elif left > right:
                left = right = 0

        return res
''',
    call='Solution().longestValidParentheses(")(()()")',
    expect=4,
    views=[
        dict(type='string', var='s', label='s', cell=110, h=220, pointers={'index': 'yellow'},
             color=lambda S, k, v: 'yellow' if k == S.get('index') else None),
        dict(type='custom', draw=_draw, h=270),
    ],
    watch=[('index', 'index', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    skip=['for index in range', "if s[index] == '('"],
    captions={
        3: '`res`：最长有效长度，先为 0',
        4: '==从头开始扫描==，逐个记录左括号数目 `left` 与右括号数目 `right`',
        7: '`s[{index}] = "("` → `left = {left}`',
        9: '`s[{index}] = ")"` → `right = {right}`',
        10: _cap_eq,
        11: '更新 `res = max({B.res}, {left + right})` = =={res}==',
        12: lambda S, B, ret: ('`right > left`：右括号多了，这个串==已经没有维护的价值了==' if S.left < S.right else
                               '`right < left`：有落单的左括号，可能与后续右括号匹配 → ==无事发生=='),
        13: '`left`、`right` 置 0，从下一个位置重新数',
        15: '正向扫完 `res = {res}`：开头的 `(` 让后面的匹配都无法更新 → ==从右往左再扫一遍==',
        18: '（反向）`s[{index}] = "("` → `left = {left}`',
        20: '（反向）`s[{index}] = ")"` → `right = {right}`',
        21: _cap_eq,
        22: '更新 `res = max({B.res}, {left + right})` = =={res}==',
        23: lambda S, B, ret: ('反向时 `left > right` 不合法（==与正向正好相反==）→ 清零' if S.left > S.right else
                               '反向时单个的 `right` 是合法的：它可能与更左边的 `(` 匹配 → 无事发生'),
        24: '`left`、`right` 置 0',
        26: '两趟扫描取最大：返回 =={ret}==',
    },
    cards=dict(
        one_liner='只数左右括号：正着扫一遍，再反着扫一遍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['只含 `(` 和 `)` 的字符串，求==最长有效（格式正确且连续）括号子串==的长度',
                 '示例：`")()())"` → `4`（`"()()"`）',
                 '演示：`")(()()"` → `4`（`"()()"`）'],
        quote='对于新加入一个括号：==right > left，说明这个串已经没有维护的价值了==，将left与right置0；right == left，说明当前串是匹配上的，更新res；right < left，无事发生。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用栈维护下标，换一种==简单的匹配思路==：只数 `left`、`right`',
              '`right < left`：落单的左括号可能与后续右括号匹配，所以先不动',
              '漏洞：`(()()()()` 开头多一个 `(`，正向扫永远等不到相等 → 反向再扫'],
        after=[dict(heading='为什么正反两遍就够？', lines=[
            '存在==左单括号==影响后续匹配 → 从后往前扫能找到答案',
            '存在==右单括号==影响后续匹配 → 从前往后扫能找到答案',
            '同时存在左、右单括号？不可能——「这两个单括号本身就能匹配」',
        ])],
        summary=['两趟扫描，时间 `O(n)`，空间 `O(1)`',
                 '易错：反向扫描时==判断条件反过来==，`left > right` 才清零',
                 '易错：第二趟开始前要把 `left`、`right` 重新置 0',
                 '原文为 Python 2 风格：只删掉了 docstring，其余未改'],
    ),
)
