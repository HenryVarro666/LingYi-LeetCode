CONFIG = dict(
    num=1704, title='判断字符串的两半是否相似', difficulty='Easy', category='字符串',
    author='yiduobo', technique='元音计数抵消',
    tags=[],
    code='''
class Solution(object):
    def halvesAreAlike(self, s):

        char_set = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])
        p = len(s) // 2
        cnt = 0
        
        for char in s[:p]:
            if char in char_set:
                cnt += 1
        
        for char in s[p:]:
            if char in char_set:
                cnt -= 1
        
        return cnt == 0
''',
    call='Solution().halvesAreAlike("textbook")',
    expect=False,
    views=[
        dict(type='string', var='s', label='s（前半 / 后半以 p 分界）', pointers={'p': 'pink'}, h=240,
             color=lambda S, i, v: ('green' if v in 'aeiouAEIOU' else None)),
        dict(type='set', var='char_set', fmt=lambda x: str(x), h=200),
        dict(type='text', size=28, fn=lambda S: (f"当前字符 `{S['char']}`；`cnt = {S['cnt']}`（前半元音数 − 已扫的后半元音数）" if 'char' in S and 'cnt' in S else '')),
    ],
    watch=[('p', 'p', 'pink'), ('char', 'char', 'cyan'), ('cnt', 'cnt', 'green')],
    captions={
        'char_set = set': '元音集合：大小写共 10 个',
        'p = len': '中点 `p = {len(s)} // 2 = {p}`：前半 `s[:{p}]`，后半 `s[{p}:]`',
        'cnt = 0': '`cnt` 记录两半元音数之差，开始是 `0`',
        'for char in s[:p]': '扫前半，当前字符 `{char}`',
        'for char in s[p:]': '扫后半，当前字符 `{char}`',
        'cnt += 1': '`{char}` 是元音，前半多一个：`cnt` = {cnt}',
        'cnt -= 1': '`{char}` 是元音，后半也有一个，抵消一个：`cnt` = {cnt}',
        'if char in char_set': lambda S, B, r: (f'`{S.char}` 是元音 → 计数' if S.char in S.char_set else f'`{S.char}` 不是元音 → 跳过'),
        'return cnt == 0': '前半元音数 − 后半元音数 = `cnt = {cnt}`：不为 0 → 两半==不相似==，返回 `{cnt == 0}`',
    },
    cards=dict(
        one_liner='前半加、后半减，元音数相同就恰好抵消为 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 长度为偶数，平分成前后两半',
                 '两半包含的元音字母（大小写）数量相同，就是相似的',
                 '示例：`"textbook"` → 前半 1 个、后半 2 个 → `False`'],
        quote='比较基础的题目，分别遍历字符串的前半和后半部分，计算元音字母的数量即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `p = len(s) // 2` 找到分界点',
              '前半遇元音 `cnt += 1`，后半遇元音 `cnt -= 1`',
              '最后 `cnt == 0` 就说明两半元音一样多'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '别忘了大写元音 `A E I O U`',
                 '原文为 Python 2 写法，`len(s) / 2` 已改为 `len(s) // 2`'],
    ),
)
