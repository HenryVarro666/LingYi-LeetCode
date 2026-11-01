CONFIG = dict(
    num=1451, title='重新排列句子中的单词', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='按长度稳定排序（Go 原文转写）',
    code='''
class Solution:
    def arrangeWords(self, text: str) -> str:
        sp = text.split(" ")
        sp[0] = sp[0].lower()
        sp.sort(key=len)
        sp[0] = sp[0].title()
        return " ".join(sp)
''',
    call='Solution().arrangeWords("Keep calm and code on")',
    expect='On and keep calm code',
    views=[
        dict(type='array', var='sp', label='sp（单词列表）', cell=150, h=260,
             color=lambda S, i, v: 'green' if i == 0 and S['_line'] in (6, 7) else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: '按长度：' + '  '.join(f'`{w}`={len(w)}' for w in S['sp']) if 'sp' in S else ''),
    ],
    watch=[('sp', 'sp')],
    captions={
        'text.split': '按空格切开，得到单词列表 `{sp}`',
        'lower()': '第一个单词首字母是大写，先==转小写==：`{sp[0]!r}`，免得它被排到后面还大写',
        'sort(key=len)': '按单词长度排序；==排序是稳定的==，等长单词保持原来的相对顺序 → `{sp}`',
        'title()': '新的第一个单词首字母转大写：`{sp[0]!r}`',
        'return': '用空格拼回句子：`{ret!r}`',
    },
    cards=dict(
        one_liner='先把首词降成小写，稳定排序后再把新首词升成大写',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['句子首字母大写、单词以单个空格分隔，按单词长度升序重排',
                 '长度相同保持原来的相对顺序，输出同样格式的句子',
                 '示例：`"Keep calm and code on"` → `"On and keep calm code"`'],
        quote='sort.SliceStable(sp, func(i, j int) bool { return len(sp[i]) < len(sp[j]) })',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['`SliceStable` 是稳定排序，正好满足“等长保持原顺序”',
              '排序前把首词转小写，排序后把新的首词转大写，格式就对了'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`sort.SliceStable` → `list.sort(key=len)`（Python 排序本身稳定），`strings.Title` → `str.title()`',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：不先转小写，原首词（如 `Keep`）排到后面仍是大写',
                 '易错：不稳定排序会打乱等长单词的顺序'],
    ),
)
