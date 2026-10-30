SEATS = [['.', '#'], ['.', '.'], ['.', '#']]
NC = len(SEATS[0])


def b(x):
    return format(x, f'0{NC}b')


def _lv(S):
    return S.get('level')


def _cell(S, i, j, v):
    lv = _lv(S)
    if lv is None:
        return None
    ns, ls, p = S.get('now_state'), S.get('last_state', S.get('state')), S.get('p')
    if i == lv:
        if ns is not None and (ns >> j) & 1:
            return 'pink'
        if p is not None and j == p and S.get('_line', 0) >= 17 and 'now_state' in S:
            return 'yellow'
        if v == '.':
            return 'cyan'
    if i == lv - 1 and ls is not None and (ls >> j) & 1:
        return 'blue'
    return None


def _fmt(d):
    return '  '.join(f"{b(k)}:{'-' if x is None else x}" for k, x in enumerate(d))


def _txt(S):
    g, f = S.get('g'), S.get('f')
    parts = []
    if g is not None:
        parts.append(f'`g` = {_fmt(g)}（上一排的 `最后一排状态:最多人数`）')
    return '　'.join(parts)


def _txt2(S):
    f = S.get('f')
    if f is None:
        return ''
    if 'now_state' in S and 'f' in S:
        return f'`f` = {_fmt(f)}（这一排）'
    return f'`f` = {_fmt(f)}（这一排）'


