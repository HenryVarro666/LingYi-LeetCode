def _cmp(S):
    if 'p1' not in S or 'res' not in S:
        return ''
    a = S['word1'][S['p1']:] + S['word2'][S['p2']:]
    b = S['word2'][S['p2']:] + S['word1'][S['p1']:]
    if S['p1'] >= len(S['word1']) or S['p2'] >= len(S['word2']):
        return f"有一边用完了：`{S['word1'][S['p1']:]}` / `{S['word2'][S['p2']:]}`，剩下的直接接上"
    return f"`word1[p1:] + word2[p2:]` = `{a}`　{'>' if a > b else '≤'}　`word2[p2:] + word1[p1:]` = `{b}`"


CONFIG = dict(
    num=1754, title='构造字典序最大的合并字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='双指针 · 比较两种拼接',
    tags=['灵神题单·贪心与思维', '灵神题单·字符串', '难度分 1829'],
    code='''
class Solution(object):
    def largestMerge(self, word1, word2):

        n1 = len(word1)
        n2 = len(word2)
        p1 = p2 = 0
        res = []
        while p1 < n1 and p2 < n2:
            if word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]:
                res.append(word1[p1])
                p1 += 1
            else:
                res.append(word2[p2])
                p2 += 1
        
        if p1 == n1:
            return ''.join(res) + word2[p2:]
        else:
            return ''.join(res) + word1[p1:]
''',
    call='Solution().largestMerge("cabaa", "bcaaa")',
    expect='cbcabaaaaa',
    views=[
        dict(type='string', var='word1', label='word1（粉 = p1，灰 = 已取走）', cell=84, h=230, pointers={'p1': 'pink'},
             dim=lambda S, i, v: 'p1' in S and i < S['p1']),
        dict(type='string', var='word2', label='word2（蓝 = p2，灰 = 已取走）', cell=84, h=230, pointers={'p2': 'blue'},
             dim=lambda S, i, v: 'p2' in S and i < S['p2']),
        dict(type='string', var=lambda S: ''.join(S['res']) if 'res' in S and S['res'] else '', label='res（已合并的结果）', cell=64, h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='text', fn=_cmp, size=24),
    ],
    watch=[('p1', 'p1', 'pink'), ('p2', 'p2', 'blue')],
    captions={
        'n1 = len': '`n1 = {n1}`',
        'n2 = len': '`n2 = {n2}`',
        'p1 = p2': '两个指针 `p1`、`p2` 分别指向两个单词还没用的第一个字符',
        'res = []': '`res` 收集合并结果',
        'while p1 < n1': lambda S, B, r: (f'`p1 = {S.p1} < {S.n1}` 且 `p2 = {S.p2} < {S.n2}`，两边都还有字符' if S.p1 < S.n1 and S.p2 < S.n2
                                          else f'`p1 = {S.p1}`，`p2 = {S.p2}`：有一边用完了，退出循环'),
        'if word1[p1:]': lambda S, B, r: (f'比较两种拼接：`{S.word1[S.p1:] + S.word2[S.p2:]}` vs `{S.word2[S.p2:] + S.word1[S.p1:]}` → '
                                          + ('前者更大，==取 word1== 的字符' if S.word1[S.p1:] + S.word2[S.p2:] > S.word2[S.p2:] + S.word1[S.p1:]
                                             else '后者更大（或相等），==取 word2== 的字符')),
        'res.append(word1': '取 `word1[p1] = {word1[p1]}` 加入 `res`',
        'p1 += 1': '`p1` → {p1}',
        'res.append(word2': '取 `word2[p2] = {word2[p2]}` 加入 `res`',
        'p2 += 1': '`p2` → {p2}',
        'if p1 == n1': lambda S, B, r: ('`p1 == n1`：word1 用完了，只剩 word2 的后缀可以接' if S.p1 == S.n1 else '`p1 != n1`：word2 用完了，只剩 word1 的后缀可以接'),
        'return': '`res` 加上剩余部分 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='谁的「后缀+对方后缀」拼出来更大，就先取谁',
        complexity='时间 `O(n·(n+m))`（每步比较切片），空间 `O(n+m)`',
        problem=['把 `word1`、`word2` 每次从某一个的开头取一个字符追加到 `merge`',
                 '求能构造的字典序最大的 `merge`',
                 '示例：`"cabaa"`、`"bcaaa"` → `"cbcabaaaaa"`'],
        quote='若当前的word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]，那么此时就应该合并word1[p1]，否则合并word2[p2]。',
        quote_src='—— yiduobo 题解原文',
        idea=['像归并排序一样用两个指针，但字符相同时不能只比一个字符',
              '把「剩余的 word1 + 剩余的 word2」和反过来拼的结果整串比较，谁大先取谁',
              '加上另一个字符串，是为了一边走到末尾时仍能比较下去'],
        summary=['时间 `O(n·(n+m))`，每次比较切片要 `O(n+m)`，题目数据 3000 可以过',
                 '循环结束后，剩下的那个单词的后缀直接接在末尾',
                 '不能只比较 `word1[p1]` 和 `word2[p2]`，字符相同时会选错',
                 '原文提到也可以用后缀数组把比较做到线性，作者偷懒没用'],
    ),
)
