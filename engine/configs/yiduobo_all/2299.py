def _flags(S):
    if 'up_flag' not in S:
        return ''
    items = [('小写', S['down_flag']), ('大写', S['up_flag']), ('数字', S['digit_flag']), ('特殊', S['spe_flag'])]
    return '  '.join(f"{n}{'✓' if f else '·'}" for n, f in items)


CONFIG = dict(
    num=2299, title='强密码检验器 II', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 + 四个标记',
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
    call="Solution().strongPasswordCheckerII('Ab3$xYz-')",
    expect=True,
    views=[
        dict(type='string', var='password', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', fn=_flags, h=90),
    ],
    watch=['index', 'char'],
    captions={
        'len(password) < 8': '长度 `{len(password)}`：{"不足 8 位 → 不合格" if len(password) < 8 else "长度达标"}',
        'spe_set = set': '把 12 个特殊字符放进集合，方便 `in` 判断',
        'up_flag = down_flag': '四个标记：大写、小写、数字、特殊，先都设为 False',
        'for index, char': '遍历密码，当前字符 `{char!r}`',
        "'a' <= char": '`{char!r}` {"是" if "a" <= char <= "z" else "不是"}小写字母{" → 继续往下看" if not ("a" <= char <= "z") else ""}',
        "'A' <= char": '`{char!r}` {"是" if "A" <= char <= "Z" else "不是"}大写字母{" → 继续往下看" if not ("A" <= char <= "Z") else ""}',
        "'0' <= char": '`{char!r}` {"是" if "0" <= char <= "9" else "不是"}数字{" → 继续往下看" if not ("0" <= char <= "9") else ""}',
        'char in spe_set': '`{char!r}` {"在" if char in spe_set else "不在"}特殊字符集合里',
        'down_flag = True': '出现小写字母 → `down_flag = True`',
        'up_flag = True': '出现大写字母 → `up_flag = True`',
        'digit_flag = True': '出现数字 → `digit_flag = True`',
        'spe_flag = True': '出现特殊字符 → `spe_flag = True`',
        'if index > 0 and char': '和上一个字符比：`{char!r}` vs `{password[index-1]!r}` → 不同，继续',
        'return up_flag': '四个标记 {up_flag}/{down_flag}/{digit_flag}/{spe_flag} → =={up_flag and down_flag and digit_flag and spe_flag}==',
    },
    cards=dict(
        one_liner='一趟遍历：每类字符一个标记，再比相邻字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['强密码要求：至少 8 位，含小写、大写、数字、特殊字符，且相邻字符不同',
                 '特殊字符是 `!@#$%^&*()-+` 之一',
                 '示例：`"Ab3$xYz-"` → `true`'],
        quote='首先判断密码长度是否达标，接下来一趟遍历，判断是否出现每种需要出现的字符，同时判断每个字符是否与上一个字符不同就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度不够直接返回',
              '特殊字符放进 `set`，判断是否特殊只需 `in`',
              '遍历时更新四个布尔标记，同时和前一个字符比较',
              '最后四个标记都为真才是强密码'],
        summary=['时间 `O(n)`，空间 `O(1)`（特殊字符集合大小固定）',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '易错：`index > 0` 才能比前一个字符',
                 '对比灵神：灵神用一个 mask 的 4 个二进制位；这里用 4 个布尔变量'],
    ),
)
