CONFIG = dict(
    num=3163, title='压缩字符串 III', difficulty='Medium', category='字符串',
    author='yiduobo', technique='p、q 双指针分段',
    code='''
class Solution(object):
    def compressedString(self, word):

        res = []
        p = 0
        while p < len(word):
            q = p
            while q < len(word) and word[p] == word[q]:
                q += 1
            
            length = q - p
            for _ in range(length // 9):
                res.append('9')
                res.append(word[p])
            length %= 9
            if length > 0:
                res.append(str(length))
                res.append(word[p])
            
            p = q
        
        return ''.join(res)
''',
    call="Solution().compressedString('aaaaaaaaaaaaaabb')",
    expect='9a5a2b',
    views=[
        dict(type='string', var='word', label='word（p = 段起点，q = 向后找段终点）', cell=70, h=190,
             pointers={'p': 'blue', 'q': 'pink'}, window=('p', lambda S: S['q'] - 1 if S.get('q', 0) > S['p'] else S['p'])),
        dict(type='array', var='res', label='res', h=150),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"当前段：字符 `{S['word'][S['p']]}`，长度 `{S['length']}`" if 'length' in S and S['p'] < len(S['word']) else ''),
    ],
    watch=['p', 'q', 'length'],
    captions={
        'res = []': '`res` 收集压缩后的片段',
        'p = 0': '`p` 指向当前段的起点',
        'while p < len': '`p = {p}`：{"还有字符没压缩，继续" if p < len(word) else "全部处理完"}',
        'q = p': '`q` 从 `p` 出发，向后找这一段的终点',
        'while q < len': '`word[p] = {word[p]}`，{"q 没越界且 word[q] 相同 → 继续往后" if q < len(word) and word[p] == word[q] else "q 到头或遇到不同字符 → 这一段结束"}',
        'q += 1': '`q` → {q}',
        'length = q - p': '这一段 `word[{p}:{q}]` 长度 `length = {length}`',
        'for _ in range': '长度 `{length}` 里有 `{length // 9}` 个整 9',
        "res.append('9')": '写下 `9`',
        'res.append(word[p])': '写下字符 `{word[p]}`',
        'length %= 9': '去掉整 9 后还剩 `length = {length}`',
        'if length > 0': '`length = {length}`：{"还有零头，写成 r + 字符" if length > 0 else "没有零头"}',
        'res.append(str(length))': '写零头长度 `{length}`',
        'p = q': '下一段从 `q = {q}` 开始',
        'return': '拼接得到 `{ret}`',
    },
    cards=dict(
        one_liner='p、q 圈出连续相同的一段，再切成 9 一组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `word` 的单字符前缀（长度最多 9）依次取走，追加「长度+字符」',
                 '示例：`"aaaaaaaaaaaaaabb"` → `"9a5a2b"`'],
        quote='使用两个指针p和q将word中所有由同一个字符构成的子串分离出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 是段起点，`q` 向后走到第一个不同字符', '长度 `length`：能构成 `length // 9` 个 "9c"',
              '`r = length % 9` 不为 0 时再追加 `r` 和 `c`，然后 `p = q`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`q < len(word)` 要写在前面，防止越界',
                 '`length %= 9` 后只有大于 0 才追加',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改',
                 '对比灵神：灵神一次循环里用 `divmod`，这里是双指针 + 两个小循环'],
    ),
)
