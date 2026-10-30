S, K = 'ULURRD', 2


def _win(S_):
    i = S_.get('index')
    if i is None:
        return None
    return i + 1


def _win_r(S_):
    i = S_.get('index')
    if i is None:
        return None
    return i + S_['k']


CONFIG = dict(
    num=3694, title='删除子字符串后不同的终点', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 · 集合记偏移量',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1739'],
    code='''
class Solution(object):
    def distinctPoints(self, s, k):

        def move(x, y, c, delta):
            if c == 'U':
                return x, y + delta
            elif c == 'D':
                return x, y - delta
            elif c == 'L':
                return x - delta, y
            else:
                return x + delta, y

        dx, dy = 0, 0
        for c in s[:k]:
            dx, dy = move(dx, dy, c, 1)
        vis = set([(dx, dy)])

        for index, c in enumerate(s[k:]):
            dx, dy = move(dx, dy, c, 1)
            dx, dy = move(dx, dy, s[index], -1)
            vis.add((dx, dy))

        return len(vis)
''',
    call=f'Solution().distinctPoints({S!r}, {K})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 偏移量对应的长为 k 的窗口）', cell=96, h=190,
             window=(lambda S_: 0 if 'index' not in S_ and 'vis' in S_ else _win(S_),
                     lambda S_: S_['k'] - 1 if 'index' not in S_ and 'vis' in S_ else _win_r(S_))),
        dict(type='set', var='vis', label='vis（不同的偏移量）', fmt=lambda p: f'({p[0]},{p[1]})', h=170, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S_: f"窗口偏移 `(dx, dy) = ({S_['dx']}, {S_['dy']})`" if 'dx' in S_ else '偏移量 = 窗口内每个字符的移动之和'),
    ],
    skip=['if c ==', 'elif c ==', 'return x', 'else:'],
    watch=[('dx', 'dx', 'orange'), ('dy', 'dy', 'orange'), ('index', 'index', 'blue'), ('len(vis)', 'len(vis)', 'green')],
    captions={
        'dx, dy = 0, 0': '`(dx, dy)` 表示当前窗口内字符的总偏移量',
        'for c in s[:k]': '先把第一个窗口 `s[:k]` 的字符逐个累加',
        'dx, dy = move(dx, dy, c, 1)': lambda S, B, ret: (
            f"第一个窗口：把 `{S.c!r}` 的移动累加进偏移（delta = +1）" if S._line == 16
            else f"窗口右边进来 `{S.c!r}`：把它的移动加到偏移上（delta = +1）"),
        'move(dx, dy, s[index], -1)': '窗口左边出去 `{s[index]!r}`：把它的移动撤销（delta = −1）',
        'vis = set': '第一个窗口的偏移量放进集合：`({dx}, {dy})`',
        'for index, c in enumerate': lambda S, B, ret: (
            f'窗口右移：进来 `s[{S.index + S.k}] = {S.c!r}`，出去 `s[{S.index}] = {S.s[S.index]!r}`' if 'index' in S and 'c' in S and S.index + S.k < len(S.s) and (('index' not in B) or S.index != B.index or S._line == 20)
            else '遍历结束'),
        'vis.add': '不同的偏移量 ⇔ 不同的终点，记录 `({dx}, {dy})`，现有 `{len(vis)}` 个',
        'return len(vis)': '集合大小 `{len(vis)}` 就是不同终点的数量',
    },
    cards=dict(
        one_liner='删掉一个子串 = 终点加一个偏移量，数偏移量就行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 由 `U/D/L/R` 组成，从 `(0,0)` 出发按顺序走；要删掉==一个长为 k 的子串==',
                 '求删完后可能的不同最终坐标个数',
                 f'本视频：`s = "{S}", k = {K}`'],
        quote='从s中移除一个子串，就相当于在原始最终位置的基础上增加了一个偏移量。……不同偏移量的数量实际上就是可以到达的不同最终坐标数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['不需要知道具体坐标，只需知道偏移量有几种',
              '先累加第一个窗口，再右移：==加入新字符，减去旧字符==',
              '用 `set` 去重，最后看集合大小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`move(..., delta)`：`delta = 1` 是加入，`delta = -1` 是撤销',
                 '第一个窗口的偏移要先放进集合，别漏掉',
                 '原文为 Python 2 写法，只删去了类型说明；对比灵神：灵神把第一个窗口记作 `(0,0)`，这里记的是窗口的真实偏移'],
    ),
)
