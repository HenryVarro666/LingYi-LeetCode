S0, K0 = '0110011', 2


def _right(S):
    return S['q'] - 1 if 'q' in S else None


def _color(S, i, v):
    if 'q' not in S or 'p' not in S:
        return None
    if S['p'] <= i < S['q']:
        return 'green' if S['_line'] in (25, 26) else 'blue'
    return None


def _top(S):
    if 'q' not in S:
        return f'`k = {K0}`：答案必然==以 1 开头、以 1 结尾=='
    p, q = S['p'], S['q']
    if p >= len(S0):
        return '左边界走到末尾'
    t = S0[p:q] if q > p else ''
    return f"窗口 `[{p}, {q})` = `{t!r}`，`cnt = {S['cnt']}`；当前 `res = {S['res']!r}`"


def _upd(S, B, ret):
    t, r = S.s[S.p:S.q], S.res
    if len(r) == 0:
        return f'`res` 还是空的 → 用 `{t!r}` 更新'
    if len(r) > len(t):
        return f'`{t!r}` 长 {len(t)}，比 `res` 的 {len(r)} ==更短== → 更新'
    if len(r) == len(t) and r > t:
        return f'长度相同，`{t!r}` ==字典序更小== → 更新'
    if len(r) == len(t):
        return f'长度相同，但 `{t!r}` 字典序不比 `{r!r}` 小 → 不更新'
    return f'`{t!r}` 比 `res` 长 → 不更新'


CONFIG = dict(
    num=2904, title='最短且字典序最小的美丽子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 两端对齐到 1',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def shortestBeautifulSubstring(self, s, k):

        res = ''
        p = 0
        q = 0
        cnt = 0
        while p < len(s):
            while p < len(s) and s[p] == '0':
                p += 1

            if p == len(s):
                break

            if q < p:
                q = p
            while q < len(s) and cnt < k:
                if s[q] == '1':
                    cnt += 1
                q += 1

            if cnt < k:
                break

            if len(res) == 0 or len(res) > q - p or (len(res) == q - p and res > s[p : q]):
                res = s[p: q]

            cnt -= 1
            p += 1

        return res
''',
    call=f'Solution().shortestBeautifulSubstring({S0!r}, {K0})',
    expect='11',
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='string', var='s', label='s（框 = 窗口 [p, q−1]，绿 = 用来更新答案）',
             pointers={'p': 'cyan', 'q': 'orange'}, window=('p', _right), color=_color, cell=120, h=300),
    ],
    watch=[('p', 'p', 'cyan'), ('q', 'q', 'orange'), ('cnt', 'cnt', 'blue'), ('res', 'res', 'green')],
    skip=['p = 0', 'q = 0', "if s[q] == '1'"],
    captions={
        "res = ''": "`res` 记录答案，一开始为空",
        'cnt = 0': '窗口 `[p, q)`，`cnt` 是窗口里 1 的个数',
        'while p < len(s):': lambda S, B, r: (f'`p = {S.p}`，继续找下一个起点' if S.p < len(S.s) else '`p` 越界，结束'),
        "while p < len(s) and s[p] == '0'": lambda S, B, r: (f"`s[{S.p}] = '0'`：答案不会以 0 开头 → 跳过" if S.p < len(S.s) and S.s[S.p] == '0'
                                                            else (f"`s[{S.p}] = '1'`：左边界停在==最左侧的 1== 上" if S.p < len(S.s) else '后面没有 1 了')),
        "p += 1": '`p` → {p}',
        'if p == len(s)': lambda S, B, r: ('剩下全是 0，结束' if S.p == len(S.s) else f'`p = {S.p}` 没有越界'),
        'if q < p': lambda S, B, r: (f'`q = {S.q} < p`：右边界至少要从 p 开始' if S.q < S.p else f'`q = {S.q}` 在上一轮基础上==继续==，不用回退'),
        'q = p': '`q` → {q}',
        'while q < len(s) and cnt < k': lambda S, B, r: (f'`cnt = {S.cnt} < {S.k}`：1 还不够 → q 往右滑' if S.q < len(S.s) and S.cnt < S.k
                                                         else (f'`cnt = {S.cnt} == {S.k}`：右边界刚好停在==第 k 个 1 之后==' if S.cnt >= S.k
                                                               else '`q` 到末尾了')),
        'cnt += 1': "`s[{q}] = '1'`：`cnt` → {cnt}",
        'q += 1': '`s[{q - 1}] = {s[q - 1]!r}` 收进窗口，`q` → {q}',
        'if cnt < k': lambda S, B, r: ('剩余部分 1 不够 k 个 → 直接退出' if S.cnt < S.k else f'窗口 `{S.s[S.p:S.q]!r}` 恰好有 {S.k} 个 1'),
        'if len(res) == 0 or': _upd,
        'res = s[p: q]': '`res` → =={res!r}==',
        'cnt -= 1': '左边界的 1 要移出：`cnt` → {cnt}',
        'return res': '答案：=={ret!r}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='左边界跳到下一个 1，右边界接着滑到凑满 k 个 1',
        complexity='时间 `O(n^2)`（比较子串 `O(n)`），空间 `O(n)`',
        problem=['二进制串 `s`，==恰好含 k 个 1== 的子串叫美丽子串',
                 '返回最短美丽子串中字典序最小的，没有就返回空串',
                 '示例：`"1011", k = 2` → `"11"`；本视频 `"0110011", k = 2` → `"11"`'],
        quote='为了使得最终答案最小，那么答案字符串必然以1开头，再以1结尾，因此可以先将窗口左边界滑动到剩余字符串中==最左侧1所在的位置==，然后将右边界在上一轮的基础上滑动到下一个1。',
        quote_src='—— yiduobo 题解原文',
        idea=['窗口是左闭右开 `[p, q)`，`cnt` 记录其中 1 的个数',
              '左边界跳过 0 停在 1 上；右边界只增不减，凑满 k 个 1 就停',
              '移走左端的 1 后 `cnt -= 1`，下一轮右边界接着往后找'],
        summary=['时间 `O(n^2)`：p、q 都只右移，但每次切片比较 `O(n)`',
                 '易错：先比长度再比字典序，`res` 为空时直接更新',
                 '剩余部分凑不齐 k 个 1 时可以提前 break',
                 '对比灵神：灵神枚举右端点、缩左端点；这里枚举以 1 开头的左边界',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
