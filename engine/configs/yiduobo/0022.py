def _chip(cv, x, y, s, T, fill=None, outline=None, fg=None):
    txt = s if s != '' else '""'
    w = cv.tlen(txt, 24, mono=True) + 24
    cv.rect((x, y, x + w, y + 40), fill=fill or T['panel2'], outline=outline or T['border'], width=3 if outline else 1, r=9)
    cv.text((x + w / 2, y + 20), txt, 24, fg or T['text'], anchor='mm', mono=True, bold=True)
    return w


def _draw_f(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        cv.text((x0 + 18, y0 + 10), 'f[i] = 用 i 组括号能形成的所有答案（尚未创建）', 24, T['dim'])
        return
    cv.text((x0 + 18, y0 + 4), 'f[i] = 用 i 组括号能形成的所有答案（蓝 = f[j] 里的 left，粉 = f[i-j-1] 里的 right）', 22, T['muted'], bold=True)
    i, j = S.get('i'), S.get('j')
    rows = list(enumerate(f))
    building = 'now' in S and i is not None and len(f) == i
    y = y0 + 44
    for k, lst in rows:
        jrow = j is not None and i is not None and building and k == j
        rrow = j is not None and i is not None and building and k == i - j - 1
        lab_c = T['blue'] if jrow else (T['pink'] if rrow else T['muted'])
        cv.text((x0 + 24, y + 20), f'f[{k}]', 24, lab_c, anchor='lm', mono=True, bold=True)
        x = x0 + 110
        for s in lst:
            fill = fg = None
            if jrow and s == S.get('left'):
                fill, fg = T['blue'], T['bg']
            if rrow and s == S.get('right') and not (jrow and fill):
                fill, fg = T['pink'], T['bg']
            elif rrow and s == S.get('right') and jrow and fill:
                fill, fg = T['purple'], T['bg']
            new = B.get('f') is not None and len(B['f']) <= k
            w = _chip(cv, x, y, s, T, fill=fill, outline=T['yellow'] if new else None, fg=fg)
            x += w + 10
        y += 54
    if building:
        cv.text((x0 + 24, y + 20), 'now', 24, T['green'], anchor='lm', mono=True, bold=True)
        x = x0 + 110
        bnow = B.get('now') or []
        for k, s in enumerate(S['now']):
            new = k >= len(bnow)
            w = _chip(cv, x, y, s, T, fill=T['green'] if new else None, fg=T['bg'] if new else None)
            x += w + 10
        if not S['now']:
            cv.text((x, y + 20), f'（正在生成 f[{i}]，还是空的）', 22, T['dim'], anchor='lm')


def _formula(S):
    if 'left' in S and 'right' in S and 'j' in S and 'i' in S:
        L, R = S['left'], S['right']
        return (f"`i = {S['i']}`，第一个 `(` 里面 `j = {S['j']}` 对，右边 `i-j-1 = {S['i'] - S['j'] - 1}` 对："
                f"`'(' + '{L}' + ')' + '{R}'` = =={'(' + L + ')' + R}==")
    if 'i' in S and 'j' in S:
        return f"`i = {S['i']}`：枚举第一个左括号对里面有 `j = {S['j']}` 对括号"
    return ''


_st = {'fresh': False}  # 内层 for 是否刚开始（上一步是外层 for 取到了新 left）


def _for_left(S, B, ret):
    if 'left' in S and (S.left != B.get('left') or S.j != B.get('j')):
        _st['fresh'] = True
        return f"从 `f[{S.j}]` 取括号里面的 `left = '{S.left}'`"
    return f'`f[{S.j}]` 取完了'


def _for_right(S, B, ret):
    fresh, _st['fresh'] = _st['fresh'], False
    if 'right' in S and (fresh or S.right != B.get('right')):
        return f"从 `f[{S.i - S.j - 1}]` 取括号右边的 `right = '{S.right}'`"
    return f'`f[{S.i - S.j - 1}]` 取完了'


CONFIG = dict(
    num=22, title='括号生成', difficulty='Medium', category='回溯',
    author='yiduobo', technique='动态规划：(left)right 分解',
    code='''
class Solution(object):
    def generateParenthesis(self, n):
        f = []
        f.append([''])
        f.append(['()'])

        for i in range(2, n + 1):
            now = []
            for j in range(i):
                for left in f[j]:
                    for right in f[i - j - 1]:
                        now.append('(' + left + ')' + right)
            f.append(now)

        return f[n]
''',
    call='Solution().generateParenthesis(3)',
    expect=['()()()', '()(())', '(())()', '(()())', '((()))'],
    views=[
        dict(type='text', fn=_formula, h=96, size=26, lines=2),
        dict(type='custom', draw=_draw_f, h=330),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), ('i-j-1', 'i - j - 1', 'pink'),
           ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'f = []': '`f[i]` 表示使用 `i` 组括号能形成的所有答案',
        "f.append([''])": "边界：`f[0] = ['']`，0 组括号只有空串",
        "f.append(['()'])": "边界：`f[1] = ['()']`，一对括号",
        'for i in range(2, n + 1)': lambda S, B, ret: (
            f'开始求 `f[{S.i}]`：用 `{S.i}` 组括号' if S.i != B.get('i') else '`f[n]` 求完了，循环结束'),
        'now = []': '`now` 收集 `f[{i}]` 的所有答案',
        'for j in range(i)': lambda S, B, ret: (
            f'枚举 `j = {S.j}`：第一个 `(` 和它配对的 `)` 之间放 `{S.j}` 对，右边放 `{S.i - S.j - 1}` 对'
            if S.j != B.get('j') or S.i != B.get('i') else f'`j` 枚举完了，`f[{S.i}]` 收集齐了'),
        'for left in f[j]': _for_left,
        'for right in f[i - j - 1]': _for_right,
        "now.append('(' + left + ')' + right)": "拼成 `(left)right` = `'{now[-1]}'`，加入 now",
        'f.append(now)': '`f[{i}]` 求好了：`{len(now)}` 个答案',
        'return f[n]': '返回 `f[{n}]`，共 `{len(ret)}` 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='第一个左括号把答案切成 (left)right 两部分',
        complexity='时间与答案个数挂钩（Catalan 数），空间同答案规模',
        problem=['给定括号对数 `n`，生成所有==有效的==括号组合',
                 '示例：`n = 3` → `["((()))","(()())","(())()","()(())","()()()"]`'],
        quote='所有的答案都是左括号起头，可以写成 ==(xxx...xx)yyy...yy== 的形式，且括号内的 x 和括号外的 y 都必须是合法的。……f[i] 就可以写成 ==(left)right== 的形式。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]`：用 `i` 组括号能形成的所有答案',
              '第一个 `(` 配对的括号里有 `j` 对，右边有 `i-j-1` 对，`j` 取 `0 … i-1`',
              '枚举 `left ∈ f[j]`、`right ∈ f[i-j-1]`，拼出 `(left)right`'],
        summary=['复杂度：枚举 `i`、`j` 是 `O(n²)`，内部还要枚举 left/right，总量和解的个数挂钩',
                 '边界：`f[0] = [\'\']`，`f[1] = [\'()\']`',
                 '每个答案只按「第一个 ( 的配对位置」被拆一次 → 不重复也不遗漏',
                 'yiduobo 这题用 DP 而非回溯；回溯写法见灵神：`right < left` 才能填 `)`',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
