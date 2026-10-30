ARR = [1, 2, 3, 3, 3, 4, 3, 1]
W, M = 3, 2


def _sim(arr, w, m):
    """贪心模拟，返回被丢弃的下标集合（仅用于上色）"""
    from collections import Counter
    cnt, disc = Counter(), set()
    for i, x in enumerate(arr):
        if i >= w and i - w not in disc:
            cnt[arr[i - w]] -= 1
        if cnt[x] == m:
            disc.add(i)
        else:
            cnt[x] += 1
    return disc


DISC = _sim(ARR, W, M)


def _pos(S):
    if 'index' not in S:
        return None
    return S['index'] + S['w'] if S.get('_line', 0) >= 15 else S['index']


def _wl(S):
    p = _pos(S)
    return None if p is None else max(0, p - S['w'] + 1)


def _acol(S, i, v):
    p = _pos(S)
    if p is None or i > p:
        return None
    if i in DISC:
        done = sum(d <= p for d in DISC) == S['res']
        if i < p or done:
            return 'red'
        return None
    return 'cyan' if i >= _wl(S) else None


def _adim(S, i, v):
    p = _pos(S)
    return p is not None and i < _wl(S) and i not in DISC


def _txt(S):
    if 'q' not in S:
        return ''
    return f"队列 `q` 记录窗口内==没被丢弃==的物品下标：`{list(S['q'])}`，已丢弃 =={S['res']}== 个"


CONFIG = dict(
    num=3679, title='使库存平衡的最少丢弃次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心 + 滑窗 · 哈希表计数 + 队列记保留',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1639'],
    code='''
class Solution(object):
    def minArrivalsToDiscard(self, arrivals, w, m):

        freq = {}
        res = 0
        q = deque()

        for index, v in enumerate(arrivals[:w]):
            if freq.get(v, 0) + 1 > m:
                res += 1
            else:
                freq[v] = freq.get(v, 0) + 1
                q.append(index)

        for index, v in enumerate(arrivals[w:]):
            if q and q[0] == index:
                freq[arrivals[index]] -= 1
                q.popleft()

            if freq.get(v, 0) + 1 > m:
                res += 1
            else:
                freq[v] = freq.get(v, 0) + 1
                q.append(index + w)

        return res
''',
    call=f'Solution().minArrivalsToDiscard({ARR}, {W}, {M})',
    expect=1,
    views=[
        dict(type='array', var='arrivals', label='arrivals（框 = 最近 w 天，红 = 丢弃）', h=230, cell=100,
             pointers={_pos: 'blue'}, pointer_labels={_pos: '当天'}, window=(_wl, _pos), color=_acol, dim=_adim),
        dict(type='map', var='freq', label='freq：窗口内保留的每种物品个数', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='queue', var='q', label='q：窗口内保留物品的下标', fmt=lambda i: f'{i}:{ARR[i]}', h=130),
        dict(type='text', h=80, size=26, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v'), ('m', 'm'), ('res', 'res', 'red')],
    captions={
        'freq = {}': '`freq`：窗口内==保留下来==的每种物品个数',
        'res = 0': '`res`：丢弃次数',
        'q = deque()': '`q`：按顺序记录窗口内没被丢弃的物品下标',
        'for index, v in enumerate(arrivals[:w])': lambda S, B, ret: (f'前 w 天：第 `{S.index + 1}` 天到达 `v = {S.v}`'
                                                                      if 'index' not in B or S.index != B.index else '前 w 天处理完'),
        'for index, v in enumerate(arrivals[w:])': lambda S, B, ret: (f'窗口右移：第 `{S.index + S.w + 1}` 天到达 `v = {S.v}`，第 `{S.index + 1}` 天离开窗口'
                                                                      if B.get('index') != S.index
                                                                      else '所有天都处理完'),
        'if freq.get(v, 0) + 1 > m': lambda S, B, ret: (f'`freq[{S.v}] + 1 = {S.freq.get(S.v, 0) + 1} > m = {S.m}`：再留就超限 → ==只能丢==' if S.freq.get(S.v, 0) + 1 > S.m
                                                         else f'`freq[{S.v}] + 1 = {S.freq.get(S.v, 0) + 1} ≤ {S.m}`：==不得不丢时才丢==，这次保留'),
        'res += 1': '丢弃次数 `res = {res}`',
        'freq[v] = freq.get': '保留：`freq[{v}]` → `{freq[v]}`',
        'q.append(index)': '保留的下标 `{index}` 入队',
        'q.append(index + w)': '保留的下标 `{index + w}` 入队',
        'if q and q[0] == index': lambda S, B, ret: (f'队头 `{S.q[0]}` 就是离开窗口的第 `{S.index + 1}` 天：它==被保留过==，要从 freq 减掉'
                                                     if S.q and S.q[0] == S.index else
                                                     f'离开的第 `{S.index + 1}` 天不在队列里：它==早被丢弃==，freq 不用改'),
        'freq[arrivals[index]] -= 1': '`freq[{arrivals[index]}]` 减一 → `{freq[arrivals[index]]}`',
        'q.popleft()': '队头出队',
        'return res': '最少丢弃 =={res}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='按到达顺序，不得不丢时才丢；队列记住谁没被丢',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arrivals[i]` 是第 i+1 天到达的物品类型，只能在到达当天决定保留或丢弃',
                 '要求最近 `w` 天里，每种类型最多保留 `m` 个；求最少丢弃数',
                 '本视频：`[1,2,3,3,3,4,3,1], w = 3, m = 2` → `1`'],
        quote='丢弃的物品越靠后，更后面的物品重复的次数就越少，丢弃的可能性就越小。……还需要==额外使用一个哈希表或者队列来记录窗口内没有被丢弃掉的物品==。',
        quote_src='—— yiduobo 题解原文',
        idea=['长为 w 的滑窗 + 哈希表 `freq` 记录窗口内每种物品的个数',
              '新物品让 `freq[v]` 超过 m 才丢弃，否则保留并入队',
              '左边界离开时，只有它是队头（没被丢）才减 `freq`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第二个循环里 `index` 从 0 开始：当天是 `index + w`，离开的是 `index`',
                 '易错：被丢弃的物品离开窗口时不能再减 freq',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神把丢弃的物品改成 0，省掉了队列'],
    ),
)
