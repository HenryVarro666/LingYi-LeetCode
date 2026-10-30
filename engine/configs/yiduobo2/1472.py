CODE = '''
class BrowserHistory(object):

    def __init__(self, homepage):
        self.q = [homepage]
        self.cnt = 1
        self.now = 0

    def visit(self, url):

        if len(self.q) - 1 > self.now:
            self.now += 1
            self.q[self.now] = url
        else:
            self.now += 1
            self.q.append(url)

        self.cnt = self.now + 1

    def back(self, steps):
        self.now -= steps
        if self.now < 0:
            self.now = 0

        return self.q[self.now]

    def forward(self, steps):
        self.now += steps
        if self.now > self.cnt - 1:
            self.now = self.cnt - 1

        return self.q[self.now]
'''
_LINES = CODE.strip('\n').split('\n')


def _lns(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s]


L_VISIT, L_BACK, L_FWD = _lns('def visit')[0], _lns('def back')[0], _lns('def forward')[0]
NOW_P1 = _lns('self.now += 1')                     # [覆盖分支, 追加分支]
RET = _lns('return self.q[self.now]')


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


def _now(S):
    v = S.get('self.now')
    if not isinstance(v, int):
        return None
    q = S.get('self.q') or []
    return max(-0.6, min(v, len(q) + 0.4)) if v < 0 or v >= len(q) else v


def _if_visit(S, B, ret):
    n, now = len(S['self.q']), S['self.now']
    head = f'`visit("{_short(S["url"])}")`：'
    if n - 1 > now:
        return head + f'`len(q) − 1 = {n - 1} > now = {now}`：之前回退过，后面还有旧网页 → ==直接覆盖== `q[now + 1]`'
    return head + f'`len(q) − 1 = {n - 1}`，`now = {now}`：now 已在队尾 → 正常新增，追加到末尾'


def _back_if(S, B, ret):
    if S['self.now'] < 0:
        return f'`now = {S["self.now"]} < 0`：越过了第一个网页'
    return f'`now = {S["self.now"]} ≥ 0`，没越界'


def _fwd_if(S, B, ret):
    cnt = S['self.cnt']
    if S['self.now'] > cnt - 1:
        return f'`now = {S["self.now"]} > cnt − 1 = {cnt - 1}`：超过了==最后一个有效网页=='
    return f'`now = {S["self.now"]} ≤ cnt − 1 = {cnt - 1}`，没越界'


