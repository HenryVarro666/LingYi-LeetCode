WORDS = ["cd", "ac", "dc", "ca", "zz"]

CONFIG = dict(
    num=2744, title='最大字符串配对数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='二重循环暴力 · 标记已用',
    code='''
class Solution(object):
    def maximumNumberOfStringPairs(self, words):

        n = len(words)
        vis = set()
        for i in range(n - 1):
            if i not in vis:
                for j in range(i + 1, n):
                    if j not in vis and words[i][0] == words[j][1] and words[i][1] == words[j][0]:
                        vis.add(i)
                        vis.add(j)
        
        return len(vis) // 2
''',
    call=f'Solution().maximumNumberOfStringPairs({WORDS})',
    expect=2,
    views=[
        dict(type='array', var='words', label='words（蓝 = i，粉 = j，绿 = 已配对标记）', cell=110, h=230,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: 'green' if 'vis' in S and i in S['vis'] else None),
        dict(type='set', var='vis', label='vis（已配对的下标）', fmt=lambda x: str(x), h=160, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"比较 `{S['words'][S['i']]!r}` 与 `{S['words'][S['j']]!r}`" if S.get('_inner', {}).get('j') is not None and 'j' in S and 'i' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('len(vis)', 'len(vis)', 'green')],
    skip=['n = len'],
    captions={
        'vis = set()': '`vis` 记录已经配过对的下标',
        'for i in range': lambda S, B, r: ('外层循环结束' if B.get('i') == S.i else f'`i = {S.i}`：固定第一个字符串 `{S.words[S.i]!r}`'),
        'if i not in vis': lambda S, B, r: (f'`{S.i}` 没配过对，继续找它的搭档' if S.i not in S.vis else f'`{S.i}` 已经配过对，跳过'),
        'for j in range': lambda S, B, r: ('内层结束，没有更多候选' if B.get('j') == S.j and B.get('i') == S.i else f'`j = {S.j}`：候选搭档 `{S.words[S.j]!r}`'),
        'if j not in vis': lambda S, B, r: (f'`j = {S.j}` 已用过，跳过' if S.j in S.vis else
                                             (f'`{S.words[S.i]!r}` 反转是 `{S.words[S.i][::-1]!r}` = `words[j]` → ==配对==' if S.words[S.i][::-1] == S.words[S.j]
                                              else f'`{S.words[S.i]!r}` 反转是 `{S.words[S.i][::-1]!r}` ≠ `{S.words[S.j]!r}`，不配')),
        'vis.add(i)': '标记 `i = {i}` 已用',
        'vis.add(j)': '标记 `j = {j}` 已用 → `vis = {sorted(vis)}`',
        'return': '`vis` 里有 `{len(vis)}` 个下标，每对占 2 个 → `{len(vis)} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='数据规模小，二重循环找搭档，标记用过的',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`words` 里每个字符串长为 2、互不相同',
                 '`words[i]` 等于 `words[j]` 的反转（`i < j`）就能配对，每个串最多配一次',
                 '示例：`["ab","ba","cc"]` → `1`',
                 '本视频：`["cd","ac","dc","ca","zz"]` → `2`'],
        quote='由于题目的数据规模非常小，因此可以直接二重循环暴力枚举所有当前还未使用过的字符串组合。若某个组合符合条件，那么就将这两个字符串标记为使用过。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举 `i`，内层枚举 `j > i`，都要求没被标记过',
              '反转的判断写成两个字符对调：`w[i][0] == w[j][1]` 且 `w[i][1] == w[j][0]`',
              '配对后两个下标都进 `vis`，最后 `len(vis) // 2` 就是对数'],
        summary=['时间 `O(n^2)`，`n <= 50` 完全够用',
                 '易错：`vis` 里每对有两个下标，最后要除以 2',
                 '原文为 Python 2 写法，`len(vis) / 2` 已改为 `//`',
                 '对比灵神：灵神用哈希集合一次遍历 `O(n)`；这里用暴力枚举'],
    ),
)
