S_IN = '  a good   example '


def _chars(S):
    s = S.get('s')
    return None if s is None else ['·' if c == ' ' else c for c in s]


def _contrast(S):
    if 'word_list' not in S:
        return '输入有==首尾空格==，单词之间还可能有==多个空格=='
    bad = S_IN.split(' ')
    return f"对比 `s.split(' ')` = `{bad}`：==切出一堆空串=="


def _result(S, B):
    if S.get('_line') == 5:
        r = ' '.join(S['word_list'])
        return f"`' '.join(word_list)` = =='{r}'==（长度 {len(r)}，没有多余空格）"
    if 'word_list' in S:
        return f"单词个数 `len(word_list) = {len(S['word_list'])}`"
    return ''


CONFIG = dict(
    num=151, title='翻转字符串里的单词', difficulty='Medium', category='字符串',
    author='yiduobo', technique='split + reverse + join',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def reverseWords(self, s):
        word_list = s.split()
        word_list.reverse()
        return ' '.join(word_list)
''',
    call=f'Solution().reverseWords({S_IN!r})',
    expect='example good a',
    views=[
        dict(type='string', var=_chars, label=f's（· 表示空格，共 {len(S_IN)} 个字符）', cell=50,
             color=lambda S, i, v: None if v == '·' else 'blue',
             dim=lambda S, i, v: v == '·'),
        dict(type='text', h=100, fn=_contrast, size=24),
        dict(type='array', var='word_list', label='word_list', cell=150, h=220,
             color=lambda S, i, v: 'green' if S.get('_line') in (4, 5) else 'purple'),
        dict(type='text', h=70, fn=_result, size=27),
    ],
    watch=[('word_list', 'word_list', 'green')],
    captions={
        'word_list = s.split()': '`split()` 不带参数：按==任意长度的空白==切分，首尾空格自动丢掉 → `{word_list}`',
        'word_list.reverse()': '`reverse()` ==原地==反转单词顺序 → `{word_list}`',
        'return': "`' '.join(...)` 用==单个空格==把单词连起来 → `'{ret}'`",
    },
    cards=dict(
        one_liner='用 Python 来写：split 切单词，reverse 反转，join 拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你字符串 `s`，==反转单词的顺序==（单词 = 连续的非空格字符）',
                 '`s` 可能有前导、尾随空格，单词间也可能有多个空格；结果里单词间==只留一个空格==',
                 '示例：`"the sky is blue"` → `"blue is sky the"`；`"  hello world  "` → `"world hello"`',
                 "本视频：`'  a good   example '` → `'example good a'`"],
        quote='这题用python来写==非常简单，split加上reverse最后join一下就搞定了==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s.split()`：按空白切分，==连续空格、首尾空格都被吞掉==，只剩单词',
              '`word_list.reverse()`：把单词顺序倒过来',
              "`' '.join(word_list)`：单词之间正好放一个空格"],
        after=[dict(heading='面试官要求不用库函数呢？', lines=[
            '思路一：双指针从后往前扫，找到一个单词就追加到答案',
            '思路二：先==整体翻转==字符串，再把==每个单词各自翻转==，最后去掉多余空格',
            'C++ 等可变字符串可以做到 `O(1)` 额外空间'])],
        result="运行结束，返回 `'example good a'`",
        summary=['时间 `O(n)`，空间 `O(n)`（单词列表）',
                 "易错：==`split()` 和 `split(' ')` 不一样==，后者会切出空串",
                 '`reverse()` 原地反转、返回 None；也可以写 `word_list[::-1]`',
                 '原文为 Python 2 风格，只删去了 docstring，代码未改'],
    ),
)
