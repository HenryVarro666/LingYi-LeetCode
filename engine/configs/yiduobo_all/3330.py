W = 'abbcccc'


def _runs(word):
    out, p = [], 0
    while p < len(word):
        q = p + 1
        while q < len(word) and word[q] == word[p]:
            q += 1
        out.append((p, q))
        p = q
    return out


def _txt(S):
    if 'q' not in S:
        return '把字符串切成若干段相同字符；长为 `k` 的一段有 `k − 1` 种可能'
    return f'当前段 `[{S["p"]}, {S["q"]})`，长 `{S["q"] - S["p"]}` → 贡献 `{S["q"] - S["p"] - 1}`，累计 `res = {S["res"]}`'


CONFIG = dict(
    num=3330, title='找到初始输入字符串 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按相同字符分段累加',
    tags=[],
    code='''
class Solution(object):
    def possibleStringCount(self, word):
        
        res = 0
        p = 0
        while p < len(word):
            q = p + 1
            while q < len(word) and word[q] == word[p]:
                q += 1
            
            res += q - p - 1
            p = q
        
        return res + 1
''',
    call=f'Solution().possibleStringCount({W!r})',
    expect=5,
    views=[
        dict(type='string', var='word', label='word（交替着色 = 相同字符的一段）', cell=96, h=200,
             pointers={'p': 'blue', 'q': 'pink'},
             color=lambda S, i, v: next(('cyan' if n % 2 == 0 else 'purple' for n, (a, b) in enumerate(_runs(S['word'])) if a <= i < b), None)),
        dict(type='text', h=120, size=30, fn=_txt),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累加每一段的可能数',
        'p = 0': '`p` 是当前一段的起点',
        'while p < len': lambda S, B, r: (f'`p = {S.p} < {len(S.word)}`：还有没处理的段' if S.p < len(S.word) else '全部分段完毕'),
        'q = p + 1': '`q` 从 `p + 1` 起，向右找这一段的终点',
        'while q < len': lambda S, B, r: (f'`word[{S.q}] == word[{S.p}]`（{S.word[S.q]}）：还是同一段，继续' if S.q < len(S.word) and S.word[S.q] == S.word[S.p]
                                           else f'`q = {S.q}`：这一段到此为止'),
        'q += 1': '同一段，`q` → {q}',
        'res += q - p - 1': '这一段长 `{q - p}`，可能由长 1 到 `{q - p - 1}` 的段多按得到 → 加 `{q - p - 1}`，`res = {res}`',
        'p = q': '跳到下一段：`p` → {p}',
        'return res + 1': '再加上「没犯错」的 1 种：`{res} + 1` = =={res + 1}==',
    },
    cards=dict(
        one_liner='相同字符的一段，长 k 就有 k−1 种误输入',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`word` 是最终显示的字符串，至多有一处某个字符被重复输入了若干次',
                 '求一开始想输入的字符串有几种可能',
                 '示例：`abbcccc` → `5`'],
        quote='对于一个长度为k的由相同字符形成的子串，其可能是由长度为1到长度为k - 1的子串经过误输入得到的，也就是说一共有k - 1中可能的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，把字符串分成若干段相同字符',
              '每段 `k − 1` 种误输入情况，累加起来',
              '最后再加 1：什么都没输错'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '长为 1 的段贡献 0，所以不会多算',
                 '最后别忘了 `+ 1`（不犯错）',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神直接数相邻相同对，yiduobo 先分段再数 `k − 1`，结果相同'],
    ),
)
