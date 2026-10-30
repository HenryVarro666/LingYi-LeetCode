EXPR = '2*3-4'


def _fmap(S):
    f = S.get('f')
    if f is None:
        return None
    n = len(f)
    return {(i, j): f[i][j] for i in range(n) for j in range(i, n) if f[i][j]}


def _seg(S):
    nums, ops = S['nums'], S['operators']
    return lambda a, b: ''.join(str(nums[k]) + (ops[k] if k < b else '') for k in range(a, b + 1))


def _text(S):
    line = S.get('_line')
    if 'length' not in S or line not in range(23, 39):
        return '`f[i][j]`：第 i 个到第 j 个数这一段表达式==所有可能的结果=='
    first, length = S['first'], S['length']
    last = first + length - 1
    seg = _seg(S)
    if 'operator_pos' in S and line in range(26, 39):
        p = S['operator_pos']
        if first <= p < last:
            return f"算 `{seg(first, last)}`：从第 {p} 个运算符 `{S['operators'][p]}` 切开 → `({seg(first, p)})` 与 `({seg(p + 1, last)})`"
    return f"长度 `{length}`，起点 `{first}`：求 `f[{first}][{last}]` = `{seg(first, last)}` 的所有结果"


def _op(S, B, ret):
    o = S.operators[S.operator_pos]
    return f'运算符是 `{o}`'


CONFIG = dict(
    num=241, title='为运算表达式设计优先级', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP · 枚举分割点',
    tags=['labuladong'],
    code='''
class Solution(object):
    def diffWaysToCompute(self, input):

        nums = []
        operators = []

        now = 0
        for char in input:
            if char not in ['+', '-', '*']:
                now = now * 10 + ord(char) - 48
            else:
                nums.append(now)
                operators.append(char)
                now = 0

        nums.append(now)

        f = [[[] for _ in range(len(nums))] for _ in range(len(nums))]

        for i in range(len(nums)):
            f[i][i].append(nums[i])

        for length in range(2, len(nums) + 1):
            for first in range(len(nums) - length + 1):
                for cut_pos in range(length - 1):
                    operator_pos = first + cut_pos
                    second = operator_pos + 1

                    for num1 in f[first][second - 1]:
                        for num2 in f[second][first + length - 1]:
                            if operators[operator_pos] == '+':
                                res = num1 + num2
                            elif operators[operator_pos] == '-':
                                res = num1 - num2
                            else:
                                res = num1 * num2

                            f[first][first + length - 1].append(res)

        return f[0][len(nums) - 1]
''',
    call=f'Solution().diffWaysToCompute({EXPR!r})',
    expect=[-2, 2],
    views=[
        dict(type='string', var='input', label='input', h=130, cell=70, index=False),
        dict(type='array', var='nums', label='nums', h=130, cell=70, min_slots=4),
        dict(type='array', var='operators', label='operators', h=130, cell=70, min_slots=3,
             color=lambda S, k, v: 'yellow' if S.get('_line') in range(26, 39) and k == S.get('operator_pos') else None),
        dict(type='text', fn=_text, size=24, h=56),
        dict(type='map', var=_fmap, label='f[i][j]（只列出已算出的区间）', h=230, font=24,
             fmt=lambda k, v: f'f[{k[0]}][{k[1]}]: {v}'),
    ],
    watch=['now', 'length', 'first', ('cut_pos', 'cut_pos'), ('num1', 'num1', 'blue'), ('num2', 'num2', 'pink'), ('res', 'res', 'green')],
    skip=['for num1 in', 'for first in', 'for cut_pos in', 'nums = []', 'operators = []', 14, 'for num2 in', 'second = operator_pos', 'if char not in', 'elif operators', "if operators[operator_pos] == '+'"],
    max_steps=75,
    captions={
        7: '`now` 累积当前数字',
        'for char in input': lambda S, B, r: ('扫描结束，最后一个数字还在 `now` 里' if B.get('char') == S.get('char')
                                              else (f"`'{S.char}'` 是==运算符==" if S.char in '+-*' else f"`'{S.char}'` 是数字")),
        'now = now * 10': "数字字符 → `now = {now}`（支持多位数）",
        'nums.append(now)': '数字 `{nums[-1]}` 读完，收进 `nums`',
        'operators.append(char)': "运算符 `{char}` 收进 `operators`",
        'f = [[[]': '`f[i][j]` 是一个==列表==：第 i 到第 j 个数的所有可能结果',
        'f[i][i].append': '只有一个数：`f[{i}][{i}] = [{nums[i]}]`',
        'for length in range': lambda S, B, r: (f'==从短到长==枚举长度 `length = {S.length}`：长的要用到短的结果'
                                                if B.get('length') != S.get('length') else '所有长度都算完'),
        'for first in range': '起点 `first = {first}`，终点 `{first + length - 1}`',
        'for cut_pos in range': '枚举分割点 `cut_pos = {cut_pos}`',
        'operator_pos = first': lambda S, B, r: (f'从运算符 `operators[{S.operator_pos}] = {S.operators[S.operator_pos]}` 切开：'
                                                 f'左边 `f[{S.first}][{S.operator_pos}]`，右边 `f[{S.operator_pos + 1}][{S.first + S.length - 1}]`'),
        'for num1 in': '左边取 `num1 = {num1}`，和右边的每个结果组合',
        'res = num1 + num2': '左段结果 `{num1}` + 右段结果 `{num2}` = `{res}`',
        'res = num1 - num2': '左段结果 `{num1}` − 右段结果 `{num2}` = `{res}`',
        'res = num1 * num2': '左段结果 `{num1}` × 右段结果 `{num2}` = `{res}`',
        'f[first][first + length - 1].append(res)': '`f[{first}][{first + length - 1}]` 加入 =={res}==（不需要去重）',
        'return f[0]': '`f[0][{len(nums) - 1}]` 就是整个表达式的所有结果：=={ret}==',
    },
    cards=dict(
        one_liner='在哪个运算符最后算，就从哪里把表达式切成两半',
        complexity='时间约 `O(n × 卡特兰数)`，结果个数是卡特兰数级别',
        problem=['给一个由数字和 `+ - *` 组成的表达式字符串',
                 '按不同的==加括号方式==计算，返回所有可能的结果（不去重，顺序任意）',
                 '示例：`"2-1-1"` → `[0, 2]`',
                 f'本视频：`"{EXPR}"` → `[-2, 2]`（`2*(3-4)`、`(2*3)-4`）'],
        quote='设f[i][j]表示第i个数到第j个数这一段表达式所有可能形成的答案……对于求解f[i][j]，需要==枚举分割点cut_pos==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 input 分成 n 个数字和 n − 1 个运算符',
              '`f[i][j]`：枚举最后算的运算符，左右两段的结果两两组合',
              '普通 DP 写法 → 要==从短到长==枚举长度 length，再枚举起点 first'],
        summary=['结果个数是卡特兰数级别，总复杂度由结果个数决定',
                 '易错：结果==不需要去重==，相同的值可能来自不同的括号方式',
                 '`ord(char) - 48` 就是把数字字符转成整数，支持多位数',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '也可以写成记忆化搜索，按运算符递归切分'],
    ),
)