CONFIG = dict(
    num=1472, title='设计浏览器历史记录', difficulty='Medium', category='设计',
    author='yiduobo', technique='数组 + 当前位置 now + 有效个数 cnt',
    tags=['字节30天'],
    code=CODE,
    call='''bh = BrowserHistory("leetcode.com")
bh.visit("google.com"); bh.visit("facebook.com"); bh.visit("youtube.com")
a = bh.back(2)
bh.visit("linkedin.com")
b = bh.forward(2); c = bh.back(7)
[a, b, c]''',
    expect=['google.com', 'linkedin.com', 'leetcode.com'],
    views=[
        dict(type='text', fn=lambda S: '操作：`visit×3` → `back(2)` → `visit("linkedin")` → `forward(2)` → `back(7)`', h=60, size=24),
        dict(type='text', fn=lambda S: f'当前操作：=={_op(S)}==', h=60),
        dict(type='array', var=lambda S: [_short(x) for x in S['self.q']] if 'self.q' in S else None,
             label='q（省略 .com；蓝箭头 = now；下标 ≥ cnt 的灰色格子 = 无效网页）', cell=150, h=270,
             pointers={_now: 'blue'}, pointer_labels={_now: 'now'},
             color=lambda S, i, v: 'blue' if i == S.get('self.now') else None,
             dim=lambda S, i, v: isinstance(S.get('self.cnt'), int) and i >= S['self.cnt']),
        dict(type='custom', h=150, draw=lambda cv, S, B, box, T: (
            cv.rich(box[0] + 22, box[1] + 10, f"`cnt = {S.get('self.cnt', '?')}`：有效网页数，前进最多到 `q[cnt − 1]`", box[2] - box[0] - 44, size=24, color=T['muted']),
            cv.rich(box[0] + 22, box[1] + 60, '回退后再 `visit`：旧网页不删，==直接覆盖==，用 `cnt` 把后面的标记为无效', box[2] - box[0] - 44, size=24, color=T['muted']))),
    ],
    watch=[('now', 'self.now', 'blue'), ('cnt', 'self.cnt', 'green'), ('len(q)', lambda S: len(S['self.q']))],
    captions={
        'self.q = [homepage]': '初始化：队列 `q = ["{homepage}"]` 保存浏览过的所有地址',
        'self.cnt = 1': '`cnt = 1`：当前有效网页的数目',
        _lns('self.now = 0')[0]: '`now = 0`：正在访问 `q[now]`',
        'if len(self.q) - 1 > self.now': _if_visit,
        NOW_P1[0]: '`now` + 1 → `{self.now}`',
        'self.q[self.now] = url': lambda S, B, ret: (f'覆盖：`q[{S["self.now"]}] = "{_short(S.url)}"`'
                                                     f'（原来的 `{_short(B["self.q"][S["self.now"]])}` 被替换掉）'),
        NOW_P1[1]: '`now` + 1 → `{self.now}`',
        'self.q.append(url)': '`"{url}"` 追加到 `q` 末尾',
        'self.cnt = self.now + 1': lambda S, B, ret: (
            f'`cnt = now + 1 = {S["self.cnt"]}`：' + (f'`q[{S["self.cnt"]}:]` = `{[_short(x) for x in S["self.q"][S["self.cnt"]:]]}` ==变成无效网页=='
                                                     if len(S['self.q']) > S['self.cnt'] else '所有网页都有效')),
        'self.now -= steps': '`back({steps})`：`now` − {steps} → `{self.now}`',
        'if self.now < 0': _back_if,
        _lns('self.now = 0')[1]: '下限是 0：`now = 0`',
        'self.now += steps': '`forward({steps})`：`now` + {steps} → `{self.now}`',
        'if self.now > self.cnt - 1': _fwd_if,
        'self.now = self.cnt - 1': '上限是最后一个有效网页：`now = cnt − 1 = {self.now}`',
        RET[0]: '返回 `q[{self.now}] = "{ret}"`',
        RET[1]: '返回 `q[{self.now}] = "{ret}"`',
    },
    cards=dict(
        one_liner='不删除旧记录：用 now 标当前页，用 cnt 标有效网页的个数',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['实现单标签页浏览器：`visit(url)`、`back(steps)`、`forward(steps)`',
                 '`visit` 会清空前进记录；后退 / 前进最多走到头，返回所在网页',
                 '本视频：`visit` ×3 → `back(2)` → `visit` → `forward(2)` → `back(7)`'],
        quote='使用一个队列q维护当前浏览过的所有地址，并使用一个变量now表示目前正在访问队列中哪个位置表示的网页，以及另一个变量cnt表示==当前队列中有效网页的数目==。',
        quote_src='—— yiduobo 题解',
        idea=['visit：回退过就覆盖 `q[now+1]`，否则追加；然后 `cnt = now + 1`',
              'back：`now −= steps`，小于 0 就置 0',
              'forward：`now += steps`，超过 `cnt − 1` 就置为 `cnt − 1`（不能走进无效网页）'],
        result='`back(2)` → google，`forward(2)` 被 `cnt` 拦在 linkedin，`back(7)` → leetcode ✓',
        summary=['所有操作 `O(1)`，空间 `O(q)`',
                 '`back` / `forward` 不改变浏览历史，所以==不更新 cnt==',
                 '易错：`forward` 的上限是 `cnt − 1` 而不是 `len(q) − 1`，否则会走到被作废的 youtube',
                 '另一种做法：回退栈 + 前进栈，网页在两个栈之间来回倒腾',
                 '原文为 Python 2 风格，删去了文档字符串和调用示例注释，代码未改'],
    ),
)
