def _isv(ch):
    return ch in 'aeiouAEIOU'


CONFIG = dict(
    num=2785, title='将字符串中的元音字母排序', difficulty='Medium', category='字符串',
    author='yiduobo', technique='两趟遍历 · 收集元音再回填',
    tags=[],
    code='''
class Solution(object):
    def sortVowels(self, s):

        vowel_set = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])
        vowel_list = []
        for char in s:
            if char in vowel_set:
                vowel_list.append(char)
        
        vowel_list.sort()
        p = 0
        res = []
        for char in s:
            if char in vowel_set:
                res.append(vowel_list[p])
                p += 1
            else:
                res.append(char)
        
        return ''.join(res)
''',
    call='Solution().sortVowels("lEetcOde")',
    expect='lEOtcede',
    views=[
        dict(type='string', var='s', label='s（橙 = 元音）', cell=84,
             color=lambda S, i, v: 'orange' if _isv(v) else None),
        dict(type='array', var='vowel_list', label='vowel_list（收集到的元音）', cell=84,
             pointers={'p': 'pink'}, color=lambda S, k, v: 'green' if k < S.get('p', 0) else None),
        dict(type='array', var='res', label='res（答案：辅音照抄，元音取 vowel_list[p]）', cell=84,
             color=lambda S, k, v: 'green' if _isv(v) else None),
    ],
    watch=[('char', 'char'), ('p', 'p', 'pink'), ('vowel_list', 'vowel_list', 'orange')],
    captions={
        'vowel_set =': '把 10 个元音放进集合，判断是不是元音只要 `char in vowel_set`',
        'vowel_list = []': '第一趟遍历：把所有元音收集起来',
        'for char in s': lambda S, B, r: f"遍历：`char = '{S.char}'`",
        'if char in vowel_set': lambda S, B, r: (
            (f"`'{S.char}'` 是元音" if S.char in S.vowel_set else f"`'{S.char}'` 不是元音，不收集") if S['_line'] == 7 else
            (f"`'{S.char}'` 是元音 → 取排好序的元音" if S.char in S.vowel_set else f"`'{S.char}'` 是辅音 → 原样保留")),
        'res = []': '`res` 保存答案，按顺序一位一位追加',
        'vowel_list.append': '收集元音 `{vowel_list}`',
        'vowel_list.sort()': '排序：`{vowel_list}`（大写 ASCII 更小，在前）',
        'p = 0': '`p` 表示当前用到第几个元音',
        'res.append(vowel_list[p])': "是元音 → 不放原来的，放 `vowel_list[{p}] = '{res[-1]}'`",
        'p += 1': '用掉一个，`p` → {p}',
        'res.append(char)': "辅音 → 直接放原字符 `'{char}'`",
        "return ''.join": '拼接 `res`：`"{ret}"`',
    },
    cards=dict(
        one_liner='先收集排序所有元音，再扫一遍按位回填',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`s` 中的辅音位置不变，元音按 ASCII 非递减重新排列',
                 '示例：`"lEetcOde"` → `"lEOtcede"`',
                 '元音大小写都算：`aeiouAEIOU`'],
        quote='首先一趟遍历，将所有元音字母都收集起来并排序，得到排序后的元音字母数组vowel_list。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：收集元音并排序得到 `vowel_list`',
              '第二趟：变量 `p` 表示用到第几个元音',
              '不是元音就照抄，是元音就取 `vowel_list[p]` 并 `p += 1`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`p` 只在遇到元音时才加一',
                 '原文为 Python 2 风格，在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神原地改 list，这里另建 `res` 列表按位追加'],
    ),
)
