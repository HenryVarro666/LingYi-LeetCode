def _sub(S, a, b):
    nl, ol = S.get('num_list', []), S.get('op_list', [])
    t = str(nl[a])
    for k in range(a, b):
        t += ol[k] + str(nl[k + 1])
    return t


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    nl, ol = S.get('num_list', []), S.get('op_list', [])
    line = S.get('_line', 0)
    W = x1 - x0
    # ---- 行 A：表达式 s
    cv.text((x0 + 18, y0 + 4), f's = "{s}"', 24, T['muted'], bold=True, mono=True)
    cw = min(60, (W - 40) / max(len(s), 1))
    for i, ch in enumerate(s):
        X = x0 + 24 + i * cw
        op = ch in '+*'
        cv.rect((X, y0 + 40, X + cw - 6, y0 + 40 + 52), fill=T['panel2'], outline=T['border'], r=8)
        cv.text((X + (cw - 6) / 2, y0 + 66), ch, 30, T['orange'] if op else T['text'], anchor='mm', bold=True, mono=True)
    # ---- 行 B：num_list / op_list / 栈
    yb = y0 + 112
    cv.text((x0 + 18, yb), 'num_list', 20, T['cyan'], bold=True)
    for i, v in enumerate(nl):
        X = x0 + 150 + i * 60
        cv.rect((X, yb - 6, X + 52, yb + 36), fill=T['panel2'], outline=T['cyan'], r=8)
        cv.text((X + 26, yb + 15), v, 26, T['text'], anchor='mm', bold=True)
    cv.text((x0 + 18, yb + 50), 'op_list', 20, T['orange'], bold=True)
    for i, v in enumerate(ol):
        X = x0 + 150 + i * 60
        cv.rect((X, yb + 44, X + 52, yb + 86), fill=T['panel2'], outline=T['orange'], r=8)
        cv.text((X + 26, yb + 65), v, 26, T['text'], anchor='mm', bold=True)
    xs = x0 + W * 0.52
    if 'stack' in S and line >= 17:
        cv.text((xs, yb - 6), f"now = {S.get('now')}", 24, T['yellow'], bold=True, mono=True)
        cv.text((xs, yb + 30), f"stack = {S['stack']}", 24, T['purple'], bold=True, mono=True)
    if 'correct_ans' in S:
        cv.text((xs, yb + 66), f"正确结果 = {S['correct_ans']}", 24, T['green'], bold=True)
    # ---- 行 C：区间 DP 三角表
    yc = yb + 170
    if 'f' in S and nl and 'n' in S:
        n = S['n']
        cv.text((x0 + 18, yc - 30), 'f[left][right] = 数字 left~right 的所有可能结果（黄 = 正在算，蓝 = 当前用到的两段）', 20, T['muted'], bold=True)
        cell_w = min(220, (W - 60) / n)
        cell_h = 66
        lft, rgt = S.get('left'), S.get('right')
        in_dp = 'left' in S and 'right' in S and 28 <= line <= 44
        cutp = S.get('cut_pos') if in_dp and 'cut_pos' in S and line >= 35 else None
        for a in range(n):
            for b in range(a, n):
                X = x0 + 30 + b * cell_w
                Y = yc + a * (cell_h + 6)
                fill = T['panel2']
                outline = T['border']
                if in_dp and (a, b) == (lft, rgt):
                    outline = T['yellow']
                elif cutp is not None and (a, b) in ((lft, cutp), (cutp + 1, rgt)):
                    outline = T['blue']
                vals = sorted(S['f'][a][b])
                cv.rect((X, Y, X + cell_w - 8, Y + cell_h), fill=fill, outline=outline, width=4 if outline != T['border'] else 1, r=8)
                cv.text((X + 8, Y + 4), _sub(S, a, b), 16, T['dim'], mono=True)
                txt = '{' + ', '.join(map(str, vals)) + '}' if vals else '{ }'
                cv.text((X + (cell_w - 8) / 2, Y + cell_h * 0.62), txt, 24 if len(txt) < 14 else 18, T['text'] if vals else T['dim'], anchor='mm', bold=True, mono=True)
    # ---- 行 D：学生答案
    if 'answers' in S and 'correct_ans' in S and line >= 46:
        ya = y1 - 70
        cv.text((x0 + 18, ya - 34), 'answers（绿 = 正确 5 分，蓝 = 运算顺序错 2 分，灰 = 0 分）', 20, T['muted'], bold=True)
        f0 = S['f'][0][S['n'] - 1]
        cur = S.get('ans')
        for i, a in enumerate(S['answers']):
            X = x0 + 24 + i * 100
            c = T['green'] if a == S['correct_ans'] else T['blue'] if a in f0 else None
            hot = ('ans' in S and line >= 47 and ((i < S['answers'].index(cur)) or (a == cur and i == S['answers'].index(cur) and line >= 48))) if cur is not None else False
            cv.rect((X, ya, X + 90, ya + 52), fill=c if (c and hot) else T['panel2'], outline=T['yellow'] if a == cur else T['border'],
                    width=4 if a == cur else 1, r=8)
            cv.text((X + 45, ya + 26), a, 28, T['bg'] if (c and hot) else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=2019, title='解出数学表达式的学生分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='栈求正确值 + 区间 DP 求所有可能值',
    tags=['灵神题单', '动态规划', '难度分 2584'],
    code='''
class Solution(object):
    def scoreOfStudents(self, s, answers):

        num_list = []
        op_list = []
        now = 0
        for char in s:
            if char == '+' or char == '*':
                num_list.append(now)
                op_list.append(char)
                now = 0
            else:
                now = now * 10 + int(char)
            
        num_list.append(now)
        now = num_list[0]
        stack = []
        n = len(num_list)
        for index in range(1, n):
            if op_list[index - 1] == '+':
                stack.append(now)
                now = num_list[index]
            else:
                now *= num_list[index]
        
        correct_ans = now + sum(stack)
        
        f = [[set() for _ in range(n)] for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n - l + 1):
                right = left + l - 1
                if left == right:
                    f[left][right].add(num_list[left])
                else:
                    for cut_pos in range(left, right):
                        for x in f[left][cut_pos]:
                            for y in f[cut_pos + 1][right]:
                                if op_list[cut_pos] == '+':
                                    if x + y <= 1000:
                                        f[left][right].add(x + y)
                                else:
                                    if x * y <= 1000:
                                        f[left][right].add(x * y)

        res = 0
        for ans in answers:
            if ans == correct_ans:
                res += 5
            elif ans in f[0][n - 1]:
                res += 2
        
        return res
''',
    call='Solution().scoreOfStudents("3+5*2", [13, 16, 10])',
    expect=7,
    skip=['for char in s', "if char == '+'", 'now = 0', 'for index in range', 'right = left + l - 1', 'if left == right',
          'for x in f[', 'for y in f[', 'if op_list[cut_pos]', 'for ans in answers', 'res = 0'],
    max_steps=80,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('l', 'l', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cut_pos', 'cut_pos', 'green'), ('res', 'res', 'green')],
    captions={
        'num_list = []': '`num_list` 存表达式里的数字，`op_list` 存运算符',
        'op_list = []': '`op_list` 存运算符，顺序和数字交替',
        'num_list.append(now)': lambda S, B, r: (f'遇到运算符：把攒好的数 `{S.num_list[-1]}` 存进 `num_list`' if S.get('_line') == 9
                                                 else f'末尾没有运算符，把最后一个数 `{S.num_list[-1]}` 也存进去：`{S.num_list}`'),
        'op_list.append(char)': '运算符 `{char}` 存进 `op_list` → `{op_list}`',
        'now = now * 10': '数字字符 `{char}`：`now = {now}`（题目保证个位数，所以 now 就是这个数）',
        'now = num_list[0]': '开始算正确结果：`now` 是当前乘积项，先取第一个数 `{now}`',
        'stack = []': '`stack` 存已经确定的加法项',
        'n = len': '`n = {n}` 个数字，`op_list` 有 `{n-1}` 个运算符',
        'stack.append(now)': '遇到 `+`：左边这一项 `{now}` 已经确定，压入栈 → `stack = {stack}`',
        'now = num_list[index]': '`now` 换成下一个数 `{now}`，开始新的一项',
        'now *= num_list': '遇到 `*`：乘号优先，另一个值必然是下一个数，直接乘：`now` = {B.now} × {num_list[index]} = =={now}=='
                           .replace('{num_list[index]}', '{num_list[index]}'),
        'correct_ans =': '正确结果 = 当前项 `{now}` + 栈里所有加法项 `{stack}` = =={correct_ans}=='.replace('`{stack}`', '`{sum(stack)}`'),
        'f = [[set()': '`f[i][j]`：数字 `i`~`j` 所有运算顺序能得到的结果集合，初始都是空集',
        'for l in range': lambda S, B, r: (f'区间包含 `l = {S.l}` 个数字：==先算短区间，再算长区间==' if S.get('l') != B.get('l') else '所有区间都算完了'),
        'for left in range': lambda S, B, r: ('这个长度的区间都算完了' if S.get('left') == B.get('left') and S.get('l') == B.get('l') else f'左端 `left = {S.left}`'),
        'f[left][right].add(num_list[left])': '只有一个数，结果集合就是它自己：`f[{left}][{right}]` = `{f[left][right]}`',
        'for cut_pos in range': lambda S, B, r: (
            f'分割点都试完了：`f[{S.left}][{S.right}]` = `{sorted(S.f[S.left][S.right])}`' if S.get('cut_pos') == B.get('cut_pos')
            else f'`left = {S.left}`，`right = {S.right}`：枚举分割点 `cut_pos`（最后一个算的运算符），先试 `cut_pos = {S.cut_pos}`，运算符 `{S.op_list[S.cut_pos]}`'
            if S.cut_pos == S.left else f'再试下一个分割点 `cut_pos = {S.cut_pos}`，运算符 `{S.op_list[S.cut_pos]}`：左 `f[{S.left}][{S.cut_pos}]`，右 `f[{S.cut_pos + 1}][{S.right}]`'),
        'if x + y <= 1000': lambda S, B, r: f'`{S.x} + {S.y} = {S.x + S.y}`：' + ('不超过 1000，保留' if S.x + S.y <= 1000 else '超过 1000，答案不会这么大，丢掉'),
        'f[left][right].add(x + y)': '加入 `{x + y}` → `f[{left}][{right}]` = `{sorted(f[left][right])}`',
        'if x * y <= 1000': lambda S, B, r: f'`{S.x} × {S.y} = {S.x * S.y}`：' + ('不超过 1000，保留' if S.x * S.y <= 1000 else '超过 1000，丢掉'),
        'f[left][right].add(x * y)': '加入 `{x * y}` → `f[{left}][{right}]` = `{sorted(f[left][right])}`',
        'if ans == correct_ans': lambda S, B, r: f'学生答案 `{S.ans}`：' + ('==等于正确结果== `{0}` → 5 分'.format(S.correct_ans) if S.ans == S.correct_ans else f'不等于正确结果 `{S.correct_ans}`'),
        'res += 5': '得 5 分：`res` = =={res}==',
        'elif ans in f': lambda S, B, r: f'`{S.ans}` ' + ('在 `f[0][n-1]` 里：==某种错误运算顺序能算出来== → 2 分' if S.ans in S.f[0][S.n - 1] else '不在可能结果集合里 → 0 分'),
        'res += 2': '得 2 分：`res` = =={res}==',
        'return res': '所有学生得分之和 = =={ret}==',
    },
    cards=dict(
        one_liner='栈算出正确结果，区间 DP 算出所有可能的运算顺序结果',
        complexity='时间 `O(n^3 · V^2)`（`V` ≤ 1000），空间 `O(n^2 · V)`',
        problem=['表达式 `s` 只含个位数、`+`、`*`，正确运算：先乘后加',
                 '学生答案 = 正确结果得 ==5 分==；否则能由「某种错误运算顺序」算出得 ==2 分==；否则 0 分',
                 '本视频：`s = "3+5*2"`, `answers = [13,16,10]` → `7`'],
        quote='这是一个经典的区间动态规划问题，令f[i][j]表示第i到第j个数可能得到的所有可能运算结果。……由于题目保证了答案小于等于1000，那么f[i][j]中也只需要保留小于等于1000的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['正确结果：用栈。遇 `+` 把当前项压栈，遇 `*` 直接乘，最后 `now + sum(stack)`',
              '所有可能结果：`f[i][j]` 是集合，枚举最后算的运算符 `cut_pos`，左右集合里的数两两组合',
              '结果超过 1000 的直接丢掉，防止集合爆炸；最后按规则给每个答案打分'],
        summary=['先乘后加的正确值用栈，所有顺序的值用区间 DP，两件事分开做',
                 '`f[0][n-1]` 里包含正确结果，所以要==先判断等于 `correct_ans` 得 5 分==，再判断得 2 分',
                 '易错：`x * y` 可能很大，要 `<= 1000` 才保留；个位数所以 `now` 的多位累加其实用不到',
                 '对比：同一区间 DP 框架也用于 1547 / 1039 / 1000，但这里 `f[i][j]` 存的是结果集合'],
    ),
)
