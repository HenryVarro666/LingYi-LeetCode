CONFIG = dict(
    num=816, title='模糊坐标', difficulty='Medium', category='字符串',
    author='yiduobo', technique='拆成两段 · 各自枚举小数点',
    code='''
class Solution(object):
    def ambiguousCoordinates(self, S):

        S = S[1:-1]
        n = len(S)
        res = []
        for index in range(1, n):
            part_one = self.check(S[:index])
            part_two = self.check(S[index:])
            res.extend(["(%s, %s)" % (x, y) for x in part_one for y in part_two])
        
        return res
    
    def check(self, s):
        if len(s) == 1:
            return [s]

        res = []
        if s[0] != '0':
            res.append(s)
        
        if s[-1] != '0':
            if s[0] == '0':
                res.append(s[0] + '.' + s[1:])
            else:
                for index in range(1, len(s)):
                    res.append(s[:index] + '.' + s[index:])
        
        return res
''',
    call='Solution().ambiguousCoordinates("(123)")',
    expect=['(1, 23)', '(1, 2.3)', '(12, 3)', '(1.2, 3)'],
    views=[
        dict(type='string', var='S', h=150, label='S（去掉括号后）'),
        dict(type='string', var='s', h=170, label='s（正在判断的一段）'),
        dict(type='array', var='part_one', h=170, label='part_one（左段的合法写法）'),
        dict(type='array', var='part_two', h=170, label='part_two（右段的合法写法）'),
        dict(type='array', var='res', h=200, label='res（答案）', cell=170),
    ],
    watch=[('index', 'index', 'blue'), 's', ('part_one', 'part_one', 'cyan'), ('part_two', 'part_two', 'orange'), ('res', 'len(res)', 'green')],
    captions={
        'S = S[1:-1]': '先去掉两侧括号：`S = {S}`',
        'for index in range(1, n)': '枚举逗号的位置：`S` 切成 `S[:{index}]` 和 `S[{index}:]` 两段',
        'part_one = ': '左段 `{S[:index]}`：交给 `check` 求它所有合法写法',
        'part_two = ': '右段 `{S[index:]}`：同样交给 `check`',
        'res.extend': '两段合法数两两组合，加入答案：现在共 `{len(res)}` 个',
        'if len(s) == 1': lambda S, B, r: f'长度 `{len(S.s)}`' + ('：只有一位，合法坐标就是它自己' if len(S.s) == 1 else ' > 1：继续看首位和末位'),
        'return [s]': '一位数直接返回 `{s}`',
        "if s[0] != '0'": lambda S, B, r: (f'首位 `{S.s[0]}` 不是 0 → 整数 `{S.s}` 本身合法' if S.s[0] != '0' else f'首位是 0 → `{S.s}` 不能当整数（有前导零）'),
        "if s[-1] != '0'": lambda S, B, r: (f'末位 `{S.s[-1]}` 不是 0 → 可以尝试加小数点' if S.s[-1] != '0' else f'末位是 0 → 加小数点会以 0 结尾，不合法'),
        "if s[0] == '0'": lambda S, B, r: ('首位是 0：小数点只能放在 0 后面' if S.s[0] == '0' else '首位不是 0：小数点可以放在任意两位之间'),
        "res.append(s[0] + '.' + s[1:])": '加入 `{res[-1]}`',
        'res.append(s[:index] + \'.\' + s[index:])': '小数点放在第 `{index}` 位后：加入 `{res[-1]}`',
        'res.append(s)': '加入整数 `{s}`',
        'return res': lambda S, B, r: f'`{S.s if "s" in S else ""}` 的合法写法：`{r}`' if 's' in S and isinstance(r, list) and r and '(' not in r[0] else f'全部答案：`{len(r)}` 个',
    },
    cards=dict(
        one_liner='去括号，切两段，每段单独数合法写法再两两组合',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`（n 为数字位数）',
        problem=['原本有坐标 `(1, 3)`，去掉逗号、小数点和空格后得到字符串 `S`',
                 '给定 `S`，返回所有可能的原坐标；数字不能有多余的前导 0 或末尾 0',
                 '示例：`"(123)"` → `["(1, 23)","(12, 3)","(1.2, 3)","(1, 2.3)"]`（顺序不限）'],
        quote='首先去掉S两侧的括号，然后将S分为两个部分，分别判断这两个部分可以形成的合法坐标，然后再两两组合起来加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度为 1：合法坐标就是它自己',
              '首位不是 0：整数本身合法；末位不是 0：可以加小数点',
              '首位是 0 时小数点只能放在 0 后面，否则可放在任意两位之间'],
        summary=['枚举逗号位置，左右两段互不影响，用 `check` 各算一遍再两两组合',
                 '易错点：`0` 开头不能当整数，`0` 结尾不能带小数点；单个 `0` 要单独放行',
                 '`"00"` 这类两段都无解的切法，组合后自然为空'],
    ),
)
