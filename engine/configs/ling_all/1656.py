CALL = """os = OrderedStream(5)
out = []
out.append(os.insert(3, "ccccc"))
out.append(os.insert(1, "aaaaa"))
out.append(os.insert(2, "bbbbb"))
out.append(os.insert(5, "eeeee"))
out.append(os.insert(4, "ddddd"))
out"""

CONFIG = dict(
    num=1656, title='设计有序流', difficulty='Easy', category='设计',
    author='灵茶山艾府', technique='数组 + 只右移的指针',
    code='''
class OrderedStream:
    def __init__(self, n: int):
        self.a = [""] * (n + 1)
        self.ptr = 1

    def insert(self, idKey: int, value: str) -> List[str]:
        self.a[idKey] = value
        start = self.ptr
        while self.ptr < len(self.a) and self.a[self.ptr]:
            self.ptr += 1
        return self.a[start: self.ptr]
''',
    call=CALL,
    expect=[[], ['aaaaa'], ['bbbbb', 'ccccc'], [], ['ddddd', 'eeeee']],
    views=[
        dict(type='text', fn=lambda S: (f"`ptr = {S['self.ptr']}`：下标 1 到 `ptr - 1` 的值已经输出" if 'self.ptr' in S else '')),
        dict(type='array', var='self.a', pointers={'self.ptr': 'blue'}, label='a（下标从 1 开始，0 号位不用；空串 = 还没到）', h=300, cell=110,
             dim=lambda S, i, v: 'self.ptr' in S and 0 < i < S['self.ptr'],
             color=lambda S, i, v: 'green' if (v and 'start' in S and S['start'] <= i < S['self.ptr']) else None),
        dict(type='text', fn=lambda S: (f"这次返回 `a[{S['start']}:{S['self.ptr']}]` = {S['self.a'][S['start']:S['self.ptr']]}" if 'start' in S and S['_line'] >= 11 else '')),
    ],
    watch=[('ptr', 'self.ptr', 'blue'), ('start', 'start', 'orange'), ('idKey', 'idKey', 'yellow'), ('value', 'value', 'green')],
    captions={
        '[""] * (n + 1)': '长为 `n + 1` 的数组，下标从 1 开始用；空串表示「这个位置还没收到」',
        'self.ptr = 1': '`ptr = 1`：下一个要输出的 id。==它只会向右走，不会回头==',
        'self.a[idKey] = value': '先把 `{value}` 存进 `a[{idKey}]`，无论是不是轮到它',
        'start = self.ptr': '记下起点 `start = {start}`，最后用切片 `a[start:ptr]` 取答案',
        'while self.ptr <': lambda S, B, r: (f"`a[{S['self.ptr']}]` 有值 → ptr 可以继续右移" if S['self.ptr'] < len(S['self.a']) and S['self.a'][S['self.ptr']] else (f"`a[{S['self.ptr']}]` 还是空 → 停在这里，后面的就算有也要等" if S['self.ptr'] < len(S['self.a']) else '`ptr` 到数组末尾，停')),
        'self.ptr += 1': '`a[{self.ptr - 1}]` 已经连上 → `ptr` 右移到 {self.ptr}',
        'return self.a': lambda S, B, r: (f"`ptr` 没动，返回空列表" if not r else f"返回 {r}：这段连续的值按 id 顺序输出，`ptr` 停在 {S['self.ptr']}"),
    },
    cards=dict(
        one_liner='填数组，指针只右移，连续的一段一起吐出来',
        complexity='insert 均摊 `O(1)`，空间 `O(n)`',
        problem=['`n` 个 `(id, value)` 以任意顺序到来',
                 '每次 `insert` 后，若 `ptr` 处已有值，返回从 `ptr` 起最长的连续一段，并移动 `ptr`；否则返回 `[]`',
                 '示例：依次插入 id 3, 1, 2, 5, 4 → `[]`, `[aaaaa]`, `[bbbbb, ccccc]`, `[]`, `[ddddd, eeeee]`'],
        quote='有一个只会向右移动的指针 ptr，初始值为 1。注意：ptr 不会重置为 1，而是停在上次 insert 调用后的位置。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把流看成长 `n` 的数组 `a`，`idKey` 就是下标，一开始全为空',
              '每次填完后看 `a[ptr]`：空就返回空列表；非空就一路右移，经过的值全加入答案',
              '用切片 `a[start:ptr]` 一次取出这一段'],
        summary=['初始化 `O(n)`；`insert` 总共 `n` 次，`ptr` 一共只走 `n` 步，均摊 `O(1)`',
                 '易错：`ptr` 不能每次重置为 1，否则会重复输出',
                 '数组开 `n + 1`，让 id 直接当下标；注意循环里要先判 `ptr < len(a)` 防越界',
                 '「值非空」靠空串判断，因此依赖 `value` 长度固定为 5、不会是空串'],
    ),
)
