CONFIG = dict(
    num=1859, title='将句子排序', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='按末位数字排序（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def sortSentence(self, s: str) -> str:
        a = s.split(" ")
        a.sort(key=lambda w: w[-1])
        for i, s in enumerate(a):
            a[i] = s[:-1]
        return " ".join(a)
''',
    call='Solution().sortSentence("is2 sentence4 This1 a3")',
    expect='This is a sentence',
    views=[
        dict(type='text', fn=lambda S: '按单词最后一个字符（位置编号）排序，再去掉编号', size=30, h=70),
        dict(type='array', var='a', pointers={'i': 'blue'}, cell=170, h=260, label='a（单词列表）'),
    ],
    watch=['a', 'i'],
    captions={
        's.split': '按空格拆成单词列表：`a = {a}`',
        'a.sort': '按每个单词最后一位数字排序，单词回到原本的顺序：`{a}`',
        'for i, s in': '第 {i} 个单词 `{s}`' ,
        'a[i] = s[:-1]': '去掉末尾编号：`a[{i}] = {a[i]}`',
        'return': '用空格拼回句子：`{ret}`',
    },
    cards=dict(
        one_liner='单词末位就是编号：按它排序，再把编号删掉',
        complexity='时间 `O(n log n)`（n 为单词数，至多 9），空间 `O(n)`',
        problem=['打乱的句子里每个单词末尾带着 1~9 的原始位置编号',
                 '还原出原来的句子（不带编号）',
                 '示例：`"is2 sentence4 This1 a3"` → `"This is a sentence"`'],
        quote='func sortSentence(s string) (ans string) { a := strings.Split(s, " ") ; sort.Slice(a, func(i, j int) bool { return a[i][len(a[i])-1] < a[j][len(a[j])-1] }) ... }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['先 `split` 拆词，比较器只看单词的最后一个字符',
              '排好序后，每个单词去掉最后一位，再 `join` 回去'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`sort.Slice` 对应 `a.sort(key=...)`',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：编号只有一位（至多 9 个单词），所以直接比较最后一个字符即可',
                 '去编号时用 `s[:-1]`，别忘了不是去掉最前面'],
    ),
)
