def _flushed(S):
    cur = S['f'][S['index']]
    return sum(int(cur[k]) for k in range(0, len(cur), 2))


def _pos(S):
    """正在读的字符 char 在上一项里的下标（None = 不在读）"""
    if 'index' not in S or 'cnt' not in S or 'char' not in S or S['index'] < 2:
        return None
    ln, fl = S['_line'], _flushed(S)
    if ln in (10, 11, 12):
        p = fl + S['cnt']
    elif ln in (13, 14):
        p = fl
    elif ln in (15, 17):
        p = fl + S['cnt'] - 1
    else:
        return None
    return p if p < len(S['f'][S['index'] - 1]) else None


def _prev_color(S, i, v):
    p = _pos(S)
    if p is None:
        return None
    if i == p:
        return 'yellow'
    fl = _flushed(S)
    if i < fl:
        return 'green'
    return 'blue' if i < p else None


def _desc(S):
    if 'index' not in S or S['index'] < 2:
        return '外观数列：每一项是「上一项怎么读出来」，`1` → `11`（一个 1）→ `21`（两个 1）…'
    prev = S['f'][S['index'] - 1]
    runs, k = [], 0
    while k < len(prev):
        j = k
        while j < len(prev) and prev[j] == prev[k]:
            j += 1
        runs.append(f'{j - k} 个 {prev[k]}')
        k = j
    return f"`{prev}` 读作：" + '，'.join(runs)


CONFIG = dict(
    num=38, title='外观数列', difficulty='Medium', category='字符串',
    author='yiduobo', technique='模拟 · 逐位计数',
    tags=[],
    code='''
class Solution(object):
    def countAndSay(self, n):

        f = ['', '1']

        for index in range(2, n + 1):
            now = None
            cnt = 0
            f.append('')
            for char in f[index - 1]:
                if now is None or now != char:
                    if cnt > 0:
                        f[index] += str(cnt) + now
                    now = char
                    cnt = 1
                else:
                    cnt += 1

            if cnt > 0:
                f[index] += str(cnt) + now
        return f[n]
''',
    call='Solution().countAndSay(5)',
    expect='111221',
    views=[
        dict(type='text', fn=_desc, size=30, h=80),
        dict(type='array', var='f[index - 1]', label='上一项 f[index-1]（黄 = 正在读的字符，蓝 = 当前这一段，绿 = 已写出）', h=200, cell=100,
             color=_prev_color),
        dict(type='array', var='f[index]', label='正在生成的 f[index]', h=200, cell=100,
             color=lambda S, i, v: 'green' if S['_line'] in (13, 20) and i >= len(S['f'][S['index']]) - 2 else None),
        dict(type='text', size=28, h=80, fn=lambda S: 'f = ' + '  →  '.join('`' + x + '`' for x in S['f'][1:])),
    ],
    watch=['index', ('now', 'now', 'blue'), ('cnt', 'cnt', 'orange'), ('char', 'char', 'yellow')],
    captions={
        'f = [': '`f[i]` 存第 `i` 项外观串，先放好 `f[1] = "1"`（`f[0]` 占位）',
        'for index in range(2, n + 1)': lambda S, B, r: (f'生成第 `{S.index}` 项：把上一项 `f[{S.index - 1}] = {S.f[S.index - 1]}` 读出来' if B.get('index') != S.index else f'`index` 已经到 `n = {S.n}`，每一项都生成完了'),
        'now = None': '`now` = 当前这一段的字符，`cnt` = 它连续出现了几次',
        'cnt = 0': '`cnt` 从 0 开始',
        'f.append': '给第 `{index}` 项先放一个空串，等下往里拼',
        'for char in f[index - 1]': lambda S, B, r: (f'读上一项的下一位：`char = {S.char}`' if _pos(S) is not None else '上一项读完了'),
        'if now is None or now != char': lambda S, B, r: ('`now` 还是空：这是第一位 → 成立，开一段新的' if B.now is None else (f'`{B.now}` != `{S.char}`：和上一位不同 → ==成立==，上一段到此结束' if B.now != S.char else f'`{B.now}` == `{S.char}`：和上一位相同 → 不成立，计数器加一')),
        12: lambda S, B, r: (f'`cnt = {S.cnt} > 0`：已有一段数完了 → 成立，先把它写进结果' if S.cnt > 0 else '`cnt = 0`：还没有上一段 → 不成立，不用写'),
        13: '写入「{cnt} 个 {now}」：追加 `{cnt}{now}`，`f[{index}] = {f[index]}`',
        'now = char': '开始数新的字符：`now = {char}`',
        'cnt = 1': '这个字符出现了 1 次：`cnt = 1`',
        'cnt += 1': '和上一位相同 → `cnt` 加一，现在 ==`{cnt}`==',
        19: lambda S, B, r: (f'读完了，但最后一段「{S.cnt} 个 {S.now}」还没写 → `cnt = {S.cnt} > 0`，补写' if S.cnt > 0 else '读完了，没有剩余的段'),
        20: '补写最后一段：追加 `{cnt}{now}` → `f[{index}] = {f[index]}`',
        'return f[n]': '第 `{n}` 项是 `{f[n]}`',
    },
    cards=dict(
        one_liner='读上一项，数连续相同的字符，写成「个数+字符」',
        complexity='时间 `O(总长度)`，空间 `O(总长度)`',
        problem=['外观数列：`1`、`11`、`21`、`1211`、`111221`……',
                 '每一项是对上一项的「报数」：`21` 读作「一个 2，一个 1」→ `1211`',
                 '本视频：`n = 5` → `"111221"`'],
        quote='每次遍历当前的串，然后判断这一位是否与上一位相同：与上一位相同，则计数器加一；与上一位不同，那么将计数器与上一位加入到新串，并重置计数器。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` 由 `f[index-1]` 生成，从 `f[1] = "1"` 一项项推',
              '用 `now` 记当前字符、`cnt` 记连续个数',
              '换字符时把 `cnt + now` 写进新串；循环结束后别忘了补写最后一段'],
        summary=['时间与空间都和各项长度之和成正比',
                 '循环结束后还要再判断一次 `cnt > 0`，补写最后一段',
                 '`now is None` 处理每项的第一个字符，`cnt > 0` 避免把空段写进去',
                 '作者自己也说可能有生成式解法，但这里老老实实模拟',
                 '原文已是 Python 3 可运行写法，未作改动'],
    ),
)
