def _win(S):
    idx = S.get('index')
    if idx is None:
        return None
    if 'res' not in S:
        return (0, idx)
    if idx < S['k']:
        return (0, S['k'] - 1)
    return (idx - S['k'] + 1, idx)


def _out(S):
    if 'res' in S and 'index' in S and S['index'] >= S['k']:
        return S['index'] - S['k']
    return None


def _wi(S, B, ret):
    c = S.blocks[S.index]
    return f'`blocks[{S.index}] = {c!r}`：' + ('白块，要涂' if c == 'W' else '黑块，不用涂')


CONFIG = dict(
    num=2379, title='得到 K 个黑块的最少涂色次数', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='长度为 k 的窗口维护白块数',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1360'],
    code='''
class Solution(object):
    def minimumRecolors(self, blocks, k):

        cnt = 0
        for index in range(k):
            if blocks[index] == 'W':
                cnt += 1
        
        res = cnt
        for index in range(k, len(blocks)):
            if blocks[index] == 'W':
                cnt += 1
            if blocks[index - k] == 'W':
                cnt -= 1
            
            res = min(res, cnt)
            
        return res
''',
    call='Solution().minimumRecolors("WBBWWBBWBW", 7)',
    expect=3,
    views=[
        dict(type='string', var='blocks', label='blocks（框 = 当前窗口；黄 = 白块 W）', cell=96, h=270,
             pointers={'index': 'blue', _out: 'pink'}, pointer_labels={_out: 'index−k'},
             window=(lambda S: (_win(S) or (None,))[0], lambda S: (_win(S) or (None, None))[1]),
             color=lambda S, i, v: 'yellow' if v == 'W' else None),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"窗口 `{S['blocks'][_win(S)[0]:_win(S)[1] + 1]}` 中白块 `cnt = {S['cnt']}`" if _win(S) and 'cnt' in S
                           else '==白块越少，要涂黑的就越少==')),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt`：窗口内白色块的数量',
        'for index in range(k)': lambda S, B, r: ('初始窗口统计完毕' if 'index' in B and S.index == B.index
                                                  else f'统计初始窗口 `blocks[:{S.k}]`：看第 {S.index} 块'),
        "if blocks[index] == 'W'": _wi,
        'cnt += 1': lambda S, B, r: (f'`cnt` → {S.cnt}' if 'res' not in S else f'滑入的是白块：`cnt` → {S.cnt}'),
        'res = cnt': '初始窗口有 `{cnt}` 个白块：先令 `res = {res}`',
        'for index in range(k, len(blocks))': lambda S, B, r: (f'窗口右滑：`blocks[{S.index}]` 滑入，`blocks[{S.index - S.k}]` 滑出'
                                                               if 'index' in B and S.index != B.index else '窗口滑到末尾'),
        "if blocks[index - k] == 'W'": lambda S, B, r: (f"滑出的 `blocks[{S.index - S.k}] = {S.blocks[S.index - S.k]!r}`："
                                                        + ('白块离开' if S.blocks[S.index - S.k] == 'W' else '黑块离开，不影响 cnt')),
        'cnt -= 1': '白块离开窗口：`cnt` → {cnt}',
        'res = min(res, cnt)': lambda S, B, r: (f'cnt 越小越好：`res = min({B.res}, {S.cnt}) = {S.res}`'
                                                + ('，==更新了==' if S.res < B.res else '')),
        'return res': '最少涂 `{res}` 次',
    },
    cards=dict(
        one_liner='窗口里有几个白块就要涂几次，取最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`blocks` 由 `W`（白）和 `B`（黑）组成，每次操作把一个白块涂黑',
                 '求出现==连续 k 个黑块==的最少操作次数',
                 '示例：`"WBBWWBBWBW", k = 7` → `3`'],
        quote='使用一个长度为k的滑动窗口从左向右滑就行了，维护窗口内白色块的数量cnt。cnt越小，需要涂黑的色块就越少，因此取窗口滑动过程中cnt的最小值作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['把某个长为 k 的区间全涂黑，代价就是区间里的白块数',
              '先数初始窗口 `blocks[:k]`，再逐格右滑：滑入 `index`、滑出 `index − k`',
              '答案是所有窗口 `cnt` 的最小值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 要用初始窗口的 `cnt` 初始化，`len(blocks) == k` 时循环不执行',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神用 `zip(blocks[k:], blocks)` 一行算出进出差值'],
    ),
)
