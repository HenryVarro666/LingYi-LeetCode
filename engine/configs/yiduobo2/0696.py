S0 = '1100011'


def _start(s, i):
    """s[i] 所在这一段的起点"""
    while i > 0 and s[i - 1] == s[i]:
        i -= 1
    return i


def _live(S):
    return 'pos' in S and 'last_pos' in S and 'res' in S


def _cur_end(S):
    """当前段已确认的右端（不含）：在内层 while 里时就是 pos"""
    return min(S['pos'], len(S['s']))


def _color(S, i, v):
    if not _live(S):
        return None
    lp, s = S['last_pos'], S['s']
    if lp < len(s) and lp <= i < _cur_end(S):
        return 'blue'                       # 当前这一段
    if lp > 0:
        ps = _start(s, lp - 1)
        if ps <= i < lp:
            return 'pink'                   # 上一段
    return None


def _dim(S, i, v):
    if not _live(S):
        return False
    lp, s = S['last_pos'], S['s']
    ps = _start(s, lp - 1) if lp > 0 else 0
    return i < ps or i >= max(_cur_end(S), lp)


def _info(S):
    if not _live(S):
        return '粉 = 上一段，蓝 = 当前这一段 `[last_pos, pos)`'
    if S.get('_line') == 12:
        s, lp, pos = S['s'], S['last_pos'], S['pos']
        m, k = S['res'] - 0, pos - lp
        last = (lp - _start(s, lp - 1)) if lp > 0 else 0
        g = min(last, k)
        if g == 0:
            return '前面没有上一段，交界处扩展不出子串'
        subs = [s[lp - 1] * j + s[lp] * j for j in range(1, g + 1)]
        return '从交界处往外扩展：' + '、'.join(f'`{t}`' for t in subs) + f'　共 =={g}== 个'
    return f'上一段长 `last_len = {S["last_len"]}`；当前段 `[{S["last_pos"]}, {S["pos"]})`；`res = {S["res"]}`'


def _inner(S, B, r):
    s, pos, lp = S.s, S.pos, S.last_pos
    if pos < len(s) and s[pos] == s[lp]:
        return f'`s[{pos}] = {s[pos]}` 和段首 `s[{lp}]` 相同 → 这一段还没完'
    if pos >= len(s):
        return f'`pos = {pos} = n`：到字符串末尾，这一段长 `{pos - lp}`'
    return f'`s[{pos}] = {s[pos]}` ≠ `{s[lp]}` → 这一段结束，长 `pos − last_pos = {pos - lp}`'


def _add(S, B, r):
    m, k = B.last_len, S.pos - S.last_pos
    if m == 0:
        return f'第一段之前没有别的段：`min(0, {k}) = 0`'
    return f'上一段 `{m}` 个、这一段 `{k}` 个 → 扩展到较短的一边为止，得 `min({m}, {k})` = =={min(m, k)}== 个，`res` → {S.res}'


CONFIG = dict(
    num=696, title='计数二进制子串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='交替统计连续段 · 交界处向外扩展',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def countBinarySubstrings(self, s):
        last_len = 0
        last_pos = 0
        n = len(s)
        res = 0

        while last_pos < n:
            pos = last_pos + 1
            while pos < n and s[pos] == s[last_pos]:
                pos += 1
            res += min(last_len, pos - last_pos)
            last_len = pos - last_pos
            last_pos = pos

        return res
''',
    call=f'Solution().countBinarySubstrings({S0!r})',
    expect=4,
    views=[
        dict(type='text', fn=_info, size=28, h=90),
        dict(type='string', var='s', label='s（粉 = 上一段，蓝 = 当前段）', cell=100, h=300,
             pointers={'last_pos': 'pink', 'pos': 'blue'}, color=_color, dim=_dim),
    ],
    watch=[('last_pos', 'last_pos', 'pink'), ('pos', 'pos', 'blue'), ('last_len', 'last_len', 'orange'),
           ('res', 'res', 'green')],
    captions={
        'last_len = 0': '`last_len`：上一段连续相同字符的长度',
        'last_pos = 0': '`last_pos`：当前这一段的起点',
        'res = 0': '`res` 累加答案',
        'while last_pos < n': lambda S, B, r: (f'从 `last_pos = {S.last_pos}` 开始统计新的一段（字符 `{S.s[S.last_pos]}`）'
                                               if S.last_pos < S.n else '`last_pos = n`：所有段都统计完了'),
        'pos = last_pos + 1': '`pos` 从 `{pos}` 开始往后找这一段的末尾',
        'while pos < n and': _inner,
        'pos += 1': '`pos` → {pos}',
        'res += min': _add,
        'last_len = pos - last_pos': '这一段成为下一轮的「上一段」：`last_len = {last_len}`',
        'last_pos = pos': '下一段从 `last_pos = {last_pos}` 开始',
        'return res': '符合条件的子串一共 =={res}== 个',
    },
    cards=dict(
        one_liner='m 个 1 接 n 个 0，从交界处往外扩展，能得到 min(m, n) 个子串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计 01 串 `s` 中 ==0 和 1 个数相同且各自挨在一起== 的子串个数（不同位置分别计数）',
                 '即形如 `1…10…0` 或 `0…01…1`，两段长度相等',
                 f'示例：`"00110011"` → `6`；本视频：`"{S0}"` → `4`'],
        quote='假设现在有m个连续的1和n个连续的0组成的字符串，那么我们从1和0的交界处开始往外扩展，就可以得到10、1100、111000、...，因此我们可以从中得到min(m, n)个符合条件的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['`11|000`：从交界处往外扩，`10`、`1100` 都合法，扩到短的一边用完为止',
              '所以相邻两段贡献 ==min(m, n)== 个子串',
              '从头扫描，交替统计每一段的长度，和上一段取 min 累加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '内层 `while` 找段尾，`pos − last_pos` 就是段长；==`pos < n` 要写在前面防越界==',
                 '`last_len` 初始为 0，第一段自然贡献 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神 for 循环里逐字符 `cur += 1`，遇组末尾结算；这里用双指针整段跳'],
    ),
)
