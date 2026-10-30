CODE = '''
class BrowserHistory:
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.cur = 0  # 当前页面是 history[cur]

    def visit(self, url: str) -> None:
        self.cur += 1
        del self.history[self.cur:]  # 把浏览历史前进的记录全部删除
        self.history.append(url)  # 从当前页跳转访问 url 对应的页面

    def back(self, steps: int) -> str:
        self.cur = max(self.cur - steps, 0)  # 后退 steps 步
        return self.history[self.cur]

    def forward(self, steps: int) -> str:
        self.cur = min(self.cur + steps, len(self.history) - 1)  # 前进 steps 步
        return self.history[self.cur]
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][0]


L_VISIT, L_BACK, L_FWD = _ln('def visit'), _ln('def back'), _ln('def forward')


def _short(u):
    return u.replace('.com', '')


def _op(S):
    ln = S.get('_line', 0)
    if ln > L_FWD:
        return f'forward({S["steps"]})'
    if ln > L_BACK:
        return f'back({S["steps"]})'
    if ln > L_VISIT:
        return f'visit("{S["url"]}")'
    return f'BrowserHistory("{S.get("homepage", "")}")'


def _del_cap(S, B, ret):
    h0, cur = B['self.history'], S['self.cur']
    gone = h0[cur:]
    if gone:
        return f'删掉 `history[{cur}:]` = `{[_short(x) for x in gone]}`：==前进的记录全部作废=='
    return f'`history[{cur}:]` 是空的，没有前进记录可删'


def _back_cap(S, B, ret):
    c0, k, c = B['self.cur'], S['steps'], S['self.cur']
    s = f'`back({k})`：`cur = max({c0} − {k}, 0)` = =={c}=='
    if c0 - k < 0:
        s += f'（最多只能后退 {c0} 步）'
    return s


def _fwd_cap(S, B, ret):
    c0, k, c, n = B['self.cur'], S['steps'], S['self.cur'], len(S['self.history'])
    s = f'`forward({k})`：`cur = min({c0} + {k}, {n - 1})` = =={c}=='
    if c0 + k > n - 1:
        s += '（已经是栈顶，最多前进到这里）' if c == c0 else f'（最多只能前进 {c - c0} 步）'
    return s


CONFIG = dict(
    num=1472, title='设计浏览器历史记录', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='栈模拟：列表 + 当前位置 cur',
    tags=['字节30天'],
    code=CODE,
    call='''bh = BrowserHistory("leetcode.com")
bh.visit("google.com"); bh.visit("facebook.com"); bh.visit("youtube.com")
a = bh.back(1); b = bh.back(1); c = bh.forward(1)
bh.visit("linkedin.com")
d = bh.forward(2); e = bh.back(2); f = bh.back(7)
[a, b, c, d, e, f]''',
    expect=['facebook.com', 'google.com', 'facebook.com', 'linkedin.com', 'google.com', 'leetcode.com'],
    views=[
        dict(type='text', fn=lambda S: ('操作：`visit×3` → `back(1)` → `back(1)` → `forward(1)` → `visit` → '
                                        '`forward(2)` → `back(2)` → `back(7)`'), h=90, size=24, lines=2),
        dict(type='text', fn=lambda S: f'当前操作：=={_op(S)}==', h=60),
        dict(type='array', var=lambda S: [_short(x) for x in S['self.history']] if 'self.history' in S else None,
             label='history（栈底 → 栈顶，省略了 .com；蓝箭头 = cur 当前页面）', cell=150, h=270,
             pointers={'self.cur': 'blue'}, pointer_labels={'self.cur': 'cur'},
             color=lambda S, i, v: 'blue' if i == S.get('self.cur') else None,
             dim=lambda S, i, v: isinstance(S.get('self.cur'), int) and i > S['self.cur']),
        dict(type='custom', h=160, draw=lambda cv, S, B, box, T: (
            cv.rich(box[0] + 22, box[1] + 10, '`cur` 左边：可以后退的页面；`cur` 右边（灰）：可以前进的页面', box[2] - box[0] - 44, size=24, color=T['muted']),
            cv.rich(box[0] + 22, box[1] + 60, '`visit` 会把 `cur` 右边==全部删掉==，再把新页面放到栈顶', box[2] - box[0] - 44, size=24, color=T['muted']))),
    ],
    watch=[('cur', 'self.cur', 'blue'), ('len(history)', lambda S: len(S['self.history'])), ('当前页', lambda S: S['self.history'][S['self.cur']], 'green')],
    captions={
        'self.history = [homepage]': '初始化：`history = ["{homepage}"]`，用列表==模拟栈==',
        'self.cur = 0': '`cur = 0`：当前页面是 `history[cur]`',
        'self.cur += 1': '`visit("{url}")`：`cur` 先加一 → `{self.cur}`',
        'del self.history[self.cur:]': _del_cap,
        'self.history.append(url)': '`"{url}"` 入栈：现在 `history[{self.cur}]` 就是当前页',
        'self.cur = max': _back_cap,
        'self.cur = min': _fwd_cap,
        'return self.history[self.cur]': '返回当前页 `"{ret}"`',
    },
    cards=dict(
        one_liner='用一个列表当栈保存浏览历史，cur 指向当前页',
        complexity='所有操作 `O(1)`（visit 均摊），空间 `O(q)`',
        problem=['实现单标签页浏览器：`BrowserHistory(homepage)`、`visit(url)`、`back(steps)`、`forward(steps)`',
                 '`visit` 会==清空所有前进记录==；`back` / `forward` 最多走到头，返回所在的 url',
                 '示例：`visit` google、facebook、youtube 后 `back(1)` → `"facebook.com"`'],
        quote='用一个列表（视作栈）维护浏览历史……visit：先把 cur 加一，==把 history 中的从 cur 到末尾的字符串全部删除==，然后把 url 加到 history 的末尾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`back`：`cur = max(cur − steps, 0)`，不能退到栈底之下',
              '`forward`：`cur = min(cur + steps, n − 1)`，不能超过栈顶',
              '不需要两个栈：`cur` 右边的元素就是「前进栈」'],
        result='依次返回 `facebook, google, facebook, linkedin, google, leetcode` ✓',
        summary=['所有操作 `O(1)`：`del` 删掉的元素之前各 append 过一次，均摊 `O(1)`；空间 `O(q)`',
                 '易错：`visit` 要==先 `cur += 1` 再删除== `history[cur:]`，否则会把当前页也删掉',
                 '`back(7)` 只能退到 0，`forward(2)` 只能进到栈顶',
                 '相似题：数据结构题单「三、栈」'],
    ),
)
