OPS = ['MyQueue()', 'push(1)', 'push(2)', 'peek()', 'pop()', 'push(3)', 'peek()', 'pop()', 'peek()', 'pop()', 'empty()']
RES = [None, None, None, 1, 1, None, 2, 2, 3, 3, True]
FIRST = {4, 9, 14, 20, 26}   # 每个方法体的第一行：执行到这里说明开始了一个新操作
OPIDX = {}                   # id(S['_inner']) -> 第几个操作
_cnt = [-1]


def track(fn):
    def cap(S, B, ret):
        if S['_line'] in FIRST:
            _cnt[0] += 1
        OPIDX[id(S['_inner'])] = _cnt[0]
        if callable(fn):
            return fn(S, B, ret)
        env = dict(S)
        env.update(B=B, ret=ret)
        return eval('f' + repr(fn), {}, env)
    return cap


def ops_view(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '操作序列（黄 = 正在执行）', 24, T['muted'], bold=True)
    cur = OPIDX.get(id(S.get('_inner')), -1)
    x, y = x0 + 18, y0 + 42
    for k, op in enumerate(OPS):
        s = op if k >= cur or RES[k] is None else f'{op}→{RES[k]}'
        w = cv.tlen(s, 22, mono=True) + 22
        if x + w > x1 - 12:
            x, y = x0 + 18, y + 46
        if k == cur:
            fill, tc, oc = T['yellow'], T['bg'], T['yellow']
        elif k < cur:
            fill, tc, oc = T['panel2'], T['muted'], T['border']
        else:
            fill, tc, oc = T['panel'], T['dim'], T['border']
        cv.rect((x, y, x + w, y + 38), fill=fill, outline=oc, width=2, r=8)
        cv.text((x + w / 2, y + 19), s, 22, tc, anchor='mm', mono=True, bold=k == cur)
        x += w + 8


