N = 3
LOGS = ["0:start:0", "1:start:2", "2:start:3", "2:end:4", "1:end:5", "0:end:6"]
FCOL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _owners(logs):
    """每个时间单位属于哪个函数（end 的时刻也算它自己的一格）"""
    own, stack, prev = {}, [], 0
    for lg in logs:
        f, st, t = lg.split(':')
        f, t = int(f), int(t)
        if st == 'start':
            if stack:
                for u in range(prev, t):
                    own[u] = stack[-1]
            stack.append(f)
            prev = t
        else:
            for u in range(prev, t + 1):
                own[u] = stack[-1]
            stack.pop()
            prev = t + 1
    return own


OWN = _owners(LOGS)
TOTAL = max(OWN) + 1


def _finished(S, B):
    ln = S.get('_line')
    return ln == 27 or (ln == 8 and 'log' in B and B['log'] == S.get('log'))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    logs = S['logs']
    n = len(logs)
    cur = logs.index(S['log']) if 'log' in S else -1
    fin = _finished(S, B)
    cv.text((x0 + 18, y0 + 4), 'logs（蓝框 = 正在处理的日志）', 24, T['muted'], bold=True)
    cw = min(160, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cw * n) / 2
    ly, lh = y0 + 42, 54
    for i, lg in enumerate(logs):
        X = sx + i * cw
        fid, st, t = lg.split(':')
        active = i == cur and not fin
        done = i < cur or (i == cur and fin)
        cv.rect((X + 4, ly, X + cw - 4, ly + lh), fill=(40, 45, 53) if done else T['panel2'], r=8,
                outline=T['blue'] if active else T['border'], width=4 if active else 1)
        cv.text((X + cw / 2, ly + 18), lg, 22, T['dim'] if done else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cw / 2, ly + 40), f'函数 {fid} ' + ('开始' if st == 'start' else '结束'), 18,
                T['dim'] if done else T[FCOL[int(fid)]], anchor='mm', bold=True)
    # 时间轴
    cv.text((x0 + 18, y0 + 102), '时间轴（每格 = 1 个时间单位，颜色 = 谁在运行，黄框 = 刚结算的）', 22, T['muted'], bold=True)
    sw = min(120, (x1 - x0 - 60) / TOTAL)
    tx = x0 + 30 + ((x1 - x0 - 60) - sw * TOTAL) / 2
    ty, sh = y0 + 184, 54
    got = sum(S['res']) if 'res' in S else 0
    before = sum(B['res']) if 'res' in B else 0
    for t in range(TOTAL):
        X = tx + t * sw
        if t < got:
            cv.rect((X + 3, ty, X + sw - 3, ty + sh), fill=T[FCOL[OWN[t]]], r=8)
            cv.text((X + sw / 2, ty + sh / 2), f'f{OWN[t]}', 26, T['bg'], anchor='mm', bold=True)
        else:
            cv.rect((X + 3, ty, X + sw - 3, ty + sh), fill=T['panel2'], r=8, outline=T['border'])
        if before <= t < got:
            cv.rect((X, ty - 3, X + sw, ty + sh + 3), outline=T['yellow'], width=4, r=10)
        cv.text((X + sw / 2, ty + sh + 8), t, 20, T['dim'], anchor='mt', mono=True)
    if fin:
        return
    tm = S.get('time')
    if isinstance(tm, int) and 0 <= tm < TOTAL and S.get('_line', 0) >= 11:
        X = tx + tm * sw + sw / 2
        cv.tri_down(X, ty - 4, 9, T['orange'])
        cv.text((X, ty - 24), f'time={tm}', 20, T['orange'], anchor='mb', bold=True)
    lt = S.get('last_time')
    if isinstance(lt, int) and 0 <= lt < TOTAL:
        X = tx + lt * sw + sw / 2
        cv.tri_up(X, ty + sh + 40, 9, T['cyan'])
        cv.text((X, ty + sh + 54), f'last_time={lt}', 20, T['cyan'], anchor='mt', bold=True)


