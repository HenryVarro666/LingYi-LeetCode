def _flags(S):
    if 'number_flag' not in S:
        return '用四个 flag 拼成一个低配自动机'
    f = lambda k: '==是==' if S.get(k) else '否'
    return (f"symbol_flag {f('symbol_flag')}　point_flag {f('point_flag')}　"
            f"e_flag {f('e_flag')}　number_flag {f('number_flag')}")


def _col(S, i, v):
    if 'index' not in S:
        return None
    k = S['index']
    if i == k:
        return 'blue'
    if S.get('left', 0) <= i < k:
        return 'green' if v.isdigit() else 'yellow'
    return None


def _dim(S, i, v):
    return 'right' in S and (i < S['left'] or i > S['right'])


def _char(S, B, r):
    return f"当前字符 `{S.char!r}`"


CONFIG = dict(
    num=65, title='有效数字', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='flag 拼成的低配自动机',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def isNumber(self, s):

        if not s:
            return False

        symbol_flag= False
        point_flag = False
        number_flag = False
        e_flag = False
        left = 0
        right = len(s) - 1
        
        while left < len(s) and s[left] == ' ':
            left += 1

        if left == len(s):
            return False

        while right > -1 and s[right] == ' ':
            right -= 1

        for index in range(left, right + 1):
            char = s[index]
            if char in ['+', '-']:
                if symbol_flag:
                    return False
                symbol_flag = True
            elif char == 'e':
                if e_flag:
                    return False
                if not number_flag:
                    return False
                e_flag = True
                number_flag = False
                point_flag = True
                symbol_flag = False
            elif char == '.':
                if point_flag:
                    return False
                point_flag = True
                symbol_flag = True
            elif ord(char) >= 48 and ord(char) <= 57:
                symbol_flag = True
                number_flag = True
            else:
                return False

        return number_flag
''',
    call='Solution().isNumber(" 1.e-5 ")',
    expect=True,
    views=[
        dict(type='text', fn=_flags, size=26, h=80),
        dict(type='string', var='s', label='s（灰 = 首尾空格，绿 = 数字，黄 = 符号/点/e，蓝 = 当前字符）', cell=100,
             pointers={'index': 'blue'}, color=_col, dim=_dim, h=300),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('symbol_flag', 'symbol_flag', 'yellow'),
           ('point_flag', 'point_flag', 'orange'), ('e_flag', 'e_flag', 'purple'), ('number_flag', 'number_flag', 'green')],
    captions={
        'if not s': '空串直接不是数字',
        7: '`symbol_flag`：这一段里正负号==不能再出现==了吗（也表示已冲突）',
        8: '`point_flag`：小数点出现过没有（进入指数后也置为 True，指数必须是整数）',
        9: '`number_flag`：当前这一段里有没有数字',
        10: '`e_flag`：字符 e 出现过没有，最多一次',
        'left = 0': '`left` 去掉头部空格，`right` 去掉尾部空格',
        'right = len': '`right = {right}`，先指向最后一个字符',
        'while left < len(s) and s[left]': lambda S, B, r: (f"`s[{S.left}]` 是空格 → 头部空格，`left` 右移" if S.left < len(S.s) and S.s[S.left] == ' ' else '头部没有空格了'),
        'left += 1': '`left` → {left}',
        'if left == len(s)': '`left = {left}`：全是空格才会等于 `len(s)`，这里不是',
        'while right > -1': lambda S, B, r: (f"`s[{S.right}]` 是空格 → 尾部空格，`right` 左移" if S.right > -1 and S.s[S.right] == ' ' else '尾部没有空格了'),
        'right -= 1': '`right` → {right}',
        'for index in range': lambda S, B, r: (f"检查第 `{S.index}` 个字符，只扫 `[{S.left}, {S.right}]`" if 'index' in B and B.index != S.index or 'index' not in B else '每个字符都检查完了'),
        'char = s[index]': '`char = {char!r}`',
        "if char in ['+', '-']": lambda S, B, r: (f"`{S.char!r}` 是正负号 → 看 `symbol_flag = {S.symbol_flag}`" if S.char in '+-' else f"`{S.char!r}` 不是正负号"),
        'if symbol_flag': '`symbol_flag = {symbol_flag}`：为 True 说明正负号不在这一段最前面 → ==False==',
        28: '记下：这一段的正负号==用掉了==，后面不能再出现',
        "elif char == 'e'": lambda S, B, r: (f"`{S.char!r}` 是 e → 要做三个检查" if S.char == 'e' else f"`{S.char!r}` 不是 e"),
        'if e_flag': '`e_flag = {e_flag}`：e 最多出现一次',
        'if not number_flag': '`number_flag = {number_flag}`：==e 前面必须已经有数字==（`1.e-5` 也合法）',
        34: '记下 e 已出现，后面不能再有 e',
        35: '进入指数部分：==指数里还得再出现数字==，所以 `number_flag` 清零',
        36: '指数必须是整数 → `point_flag` 置 True，禁止再出现小数点',
        37: '指数部分还可以有一次正负号 → `symbol_flag` 清零',
        "elif char == '.'": lambda S, B, r: (f"`{S.char!r}` 是小数点 → 看 `point_flag = {S.point_flag}`" if S.char == '.' else f"`{S.char!r}` 不是小数点"),
        'if point_flag': '`point_flag = {point_flag}`：已有小数点（或已在指数里）→ 冲突',
        41: '记下小数点已出现；小数点前要有符号只能在最前，所以 `symbol_flag` 也置 True',
        42: '`symbol_flag = True`：符号只能在这一段最前面，数字或点之后不再允许',
        44: '数字也让 `symbol_flag = True`：正负号不能出现在数字之后',
        45: '`number_flag = True`：这一段有数字了',
        'elif ord(char)': lambda S, B, r: (f"`{S.char!r}` 是数字" if S.char.isdigit() else f"`{S.char!r}` 是其他字符 → 非法"),
        'return number_flag': '全部检查完：`number_flag = {number_flag}`，最后一段里==至少有一个数字==才合法',
    },
    cards=dict(
        one_liner='用四个 flag 记录出现过什么，逐个字符判冲突',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['判断字符串 `s` 是否是有效数字：整数/小数，可带 `e` 指数；原文的题版允许首尾空格',
                 '合法：`"2"`、`"-.9"`、`"1.e-5"`；不合法：`"e"`、`"."`、`"99e2.5"`、`"--6"`',
                 '本视频：`" 1.e-5 "` → `True`'],
        quote='比较复杂的题目，用自动机来做应该是最清晰的，不过我在这里使用的利用各种flag拼凑起来的低配自动机。',
        quote_src='—— yiduobo 题解原文',
        idea=['先剪掉首尾空格，再从左到右看每个字符，遇到冲突直接 `False`',
              '正负号只能在每段最前；小数点只能在 e 之前一次；e 前要有数字、后要有整数',
              '遇到 e，把 `number_flag`、`symbol_flag` 清零、`point_flag` 置位，等于重开一段整数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`1.e-5` 这种小数点直接在 e 前的写法也合法，不能禁止',
                 '易错：e 之后 `number_flag` 要清零，否则 `"1e"` 会误判为 True',
                 '原文只处理小写 `e`，没有处理 `E`，演示代码保持原样',
                 '对比灵神：灵神拆成指数前/后两段分别检查，yiduobo 用 flag 一趟扫完'],
    ),
)
