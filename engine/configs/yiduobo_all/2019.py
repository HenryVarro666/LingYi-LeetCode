def _cnt(S):
    f = S.get('f')
    if not f:
        return [[0]]
    return [[len(c) for c in row] for row in f]


def _col(S, r, c, v):
    L, left, right = S.get('l'), S.get('left'), S.get('right')
    if left is None or right is None or S.get('_line', 0) < 32:
        return None
    if (r, c) == (left, right):
        return 'yellow'
    cp = S.get('cut_pos')
    if cp is not None and S.get('_line') in (38, 39, 40, 41, 42, 43) and (r, c) in ((left, cp), (cp + 1, right)):
        return 'blue'
    return None


def _txt(S):
    f, left, right = S.get('f'), S.get('left'), S.get('right')
    if f is None or left is None or right is None or S.get('_line', 0) < 32:
        return '`f[i][j]` = 第 i 到第 j 个数在所有运算顺序下的可能结果（右边表格显示个数）'
    nums = S['num_list']
    return f'`f[{left}][{right}]`（数 {nums[left:right+1]}）= =={sorted(f[left][right])}=='


CONFIG = dict(
    num=2019, title='解出数学表达式的学生分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='栈算正确值 + 区间 DP 集合',
    tags=['灵神题单·动态规划', '难度分 2584'],
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
    call='Solution().scoreOfStudents("3+5*2", [13, 0, 10, 13, 13, 16, 16])',
    expect=19,
    views=[
        dict(type='array', var='num_list', label='num_list（数字）', cell=80, h=200,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='table', var=_cnt, label='f[left][right] 的结果个数（黄 = 正在填，蓝 = 左右两段）', h=220, cell=64, color=_col),
        dict(type='stack', var='stack', label='stack（遇到 + 压入的前一段乘积）', h=100),
        dict(type='array', var='answers', label='answers', cell=64, h=130),
    ],
    watch=[('now', 'now', 'blue'), ('correct_ans', 'correct_ans', 'green'), ('l', 'l'), ('cut_pos', 'cut_pos', 'pink'), ('res', 'res', 'orange')],
    skip=['for left in range', 'for char in s', "if char ==", 'now = now * 10', 'op_list.append(char)', 'for x in f[', 'for y in f[', 'for cut_pos in range', 'right = left + l - 1', 'num_list = []', 'op_list = []', 'stack = []', 'now = 0', 'f[left][right].add(x + y)'],
    captions={
        'num_list.append(now)': '遇到运算符/到末尾：把读到的数存进 `num_list` → `{num_list}`',
        'now = num_list[0]': '`now` 记录当前这一段乘积，从第一个数开始 = {now}',
        'stack.append(now)': '遇到 `+`：前面的乘积已定，==压栈==，`stack = {stack}`',
        'now = num_list[index]': '`now` 从新的一段开始 = {now}',
        'now *= num_list[index]': '遇到 `*`：直接连乘 → `now = {now}`',
        'correct_ans =': '最后一段 `{now}` + 栈里各段 `{stack}` = =={correct_ans}==',
        'f = [[set()': '`f[i][j]` 存区间 `i..j` 个数的所有可能运算结果（集合）',
        'for l in range': '按区间长度 `l = {l}` 从小到大算（短区间先算好）',
        'if left == right': lambda S, B, r: (f'`left = right = {S.left}`：只有一个数' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 有多个数 → 枚举分割点'),
        'f[left][right].add(num_list[left])': '单个数的结果就是它自己：`f[{left}][{right}] = {{{num_list[left]}}}`',
        "if op_list[cut_pos] == '+'": '分割点 `{cut_pos}`（运算符 `{op_list[cut_pos]}`）：左段取 `{x}`，右段取 `{y}`，两两配对',
        'if x + y <= 1000': '`{x} + {y} = {x+y}`，不超过 1000 才保留',
        'f[left][right].add(x + y)': '加入 `{x+y}` → `f[{left}][{right}]` = {sorted(f[left][right])}',
        'if x * y <= 1000': '`{x} × {y} = {x*y}`，不超过 1000 才保留',
        'f[left][right].add(x * y)': '加入 `{x*y}` → `f[{left}][{right}]` = {sorted(f[left][right])}',
        'for ans in answers': '逐个看答案 `{ans}`',
        'if ans == correct_ans': lambda S, B, r: (f'`{S.ans} == {S.correct_ans}` → ==5 分==' if S.ans == S.correct_ans else f'`{S.ans} ≠ {S.correct_ans}`：不是正确答案'),
        'res += 5': '`res = {res}`',
        'elif ans in': lambda S, B, r: (f'`{S.ans}` 在 `f[0][{S.n-1}]` = {sorted(S.f[0][S.n-1])} 里 → 错顺序凑出来，==2 分==' if S.ans in S.f[0][S.n - 1] else f'`{S.ans}` 凑不出来 → 0 分'),
        'res += 2': '`res = {res}`',
        'return res': '总分 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='栈算出正确值，区间 DP 存下所有可能值的集合',
        complexity='时间约 `O(n^3·V^2)`，空间 `O(n^2·V)`',
        problem=['表达式只含个位数、`+`、`*`，正确顺序是先乘后加',
                 '答案正确得 `5` 分；能由某种错误运算顺序得到得 `2` 分；否则 `0` 分',
                 '示例：`s = "3+5*2"`，`answers = [13,0,10,13,13,16,16]` → `19`'],
        quote='这是一个经典的区间动态规划问题，令f[i][j]表示第i到第j个数可能得到的所有可能运算结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['正确值：遇到加号把当前值压栈，遇到乘号直接乘下一个数，最后把栈里的值加起来',
              '`f[i][j]`：枚举分割点，左右两段的结果两两做运算',
              '题目保证答案不超过 1000，所以大于 1000 的结果不用存'],
        summary=['时间约 `O(n^3·V^2)`，V 是集合大小（≤ 1001）',
                 '易错：错误顺序恰好算出正确值时仍得 5 分，先判断 `correct_ans`',
                 '区间按长度从小到大枚举，保证两段子区间已算好',
                 '原文为 Python 2 风格，本题代码无需改动（仅删去了类型说明文档字符串）',
                 '对比灵神：灵神用记忆化递归，这里是自底向上填表'],
    ),
)
