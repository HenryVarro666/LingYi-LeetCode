def _idx(S):
    cmd, logs = S.get('cmd'), S.get('logs')
    if cmd is None or not logs:
        return None
    ids = [id(x) for x in logs]
    return ids.index(id(cmd)) if id(cmd) in ids else None


def _top(S):
    if 'now' not in S:
        return ''
    return '当前深度 `now = %d`：' % S['now'] + ('在主文件夹（根目录）' if S['now'] == 0 else '主文件夹' + '/子' * S['now'])


def _color(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    return None


CONFIG = dict(
    num=1598, title='文件夹操作日志搜集器', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='括号匹配 · 只记深度',
    tags=[],
    setup='''
class Log(str):
    pass
logs = [Log(x) for x in ["d1/", "../", "../", "d2/", "./", "d3/"]]
''',
    code='''
class Solution(object):
    def minOperations(self, logs):

        now = 0
        for cmd in logs:
            if cmd == './':
                continue
            elif cmd == '../':
                now -= 1
                if now < 0:
                    now = 0
            else:
                now += 1
        
        return now
''',
    call='Solution().minOperations(logs)',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var='logs', label='logs（蓝 = 当前操作）', cell=130,
             color=_color),
        dict(type='text', fn=lambda S: ('`now` 就是括号匹配里「还没闭合的左括号数」' if 'now' in S else ''), size=24),
    ],
    watch=[('now', 'now', 'green'), ('cmd', 'cmd', 'blue')],
    captions={
        'for cmd in logs': "取出下一个操作 `cmd = '{cmd}'`",
        "if cmd == './'": lambda S, B, ret: ("`./`：留在当前文件夹，深度不变 → `continue`" if S.cmd == './'
                                             else f"`'{S.cmd}' ≠ './'`，不是原地不动，继续判断"),
        "elif cmd == '../'": lambda S, B, ret: ("`../`：回到父文件夹，相当于一个==右括号==" if S.cmd == '../'
                                                else "不是 `../`，那就是进入子文件夹，相当于一个==左括号=="),
        'now -= 1': '返回上一级：`now` → {now}',
        'if now < 0': lambda S, B, ret: (f'`now = {S.now} < 0`：已经在主文件夹还要 `../`，==仍停在主文件夹==' if S.now < 0
                                         else f'`now = {S.now} >= 0`：没有越过根目录，不用修正'),
        'now = 0': lambda S, B, ret: ('`now` = 当前所在目录的深度，主文件夹为 `0`' if S['_line'] < 6 else '括号数不能为负 → 重置 `now = 0`'),
        'now += 1': '进入子文件夹 `{cmd}`：`now` → =={now}==',
        'return now': '要回到主文件夹，只需 `../` ==`{now}`== 次',
    },
    cards=dict(
        one_liner='进入子文件夹 = 左括号，../ = 右括号，数剩余的左括号',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['文件系统从主文件夹开始，`logs` 记录每次操作：`"d/"` 进入子文件夹，`"../"` 回到父文件夹，`"./"` 留在原地',
                 '在主文件夹执行 `"../"` 仍停在主文件夹',
                 '求回到主文件夹的==最少操作次数==（本视频：`["d1/","../","../","d2/","./","d3/"]` → `2`）'],
        quote='题目看上去描述还蛮复杂的，但是仔细观察可以发现完全就是一个括号匹配问题。向下就相当于添加了一个左括号，而向上则相当于添加了一个右括号。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描，只维护深度 `now`：进入 `+1`，`../` 则 `-1`，`./` 跳过',
              '最终剩下的「左括号数」就是回到主文件夹要走的 `../` 次数',
              '根目录再向上不会变成负数：`now < 0` 时重置为 `0`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：在主文件夹时 `../` 无效，必须把 `now` 重置为 `0`（本例第 3 个操作）',
                 '`./` 不改变深度，别当成进入子文件夹',
                 '本质是括号匹配，不用真的建栈'],
    ),
)
