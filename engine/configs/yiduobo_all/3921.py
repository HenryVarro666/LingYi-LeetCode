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
    author='yiduobo', technique='一趟遍历模拟 · 计数器满 10 退出',
    code='''
class Solution(object):
    def scoreValidator(self, events):
        
        score = 0
        counter = 0
        for e in events:
            if e == 'W':
                counter += 1
                if counter == 10:
                    break
            elif e == 'WD' or e == 'NB':
                score += 1
            else:
                score += int(e)
        
        return [score, counter]
''',
    call='Solution().scoreValidator(["1","4","W","6","WD","NB"])',
    expect=[13, 1],
    views=[
        dict(type='array', var='events', label='events（蓝 = 正在处理，绿 = 已处理，灰 = 还没轮到）', h=230, cell=80,
             color=lambda S, i, v: None if _cur(S, (6, 7, 11)) is None or S['_line'] == 16 else ('blue' if i == _cur(S, (6, 7, 11)) else 'green' if i < _cur(S, (6, 7, 11)) else None),
             dim=lambda S, i, v: _cur(S, (6, 7, 11)) is not None and S['_line'] != 16 and i > _cur(S, (6, 7, 11))),
        dict(type='text', size=34, fn=lambda S: f"score = =={S['score']}==　　counter = =={S['counter']}==" if 'score' in S and 'counter' in S else ''),
    ],
    watch=['e', ('score', 'score', 'green'), ('counter', 'counter', 'pink')],
    skip=['score = 0', 'counter = 0'],
    captions={
        'for e in events': '轮到事件 `"{e}"`',
        "if e == 'W'": lambda S, B, r: (f'`"{S.e}"` 是 W → 只动计数器，不加分' if S.e == 'W' else f'`"{S.e}"` 不是 W，继续往下判断'),
        'counter += 1': '计数器加 1：`counter` → =={counter}==',
        'if counter == 10': lambda S, B, r: ('`counter = 10`：达到 10 → ==退出循环==' if S.counter == 10 else f'`counter = {S.counter}` 还没到 10，继续处理'),
        'break': '计数器已满，`break`：后面的事件不再处理',
        "elif e == 'WD'": lambda S, B, r: (f'`"{S.e}"` 是 WD / NB → 加 1 分' if S.e in ('WD', 'NB') else f'`"{S.e}"` 不是 WD / NB → 一定是数字'),
        'score += 1': '`WD` / `NB` 加 1 分：`score` → =={score}==',
        'score += int(e)': '数字事件：`int("{e}")` 分加进去，`score` → =={score}==',
        'return': '返回 `[score, counter]` = `{ret}`',
    },
    cards=dict(
        one_liner='遍历一趟，按事件类型改 score 或 counter',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`events` 中：数字加到总得分，`W` 让计数器加 1，`WD` / `NB` 总得分加 1',
                 '从左到右处理，直到处理完，或计数器变为 10',
                 '返回 `[score, counter]`',
                 '本视频：`["1","4","W","6","WD","NB"]` → `[13, 1]`'],
        quote='按照题目要求对events进行一趟遍历，根据具体的元素更新score或者counter即可。注意counter变为10时应该退出遍历的循环。',
        quote_src='—— yiduobo 题解原文',
        idea=['`score` 和 `counter` 初始都是 0',
              '`W` 加计数器，`WD` / `NB` 加 1 分，其余是数字',
              '`counter` 一到 10 就 `break`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`W` 要先判断，别把它拿去 `int()`',
                 '易错：`counter == 10` 放在加一之后检查',
                 '对比灵神：灵神用 `len(s) > 1` 识别 WD / NB，这里直接比较两个字符串'],
    ),
)
