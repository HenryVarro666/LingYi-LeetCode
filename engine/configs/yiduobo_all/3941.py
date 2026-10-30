CONFIG = dict(
    num=3941, title='密码强度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='set 去重 + 按字符类型累加',
    tags=[],
    code='''
class Solution(object):
    def passwordStrength(self, password):
        
        res = 0
        for c in set(password):
            if 'a' <= c <= 'z':
                res += 1
            elif 'A' <= c <= 'Z':
                res += 2
            elif '0' <= c <= '9':
                res += 3
            else:
                res += 5
        
        return res
''',
    call='Solution().passwordStrength("aA1!a#1")',
    expect=16,
    views=[
        dict(type='string', var='password', h=190,
             color=lambda S, i, v: ('blue' if 'c' in S and v == S['c'] else None)),
        dict(type='text', size=34, h=150, fn=lambda S: (
            f"当前类型：`{S['c']!r}` → " + ('小写 +1' if 'a' <= S['c'] <= 'z' else '大写 +2' if 'A' <= S['c'] <= 'Z'
                                          else '数字 +3' if '0' <= S['c'] <= '9' else '特殊字符 +5')) if 'c' in S else
            f"先去重：`set(password)` 里一共 `{len(set(S['password']))}` 种不同字符" if 'password' in S else ''),
    ],
    watch=['c', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计强度，从 0 开始',
        'for c in set': '`set(password)` 去重后逐个取字符：`c = {c!r}`，password 里重复的只会出现一次',
        "if 'a' <= c <= 'z'": '`{c!r}` 是小写字母吗？→ {"==是==" if "a" <= c <= "z" else "不是"}',
        "elif 'A' <= c <= 'Z'": '不是小写；`{c!r}` 是大写字母吗？→ {"==是==" if "A" <= c <= "Z" else "不是"}',
        "elif '0' <= c <= '9'": '不是字母；`{c!r}` 是数字吗？→ {"==是==" if "0" <= c <= "9" else "不是"}',
        'res += 1': '小写字母计 1 分 → `res = {res}`',
        'res += 2': '大写字母计 2 分 → `res = {res}`',
        'res += 3': '数字计 3 分 → `res = {res}`',
        'res += 5': '题目保证只剩 `!@#$`，计 5 分 → `res = {res}`',
        'return res': '密码强度 =={res}==',
    },
    cards=dict(
        one_liner='先转成集合去重，再按字符类型各计一次分',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['小写 1 分、大写 2 分、数字 3 分、`!@#$` 特殊字符 5 分',
                 '==每种字符最多计一次分==，求密码强度',
                 '本视频：`"aA1!a#1"` → `1+2+3+5+5 = 16`'],
        quote='由于每个字符只贡献一次分数，因此可以先将password转化为集合来去重，接下来遍历其中的每种字符，根据字符类型更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`set(password)` 一步去重，后面不用再记哪些字符见过',
              '遍历集合，用范围比较 `\'a\' <= c <= \'z\'` 判类型',
              '题目保证只含这四类，`else` 就是特殊字符'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错点：大小写是不同字符，`a` 和 `A` 各计一次',
                 '集合遍历顺序不固定，但总分与顺序无关',
                 '对比灵神：他边遍历边用 `vis` 去重，yiduobo 先整体转成 set'],
    ),
)
