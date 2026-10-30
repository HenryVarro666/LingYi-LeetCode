CONFIG = dict(
    num=2671, title='频率跟踪器', difficulty='Medium', category='设计',
    author='yiduobo', technique='两个哈希表：数 → 频率、频率 → 个数', tags=[],
    code='''
class FrequencyTracker(object):

    def __init__(self):
        self.num_dict = {}
        self.freq_dict = {}

    def add(self, number):
        freq = self.num_dict.get(number, 0)
        self.num_dict[number] = freq + 1
        self.freq_dict[freq] = self.freq_dict.get(freq, 0) - 1
        self.freq_dict[freq + 1] = self.freq_dict.get(freq + 1, 0) + 1

    def deleteOne(self, number):
        if self.num_dict.get(number, 0) > 0:
            freq = self.num_dict[number]
            self.num_dict[number] -= 1
            self.freq_dict[freq] -= 1
            self.freq_dict[freq - 1] = self.freq_dict.get(freq - 1, 0) + 1

    def hasFrequency(self, frequency):
        return self.freq_dict.get(frequency, 0) > 0
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
        dict(type='map', var='self.num_dict', label='num_dict（数 → 频率）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='map', var='self.freq_dict', label='freq_dict（频率 → 有几个数）', fmt=lambda k, v: f'{k} 次（无意义）→ {v}' if k == 0 else f'{k} 次 → {v} 个', h=130),
    ],
    watch=[('number', 'number', 'blue'), ('freq', 'freq', 'orange'), ('frequency', 'frequency', 'pink'), ('out', 'out', 'green')],
    captions={
        'self.num_dict = {}': '`num_dict`：每种数出现的频率',
        'self.freq_dict = {}': '`freq_dict`：每种频率出现的次数',
        'freq = self.num_dict.get(number, 0)': '`{number}` 当前频率 `freq` = {freq}',
        'self.num_dict[number] = freq + 1': '`{number}` 的频率升到 `{freq + 1}`',
        'self.freq_dict[freq] = ': '旧频率 `{freq}` 少了一个数：`freq_dict[{freq}] = {self.freq_dict[freq]}`',
        'self.freq_dict[freq + 1] = ': '新频率 `{freq + 1}` 多了一个数：`freq_dict[{freq + 1}] = {self.freq_dict[freq + 1]}`',
        'if self.num_dict.get(number, 0) > 0': lambda S, B, r: (f'`{S.number}` 的频率 `{S.self.num_dict.get(S.number, 0)}` > 0 → 可以删' if S.self.num_dict.get(S.number, 0) > 0
                                                                else f'`{S.number}` 不存在 → 不删除'),
        'freq = self.num_dict[number]': '删除前频率 `freq` = {freq}',
        'self.num_dict[number] -= 1': '`{number}` 的频率降到 `{self.num_dict[number]}`',
        'self.freq_dict[freq] -= 1': '旧频率 `{freq}` 少一个数：`freq_dict[{freq}] = {self.freq_dict[freq]}`',
        'self.freq_dict[freq - 1] = ': '新频率 `{freq - 1}` 多一个数：`freq_dict[{freq - 1}] = {self.freq_dict[freq - 1]}`',
        'return self.freq_dict': lambda S, B, r: f'`freq_dict[{S.frequency}]` 是 `{S.self.freq_dict.get(S.frequency, 0)}` → ==返回 {r}==',
    },
    cards=dict(
        one_liner='一个表记每个数几次，另一个表记每种次数几个',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['`add` 加一个数，`deleteOne` 删一个数（可能不存在）',
                 '`hasFrequency(f)`：是否有数恰好出现 `f` 次',
                 '本视频：add 3、3、5，再 delete 3、7、5，并多次查询'],
        quote='使用两个哈希表，分别记录每种数次出现的频率，以及每种频率出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次增删：先改这个数的频率，再改 `freq_dict`',
              '旧频率的个数减一，新频率的个数加一',
              '询问时只判断 `freq_dict` 里该频率的个数是否大于 0'],
        summary=['所有操作 `O(1)`，空间 `O(q)`',
                 '`deleteOne` 必须先判断频率大于 0，不存在就不做任何事',
                 '用 `.get(x, 0)` 取默认值，避免 KeyError',
                 '对比灵神：灵神用 defaultdict，并让 deleteOne 复用 add(-1)'],
    ),
)
