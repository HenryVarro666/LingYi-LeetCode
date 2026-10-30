CONFIG = dict(
    num=1429, title='第一个唯一数字', difficulty='Medium', category='设计',
    author='yiduobo', technique='数组 + 哈希表计数 + 单向移动指针',
    tags=['常用数据结构'],
    code='''
class FirstUnique(object):

    def __init__(self, nums):
        self.p = 0
        self.q = []
        self.cnt = {}

        for num in nums:
            self.add(num)

    def showFirstUnique(self):
        while self.p < len(self.q) and self.cnt[self.q[self.p]] > 1:
            self.p += 1
        
        if self.p == len(self.q):
            return -1
        
        return self.q[self.p]

    def add(self, value):
        if value not in self.cnt:
            self.q.append(value)
        
        self.cnt[value] = self.cnt.get(value, 0) + 1
''',
    call='''f = FirstUnique([2, 3, 5])
r = [f.showFirstUnique()]
f.add(5)
r.append(f.showFirstUnique())
f.add(2)
r.append(f.showFirstUnique())
f.add(3)
r.append(f.showFirstUnique())
r''',
    expect=[2, 2, 3, -1],
    views=[
        dict(type='array', var='self.q', label='q（按首次出现顺序）', pointers={'self.p': 'blue'}, h=170,
             dim=lambda S, i, v: i < S['self.p'] if 'self.p' in S else False),
        dict(type='map', var='self.cnt', label='cnt（数字 → 出现次数）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('p', 'self.p', 'blue'), ('value', 'value', 'yellow')],
    captions={
        'self.cnt = {}': '`q` 记录首次出现的顺序，`cnt` 记录出现次数',
        'while self.p < len': lambda S, B, r: (
            f'`q[p] = {S.self.q[S.self.p]}` 出现了 `{S.self.cnt[S.self.q[S.self.p]]}` 次 → 不唯一，继续往后'
            if S.self.p < len(S.self.q) and S.self.cnt[S.self.q[S.self.p]] > 1
            else '`p` 走到头了或者 `q[p]` 是唯一的 → 停下'),
        'self.p += 1': '`q[p]` 已重复，永远不会再唯一（没有删除）→ `p` 右移到 `{self.p}`',
        'self.p == len(self.q)': lambda S, B, r: ('`p` 走到了 `q` 末尾：没有唯一数字 → 返回 `-1`' if S.self.p == len(S.self.q)
                                                  else '`p` 还在 `q` 里 → `q[p]` 就是答案'),
        'return self.q[self.p]': '`q[p]` 是第一个唯一数字 → 返回 `{ret}`',
        'if value not in self.cnt': lambda S, B, r: (f'`add({S.value})`：`{S.value}` 之前没出现过 → 要进 `q`' if S.value not in S.self.cnt
                                                     else f'`add({S.value})`：`{S.value}` 见过了 → 不进 `q`，只增加次数'),
        'self.q.append': '`{value}` 首次出现 → 追加到 `q`',
        'self.cnt[value] =': '`cnt[{value}] = {self.cnt[value]}`',
    },
    cards=dict(
        one_liner='没有删除操作，答案指针只会往后走',
        complexity='均摊每次操作 `O(1)`，空间 `O(n)`',
        problem=['`FirstUnique(nums)` 初始化；`showFirstUnique()` 返回队列里第一个只出现一次的数，没有返回 `-1`',
                 '`add(value)` 往队列末尾加入一个数',
                 '本视频：`[2,3,5]`，依次 add 5、2、3 并查询'],
        quote='题目中不存在删除操作，因此每一次查询操作的答案只会出现在上一次查询的答案之后，于是可以使用一个变量p指向当前查询的答案在数组中出现的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组 `q` 保存数字的首次出现顺序，哈希表 `cnt` 保存次数',
              '某个数一旦重复就永远不再唯一，所以 `p` ==只增不减==',
              '查询时从上次的 `p` 接着跳过重复数，每个位置最多被跳过一次'],
        summary=['`add` 和 `show` 均摊 `O(1)`，空间 `O(n)`',
                 '`q` 只在首次出现时追加，重复数不会入 `q`',
                 '`p` 不会回退，是因为没有删除操作',
                 '原文就是 Python 3 可运行的写法，未做改动'],
    ),
)
