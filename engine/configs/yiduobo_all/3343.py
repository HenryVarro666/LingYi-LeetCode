def _cols(S):
    s = S.get('s')
    return [f'{d - s:+d}' if d != s else '0' for d in range(2 * s + 1)] if s is not None else []


def _col(S, r, c, v):
    if S.get('_line') == 49 and 'now_even' in S and r == S['now_even'] and c == S['now_diff']:
        return 'yellow'
    return 'green' if v else None


def _top(S):
    if 'e' in S and 'now_diff' in S:
        return (f"数字 `{S['num']}`：偶 `{S['e']}` 个、奇 `{S['o']}` 个 → 差 `{S['diff'] - S['s']:+d}` 变 =={S['now_diff'] - S['s']:+d}==")
    if 's' in S and 'even' in S:
        return f"偶数位 `{S['even']}` 个、奇数位 `{S['odd']}` 个；差 = 偶位和 − 奇位和"
    return '逐个数字填充：把相同的数字 `v` 分到偶数位或奇数位'


CONFIG = dict(
    num=3343, title='统计平衡排列的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='逐个数字填充 · 奇偶位分配 DP',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2615'],
    code='''
class Solution(object):
    def countBalancedPermutations(self, num):
        
        cnt = [0] * 10
        s = 0
        for c in num:
            cnt[int(c)] += 1
            s += int(c)
        
        if s % 2 == 1:
            return 0
        
        s //= 2
        odd = len(num) // 2
        even = len(num) - odd

        f = [[0] * (s + s + 1) for _ in range(even + 1)]
        f[0][s] = 1
        mod = 10 ** 9 + 7
        tot = 0

        C = [[0] * (even + 1) for _ in range(even + 1)]
        C[0][0] = 1
        for n in range(1, even + 1):
            for k in range(n + 1):
                if k == 0 or k == n:
                    C[n][k] = 1
                else:
                    C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % mod

        for num in range(10):
            if cnt[num] == 0:
                continue
            g = copy.deepcopy(f)
            f = [[0] * (s + s + 1) for _ in range(even + 1)]
            for pre_even in range(min(even, tot) + 1):
                pre_odd = tot - pre_even
                for diff in range(s + s + 1):
                    if g[pre_even][diff] == 0:
                        continue
                    
                    for e in range(cnt[num] + 1):
                        o = cnt[num] - e
                        now_even = pre_even + e
                        now_odd = pre_odd + o
                        now_diff = diff + (e - o) * num
                        if now_even > even or now_odd > odd or now_diff < 0 or now_diff > s + s:
                            continue
                        f[now_even][now_diff] = (f[now_even][now_diff] + g[pre_even][diff] * C[even - pre_even][e] % mod * C[odd - pre_odd][o] % mod) % mod

            tot += cnt[num]

        return f[even][s]
''',
    call='Solution().countBalancedPermutations("112")',
    expect=1,
    setup='import copy',
    skip=['for c in num', 'cnt[int(c)] += 1', 's += int(c)', 'mod = 10', 'tot = 0', 'C = [[0]', 'C[0][0] = 1', 'for n in range', 'for k in range',
          'if k == 0 or', 'C[n][k] = 1', 'else:', 'C[n][k] = (', 'for pre_even', 'pre_odd = tot', 'o = cnt', 'now_even = ', 'now_odd = ',
          'if g[pre_even][diff] == 0', 'continue', 'for diff in range'],
    max_steps=60,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='table', var='f', label='f[偶数位已放个数][差]（列 = 偶位和 − 奇位和；绿 = 有方案）', h=300, cell=90,
             rows=lambda S: [f'偶 {r}' for r in range(S['even'] + 1)] if 'even' in S else [], cols=_cols, color=_col),
        dict(type='array', var='cnt', label='cnt[d]：数字 d 的出现次数', cell=64, h=170, pointers={'num': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('num') and 'g' in S else None),
    ],
    watch=[('num', 'num', 'blue'), ('pre_even', 'pre_even', 'cyan'), ('diff', 'diff', 'orange'), ('e', 'e', 'pink'), ('tot', 'tot')],
    captions={
        'cnt = [0] * 10': '`cnt[d]` 统计数字 d 出现的次数',
        'if s % 2 == 1': lambda S, B, r: (f'数字和 `{S.s}` 是奇数，奇偶位和不可能相等 → 返回 0' if S.s % 2 else f'数字和 `{S.s}` 是偶数，奇偶位的和都应是 `{S.s // 2}`'),
        's //= 2': '`s` 改成一半：每边的和都要等于 `s = {s}`',
        'odd = len(num)': '奇数位 `odd = {odd}` 个，偶数位 `even = {even}` 个',
        'f = [[0] * (s + s + 1)': lambda S, B, r: ('`f[i][d]`：偶数位已放 `i` 个、差为 `d - s` 的方案数；差整体 `+ s` 避免负下标' if S['_line'] < 20
                                                  else f'`f` 清零，准备记录填完数字 `{S.num}` 后的状态'),
        'f[0][s] = 1': '起点：什么都没放，差 `0` 对应下标 `s` → `f[0][{s}] = 1`',
        'for num in range(10)': lambda S, B, r: (f'开始填数字 `{S.num}`' if S.get('num') != B.get('num') or 'num' not in B else '数字 0~9 都填完'),
        'if cnt[num] == 0': lambda S, B, r: (f'数字 `{S.num}` 一个也没有 → 跳过' if S.cnt[S.num] == 0 else f'数字 `{S.num}` 有 `{S.cnt[S.num]}` 个，要把它们分到奇偶位'),
        'g = copy.deepcopy': '把上一轮的 `f` 存进 `g`，`f` 清零重新累加（相当于滚动数组）',
        'for e in range': '枚举 `e`：这 `cnt[num]` 个数字里有几个放偶数位',
        'if now_even > even': lambda S, B, r: ('偶/奇数位放不下，或差超出 `[0, 2s]` → 不合法，跳过' if (S.now_even > S.even or S.now_odd > S.odd or S.now_diff < 0 or S.now_diff > S.s + S.s)
                                              else f'合法：偶 `{S.now_even}` 个、奇 `{S.now_odd}` 个，差 `{S.now_diff - S.s:+d}`'),
        'f[now_even][now_diff] =': lambda S, B, r: f'`f[{S.now_even}][{S.now_diff}]` += `g[{S.pre_even}][{S.diff}]`({S.g[S.pre_even][S.diff]}) × `C({S.even - S.pre_even},{S.e})` × `C({S.odd - (S.tot - S.pre_even)},{S.o})` → ==`{S.f[S.now_even][S.now_diff]}`==',
        'tot += cnt[num]': '数字 `{num}` 分配完：已填 `tot = {tot}` 个',
        'return f[even][s]': '偶数位刚好放满 `{even}` 个、差为 0 的方案数：==`{ret}`==',
    },
    cards=dict(
        one_liner='不按位置填，按数字填：每种数字分到奇数位或偶数位',
        complexity='时间约 `O(10·n·s·cnt)`，空间 `O(n·s)`',
        problem=['奇数下标的数字和 = 偶数下标的数字和，叫==平衡==字符串',
                 '求 `num` 所有不同排列中平衡的有几个（模 `10^9+7`）',
                 '本视频：`"112"` → `1`（`"121"` 平衡）'],
        quote='既然逐位填充的方案行不通，那么不妨换一种思路，改成逐个数字填充。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位填会记不住 10 种数字的个数；改成==逐个数字==填，一次把同一种数字分完',
              '`f[偶数位已放个数][差]`：差 = 偶数位和 − 奇数位和，要保证差回到 0',
              '数字 `v` 放 `e` 个到偶数位：位置选法 `C(剩余偶数位, e) × C(剩余奇数位, o)`'],
        summary=['时间约 `O(10·n·s)`（再乘每种数字的个数），空间 `O(n·s)`',
                 '`s` 是一半数字和；差加上偏移 `s`，因为 Python 的负下标会从尾部取',
                 '用 `g = copy.deepcopy(f)` 做滚动数组，省掉“数字”这一维',
                 '代码里 `for num in range(10)` 复用了参数名 `num`，原文如此，保留',
                 '对比灵神：灵神把“第一组个数”和“第一组和”当状态，再除以阶乘；这里直接算位置的组合数'],
    ),
)
