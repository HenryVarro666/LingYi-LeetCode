def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S.get('self.d')
    i = S.get('self.i', 0)
    cv.text((x0 + 18, y0 + 4), '所有景点按 (−score, name) 排序：左边最好；黄框 = 当前这次 get 返回的', 22, T['muted'], bold=True)
    items = list(d._l) if d is not None else []
    n = len(items)
    if n == 0:
        cv.text((x0 + 20, y0 + 70), '（还没有景点）', 24, T['dim'])
        return
    cell = min(150, (x1 - x0 - 30) / n)
    for k, (ns, name) in enumerate(items):
        X = x0 + 15 + k * cell
        hit = (k == i - 1)
        new = False
        if B.get('self.d') is not None:
            new = (ns, name) not in B['self.d']._l
        cv.rect((X + 2, y0 + 60, X + cell - 2, y0 + 150), fill=T['green'] if new else T['panel2'], r=8,
                outline=T['yellow'] if hit else T['border'], width=5 if hit else 1)
        fs = 20 if cell > 100 else 15
        cv.text((X + cell / 2, y0 + 92), name, fs, T['bg'] if new else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 126), f'分 {-ns}', fs, T['bg'] if new else T['muted'], anchor='mm')
        cv.text((X + cell / 2, y0 + 168), f'第 {k + 1} 好', 17, T['dim'], anchor='mm')
    cv.text((x0 + 20, y0 + 205), f'已有 {n} 个景点，get 过 i = {i} 次；下一次 get 取第 {i + 1} 好 = d[{i}]', 22, T['yellow'])


CONFIG = dict(
    num=2102, title='序列顺序查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='有序列表（平衡树）+ 计数下标',
    tags=['堆（优先队列）', '难度分 2159'],
    code='''
class SORTracker:
    def __init__(self):
        self.d = SortedList()
        self.i = 0

    def add(self, name: str, score: int) -> None:
        self.d.add((-score, name))

    def get(self) -> str:
        self.i += 1
        return self.d[self.i - 1][1]
''',
    setup='''
# 缺第三方库 sortedcontainers：这里用 bisect 写一个最小的 SortedList 替代
class SortedList:
    def __init__(self):
        self._l = []

    def add(self, x):
        bisect.insort(self._l, x)

    def __getitem__(self, k):
        return self._l[k]
''',
    call='''t = SORTracker()
r = []
t.add("bradford", 2)
t.add("branford", 3)
r.append(t.get())
t.add("alps", 2)
r.append(t.get())
t.add("orland", 2)
r.append(t.get())
t.add("orlando", 3)
r.append(t.get())
t.add("alpine", 2)
r.append(t.get())
r.append(t.get())
r''',
    expect=['branford', 'alps', 'bradford', 'bradford', 'bradford', 'orland'],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('name', 'name', 'orange'), ('score', 'score', 'cyan'), ('i（已 get 次数）', lambda S: S.get('self.i'), 'blue'),
           ('r（已返回）', 'r', 'green')],
    skip=['self.d = SortedList()', 'self.i = 0'],
    captions={
        'self.d.add((-score, name))': '把 `(−score, name)` 插进有序列表：分高的在前，同分按名字字典序 → `{name}` 排在合适的位置',
        'self.i += 1': '第 `{self.i}` 次 get：要的就是第 `{self.i}` 好的景点',
        'return self.d[self.i - 1][1]': '有序列表的下标 `{self.i} - 1` 就是第 `{self.i}` 好 → 返回 ==`{ret}`==',
    },
    cards=dict(
        one_liner='景点放进有序列表，查询次数 i 就是下标 i−1',
        complexity='`add` `O(log n)`（平衡树），`get` `O(log n)`；空间 `O(n)`',
        problem=['`add(name, score)` 加景点：分高者好，同分字典序小者好',
                 '`get()`：第 i 次调用返回当前第 i 好的景点',
                 '示例：加 `bradford 2`、`branford 3`，`get` → `branford`'],
        quote='为了高效插入数据，我们可以用平衡树来维护所有景点。……Python 用户可以直接用 SortedList 模拟。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `(-score, name)` 做键：升序排列就是「从好到坏」',
              '`self.i` 记已查询次数，第 i 次 get 就是 `d[i-1]`',
              '不用手写迭代器：有序列表支持按下标访问，直接取'],
        summary=['`SortedList` 的 `add` 和下标访问都是 `O(log n)`，总体 `O(q log q)`',
                 '易错：分数取负，才能让高分排前面；名字保持原样，同分时字典序小的在前',
                 '原文还有「平衡树 + 迭代器 cur」的思路：add 排在 cur 前面就让 cur 前移',
                 '本视频用 `bisect.insort` 写了一个最小 `SortedList` 替代（缺 sortedcontainers），只演示行为',
                 '对顶堆（§5.7）是另一种写法：大小为 i 的堆放最好的 i 个'],
    ),
)