def stack_view(var, title, topc):
    """横向画栈（栈底 → 栈顶）：新压入的绿色，栈顶用 topc，刚弹出的数用红字标在右边"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), f'{title}   栈底 → 栈顶', 24, T['muted'], bold=True)
        items, bitems = S.get(var), B.get(var)
        if items is None:
            return
        bitems = bitems or []
        x, y, hgt = x0 + 18, y0 + 44, 60
        grow = len(items) > len(bitems) and items[:len(bitems)] == bitems
        for k, v in enumerate(items):
            w = max(64, cv.tlen(str(v), 30, mono=True) + 30)
            new = grow and k >= len(bitems)
            fill = T['green'] if new else (T[topc] if k == len(items) - 1 else T['panel2'])
            cv.rect((x, y, x + w, y + hgt), fill=fill, outline=T['border'], width=1, r=10)
            cv.text((x + w / 2, y + hgt / 2), str(v), 30, T['bg'] if fill != T['panel2'] else T['text'],
                    anchor='mm', mono=True, bold=True)
            x += w + 8
        if not items:
            cv.text((x, y + hgt / 2), '空', 26, T['dim'], anchor='lm')
            x += 50
        if len(bitems) > len(items) and bitems[:len(items)] == items:
            cv.text((x + 10, y + hgt / 2), '← 弹出 ' + ', '.join(map(str, bitems[len(items):][::-1])), 24,
                    T['red'], anchor='lm', bold=True)
    return draw


def _queue(S):
    s1, s2 = S.get('self.stack1'), S.get('self.stack2')
    if s1 is None or s2 is None:
        return ''
    return f"逻辑上的队列（队首 → 队尾）= `stack2 反过来 + stack1` = =={list(reversed(s2)) + s1}=="


def _first(S):
    if 'self.first' not in S:
        return ''
    s1 = S.get('self.stack1') or []
    return f"`first = {S['self.first']}`" + (f"　（stack1 栈底 = `{s1[0]}`）" if s1 else '　（stack1 为空时不使用）')


def _cap_push_if(S, B, ret):
    if not B['self.stack1']:
        return f'`push({S.x})`：stack1 是空的 → `{S.x}` 会成为 stack1 的==栈底==，记进 `first`'
    return f'`push({S.x})`：stack1 非空，栈底还是 `{S["self.first"]}`，`first` 不变'


def _cap_pop_if(S, B, ret):
    if not B['self.stack2']:
        return '`pop()`：stack2 是空的 → 把 stack1 ==逐个弹出并压入== stack2'
    return f'`pop()`：stack2 非空 → 栈顶 `{B["self.stack2"][-1]}` 就是队首，直接弹'


def _cap_while(S, B, ret):
    s1 = B['self.stack1']
    if s1:
        return f'stack1 还剩 `{len(s1)}` 个，继续倒'
    return 'stack1 倒空了：stack2 就是原 stack1 的==反序==，栈顶 = 最早进来的数'


def _cap_move(S, B, ret):
    v = B['self.stack1'][-1]
    return f'stack1 弹出栈顶 `{v}` → 压入 stack2：`stack2 = {S["self.stack2"]}`'


def _cap_peek_if(S, B, ret):
    if B['self.stack2']:
        return f'`peek()`：stack2 非空 → 队首就是 stack2 栈顶 `{B["self.stack2"][-1]}`'
    return '`peek()`：stack2 为空 → 队首是 stack1 的==栈底==，正好记在 `first` 里'


CONFIG = dict(
    num=232, title='用栈实现队列', difficulty='Easy', category='设计',
    author='yiduobo', technique='主栈 + 辅助栈 · 倒一次就反序',
    tags=['热题173'],
    code='''
class MyQueue(object):

    def __init__(self):
        self.stack1 = []
        self.stack2 = []
        self.first = None

    def push(self, x):
        if not self.stack1:
            self.first = x
        self.stack1.append(x)

    def pop(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()

    def peek(self):
        if self.stack2:
            return self.stack2[-1]
        else:
            return self.first

    def empty(self):
        return not self.stack1 and not self.stack2
''',
    call='''q = MyQueue()
q.push(1); q.push(2)
a = q.peek(); b = q.pop()
q.push(3)
c = q.peek(); d = q.pop(); e = q.peek(); f = q.pop()
[a, b, c, d, e, f, q.empty()]''',
    expect=[1, 1, 2, 2, 3, 3, True],
    views=[
        dict(type='custom', draw=ops_view, h=140),
        dict(type='custom', draw=stack_view('self.stack1', 'stack1（主栈：push 只压这里）', 'purple'), h=120),
        dict(type='custom', draw=stack_view('self.stack2', 'stack2（辅助栈：栈顶 = 队首）', 'cyan'), h=120),
        dict(type='text', fn=_first, size=26, h=56),
        dict(type='text', fn=_queue, size=26, h=90),
    ],
    watch=[('x', 'x', 'blue'), ('first', 'self.first', 'yellow'),
           ('len(stack1)', lambda S: len(S['self.stack1']) if 'self.stack1' in S else None),
           ('len(stack2)', lambda S: len(S['self.stack2']) if 'self.stack2' in S else None)],
    captions={
        4: track('主栈 `stack1`：所有新元素都压到这里'),
        5: track('辅助栈 `stack2`：存放==倒过来==的元素，栈顶就是队首'),
        6: track('`first` 记录 stack1 的栈底（stack1 里最早进来的数），`peek` 时用'),
        9: track(_cap_push_if),
        10: track('`first = {x}`'),
        11: track('无论如何，入队都==压入主栈==：`stack1 = {self.stack1}`，`O(1)`'),
        14: track(_cap_pop_if),
        15: track(_cap_while),
        16: track(_cap_move),
        17: track('弹出 stack2 栈顶 =={ret}==：它正是最早进来的数（先进先出 ✓）'),
        20: track(_cap_peek_if),
        21: track('返回 stack2 栈顶 =={ret}==（只看不弹）'),
        23: track('返回 `first = {ret}`：==不用倒栈==也能看到队首'),
        26: track('`empty()`：两个栈==都空==才是空队列 → `{ret}`'),
    },
    cards=dict(
        one_liner='push 只进主栈；pop 时辅助栈空了就把主栈整个倒过去，顺序正好反过来',
        complexity='`push / peek / empty` 为 `O(1)`，`pop` 均摊 `O(1)`',
        problem=['只用两个==栈==的标准操作（栈顶压入/弹出、看栈顶、大小、判空），实现先进先出的队列',
                 '支持 `push(x)`、`pop()`、`peek()`、`empty()`',
                 '示例：`push(1), push(2), peek() → 1, pop() → 1, empty() → false`'],
        quote='拿栈底元素之前的一系列pop操作最终得到的序列实际上队列的反序……当主栈pop空之后==此时辅助栈就是原先主栈的反序==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['入队：永远压入主栈 `stack1`',
              '出队：辅助栈非空就直接弹它的栈顶；==空了才==把主栈逐个倒进辅助栈',
              '`peek`：辅助栈空时，队首是主栈栈底 → 用 `first` 记住它，不必倒栈'],
        result='返回 `[1, 1, 2, 2, 3, 3, True]` ✓ 每个数都按进入顺序出队',
        summary=['每个元素最多进出主栈、辅助栈各一次 → `pop` ==均摊== `O(1)`',
                 '易错：只有辅助栈==为空==时才能倒栈，否则会打乱顺序',
                 '`first` 只在 stack1 为空时被 push 更新，所以它始终是 stack1 的栈底',
                 '对比 225 用队列实现栈：那题 push 时旋转 `O(n)`',
                 '原文为 Python 2 风格：删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
