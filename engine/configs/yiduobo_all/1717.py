CONFIG = dict(
    num=1717, title='删除子字符串的最大得分', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='括号匹配式计数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maximumGain(self, s, x, y):

        if x > y:
            left = 'a'
            right = 'b'
        else:
            left = 'b'
            right = 'a'

        l_cnt = r_cnt = 0
        res = 0
        s += 'c'
        for index, char in enumerate(s):
            if char == left:
                l_cnt += 1
            elif char == right:
                if l_cnt > 0:
                    res += max(x, y)
                    l_cnt -= 1
                else:
                    r_cnt += 1
            else:
                res += min(x, y) * min(l_cnt, r_cnt)
                l_cnt = r_cnt = 0

        return res
''',
    call="Solution().maximumGain('cdbcbbaaabab', 4, 5)",
    expect=19,
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, h=230,
             color=lambda S, i, v: ('yellow' if v == S.get('left') and S.get('left') else 'cyan' if v == S.get('right') and S.get('right') else None) if 'left' in S else None),
        dict(type='text', fn=lambda S: (f"左括号 `{S['left']}`，右括号 `{S['right']}`：可用左括号 `l_cnt = {S['l_cnt']}`，落单右括号 `r_cnt = {S['r_cnt']}`" if 'l_cnt' in S else '先决定谁当左括号、谁当右括号'), size=28),
    ],
    watch=[('char', 'char', 'cyan'), ('left', 'left', 'yellow'), ('right', 'right', 'cyan'), ('l_cnt', 'l_cnt', 'blue'), ('r_cnt', 'r_cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'if x > y': lambda S, B, r: (f'`x = {S.x}` > `y = {S.y}`：`ab` 得分更高，优先消 `ab`' if S.x > S.y
                                     else f'`x = {S.x}` ≤ `y = {S.y}`：`ba` 得分更高（或相等），优先消 `ba`'),
        "left = 'a'": '`a` 当左括号，`b` 当右括号：`a` 在前 `b` 在后配成 `ab`',
        "right = 'b'": '`b` 当右括号',
        "left = 'b'": '`b` 当左括号，`a` 当右括号：`b` 在前 `a` 在后配成 `ba`',
        "right = 'a'": '`a` 当右括号',
        11: '`l_cnt` 记可用的左括号数，`r_cnt` 记落单的右括号数',
        "s += 'c'": '末尾补一个 `c`：让以 a/b 结尾的那一段也触发「收尾结算」',
        'for index, char': lambda S, B, r: ('字符都扫完了' if B.get('index') == S.index and B.get('char') == S.char else f'扫描第 `{S.index}` 个字符：`{S.char}`'),
        'if char == left': lambda S, B, r: (f'`{S.char}` 是左括号 `{S.left}` → 成立' if S.char == S.left else f'`{S.char}` 不是左括号 `{S.left}` → 看是不是右括号'),
        'elif char == right': lambda S, B, r: (f'`{S.char}` 是右括号 `{S.right}` → 成立' if S.char == S.right else f'`{S.char}` 既不是 a 也不是 b：这一段结束了'),
        'l_cnt += 1': '左括号入账：`l_cnt` → {l_cnt}',
        'if l_cnt > 0': lambda S, B, r: (f'`l_cnt = {S.l_cnt}` > 0：有左括号可配对 → 成立' if S.l_cnt > 0 else '`l_cnt = 0`：没有左括号，这个右括号落单'),
        'res += max(x, y)': '配成高分的一对：`res` += `max({x}, {y})` → =={res}==，`l_cnt` 还剩 {l_cnt - 1}',
        'l_cnt -= 1': '用掉一个左括号：`l_cnt` → {l_cnt}',
        'r_cnt += 1': '落单右括号 +1：`r_cnt` → {r_cnt}（之后只能和多余左括号按另一种方式配）',
        'res += min(x, y) * min': '这一段剩下 `))..((` 形式：还能按低分消 `min({l_cnt}, {r_cnt})` 对，`res` += `{min(x, y)} × {min(l_cnt, r_cnt)}` → =={res}==',
        25: '这一段算完，计数清零，开始下一段',
        'return res': '最大得分 `{res}`',
    },
    cards=dict(
        one_liner='高分的当括号匹配，剩下的再按低分配',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除子串 `ab` 得 `x` 分，删除 `ba` 得 `y` 分，可任意次',
                 '求能得到的最大总分',
                 '示例：`s="cdbcbbaaabab"`，`x=4`，`y=5` → `19`'],
        quote='若x大于y，那么记\'a\'为左括号，\'b\'为右括号，反过来若x小于等于y，则记\'a\'为右括号，\'b\'为左括号。然后一趟扫描，记录当前可用左括号的数目l_cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到 a、b 以外的字符就把串切成独立的段，每段分别算',
              '高分的那种子串优先：当括号匹配，每配一对加 `max(x, y)`',
              '段尾剩下 `))..((`，还能再配 `min(l_cnt, r_cnt)` 对，每对 `min(x, y)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：末尾要补 `c`，否则最后一段的 `))..((` 会漏算',
                 '易错：`x == y` 时哪种当左括号都行',
                 '原文为 Python 2 风格的类写法，代码未做改动'],
    ),
)
