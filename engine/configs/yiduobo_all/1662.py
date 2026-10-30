def _cmp(S):
    if 'p1' not in S:
        return ''
    w1, w2 = S['word1'], S['word2']
    if S['p1'] < len(w1) and S['p2'] < len(w2):
        return f"`word1[{S['p1']}][{S['index1']}] = {w1[S['p1']][S['index1']]}`　对比　`word2[{S['p2']}][{S['index2']}] = {w2[S['p2']][S['index2']]}`"
    return '有一边已经走完'


CONFIG = dict(
    num=1662, title='检查两个字符串数组是否相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='两组指针逐字符比较',
    code='''
class Solution(object):
    def arrayStringsAreEqual(self, word1, word2):

        p1 = p2 = index1 = index2 = 0
        while p1 < len(word1) and p2 < len(word2):
            if p1 == len(word1) or p2 == len(word2):
                return False
            if word1[p1][index1] != word2[p2][index2]:
                return False
            
            index1 += 1
            if index1 == len(word1[p1]):
                p1 += 1
                index1 = 0
            
            index2 += 1
            if index2 == len(word2[p2]):
                p2 += 1
                index2 = 0

        return p1 == len(word1) and p2 == len(word2)
''',
    call="Solution().arrayStringsAreEqual(['ab', 'c'], ['a', 'bc'])",
    expect=True,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='array', var='word1', pointers={'p1': 'blue'}, label='word1（p1 = 第几个字符串，index1 = 串内第几个字符）', h=230,
             cell=110),
        dict(type='array', var='word2', pointers={'p2': 'pink'}, label='word2（p2、index2 同理）', h=230, cell=110),
    ],
    watch=[('p1', 'p1', 'blue'), ('index1', 'index1', 'blue'), ('p2', 'p2', 'pink'), ('index2', 'index2', 'pink')],
    captions={
        'p1 = p2 = index1': '`p1`/`p2` 指向当前字符串，`index1`/`index2` 指向串内字符，全从 0 开始',
        'while p1 <': lambda S, B, r: (f'`p1 = {S.p1}`、`p2 = {S.p2}` 都没走完 → 继续比较' if S.p1 < len(S.word1) and S.p2 < len(S.word2) else '至少有一边走完了 → 退出循环'),
        'if p1 == len(word1) or': '到末尾就返回 False（这一行在循环条件下基本不会触发）',
        'if word1[p1][index1] !=': lambda S, B, r: (f"`{S.word1[S.p1][S.index1]}` != `{S.word2[S.p2][S.index2]}` → 字符不同，返回 False" if S.word1[S.p1][S.index1] != S.word2[S.p2][S.index2] else f"`{S.word1[S.p1][S.index1]}` == `{S.word2[S.p2][S.index2]}` → 这一个字符相同"),
        'index1 += 1': 'word1 往后推一个字符：`index1 = {index1}`',
        'if index1 == len': lambda S, B, r: (f'`word1[{S.p1}]` 的字符用完了 → 换到下一个字符串' if S.index1 == len(S.word1[S.p1]) else '当前字符串还没用完'),
        'if index2 == len': lambda S, B, r: (f'`word2[{S.p2}]` 的字符用完了 → 换到下一个字符串' if S.index2 == len(S.word2[S.p2]) else '当前字符串还没用完'),
        'index2 += 1': 'word2 往后推一个字符：`index2 = {index2}`',
        'p1 += 1': '`p1 = {p1}`，下一个字符串',
        'p2 += 1': '`p2 = {p2}`，下一个字符串',
        'index1 = 0': '`index1` 归零，从新字符串的第一个字符开始',
        'index2 = 0': '`index2` 归零，从新字符串的第一个字符开始',
        'return p1 == len': lambda S, B, r: f'两边是否同时走完：`p1 == {len(S.word1)}` 且 `p2 == {len(S.word2)}` → =={r}=='
        ,
    },
    cards=dict(
        one_liner='不拼接字符串：两组指针同步逐字符比',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个字符串数组，把各自元素按顺序拼接成字符串',
                 '判断两个拼接结果是否相同',
                 '示例：`["ab","c"]` 与 `["a","bc"]` → 都是 `"abc"` → `True`'],
        quote='我在这里采用的是使用两组指针分别指向两个字符串数组当前处理到的字符，然后同时向后推进并进行比较',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 管第几个字符串，`index` 管串内第几个字符',
              '字符相同就两边同时后移；字符串用完就换下一个并把 `index` 归零',
              '任何一处字符不同返回 False；循环结束再看两边是否都走完'],
        summary=['时间 `O(n)`，空间 `O(1)`（n 为总字符数）',
                 '易错：最后必须判断两边都走完，否则 `["a"]` 与 `["ab"]` 会误判相等',
                 '循环内的 `p1 == len(word1)` 判断其实多余，原文保留',
                 '更省事的做法是 `"".join(word1) == "".join(word2)`，但要额外 `O(n)` 空间'],
    ),
)
