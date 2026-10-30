def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'cnt_dict：出现次数 → 该次数对应的栈（栈顶在上）', 24, T['muted'], bold=True)
    cv.text((x0 + 18, y0 + 40), '绿 = 刚压入，蓝 = max_cnt 那一层的栈顶（下一个 pop）', 20, T['blue'], bold=True)
    d = S.get('self.cnt_dict', {}) or {}
    od = B.get('self.cnt_dict', {}) or {}
    mx = S.get('self.max_cnt', 0)
    keys = sorted(d)
    if not keys:
        cv.text((x0 + 18, y0 + 90), '（cnt_dict 还是空的）', 24, T['dim'])
        return
    n = len(keys)
    cw = min(150, (x1 - x0 - 60) / max(n, 3))
    ch = 56
    base = y1 - 60
    sx = x0 + 40
    for c, k in enumerate(keys):
        col = d[k]
        X = sx + c * cw
        for j, v in enumerate(col):
            top = j == len(col) - 1
            fresh = top and len(col) > len(od.get(k, []))
            hot = top and k == mx
            fill = T['green'] if fresh else (T['blue'] if hot else (62, 70, 84))
            cv.rect((X + 6, base - (j + 1) * ch + 4, X + cw - 6, base - j * ch - 2), fill=fill, r=8)
            cv.text((X + cw / 2, base - j * ch - ch / 2 + 1), v, 28, T['bg'] if (fresh or hot) else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, base + 8), f'次数 {k}', 20, T['cyan'] if k == mx else T['dim'], anchor='mt', bold=True)
    cv.line([(sx, base + 2), (sx + n * cw, base + 2)], T['border'], 2)


CONFIG = dict(
    num=895, title='最大频率栈', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按次数分栈 + max_cnt',
    tags=['栈', '设计', '难度分 2028'],
    code='''
class FreqStack(object):

    def __init__(self):
        self.num_cnt = {}
        self.cnt_dict = {}
        self.max_cnt = 0

    def push(self, x):
        cnt = self.num_cnt.get(x, 0) + 1
        self.num_cnt[x] = cnt
        
        if cnt not in self.cnt_dict:
            self.cnt_dict[cnt] = []
        self.cnt_dict[cnt].append(x)

        if cnt > self.max_cnt:
            self.max_cnt = cnt

    def pop(self):
        x = self.cnt_dict[self.max_cnt].pop()
        if not self.cnt_dict[self.max_cnt]:
            self.max_cnt -= 1
        self.num_cnt[x] = self.num_cnt[x] - 1
        return x
''',
    call='''fs = FreqStack()
for v in [5, 7, 5, 7, 4, 5]:
    fs.push(v)
[fs.pop() for _ in range(4)]''',
    expect=[5, 7, 5, 4],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='map', var='self.num_cnt', label='num_cnt（每个数目前出现几次）', fmt=lambda k, v: f'{k} → {v}', h=110, font=30),
        dict(type='text', fn=lambda S: f"max_cnt = ==`{S['self.max_cnt']}`==：现在出现次数最多的数出现了这么多次" if 'self.max_cnt' in S else '', size=28, h=60),
    ],
    watch=[('x', 'x', 'yellow'), ('cnt', 'cnt', 'cyan'), ('max_cnt', 'self.max_cnt', 'blue')],
    captions={
        'self.num_cnt = {}': '`num_cnt`：记录每个数当前出现了几次',
        'self.cnt_dict = {}': '`cnt_dict`：==每个出现次数各有一个栈==',
        'self.max_cnt = 0': '`max_cnt`：当前最大的出现次数',
        'cnt = self.num_cnt.get': '`{x}` 之前出现过 `{cnt - 1}` 次，这次是第 `{cnt}` 次',
        'self.num_cnt[x] = cnt': '更新 `num_cnt[{x}] = {cnt}`',
        'if cnt not in self.cnt_dict': lambda S, B, r: (f'还没有「次数 {S.cnt}」的栈 → 新建' if S.cnt not in S.self.cnt_dict else f'已有「次数 {S.cnt}」的栈'),
        'self.cnt_dict[cnt] = []': '新建「次数 {cnt}」的空栈',
        'self.cnt_dict[cnt].append(x)': '`{x}` 压入「次数 {cnt}」的栈：只有==第 {cnt} 次出现==的数才进这个栈',
        'if cnt > self.max_cnt': lambda S, B, r: (f'`{S.cnt} > max_cnt {S.self.max_cnt}` → 最大次数要更新' if S.cnt > S.self.max_cnt else f'`{S.cnt} ≤ max_cnt {S.self.max_cnt}` → 不用更新'),
        'self.max_cnt = cnt': '`max_cnt` → {self.max_cnt}',
        'x = self.cnt_dict[self.max_cnt].pop()': '弹出 `max_cnt = {B.self.max_cnt}` 那一层的栈顶 `{x}`：次数最高，同层里最晚入栈',
        'if not self.cnt_dict[self.max_cnt]': lambda S, B, r: ('这一层空了 → 次数最高的数降一级' if not S.self.cnt_dict[S.self.max_cnt] else '这一层还有数 → `max_cnt` 不变'),
        'self.max_cnt -= 1': '`max_cnt` 减一 → {self.max_cnt}：下一层「次数 {self.max_cnt}」的栈接班',
        'self.num_cnt[x] = ': '`{x}` 少一次：`num_cnt[{x}] = {self.num_cnt[x]}`',
        'return x': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='每个出现次数配一个栈，pop 取最大次数那层的栈顶',
        complexity='push / pop 均 `O(1)`，空间 `O(q)`',
        problem=['设计 `FreqStack`：`push(x)` 入栈；`pop()` 弹出==出现频率最高==的元素',
                 '频率并列时弹最接近栈顶的',
                 '示例：push 5 7 5 7 4 5，连续 pop → `5, 7, 5, 4`'],
        quote='若对于所有的出现次数cnt，都维护一个对应的栈，那么就可以在max_cnt这个栈弹空之后，继续使用弹出max_cnt - 1这个栈中的元素来满足题目需求。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到双向链表，但 `3->4->3->4` 这种顺序没法还原，放弃',
              '数 `x` 第 `k` 次出现时进「次数 k」的栈：`k` 层栈顶弹完后，`k-1` 层按入栈顺序接着弹',
              '多记一个 `max_cnt`，`pop` 直接找到那一层；这层空了就 `max_cnt -= 1`'],
        summary=['时间：`push`、`pop` 均 `O(1)`；空间 `O(q)`',
                 '易错：一层弹空才把 `max_cnt` 减一，且要同步减 `num_cnt[x]`',
                 '原文已是 Python 3 可运行，未做修改',
                 '对比灵神：灵神用列表按下标分层，用 `len(stacks)` 代替 `max_cnt`；yiduobo 用 dict + `max_cnt`'],
    ),
)
