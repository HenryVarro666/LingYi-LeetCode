def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    ans = S.get('ans') or []
    total = n * (n - 1)
    cv.text((x0 + 18, y0 + 4), '赛程矩阵：每列一天，每行一支队（蓝 = 主场，粉 = 客场）', 22, T['muted'], bold=True)
    lab = 70
    cw = min(52, (x1 - x0 - 40 - lab) / total)
    ch = min(70, (y1 - y0 - 200) / n)
    sx, sy = x0 + 20 + lab, y0 + 90
    for t in range(n):
        cv.text((sx - 12, sy + t * ch + ch / 2), f'队{t}', 22, T['muted'], anchor='rm', bold=True)
    for day in range(total):
        X = sx + day * cw
        cv.text((X + cw / 2, sy - 8), day + 1, 14, T['dim'], anchor='mb', mono=True)
        for t in range(n):
            cv.rect((X + 1, sy + t * ch + 1, X + cw - 1, sy + (t + 1) * ch - 1), fill=T['panel2'], r=3)
    for day, (a, b) in enumerate(ans):
        X = sx + day * cw
        last = day == len(ans) - 1
        for t, c, lt in ((a, T['blue'], '主'), (b, T['pink'], '客')):
            cv.rect((X + 1, sy + t * ch + 1, X + cw - 1, sy + (t + 1) * ch - 1), fill=c, r=3,
                    outline=T['yellow'] if last else None, width=3)
            cv.text((X + cw / 2, sy + t * ch + ch / 2), lt, 20, T['bg'], anchor='mm', bold=True)
    # 相邻两天的冲突检查
    yb = sy + n * ch + 24
    if len(ans) >= 2:
        a, b = ans[-2], ans[-1]
        ok = not (set(a) & set(b))
        cv.text((x0 + 20, yb), f'第 {len(ans) - 1}、{len(ans)} 天：{a} 与 {b}  ' + ('队伍互不相同，没有冲突' if ok else '有队伍连续两天比赛！'),
                26, T['green'] if ok else T['red'], bold=True)
    elif len(ans) == 1:
        cv.text((x0 + 20, yb), f'第 1 天：{ans[0]}', 26, T['text'], bold=True)
    cv.text((x0 + 20, yb + 44), f'已排 {len(ans)} / {total} 场', 24, T['muted'], bold=True)


def _prev(S, B):
    a = S.ans
    if len(a) < 2:
        return ''
    return f'与前一天的 `{a[-2]}` 队伍互不相同'


def _ap1(S, B, r):
    return f'第 {len(S.ans)} 天：队 {S.i} 主场对 队 {(S.i + S.d) % S.n}（差 d = {S.d}）' + ('，' + _prev(S, B) if len(S.ans) > 1 else '')


def _ap2(S, B, r):
    return f'第 {len(S.ans)} 天：`d = 1` 的比赛 `{S.ans[-1]}`，' + _prev(S, B)


def _ap3(S, B, r):
    return f'第 {len(S.ans)} 天：`d = n-1` 的比赛（客队 → 主队反过来）`{S.ans[-1]}`，' + _prev(S, B)


CONFIG = dict(
    num=3680, title='生成赛程', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='构造 · 按差值 d 轮转',
    tags=['贪心与思维', '难度分 2378'],
    code='''
class Solution:
    def generateSchedule(self, n: int) -> List[List[int]]:
        if n < 5:
            return []

        ans = []

        # 处理 d=2,3,...,n-2
        for d in range(2, n - 1):
            for i in range(n):
                ans.append([i, (i + d) % n])

        # 交错排列 d=1 与 d=n-1（或者说 d=-1）
        for i in range(n):
            ans.append([i, (i + 1) % n])
            ans.append([(i - 1) % n, (i - 2) % n])

        return ans
''',
    call='Solution().generateSchedule(5)',
    expect=[[0, 2], [1, 3], [2, 4], [3, 0], [4, 1], [0, 3], [1, 4], [2, 0], [3, 1], [4, 2],
            [0, 1], [4, 3], [1, 2], [0, 4], [2, 3], [1, 0], [3, 4], [2, 1], [4, 0], [3, 2]],
    views=[
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=['n', ('d', 'd', 'cyan'), ('i', 'i', 'blue'), ('场数', 'len(ans)', 'green')],
    captions={
        'if n < 5': '`n = {n} ≥ 5`，有解。（`n ≤ 3` 连续两场必须四队互不相同，无解；`n = 4` 排到第五场就必然冲突）',
        'ans = []': '`ans` 依次放每天的比赛 `[主队, 客队]`',
        'for d in range(2, n - 1)': lambda S, B, r: ('`d = 2..n-2` 都排完了，接着处理 `d = 1` 与 `d = n-1`' if B.get('d') == S.d
                                                      else f'先排「队 i 对 队 i+d」的比赛，`d = {S.d}`：所有队轮流当主场，各队场次始终接近'),
        'ans.append([i, (i + d) % n])': _ap1,
        'for i in range(n)': lambda S, B, r: ('这一轮 `i` 全部走完' if B.get('i') == S.i else f'`i = {S.i}`：队 i 的这一对比赛'),
        'ans.append([i, (i + 1) % n])': _ap2,
        'ans.append([(i - 1) % n, (i - 2) % n])': _ap3,
        'return ans': '共 `n(n-1) = {len(ans)}` 场，每对队伍一主一客，相邻两天互不相同',
    },
    cards=dict(
        one_liner='按差值 d 轮转排比赛，最后交错排 d=1 和 d=n-1',
        complexity='时间 `O(n^2)`，空间 `O(1)`（返回值不计入）',
        problem=['`n` 支队伍两两比赛两次（一主一客），每天一场',
                 '要求没有队伍在==连续两天==都比赛，返回任意一个赛程',
                 '示例：`n = 3` → `[]`；`n = 5` → 20 场的合法赛程'],
        quote='枚举 d=1,2,3,…,n-1，枚举 a=0,1,2,…,n-1，构造比赛 (a,(a+d) mod n)。……随着赛程的进行，每个队伍的比赛场次要尽量接近。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻两天要四队互不相同，所以 `n ≤ 3` 无解；`n = 4` 也排不满，`n ≥ 5` 一定有解',
              '固定差值 `d` 时，`(i, i+d)` 与 `(i+1, i+1+d)` 的四个队互不相同（`d ≠ 1, n-1`）',
              '`d = 1` 和 `d = n-1` 会和相邻轮冲突：把它们==交错==排在最后，错开一格'],
        after=[dict(heading='其他写法', lines=['构造方法一：`d=1` 先排偶数 `a` 再排奇数 `a`，`n` 为偶数时交换末尾两场',
                                              '方法二：随机打乱全部 n(n-1) 场，再贪心取无冲突的下一场，失败重来'])],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`n < 5` 直接返回 `[]`，别漏掉 `n = 4`',
                 '`d` 只枚举 `2..n-2`；`d=1` 与 `d=n-1` 单独交错',
                 '`[(i-1)%n, (i-2)%n]` 是 `d = n-1` 的比赛（主队 a、客队 a-1），与 `d = 1` 的 `[i, i+1]` 错开一格'],
    ),
)