CONFIG = dict(
    num=1349, title='参加考试的最大学生数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 回溯逐位生成下一行状态',
    tags=['图论算法', '难度分 2386'],
    code='''
class Solution(object):
    def maxStudents(self, seats):
        m = len(seats)
        n = len(seats[0])
        g = [None] * (1 << n)
        g[0] = 0
        for level in range(m):
            f = [None] * (1 << n)
            for state in range(1 << n):
                if g[state] is not None:
                    self.dfs(0, n, 0, 0, state, g[state], f, seats[level])

            g = f[:]

        return max(x for x in g if x is not None)

    def dfs(self, p, n, now_state, now_v, last_state, last_v, f, seats):
        if p == n:
            if f[now_state] is None or f[now_state] < now_v + last_v:
                f[now_state] = now_v + last_v
            return

        self.dfs(p + 1, n, now_state, now_v, last_state, last_v, f, seats)
        if seats[p] == '.':
            if p > 0 and (last_state & (1 << (p - 1))):
                return
            if p < n - 1 and (last_state & (1 << (p + 1))):
                return
            if p > 0 and (now_state & (1 << (p - 1))):
                return
            self.dfs(p + 1, n, now_state | (1 << p), now_v + 1, last_state, last_v, f, seats)
''',
    call=f'Solution().maxStudents({SEATS!r})',
    expect=3,
    max_steps=70,
    skip=['g[0] = 0', 'g = f[:]', 'f = [None]'],
    views=[
        dict(type='grid', var=lambda S: SEATS, label='seats（青 = 本排，粉 = 本排已坐，蓝 = 上排已坐，黄 = 位置 p）', h=200, cell=64, color=_cell),
        dict(type='text', fn=_txt, size=21, h=48),
        dict(type='text', fn=_txt2, size=21, h=48),
        dict(type='calls', h=250, hide=('n', 'f', 'seats', 'last_v')),
    ],
    watch=[('level', 'level', 'blue'), ('p', 'p', 'yellow'), ('now_v', 'now_v', 'green')],
    captions={
        'm = len': '`m` 排',
        'n = len': '每排 `n = {n}` 把椅子，状态用 `n` 位二进制表示，一共 `2^n = {1 << n}` 种',
        'g = [None]': '`g[state]`：上一排坐法为 `state` 时前面最多的学生数，`None` 表示不可能；开始时只有「没人」`g[0] = 0`',
        'for level in range(m)': lambda S, B, r: (f'开始处理第 `{S.level}` 排：用 `g`（上一排）推出 `f`（这一排）' if 'level' in S and S.get('level') != B.get('level') else '所有排处理完'),
        'for state in range(1 << n)': lambda S, B, r: ('上一排的坐法都枚举完了：`f` 成为新的 `g`' if (B.get('state') == S.get('state') and S.get('state') == (1 << S.n) - 1) else f'枚举上一排的坐法 `state = {b(S.state)}`'),
        'if g[state] is not None': lambda S, B, r: (f'`g[{b(S.state)}] = {S.g[S.state]}`：这种坐法可达 → 在它基础上安排这一排' if S.g[S.state] is not None else f'`g[{b(S.state)}]` 是 None：不可能出现 → 跳过'),
        'self.dfs(0, n': '回溯：从左到右逐个位置决定「坐 / 不坐」，生成这一排所有合法坐法 `now_state`',
        'return max': '最后一排所有坐法里最大的学生数 =={ret}==',
        'if p == n': lambda S, B, r: (f'`p = {S.p} = n`：这一排决定完了，坐法 `{b(S.now_state)}`，学生数 `{S.now_v}`' if S.p == S.n else f'`p = {S.p}`：还没决定完，处理第 `{S.p}` 把椅子'),
        'if f[now_state] is None': '`f[{now_state:0{n}b}]` 取较大者：旧值 vs `now_v + last_v = {now_v + last_v}`',
        'f[now_state] = ': '`f[{now_state:0{n}b}] = {now_v + last_v}`',
        'self.dfs(p + 1, n, now_state, now_v': '先试「第 {B.p} 把椅子不坐」：状态不变，处理下一把',
        "if seats[p] == '.'": lambda S, B, r: (f'第 `{S.p}` 把椅子是好的 → 才有可能坐人' if S.seats[S.p] == '.' else f'第 `{S.p}` 把椅子是坏的 `#` → 不能坐'),
        'if p > 0 and (last_state': lambda S, B, r: ('`p = 0` 没有左上 → 不冲突' if S.p == 0 else (f'上一排第 `{S.p - 1}` 位（左上）有人 → ==冲突==，不能坐' if (S.last_state >> (S.p - 1)) & 1 else f'上一排第 `{S.p - 1}` 位（左上）没人 → 不冲突')),
        'if p < n - 1 and (last_state': lambda S, B, r: ('已是最右一把，没有右上 → 不冲突' if S.p >= S.n - 1 else (f'上一排第 `{S.p + 1}` 位（右上）有人 → ==冲突==，不能坐' if (S.last_state >> (S.p + 1)) & 1 else f'上一排第 `{S.p + 1}` 位（右上）没人 → 不冲突')),
        'if p > 0 and (now_state': lambda S, B, r: ('`p = 0` 左边没有椅子 → 不冲突' if S.p == 0 else (f'这一排第 `{S.p - 1}` 位（左边紧邻）有人 → ==冲突==，不能坐' if (S.now_state >> (S.p - 1)) & 1 else f'这一排第 `{S.p - 1}` 位（左边紧邻）没人 → 不冲突')),
        21: '这一排的这种坐法记录完了，返回上一层继续回溯',
        26: '冲突 → 这把椅子不能坐，返回',
        28: '冲突 → 这把椅子不能坐，返回',
        30: '冲突 → 这把椅子不能坐，返回',
        'self.dfs(p + 1, n, now_state | ': '三个冲突都没有 → 第 `{B.p}` 把椅子坐人：`now_state` 变成 `{B.now_state | (1 << B.p):0{n}b}`，`now_v + 1`',
    },
    cards=dict(
        one_liner='上一排的坐法 → 回溯生成这一排所有合法坐法，取最大',
        complexity='时间约 `O(m·2^n·合法坐法数)`，空间 `O(2^n)`（滚动数组）',
        problem=['教室 `m×n` 座位，`.` 好座位、`#` 坏座位',
                 '学生能看到左、右、左上、右上的答卷，求最多容纳多少学生',
                 '示例：`[[.,#],[.,.],[.,#]]` → `3`'],
        quote='f[i][state]表示前i行，最后一行座位状态为state时可以参加考试的最大学生数。……我在这里采用的是使用搜索回溯来寻找f[i + 1][state\']中合法的state\'，具体为从左向右逐个扫描，尝试跳过这个位置或者在这个位置上安排学生。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态：这一排的坐法（二进制），值：前面最多的学生数',
              '对上一排每种可达坐法 `state`，回溯生成这一排的坐法 `state\'`',
              '第 `p` 位要坐人：座位好、上一排 `p±1` 没人、本排 `p-1` 没人',
              '每一排只依赖上一排，用 `g`、`f` 两个数组滚动即可'],
        summary=['`g[state] = None` 表示不可能；`n ≤ 8`，每排最多 `256` 种状态',
                 '三个冲突检查：上一排左上、右上、本排左边紧邻',
                 '原文为 Python 2 写法：`max(g)` 里含 `None`，Python 3 不能比较，已改为 `max(x for x in g if x is not None)`；另删去 dfs 前后的空格行',
                 '对比灵神：灵神枚举 `j` 的子集和子集的子集；yiduobo 用回溯一位一位生成'],
    ),
)
