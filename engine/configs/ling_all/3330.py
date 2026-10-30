W = 'abbcccc'


def _pairs(word):
    return [i for i in range(1, len(word)) if word[i] == word[i - 1]]


def _txt(S):
    if 'x' not in S:
        return '相邻相同的位置（橙色）每个贡献 1 种犯错方案，再加 1 种不犯错'
    x, y = S['x'], S['y']
    if x == y:
        return f'`{x}` 和 `{y}` ==相同==：这里可能多按了一次 → 多 1 种方案，`ans = {S["ans"]}`'
    return f'`{x}` 和 `{y}` 不同：这里不可能犯错，方案数不变 `ans = {S["ans"]}`'


CONFIG = dict(
    num=3330, title='找到初始输入字符串 I', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='数相邻相同字母对',
    tags=[],
    code='''
class Solution:
    def possibleStringCount(self, word: str) -> int:
        ans = 1
        for x, y in pairwise(word):
            if x == y:
                ans += 1
        return ans
''',
    call=f'Solution().possibleStringCount({W!r})',
    expect=5,
    views=[
        dict(type='string', var='word', label='word（橙色 = 与左边相邻字母相同）', cell=96, h=230,
             color=lambda S, i, v: 'orange' if i in _pairs(S['word']) else None),
        dict(type='text', h=120, size=30, fn=_txt),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '先算上「Alice 没犯错」这 1 种：`ans = {ans}`',
        'for x, y in pairwise': '取相邻两个字母 `x = {x}`，`y = {y}`',
        'if x == y': lambda S, B, r: (f'`{S.x} == {S.y}`：相同 → Alice 可能在这里多按了一次' if S.x == S.y
                                      else f'`{S.x} != {S.y}`：不同 → 这里不可能是多按，跳过'),
        'ans += 1': '每一对相邻相同字母，多一种犯错方案：`ans` → =={ans}==',
        'return ans': '方案数 = 相同相邻对数 + 1 = =={ans}==',
    },
    cards=dict(
        one_liner='方案数 = 相邻相同字母对的个数 + 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`word` 是最终屏幕上的字符串，Alice 至多有一次某个字母被多按了几次',
                 '求她一开始想输入的字符串有多少种可能',
                 '示例：`abbcccc` → `5`'],
        quote='每有一对相邻相同字母，Alice 就会多一种犯错的方案。所以方案数等于相邻相同字母对的个数加一，其中加一是不犯错的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻字母都不同：不可能犯错，只有 1 种',
              '一对相邻相同：可以认为「多按了一次」，多 1 种',
              '`abbb`：想输入 `abbb`、`abb`、`ab` 共 3 种 = 2 对 + 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：至多犯错一次 = 只重复==一个==字母，所以不会把不同字母的重复叠加',
                 '题解还给了 Python 一行写法：`1 + sum(x == y for x, y in pairwise(word))`'],
    ),
)
