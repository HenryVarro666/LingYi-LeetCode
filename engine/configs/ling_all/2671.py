CONFIG = dict(
    num=2671, title='频率跟踪器', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='哈希表 cnt + 频率的频率 freq', tags=[],
    code='''
class FrequencyTracker:
    def __init__(self):
        self.cnt = defaultdict(int)  # number 的出现次数
        self.freq = defaultdict(int)  # number 的出现次数的出现次数

    def add(self, number: int, delta=1) -> None:
        self.freq[self.cnt[number]] -= 1  # 去掉一个旧的 cnt[number]
        self.cnt[number] += delta
        self.freq[self.cnt[number]] += 1  # 添加一个新的 cnt[number]

    def deleteOne(self, number: int) -> None:
        if self.cnt[number]:
            self.add(number, -1)

    def hasFrequency(self, frequency: int) -> bool:
        return self.freq[frequency] > 0  # 至少有一个 number 的出现次数恰好为 frequency
''',
    call='''t = FrequencyTracker()
out = []
out.append(t.hasFrequency(2))
t.add(3)
t.add(3)
t.add(5)
out.append(t.hasFrequency(2))
t.deleteOne(3)
out.append(t.hasFrequency(2))
t.deleteOne(7)
t.deleteOne(5)
out.append(t.hasFrequency(1))
out''',
    expect=[False, True, False, True],
    views=[
        dict(type='map', var='self.cnt', label='cnt（数 → 出现次数）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='map', var='self.freq', label='freq（出现次数 → 有几个数）', fmt=lambda k, v: f'{k} 次（无意义）→ {v}' if k == 0 else f'{k} 次 → {v} 个', h=130),
    ],
    watch=[('number', 'number', 'blue'), ('delta', 'delta', 'orange'), ('frequency', 'frequency', 'pink'), ('out', 'out', 'green')],
    captions={
        'self.cnt = defaultdict': '`cnt` 记每个数出现几次',
        'self.freq = defaultdict': '`freq` 记「出现次数」的出现次数，让查询 `O(1)`',
        'self.freq[self.cnt[number]] -= 1': '`{number}` 旧次数是 `{self.cnt[number]}`：这个次数的计数 -1',
        'self.cnt[number] += delta': '`cnt[{number}]` 变成 `{self.cnt[number]}`',
        'self.freq[self.cnt[number]] += 1': '新次数 `{self.cnt[number]}` 的计数 +1，`freq[{self.cnt[number]}] = {self.freq[self.cnt[number]]}`',
        'if self.cnt[number]': lambda S, B, r: (f'`{S.number}` 出现过（次数 `{S.self.cnt[S.number]}`）→ 复用 add，delta = -1' if S.self.cnt[S.number]
                                                else f'`{S.number}` 不在其中 → 什么都不删'),
        'self.add(number, -1)': '删除一个等于加 `-1`，复用 add 的维护逻辑',
        'return self.freq': lambda S, B, r: f'`freq[{S.frequency}]` 是 `{S.self.freq[S.frequency]}` → ==返回 {r}==',
    },
    cards=dict(
        one_liner='再开一个哈希表，记「出现次数」的出现次数',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['实现 `add`、`deleteOne`、`hasFrequency`',
                 '`hasFrequency(f)`：是否存在出现恰好 `f` 次的数',
                 '`deleteOne` 时数不存在就什么都不做'],
        quote='用哈希表 freq 统计出现次数的出现次数，从而可以 O(1) 回答 hasFrequency。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt[number]` 变化前后，对应的 `freq` 一减一加',
              '查询只看 `freq[frequency] > 0`',
              '`deleteOne` 复用 `add(number, -1)`，只写一份维护逻辑'],
        summary=['所有操作 `O(1)`，空间 `O(q)`',
                 '==先减旧次数、再改 cnt、再加新次数==，顺序不能乱',
                 '`deleteOne` 要先判断 `cnt[number]` 非零，否则会出现负次数',
                 '`freq[0]` 会被当成「出现 0 次」累计，但 `frequency >= 1`，不影响答案'],
    ),
)
