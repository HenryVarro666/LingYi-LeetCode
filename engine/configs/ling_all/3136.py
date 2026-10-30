def _cur(S, i, v):
    return 'blue' if 'c' in S and v == S['c'] else None


def _kind(S):
    if 'c' not in S:
        return '先看长度，再扫描每个字符，记录有没有辅音 / 元音'
    c = S['c']
    k = '字母，元音' if c.isalpha() and c.lower() in 'aeiou' else '字母，辅音' if c.isalpha() else '数字' if c.isdigit() else '非法字符'
    return f"当前字符 `'{c}'`：=={k}==　　f = `{S['f']}`"


CONFIG = dict(
    num=3136, title='有效单词', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='两个标记 + 一次遍历',
    tags=[],
    code='''
class Solution:
    def isValid(self, word: str) -> bool:
        if len(word) < 3:
            return False
        f = [False] * 2
        for c in word:
            if c.isalpha():
                f[c.lower() in "aeiou"] = True
            elif not c.isdigit():
                return False
        return all(f)
''',
    call='Solution().isValid("4bE")',
    expect=True,
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符）', cell=110, color=_cur, h=200),
        dict(type='array', var='f', label='f[0] = 有辅音，f[1] = 有元音', cell=130, h=200,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_kind, size=28, h=110),
    ],
    watch=[('f', 'f', 'green')],
    captions={
        'len(word) < 3': lambda S, B, r: f'长度 `{len(B.word)}`，' + ('不足 3 → ==直接不合法==' if len(B.word) < 3 else '够 3 个字符，继续检查'),
        'f = [False]': '`f[0]` 记「出现过辅音」，`f[1]` 记「出现过元音」，开始都是 False',
        'for c in word': '依次取出每个字符 `c`',
        'if c.isalpha()': lambda S, B, r: f"`'{S.c}'` 是字母吗？" + ('是 → 进入字母分支' if S.c.isalpha() else '不是 → 看它是不是数字'),
        'f[c.lower()': lambda S, B, r: f"字母转小写后 {'属于' if S.c.lower() in 'aeiou' else '不属于'} aeiou → `f[{int(S.c.lower() in 'aeiou')}] = True`，==布尔值直接当下标==",
        'elif not c.isdigit()': lambda S, B, r: f"`'{S.c}'` 是数字，合法，跳过" if S.c.isdigit() else f"`'{S.c}'` 既不是字母也不是数字 → ==非法字符，返回 False==",
        'return all(f)': '`f = {f}`：辅音和元音==都出现过==才算有效，`all(f)` = {ret}',
    },
    cards=dict(
        one_liner='f 数组两个格子，分别记辅音和元音，字符非法就立刻返回',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有效单词：长度 ≥ 3，只含字母和数字，且至少一个元音、一个辅音',
                 '给定 `word`，判断是否有效',
                 '示例：`"234Adas"` → `true`；`"b3"` → `false`；`"a3$e"` → `false`',
                 '演示用 `"4bE"`：长度 3，有辅音 b、元音 E'],
        quote='用两个变量 $f_0$ 和 $f_1$ 记录字符串中是否有辅音或元音，必须都为 true 才返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`c.lower() in "aeiou"` 是布尔值，当 0 / 1 下标用，一行就分清辅音和元音',
              '不是字母又不是数字，说明有 `@#$`，直接 `return False`',
              '数字只需放行，不影响两个标记'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只有字母才分元音 / 辅音，数字两边都不算',
                 '易错：元音要兼顾大写，先 `lower()` 再判断',
                 '长度检查放在最前面，不足 3 直接返回'],
    ),
)
