def _flags(S):
    if 'up_flag' not in S:
        return ''
    def f(n, v):
        return f'==✓ {n}==' if v else f'× {n}'
    return '   '.join([f('小写', S['down_flag']), f('大写', S['up_flag']), f('数字', S['digit_flag']), f('特殊', S['spe_flag'])])


CONFIG = dict(
    num=2299, title='强密码检验器 II', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 四个标记',
    tags=[],
    code='''
class Solution(object):
    def strongPasswordCheckerII(self, password):

        if len(password) < 8:
            return False
        
        spe_set = set(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+'])

        up_flag = down_flag = digit_flag = spe_flag = False
        for index, char in enumerate(password):
            if 'a' <= char <= 'z':
                down_flag = True
            elif 'A' <= char <= 'Z':
                up_flag = True
            elif '0' <= char <= '9':
                digit_flag = True
            elif char in spe_set:
                spe_flag = True

            if index > 0 and char == password[index - 1]:
                return False

        return up_flag and down_flag and digit_flag and spe_flag
''',
    call='Solution().strongPasswordCheckerII("Ab1!cD2e")',
    expect=True,
    views=[
        dict(type='string', var='password', pointers={'index': 'blue'}, h=200, label='password',
             color=lambda S, i, v: ('green' if (S.get('index') is not None and i < S['index']) else None) if 'index' in S else None),
        dict(type='text', fn=_flags, size=34, h=120),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'cyan'), ('up_flag', 'up_flag', 'green'), ('down_flag', 'down_flag', 'green')],
    captions={
        'if len(password) < 8': '先看长度：`len = {len(password)}`，{"不足 8 位 → 直接不合格" if len(password) < 8 else "够 8 位，继续"}',
        'spe_set = set': '把 12 个特殊字符放进集合，之后判断“是不是特殊字符”只要 `O(1)`',
        'up_flag = down_flag': '四个标记：小写、大写、数字、特殊字符，开始都没见过 → `False`',
        'for index, char': '扫描第 `{index}` 个字符 `{char}`',
        "'a' <= char <= 'z'": lambda S, B, r: f"`{S.char}` 是小写字母吗 → {'是，down_flag = True' if 'a' <= S.char <= 'z' else '不是，继续看别的类别'}",
        "'A' <= char <= 'Z'": lambda S, B, r: f"`{S.char}` 是大写字母吗 → {'是，up_flag = True' if 'A' <= S.char <= 'Z' else '不是，继续看别的类别'}",
        "'0' <= char <= '9'": lambda S, B, r: f"`{S.char}` 是数字吗 → {'是，digit_flag = True' if '0' <= S.char <= '9' else '不是，继续看别的类别'}",
        'elif char in spe_set': lambda S, B, r: f"`{S.char}` 在特殊字符集合里吗 → {'在，spe_flag = True' if S.char in S.spe_set else '不在'}",
        'down_flag = True': '见到小写字母：`down_flag = True`',
        'up_flag = True': '见到大写字母：`up_flag = True`',
        'digit_flag = True': '见到数字：`digit_flag = True`',
        'spe_flag = True': '见到特殊字符：`spe_flag = True`',
        'if index > 0 and char': lambda S, B, r: ('第 0 个字符没有前一个，不用比' if S.index == 0 else
                                                   f"和前一个字符比：`{S.char}` vs `{S.password[S.index-1]}` → {'相同，出现两个连续相同字符，直接 False' if S.char == S.password[S.index-1] else '不同，没问题'}"),
        'return up_flag': '遍历完没有连续重复：四种字符是否都出现过 → `{up_flag} and {down_flag} and {digit_flag} and {spe_flag}` = =={ret}==',
    },
    cards=dict(
        one_liner='长度先判，一趟遍历同时记四类字符并查相邻重复',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['强密码：至少 8 位，含小写、大写、数字、特殊字符各一个',
                 '并且不能有两个相邻字符相同',
                 '示例：`"IloveLe3tcode!"` → `true`；`"1aB!"` → `false`',
                 '本视频：`"Ab1!cD2e"` → `true`'],
        quote='首先判断密码长度是否达标，接下来一趟遍历，判断是否出现每种需要出现的字符，同时判断每个字符是否与上一个字符不同就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度不够，直接 `False`，后面都不用看',
              '四个布尔标记，遇到对应类别的字符就置 `True`',
              '同一趟里顺便比较 `char` 和 `password[index-1]`，重复就立刻返回'],
        summary=['时间 `O(n)`，空间 `O(1)`（特殊字符集合大小固定）',
                 '易错：相邻比较要先判 `index > 0`，否则会拿 `password[-1]` 比',
                 '易错：特殊字符只有 `!@#$%^&*()-+` 这 12 个',
                 '原文为 Python 2 写法（`class Solution(object)`），Python 3 可直接运行，代码未改动'],
    ),
)
