def _qpos(S):
    return [q[0] for q in S['qs']]


def _done(S, i, v):
    fa = S.get('fa')
    if fa is None or i >= len(fa):
        return None
    return 'green' if fa[i] != i else None


def _cur(S):
    p = S.get('p')
    if p is None:
        return None
    for k, it in enumerate(S['intervals']):
        if it is p:
            return k
    return None


def _fml(S):
    if 'l' not in S or S.get('_line', 0) < 14:
        return '按区间长度从小到大回答：每个询问只会被第一个盖住它的区间回答'
    i = S.get('i')
    m = len(S['queries'])
    s = f"区间 `[{S['l']}, {S['r']}]` 长度 =={S['length']}=="
    if i is not None and i < m:
        s += f"　当前询问位置 `{S['qs'][i][0]}`"
    return s


CONFIG = dict(
    num=1851, title='包含每个查询的最小区间', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线 + 并查集跳过已回答询问（Go 原文转写）',
    tags=['常用数据结构', '难度分 2286'],
    code='''
class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # 按照区间长度由小到大排序，这样每次回答的时候用的就是长度最小的区间
        intervals.sort(key=lambda p: p[1] - p[0])

        m = len(queries)
        qs = [(q, i) for i, q in enumerate(queries)]
        # 离线：按查询位置排序
        qs.sort(key=lambda p: p[0])

        # 初始化并查集
        fa = list(range(m + 1))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        ans = [-1] * m
        # 对每个区间，回答所有在 [l,r] 范围内的询问
        # 由于每次回答询问之后，都将其指向了下一个询问
        # 所以若 i = find(i) 符合 i < m and qs[i][0] <= r 的条件，则必然是一个在 [l,r] 范围内的还没有回答过的询问
        for p in intervals:
            l, r = p[0], p[1]
            length = r - l + 1
            # 二分找大于等于区间左端点的最小询问
            i = bisect_left(range(m), True, key=lambda i: qs[i][0] >= l)
            # 回答所有询问位置在 [l,r] 范围内的还没有被回答过的询问
            i = find(i)
            while i < m and qs[i][0] <= r:
                ans[qs[i][1]] = length
                fa[i] = i + 1
                i = find(i + 1)
        return ans
''',
    call='Solution().minInterval([[1,4],[2,4],[3,6],[4,4]], [2,3,4,5])',
    expect=[3, 3, 1, 4],
    skip=['m = len', 'def find', 'l, r = p', 'qs = ['],
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='intervals', var='intervals', pointer=_cur, label='intervals（已按长度排序，黄 = 当前区间）', h=230),
        dict(type='array', var=_qpos, label='qs 的位置（排序后；绿 = 已被回答）', pointers={'i': 'blue'}, color=_done, cell=70, h=150),
        dict(type='array', var='fa', label='fa 并查集（回答完 i 就指向 i+1）', pointers={'i': 'blue'}, cell=70, h=150),
        dict(type='array', var='ans', label='ans（按原询问顺序）', cell=70, h=140,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'length', ('i', 'i', 'yellow')],
    captions={
        'intervals.sort': '==按长度从小到大排序==：先出场的区间更短，谁先盖住询问，谁就是它的最小区间',
        'qs.sort': '询问也按位置排序（`qs` 里带着原下标 `i`），区间 `[l,r]` 里的询问就是连续的一段',
        'fa = list': '`fa[i]` 指向「从 i 起第一个还没回答的询问」，初始每个都指向自己；多开一格当哨兵',
        'for p in intervals': lambda S, B, r: ('所有区间都处理完了' if B.get('p') == S.get('p') else f'取下一个（更长的）区间 `{S.p}`'),
        'length = ': '区间长度 `{r} - {l} + 1 = {length}`',
        'bisect_left': '二分找位置 `>= {l}` 的第一个询问，下标 `i = {i}`',
        'i = find(i)': '跳过已回答的询问：`find` 直接落到第一个还没回答的下标',
        'while i < m': lambda S, B, r: (f"`i = {S.i} < m` 且位置 `{S.qs[S.i][0]} <= r = {S.r}`：还没回答、又在区间里 → ==回答它==" if S.i < len(S.queries) and S.qs[S.i][0] <= S.r
                                       else (f"`i = {S.i}` 已越过所有询问，本区间结束" if S.i >= len(S.queries) else f"位置 `{S.qs[S.i][0]} > r = {S.r}`：出了区间，本区间结束")),
        'ans[qs[i][1]]': '询问 `{qs[i][0]}`（原下标 {qs[i][1]}）被长度 =={length}== 的区间回答：`ans[{qs[i][1]}] = {length}`',
        'fa[i] = i + 1': '`fa[{i}] = {i + 1}`：以后 find 到它会直接跳到下一个，不会重复回答',
        'i = find(i + 1)': '`find({B.i + 1})`：从下一个询问起，跳过已回答的，找到第一个还没回答的',
        'return ans': '没被任何区间盖住的保持 `-1`，返回 `{ans}`',
    },
    cards=dict(
        one_liner='换个角度：让每个区间去回答询问，短的先来',
        complexity='时间 `O((n+m) log n + m α)`，空间 `O(m)`',
        problem=['`intervals[i] = [l, r]`，长度 `r-l+1`；每个询问 `q` 要找==包含 q 的最短区间==的长度，没有则 `-1`',
                 '示例：`intervals=[[1,4],[2,4],[3,6],[4,4]]`，`queries=[2,3,4,5]`',
                 '输出：`[3,3,1,4]`'],
        quote='对每个区间，去回答包含这个区间的询问。按照区间长度从小到大排序，遍历每个区间，我们可以直接回答在该区间内的尚未被回答的询问。',
        quote_src='—— 灵茶山艾府题解',
        idea=['区间按长度升序：==第一个盖住某询问的区间就是答案==',
              '询问按位置排序，区间内的询问是连续一段；二分找到起点',
              '回答过的询问用并查集指向下一个，==下次直接跳过==，每个询问只回答一次'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Search` 用 `bisect_left` 的 `key` 参数等价替换）',
                 '时间：两次排序 + 二分 + 并查集，每个询问只被回答一次',
                 '易错点：`fa` 要开 `m+1` 格；`fa[i] = i + 1` 之后用 `find(i + 1)` 继续往后走',
                 '要把询问的原下标带上排序，最后才能按原顺序写答案'],
    ),
)
