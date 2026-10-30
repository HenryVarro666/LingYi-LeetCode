def _word_state(S):
    w = S.get('word')
    if w is None:
        return ''
    return f"当前单词 `{w}`　第一行 `{S['flag1']}`　第二行 `{S['flag2']}`　其他行 `{S['flag3']}`"


CONFIG = dict(
    num=500, title='键盘行', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合判断所在行',
    code='''
class Solution(object):
    def findWords(self, words):

        set1 = set(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 
                   'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'])
        set2 = set(['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                   'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'])

        res = []
        for word in words:
            flag1 = flag2 = flag3 = 0
            for char in word:
                if char in set1:
                    flag1 = 1
                elif char in set2:
                    flag2 = 1
                else:
                    flag3 = 1

            if flag1 + flag2 + flag3 == 1:
                res.append(word)

        return res
''',
    call="Solution().findWords(['Dad', 'Hi', 'pop'])",
    expect=['Dad', 'pop'],
    max_steps=90,
    skip=['set1 = set', 'set2 = set'],
    views=[
        dict(type='array', var='words', pointers={}, h=130, label='words',
             color=lambda S, i, v: ('blue' if S.get('word') == v else 'green' if v in S.get('res', []) else None)),
        dict(type='string', var='word', h=150, label='当前单词 word', pointers={},
             color=lambda S, i, v: ('blue' if S.get('char') == v and False else None)),
        dict(type='text', size=28, fn=lambda S: _word_state(S)),
        dict(type='array', var='res', h=130, label='res（只用一行字母的单词）', color=lambda S, i, v: 'green'),
    ],
    watch=['word', 'char', ('flag1', 'flag1', 'blue'), ('flag2', 'flag2', 'pink'), ('flag3', 'flag3', 'orange')],
    captions={
        'res = []': '`set1` 是键盘第一行（qwertyuiop），`set2` 是第二行（asdfghjkl），都含大小写；不在这两个集合里的就是第三行',
        'flag1 = flag2': '每个新单词先把三个标记清零：`flag1`/`flag2`/`flag3` 分别表示用到了第几行',
        'if char in set1': lambda S, B, r: (f"`'{S.char}'` 在第一行集合里 → 标记 ==flag1==" if S.char in S.set1 else f"`'{S.char}'` 不在第一行 → 继续看第二行"),
        'elif char in set2': lambda S, B, r: (f"`'{S.char}'` 在第二行集合里 → 标记 ==flag2==" if S.char in S.set2 else f"`'{S.char}'` 不在第二行 → 只能是第三行"),
        'flag1 = 1': '`flag1 = 1`：这个单词用到了第一行',
        'flag2 = 1': '`flag2 = 1`：这个单词用到了第二行',
        'flag3 = 1': '`flag3 = 1`：这个单词用到了第三行',
        'if flag1 + flag2 + flag3': lambda S, B, r: (f'三个标记之和 `{S.flag1 + S.flag2 + S.flag3}` == 1 → ==只用了一行==，收下' if S.flag1 + S.flag2 + S.flag3 == 1
                                                   else f'三个标记之和 `{S.flag1 + S.flag2 + S.flag3}` ≠ 1 → 跨了多行，丢掉'),
        'res.append': '`{word}` 加入答案：`res = {res}`',
        'for word': '取下一个单词 `{word}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='三个标记看单词用了几行，恰好 1 行才收下',
        complexity='时间 `O(总字符数)`，空间 `O(1)`',
        problem=['给定单词列表，找出只用美式键盘==同一行==字母就能打出的单词',
                 '三行：`qwertyuiop`、`asdfghjkl`、`zxcvbnm`，大小写不敏感',
                 '示例：`["Hello","Alaska","Dad","Peace"]` → `["Alaska","Dad"]`；本视频：`["Dad","Hi","pop"]`'],
        quote='比较基础的题目，对于每个单词遍历每个字符，判断字符其所在的行。若只使用了同一行中字符则将单词加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['建两个集合存第一、二行字母（含大小写），其余都算第三行',
              '逐字符查集合，用 `flag1/2/3` 记录用过哪几行',
              '标记之和为 1 说明只用了一行'],
        summary=['时间 `O(总字符数)`，空间 `O(1)`',
                 '大小写字母都要放进集合，否则 `Dad` 里的大写 `D` 会被当成第三行',
                 '第三行不建集合：既不在 set1 也不在 set2 就是第三行',
                 '原文本身就是 Python 3 可运行的写法，代码未做改动'],
    ),
)
