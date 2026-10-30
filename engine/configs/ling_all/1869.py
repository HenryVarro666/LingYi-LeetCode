def _top(S):
    if 'm1' not in S:
        return ''
    return f"最长连续 `1`：==`{S['m1']}`==　　最长连续 `0`：==`{S['m0']}`=="


def _col(S, i, v):
    if 'st' in S and 'i' in S and S['st'] <= i < S['i']:
        return 'green' if v == '1' else 'orange'
    return None


def _grp(S, B, r):
    if S.i == S.st:
        return f'`s[{S.st}] = {S.v!r}`，一组才刚开始'
    return f'这一组 `{S.v!r}` 占 `[{S.st}, {S.i})`，长度 `{S.i - S.st}`'


CONFIG = dict(
    num=1869, title='哪种连续子字符串更长', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环（Go 原文转写）',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1205'],
    code='''
class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        m1, m0 = 0, 0
        i, n = 0, len(s)
        while i < n:
            st = i
            v = s[st]
            while i < n and s[i] == v:
                i += 1
            if v == '1':
                m1 = max(m1, i - st)
            else:
                m0 = max(m0, i - st)
        return m1 > m0
''',
    call='Solution().checkZeroOnes("110100010")',
    expect=False,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（绿 = 当前这组的 1，橙 = 当前这组的 0）', cell=84,
             pointers={'st': 'blue', 'i': 'pink'}, color=_col),
        dict(type='text', fn=lambda S: (f"这一组：`{S['v']}` × {S['i'] - S['st']}" if 'v' in S and 'i' in S and S['i'] > S['st'] else ''), size=26),
    ],
    watch=[('i', 'i', 'pink'), ('st', 'st', 'blue'), ('v', 'v'), ('m1', 'm1', 'green'), ('m0', 'm0', 'orange')],
    captions={
        'm1, m0 = 0, 0': '`m1`、`m0` 分别记录最长的连续 `1`、连续 `0`；一个都没有就是 `0`',
        'i, n = 0, len(s)': '`i` 是外层循环的下标，每组结束后正好落在下一组开头，所以整体只扫一遍（==分组循环==）',
        'while i < n:': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有一组没处理' if S.i < S.n
                                        else f'`i = {S.i} == n`：所有组都处理完了'),
        'st = i': '新的一组从 `st = {st}` 开始',
        'v = s[st]': '这一组的字符是 `v = {v!r}`',
        'while i < n and s[i] == v': lambda S, B, r: (
            f'`s[{S.i}] = {S.s[S.i]!r}` == `v` → 还在同一组，继续往右' if S.i < S.n and S.s[S.i] == S.v
            else (f'`i = {S.i} == n`，走到末尾，这一组结束' if S.i >= S.n
                  else f'`s[{S.i}] = {S.s[S.i]!r}` ≠ `v = {S.v!r}` → 这一组到 `{S.i - 1}` 结束')),
        'i += 1': '`i` → `{i}`，同一个 `i` 继续往右',
        "if v == '1'": lambda S, B, r: (f'这一组是 `1`，长度 `{S.i - S.st}`，用它更新 `m1`' if S.v == '1'
                                       else f'这一组是 `0`，长度 `{S.i - S.st}`，用它更新 `m0`'),
        'm1 = max': '`m1 = max({B.m1}, {i - st}) = {m1}`',
        'm0 = max': '`m0 = max({B.m0}, {i - st}) = {m0}`',
        'return m1 > m0': '`m1 = {m1}`，`m0 = {m0}`：连续 1 ==必须严格更长==才算赢 → `{m1 > m0}`',
    },
    cards=dict(
        one_liner='把字符串切成一段段相同字符，分别记最长的 1 段和 0 段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，比较「最长连续 1」和「最长连续 0」',
                 '连续 1 ==严格更长==才返回 `true`，否则 `false`',
                 '示例：`"110100010"` → 1 最长 2，0 最长 3 → `false`'],
        quote='for i, n := 0, len(s); i < n; { st := i; v := s[st]; for ; i < n && s[i] == v; i++ {} ... }',
        quote_src='—— 灵茶山艾府题解（Go 代码，分组循环）',
        idea=['分组循环：外层循环找每一组的起点 `st`，内层循环把相同字符一口气走完',
              '内层停下时 `i` 已经是下一组的起点，所以外层不需要再写 `i++`',
              '一组结束就用 `i - st` 更新对应字符的最大长度'],
        result='1 的最长是 2，0 的最长是 3，`2 > 3` 不成立 → `false` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for ; cond; i++ {}` 写成 `while`）',
                 '时间 `O(n)`，空间 `O(1)`：内外层共用同一个 `i`，每个字符只扫一次',
                 '易错：结尾不需要特殊处理，内层循环走到 `n` 时最后一组自然被统计',
                 '`m1 > m0` 是严格大于，相等时返回 `false`',
                 '同类题：分组循环模板，参见 674、1446'],
    ),
)
