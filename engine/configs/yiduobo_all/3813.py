def _col(S, i, v):
    if not ('a' <= v <= 'z'):
        return None
    return 'green' if v in 'aeiou' else 'orange'

CONFIG = dict(
    num=3813, title='元音辅音得分', difficulty='Easy', category='模拟',
    author='yiduobo', technique='遍历计数', tags=[],
    code='''
class Solution(object):
    def vowelConsonantScore(self, s):
        
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        v = 0
        c = 0
        for char in s:
            if char in vowel:
                v += 1
            elif 'a' <= char <= 'z':
                c += 1
        
        if c > 0:
            return v // c
        else:
            return 0
''',
    call='Solution().vowelConsonantScore("axeyizou 7")',
    expect=1,
    views=[
        dict(type='string', var='s', color=_col, h=200),
        dict(type='set', var='vowel', h=150),
        dict(type='text', fn=lambda S: f"v = =={S['v']}==，c = =={S['c']}==" if 'c' in S else '', h=100),
    ],
    watch=[('v', 'v', 'green'), ('c', 'c', 'orange'), 'char'],
    captions={
        'vowel = set': '把五个元音放进集合 `vowel`，判断元音只要 `O(1)`',
        'v = 0': '`v` 记元音个数',
        'c = 0': '`c` 记辅音个数',
        'if char in vowel': lambda S, B, r: (f'`{S.char}` 在元音集合里 → 元音' if S.char in S.vowel else f'`{S.char}` 不是元音，还要看是不是字母'),
        'v += 1': '元音：`v` → {v}',
        "elif 'a' <= char <= 'z'": lambda S, B, r: (f'`{S.char}` 在 a~z 之间 → 是字母又不是元音 → ==辅音==' if 'a' <= S.char <= 'z' else f'`{S.char!r}` 是空格或数字 → ==不算辅音==，跳过'),
        'c += 1': '辅音：`c` → {c}',
        'if c > 0': lambda S, B, r: f'`c = {S.c}`：' + ('有辅音，可以做除法' if S.c > 0 else '没有辅音，得分为 0'),
        'return v // c': '得分 `floor({v} / {c})` = =={ret}==',
    },
    cards=dict(
        one_liner='遍历一趟，元音进集合判断，其余字母算辅音',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串含小写字母、空格、数字', '`c > 0` 时得分 `floor(v / c)`，否则 0', '本视频：`"axeyizou 7"` → `1`'],
        quote='按照题目要求模拟即可。对s进行一趟遍历，计算对应的v和c，然后计算对应的score就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先建一个元音集合 `vowel`', '字符在集合里 → `v + 1`；否则只有落在 `a~z` 才 `c + 1`',
              "用 `elif 'a' <= char <= 'z'` 排除空格和数字"],
        summary=['时间 `O(n)`，空间 `O(1)`', '易错点：数字和空格不是辅音', '`c = 0` 要单独返回 0',
                 '原文为 Python 2 风格，这里 `v // c` 已是整数除法，无需修改'],
    ),
)
