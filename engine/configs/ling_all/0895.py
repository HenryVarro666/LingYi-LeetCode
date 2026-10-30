def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'stacks：第 k 层放「入栈时频率为 k」的元素', 24, T['muted'], bold=True)
    cols = [list(c) for c in S.get('self.stacks', [])]
    old = [list(c) for c in B.get('self.stacks', [])]
    if not cols:
        cv.text((x0 + 18, y0 + 56), '（stacks 还是空的）', 24, T['dim'])
        return
    n = len(cols)
    cw = min(150, (x1 - x0 - 60) / max(n, 3))
    ch = 56
    base = y1 - 60
    sx = x0 + 40
    for k, col in enumerate(cols):
        X = sx + k * cw
        for j, v in enumerate(col):
            top = j == len(col) - 1
            fresh = top and (k >= len(old) or len(col) > len(old[k]))
            fill = T['green'] if fresh else (T['blue'] if top and k == n - 1 else (62, 70, 84))
            cv.rect((X + 6, base - (j + 1) * ch + 4, X + cw - 6, base - j * ch - 2), fill=fill, r=8)
            cv.text((X + cw / 2, base - j * ch - ch / 2 + 1), v, 28, T['bg'] if (fresh or (top and k == n - 1)) else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, base + 8), f'频率 {k + 1}', 20, T['cyan'] if k == n - 1 else T['dim'], anchor='mt', bold=True)
    cv.line([(sx, base + 2), (sx + n * cw, base + 2)], T['border'], 2)
    cv.text((x0 + 18, y0 + 40), '绿 = 刚压入的元素，蓝 = 最右栈栈顶（下一个 pop）', 20, T['blue'], bold=True)


CONFIG = dict(
    num=895, title='最大频率栈', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='栈套栈 + 哈希表',
    tags=['栈', '设计', '难度分 2028'],
    code='''
class FreqStack:
    def __init__(self):
        self.stacks = []  # 栈套栈，stacks 中的每个元素都是一个栈
        self.cnt = defaultdict(int)  # 每个 val 的出现次数

    def push(self, val: int) -> None:
        if self.cnt[val] == len(self.stacks):  # 这个元素的频率已经是目前最多的，现在又出现了一次
            self.stacks.append([val])  # 那么必须创建一个新栈
        else:
            self.stacks[self.cnt[val]].append(val)  # 否则就压入对应的栈
        self.cnt[val] += 1  # 更新频率

    def pop(self) -> int:
        val = self.stacks[-1].pop()  # 弹出最右侧栈的栈顶元素
        if not self.stacks[-1]:  # 弹出后，最右侧栈为空
            self.stacks.pop()  # 删除
        self.cnt[val] -= 1  # 更新频率
        return val
''',
    call='''fs = FreqStack()
for v in [5, 7, 5, 7, 4, 5]:
    fs.push(v)
[fs.pop() for _ in range(4)]''',
    expect=[5, 7, 5, 4],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='map', var='self.cnt', label='cnt（每个 val 目前的出现次数）', fmt=lambda k, v: f'{k} → {v}', h=110, font=30),
        dict(type='text', fn=lambda S: (f"本次弹出 ==`{S['val']}`==" if S.get('_line') in (14, 15, 16, 17, 18) and 'val' in S else ''), size=30, h=60),
    ],
    watch=[('val', 'val', 'yellow'), ('cnt', 'dict(self.cnt)', 'cyan'), ('stacks', 'self.stacks', 'green')],
    captions={
        'self.stacks = []': '`stacks` 是栈套栈：每个元素又是一个栈，==按频率分层==',
        'self.cnt = defaultdict': '`cnt` 哈希表实时记录每个数的出现次数',
        'if self.cnt[val] == len': lambda S, B, r: (
            f"`{S.val}` 已出现 `{S.self.cnt[S.val]}` 次，`stacks` 共 `{len(S.self.stacks)}` 层 → 相等：它的频率==已经是最高==，再来一次就要开新栈"
            if S.self.cnt[S.val] == len(S.self.stacks) else
            f"`{S.val}` 已出现 `{S.self.cnt[S.val]}` 次，`stacks` 共 `{len(S.self.stacks)}` 层 → 不相等：第 `{S.self.cnt[S.val] + 1}` 层已存在"),
        'self.stacks.append([val])': '新建第 `{len(self.stacks)}` 层栈，放入 `{val}`',
        'self.stacks[self.cnt[val]].append(val)': '`{val}` 压入第 `{self.cnt[val] + 1}` 层（下标 `{self.cnt[val]}`）：它这是第 `{self.cnt[val] + 1}` 次出现',
        'self.cnt[val] += 1': '更新频率：`cnt[{val}] = {self.cnt[val]}`',
        'val = self.stacks[-1].pop()': '弹出==最右侧栈==（频率最高的一层）的栈顶：`{val}`，同层里它最晚入栈',
        'if not self.stacks[-1]': lambda S, B, r: ('这一层空了' if not S.self.stacks[-1] else '这一层还有元素 → 保留') if S.self.stacks else '所有层都空了',
        'self.stacks.pop()': '最右侧层空了 → 删掉，最高频率降一级',
        'self.cnt[val] -= 1': '`{val}` 少了一次：`cnt[{val}] = {self.cnt[val]}`',
        'return val': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='按频率把栈拆成多层，pop 只动最右一层',
        complexity='push / pop 均 `O(1)`，空间 `O(q)`',
        problem=['设计 `FreqStack`：`push(val)` 入栈；`pop()` 弹出==出现频率最高==的元素',
                 '频率并列时，弹最接近栈顶的那个',
                 '示例：push 5 7 5 7 4 5，连续 pop → `5, 7, 5, 4`'],
        quote='把频率（出现次数）不同的元素，压入不同的栈中。每次出栈时，弹出含有频率最高元素的栈的栈顶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第 k 个栈存「入栈时频率恰为 k」的元素，保持原来的入栈先后',
              '`pop` 取最右侧栈的栈顶：频率最高，同层里又最晚入栈',
              '再用哈希表 `cnt` 实时维护每个数的频率，决定 `push` 去哪一层'],
        summary=['时间：`push`、`pop` 均 `O(1)`；空间 `O(q)`',
                 '易错：`cnt[val] == len(stacks)` 才新开层，否则压入第 `cnt[val]` 个下标的栈',
                 '中间层不会为空：出栈总在最右层，层只会从右边消失',
                 '`cnt` 减到 0 时灵神不删键，省事',
                 '对比：不必记 max_cnt，`len(stacks)` 就是当前最高频率'],
    ),
)
