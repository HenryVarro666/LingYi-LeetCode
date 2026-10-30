S0 = '001110000'


def _start(s, i):
    """s[i] 所在这一组的起点"""
    while i > 0 and s[i - 1] == s[i]:
        i -= 1
    return i


def _groups(S):
    """(当前组起点, 上一组起点)；没有上一组时为 None"""
    if 'i' not in S or 'cur' not in S:
        return None, None
    s, i = S['s'], S['i']
    st = _start(s, i)
    return st, (_start(s, st - 1) if st > 0 else None)


def _color(S, i, v):
    if 'i' not in S or 'cur' not in S:
        return None
    st, pst = _groups(S)
    if st <= i <= S['i']:
        return 'blue'
    if pst is not None and pst <= i < st:
        return 'pink'
    return None


def _dim(S, i, v):
    if 'i' not in S or 'cur' not in S:
        return False
    st, pst = _groups(S)
    return i > S['i'] or (i < (pst if pst is not None else st))


def _subs(S):
    st, pst = _groups(S)
    s, i = S['s'], S['i']
    k = min(st - pst, i - st + 1) if pst is not None else 0
    return [s[st - 1] * j + s[st] * j for j in range(k, 0, -1)]


def _info(S):
    if 'i' not in S or 'cur' not in S:
        return '按连续相同字符分组：粉 = 上一组，蓝 = 当前组'
    if S.get('_line') == 9:
        subs = _subs(S)
        if not subs:
            return '第一组前面没有上一组：`pre = 0`，得到 `0` 个'
        return '交界处向外扩展：' + '、'.join(f'`{t}`' for t in subs) + f'　共 =={len(subs)}== 个'
    return f'上一组长度 `pre = {S["pre"]}`，当前组已数到 `cur = {S["cur"]}`，`ans = {S["ans"]}`'


def _if(S, B, r):
    i, n, s = S.i, S.n, S.s
    if i == n - 1:
        return f'`i = {i}` 是最后一个字符 → ==遍历到了这一组的末尾=='
    if s[i] != s[i + 1]:
        return f'`s[{i}] = {s[i]}` ≠ `s[{i + 1}] = {s[i + 1]}` → ==遍历到了这一组的末尾=='
    return f'`s[{i}] = s[{i + 1}] = {s[i]}`：同一组，继续往后数'


def _add(S, B, r):
    g = min(B.pre, S.cur)
    if B.pre == 0:
        return f'第一组没有上一组：`min(0, {S.cur}) = 0`，`ans` 不变'
    return f'上一组 `{B.pre}` 个、这一组 `{S.cur}` 个 → 能配出 `min({B.pre}, {S.cur})` = =={g}== 个合法子串，`ans` → {S.ans}'


CONFIG = dict(
    num=696, title='计数二进制子串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='分组循环 · 相邻两组取 min',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        n = len(s)
        pre = cur = ans = 0
        for i in range(n):
            cur += 1
            if i == n - 1 or s[i] != s[i + 1]:
                # 遍历到了这一组的末尾
                ans += min(pre, cur)
                pre = cur
                cur = 0
        return ans
''',
    call=f'Solution().countBinarySubstrings({S0!r})',
    expect=5,
    views=[
        dict(type='text', fn=_info, size=28, h=90),
        dict(type='string', var='s', label='s（粉 = 上一组，蓝 = 当前组）', cell=92, h=300,
             pointers={'i': 'yellow'}, color=_color, dim=_dim),
    ],
    watch=[('i', 'i', 'yellow'), ('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'pre = cur = ans = 0': '`pre`：上一组的长度；`cur`：当前组的长度；`ans`：答案',
        'for i in range(n)': lambda S, B, r: ('`i` 已到末尾，遍历结束' if 'i' in B and B.i == S.i else f'看 `s[{S.i}] = {S.s[S.i]}`'),
        'cur += 1': '当前组又多一个字符：`cur` → {cur}',
        'if i == n - 1': _if,
        'ans += min': _add,
        'pre = cur': '当前组变成下一轮的「上一组」：`pre = {pre}`',
        'cur = 0': '`cur = 0`，开始数下一组',
        'return ans': '合法子串一共 =={ans}== 个',
    },
    cards=dict(
        one_liner='按连续相同字符分组，相邻两组贡献 min(pre, cur) 个子串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计 01 串 `s` 中 ==0 和 1 个数相同且各自成组连续== 的子串个数（不同位置分别计数）',
                 '即形如 `0…01…1` 或 `1…10…0`，两段长度相等',
                 f'示例：`"00110011"` → `6`；本视频：`"{S0}"` → `5`'],
        quote='设当前这组的长度为 cur，上一组的长度为 pre，那么当前这组和上一组，能得到 min(pre,cur) 个合法子串，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法子串==只能横跨相邻的两组==：`00|111` 能得到 `0011`、`01`',
              '每组末尾（下一个字符不同或到结尾）结算一次 `min(pre, cur)`',
              '然后 `pre = cur`、`cur = 0`，滚动着只存两个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断组末尾：`i == n - 1 or s[i] != s[i + 1]`，==先判 `i == n - 1` 防止越界==',
                 '第一组时 `pre = 0`，`min` 自动为 0，不用特判',
                 '分组循环模板：双指针题单「六、分组循环」'],
    ),
)
