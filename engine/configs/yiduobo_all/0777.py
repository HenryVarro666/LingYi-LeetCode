def _forc(S, g, name):
    c = S.get('char')
    if c is None:
        return f'{name}，按 `L/R` 切段'
    if c != 'X' and S.get('cnt') == 0 and S.get(g) and S[g][-1] == c:
        return f'{name}：所有字符都扫完了'
    return f'{name}：下一个字符 `{c}`'


def _info(S):
    if 's_gate' not in S or 'e_gate' not in S:
        return '把每个 `L`/`R` 当作「门」，数门与门之间的 `X`'
    if 'index' not in S:
        return f"start 的门 `{''.join(S['s_gate'])}`　end 的门 `{''.join(S['e_gate'])}`"
    return ''


CONFIG = dict(
    num=777, title='在 LR 字符串中交换相邻字符', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按 L/R 分段 · 逐段搬运 X',
    tags=['灵神题单', '难度分 2337'],
    code='''
class Solution(object):
    def canTransform(self, start, end):

        cnt = 0
        s_cnt = []
        s_gate = []
        for char in start:
            if char == 'X':
                cnt += 1
            else:
                s_cnt.append(cnt)
                cnt = 0
                s_gate.append(char)
        s_cnt.append(cnt)

        cnt = 0
        e_cnt = []
        e_gate = []
        for char in end:
            if char == 'X':
                cnt += 1
            else:
                e_cnt.append(cnt)
                cnt = 0
                e_gate.append(char)
        e_cnt.append(cnt)

        if s_gate != e_gate:
            return False

        for index in range(len(s_gate)):
            if s_cnt[index] < e_cnt[index]:
                if s_gate[index] == 'R':
                    s_cnt[index + 1] -= (e_cnt[index] - s_cnt[index])
                else:
                    return False
            elif s_cnt[index] > e_cnt[index]:
                if s_gate[index] == 'L':
                    s_cnt[index + 1] += (s_cnt[index] - e_cnt[index])
                else:
                    return False
        
        return True
''',
    call='Solution().canTransform("RXXLXR", "XRLXXR")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='string', var='start', label='start', h=105, index=False,
             color=lambda S, i, v: None if v == 'X' else ('cyan' if v == 'L' else 'orange')),
        dict(type='string', var='end', label='end', h=105, index=False,
             color=lambda S, i, v: None if v == 'X' else ('cyan' if v == 'L' else 'orange')),
        dict(type='array', var='s_cnt', label='s_cnt', pointers={'index': 'blue'}, h=190),
        dict(type='array', var='e_cnt', label='e_cnt', pointers={'index': 'pink'}, h=190),
    ],
    watch=[('index', 'index', 'yellow'), 's_gate', 'e_gate'],
    skip=['cnt = 0', 's_gate.append', 'e_gate.append', 'cnt += 1', 'cnt = 0'],
    captions={
        'cnt = 0': '`cnt` 统计相邻两个 `L/R` 之间的 `X` 个数',
        'for char in start': lambda S, B, r: _forc(S, 's_gate', '扫 start'),
        'for char in end': lambda S, B, r: _forc(S, 'e_gate', '扫 end'),
        "if char == 'X'": lambda S, B, r: (f"`{S.char}` 是 X → 当前段多一个 X（`cnt = {S.cnt + 1}`）" if S.char == 'X' else f"`{S.char}` 是门 → 前面这一段 X 的个数收工"),
        's_cnt.append(cnt)': lambda S, B, r: (f"记录这一段有 `{S.s_cnt[-1]}` 个 X，`s_cnt = {S.s_cnt}`；门 `{S.char}` 另存"
                                            if S.get('char') and S.get('_line') == 11 else f"最后一段（末尾）有 `{S.s_cnt[-1]}` 个 X → `s_cnt = {S.s_cnt}`"),
        'e_cnt.append(cnt)': lambda S, B, r: (f"记录这一段有 `{S.e_cnt[-1]}` 个 X，`e_cnt = {S.e_cnt}`"
                                            if S.get('_line') == 23 else f"最后一段有 `{S.e_cnt[-1]}` 个 X → `e_cnt = {S.e_cnt}`"),
        'if s_gate != e_gate': lambda S, B, r: (f"start 的门 `{''.join(S.s_gate)}`，end 的门 `{''.join(S.e_gate)}` → ==一致==，L/R 顺序不能变" if S.s_gate == S.e_gate else f"门不一致 → 不可能 → ==False=="),
        'for index in range': lambda S, B, r: ('逐段对齐 X 的个数' if B.get('index') is None else ('每一段都处理完了' if B.get('index') == S.index else f"逐段对齐：第 `{S.index}` 段，两边 X 的数量要靠搬运变一致")),
        'if s_cnt[index] < e_cnt[index]': lambda S, B, r: (f"第 {S.index} 段：start 有 {S.s_cnt[S.index]} 个，end 要 {S.e_cnt[S.index]} 个 → ==少了==，得从下一段借" if S.s_cnt[S.index] < S.e_cnt[S.index] else f"start {S.s_cnt[S.index]} ≥ end {S.e_cnt[S.index]}，不缺 X"),
        "if s_gate[index] == 'R'": lambda S, B, r: (f"门是 `{S.s_gate[S.index]}`：" + ("`R` 往右走，把后面的 X 换到前面 → 能借" if S.s_gate[S.index] == 'R' else "`L` 在左边，没法把右边的 X 拿过来 → False")),
        's_cnt[index + 1] -=': '从下一段拿走 `{B.s_cnt[index + 1] - s_cnt[index + 1]}` 个 X：`s_cnt = {s_cnt}`',
        'elif s_cnt[index] > e_cnt[index]': lambda S, B, r: (f"第 {S.index} 段：start {S.s_cnt[S.index]} 个 > end {S.e_cnt[S.index]} 个 → ==多了==，要送给下一段" if S.s_cnt[S.index] > S.e_cnt[S.index] else "这一段个数已经相等，不用动"),
        "if s_gate[index] == 'L'": lambda S, B, r: (f"门是 `{S.s_gate[S.index]}`：" + ("`L` 往左走，X 被挤到右边 → 能送" if S.s_gate[S.index] == 'L' else "`R` 不能让 X 往右去 → False")),
        's_cnt[index + 1] +=': '多出的 X 送到下一段：`s_cnt = {s_cnt}`',
        'return True': '前面每段都配平，最后一段自动相等 → ==True==',
    },
    cards=dict(
        one_liner='把 L/R 当门，门之间的 X 个数逐段搬运配平',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `XL` 换成 `LX`，或把 `RX` 换成 `XR`',
                 '问 `start` 能否变成 `end`',
                 '本视频：`RXXLXR` → `XRLXXR` 返回 `true`'],
        quote='L和R是不能进行交换的，因此如果单独把start和end中L和R扣出来，那么这个序列是不能动的……以每个L或R作为gate，统计gate之间的X个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 个门把 X 分成 `k+1` 段，每段可以是 0 个',
              '门序列必须一致，否则直接 False',
              '少 X 时只能向 `R` 右边借；多 X 时只能让 `L` 送走'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`R` 往右走，X 被换到它左边（从后一段借）；`L` 往左走，X 被换到右边（送给后一段）',
                 '最后一段不用比：总长和门都一致，前面配平后它必然相等',
                 '对比灵神：灵神直接用 i/j 双指针比位置，yiduobo 先转成每段 X 个数再搬运',
                 '原文为 Python 2 风格（`class Solution(object)`），无需修改即可运行'],
    ),
)
