def _score(ev):
    sc = ct = 0
    for e in ev:
        if e == 'W':
            ct += 1
        elif len(e) > 1:
            sc += 1
        else:
            sc += int(e)
        if ct == 10:
            break
    return sc, ct


def _cur(S, pre_lines):
    """当前正在处理的事件下标（回放前缀，按 score/counter 反推已处理个数）"""
    ev = S['events']
    if 'score' not in S or '_line' not in S:
        return None
    k = 0
    for j in range(len(ev) + 1):
        if _score(ev[:j]) == (S['score'], S['counter']):
            k = j
            break
    return k if S['_line'] in pre_lines else k - 1


CONFIG = dict(
    num=3921, title='分数验证器', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='按题意模拟 · 满 10 个 W 提前停',
    code='''
class Solution:
    def scoreValidator(self, events: list[str]) -> list[int]:
        score = counter = 0

        for s in events:
            if s == "W":
                counter += 1
                if counter == 10:
                    break
            elif len(s) > 1:  # "WD" "NB"
                score += 1
            else:  # 数字
                score += int(s)

        return [score, counter]
''',
    call='Solution().scoreValidator(["4","W","W","W","W","W","W","W","W","W","W","6"])',
    expect=[4, 10],
    views=[
        dict(type='array', var='events', label='events（蓝 = 正在处理，绿 = 已处理，灰 = 还没轮到 / 被忽略）', h=230, cell=70,
             color=lambda S, i, v: None if _cur(S, (5, 6, 10)) is None or S['_line'] == 15 else ('blue' if i == _cur(S, (5, 6, 10)) else 'green' if i < _cur(S, (5, 6, 10)) else None),
             dim=lambda S, i, v: _cur(S, (5, 6, 10)) is not None and S['_line'] != 15 and i > _cur(S, (5, 6, 10))),
        dict(type='text', size=34, fn=lambda S: f"score = =={S['score']}==　　counter = =={S['counter']}== / 10" if 'score' in S else ''),
    ],
    watch=['s', ('score', 'score', 'green'), ('counter', 'counter', 'pink')],
    captions={
        'score = counter = 0': '`score` 和 `counter` 都从 0 开始',
        'for s in events': '处理事件 `"{s}"`',
        'if s == "W"': lambda S, B, r: (f'`"{S.s}" == "W"` → 是 ==W==，只加计数器、不加分' if S.s == 'W' else f'`"{S.s}"` 不是 W → 看看是不是 WD/NB'),
        'counter += 1': '`counter` → =={counter}==',
        'if counter == 10': lambda S, B, r: (f'`counter = 10`：达到上限 → ==停止处理==，后面的事件忽略' if S.counter == 10 else f'`counter = {S.counter}`，还没到 10，继续'),
        'break': '计数器满 10，`break` 退出：剩下的事件不再处理',
        'elif len(s) > 1': lambda S, B, r: (f'`"{S.s}"` 长度 > 1 → 是 WD / NB，加 1 分' if len(S.s) > 1 else f'`"{S.s}"` 长度为 1 → 是数字'),
        'score += 1': '`WD` / `NB` 各加 1 分：`score` → =={score}==',
        'score += int(s)': '数字事件：加 `{s}` 分，`score` → =={score}==',
        'return': '返回 `[score, counter]` = `{ret}`',
    },
    cards=dict(
        one_liner='按题意模拟，W 满 10 个就 break',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`events` 里的事件：数字加分，`"W"` 计数器加 1，`"WD"`/`"NB"` 加 1 分',
                 '从左到右处理，处理完或计数器变成 10 就停',
                 '返回 `[score, counter]`',
                 '本视频：`4` 后面跟 10 个 `"W"`，再接 `"6"` → `[4, 10]`'],
        quote='按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`"W"`：`counter += 1`，等于 10 立刻 `break`',
              '长度大于 1 的只可能是 `"WD"`、`"NB"`，各加 1 分',
              '其余就是单个数字，`int(s)` 后加分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`"W"` 要先判断，因为它长度也是 1，不能当成数字去 `int`',
                 '易错：`counter == 10` 要在加一之后立刻检查，`break` 后面的事件一律不算'],
    ),
)