CONFIG = dict(
    num=636, title='函数的独占时间', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈模拟 · now + last_time 记账',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def exclusiveTime(self, n, logs):

        res = [0] * n
        stack = []
        now = None
        last_time = None
        for log in logs:
            fid, status, time = log.split(':')
            fid = int(fid)
            time = int(time)
            if status == 'start':
                if now is not None:
                    res[now] += time - last_time
                    stack.append(now)
                now = fid
                last_time = time
            else:
                res[now] += time - last_time + 1
                if stack:
                    now = stack.pop()
                    last_time = time + 1
                else:
                    now = None
                    last_time = None

        return res
''',
    call=f'Solution().exclusiveTime({N}, {LOGS})',
    expect=[3, 2, 2],
    skip=['fid = int(fid)', 'time = int(time)'],
    views=[
        dict(type='custom', draw=_draw, h=320),
        dict(type='stack', var='stack', label='stack（被打断、等着恢复的函数 id，栈顶在右）', h=100, font=28),
        dict(type='array', var='res', label='res（每个函数的独占时间）', cell=84, h=205,
             pointers={'now': 'blue'}, pointer_labels={'now': 'now'},
             color=lambda S, i, v: FCOL[i]),
    ],
    watch=[('now', 'now', 'blue'), ('last_time', 'last_time', 'cyan'), ('stack', 'stack', 'purple'), ('res', 'res', 'green')],
    max_steps=90,
    captions={
        'res = [0] * n': '`res[i]` 是函数 `i` 的独占时间，先都是 0',
        'stack = []': '栈：存放被打断、等着恢复运行的函数',
        6: '`now`：当前正在运行的函数，开始时没有',
        7: '`last_time`：`now` 这一段从哪个时刻开始算，开始时为空',
        'for log in logs': lambda S, B, r: (
            '日志都处理完了，结束循环' if ('log' in B and B.log == S.log)
            else f'读第 `{S.logs.index(S.log)}` 条日志 `{S.log}`'),
        'fid, status, time = log.split': '按 `:` 拆开：函数 `{fid}`，状态 `{status}`，时刻 `{time}`',
        'if status ==': lambda S, B, r: (
            f'`{S.status}`：函数 `{S.fid}` ==开始运行==，它会打断当前正在跑的函数'
            if S.status == 'start' else f'`{S.status}`：函数 `{S.fid}` ==运行结束=='),
        'if now is not None': lambda S, B, r: (
            f'`now = {S.now}` 还在运行 → 它被打断了，要先结算它这一段'
            if S.now is not None else '现在没有函数在运行，没有要结算的'),
        14: '结算被打断的函数 `{now}`：`{time} - {last_time}` = {time - last_time}（新函数开始的这一刻不算它）→ `res[{now}] = {res[now]}`',
        15: '被打断的函数 `{now}` 入栈，等新函数结束后再回来：`stack = {stack}`',
        'now = fid': '`now = {fid}`：新函数开始运行',
        17: '`last_time = {time}`：从时刻 `{time}` 起给函数 `{now}` 计时',
        19: '函数 `{now}` 在 `{time}` 结束，这一刻也算它的：`{time} - {last_time} + 1` = {time - last_time + 1} → `res[{now}] = {res[now]}`',
        'if stack': lambda S, B, r: (
            f'栈里有 `{S.stack}`：刚结束的函数是被栈顶那个调用的，要回去接着跑'
            if S.stack else '栈是空的：没有函数再运行了'),
        'now = stack.pop()': '回到栈顶函数 `now = {now}`',
        22: '它从 `{time} + 1 = {last_time}` 重新计时（`{time}` 这一刻已经算给了刚结束的函数）',
        24: '没有函数在运行了：`now = None`',
        25: '计时起点也清空：`last_time = None`',
        'return res': '每个函数的独占时间 =={ret}==，总和 `{sum(ret)}` 正好是整个运行时间',
    },
    cards=dict(
        one_liner='用栈模拟调用：每遇到一条日志，就把这一段时间记给正在运行的函数',
        complexity='时间 `O(m)`（`m` 是日志条数），空间 `O(n)`',
        problem=['单线程 CPU 上运行 `n` 个函数，日志 `"id:start:time"` / `"id:end:time"`',
                 '函数可以调用别的函数；`start` 在该时刻开头，`end` 在该时刻结尾',
                 '独占时间 = 函数自己运行的时间，不含被它调用的函数',
                 '本视频：`n = 3`，6 条日志 → `[3, 2, 2]`'],
        quote='使用两个变量now和last_time分别记录当前正在运行函数的fid以及起始运行时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到 `start`：若有函数在跑，先把它到现在的时间记给它，再把它压栈，`now` 换成新函数',
              '遇到 `end`：`now` 的这一段时间（含 `end` 这一刻，所以 `+1`）记给它',
              '栈不空就回到栈顶函数，起点设成 `time + 1`；栈空则 `now`、`last_time` 都置空'],
        result='返回 `[3, 2, 2]`，总和 `7` = 时刻 `0` 到 `6` 共 7 个单位 ✓',
        summary=['时间 `O(m)`，空间 `O(n)`；`start` 用 `time - last_time`，`end` 用 `time - last_time + 1`',
                 '易错：`end` 的那一刻也属于结束的函数，所以恢复函数的起点是 `time + 1`',
                 '易错：被打断的函数要在 `start` 时就结算，不是等它恢复后再算',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动'],
    ),
)
