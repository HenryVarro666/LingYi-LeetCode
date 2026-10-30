DAYS = [1, 4, 6, 7, 8, 20]
COSTS = [2, 7, 15]


def _f_formula(S):
    if 'f' not in S or 'i' not in S or S.get('_line') != 10:
        return '`f[i+1] = min(f[i] + costs[0], f[j] + costs[1], f[k] + costs[2])`'
    f, i, j, k = S['f'], S['i'], S['j'], S['k']
    c = S['costs']
    a, b, d = f[i] + c[0], f[j] + c[1], f[k] + c[2]
    return (f'`f[{i + 1}] = min(f[{i}]+{c[0]}, f[{j}]+{c[1]}, f[{k}]+{c[2]})` = '
            f'`min({a}, {b}, {d})` = =={min(a, b, d)}==')


def _for_cap(S, B, ret):
    if 'i' in B and S['i'] == B['i']:
        return '所有旅行日处理完毕'
    return f"处理 `days[{S['i']}] = {S['d']}`：算出 `f[{S['i'] + 1}]`（完成前 {S['i'] + 1} 个旅行日的最小花费）"


def _wj(S, B, ret):
    j, d, days = S['j'], S['d'], S['days']
    if days[j] <= d - 7:
        return f'`days[{j}] = {days[j]} ≤ {d} − 7`：在这天买 7 天票，到 `{days[j] + 6}` 就过期，盖不住 `{d}` → `j` 右移'
    return f'`days[{j}] = {days[j]} > {d} − 7`：在 `days[{j}]` 买 7 天票，能一直用到第 `{d}` 天'


def _wk(S, B, ret):
    k, d, days = S['k'], S['d'], S['days']
    if days[k] <= d - 30:
        return f'`days[{k}] = {days[k]} ≤ {d} − 30`：30 天票盖不住 `{d}` → `k` 右移'
    return f'`days[{k}] = {days[k]} > {d} − 30`：在 `days[{k}]` 买 30 天票，能盖住 `days[{k}..{S["i"]}]`'


def _fcap(S, B, ret):
    f, i, j, k, c = S['f'], S['i'], S['j'], S['k'], S['costs']
    opts = [(f[i] + c[0], f'1 天票：`f[{i}] + {c[0]} = {f[i] + c[0]}`'),
            (f[j] + c[1], f'7 天票：`f[{j}] + {c[1]} = {f[j] + c[1]}`'),
            (f[k] + c[2], f'30 天票：`f[{k}] + {c[2]} = {f[k] + c[2]}`')]
    best = min(o[0] for o in opts)
    return '，'.join(o[1] for o in opts) + f' → 取最小 `f[{i + 1}] =` =={best}=='


CONFIG = dict(
    num=983, title='最低票价', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='DP · 三指针优化',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        f = [0] * (len(days) + 1)
        j = k = 0
        for i, d in enumerate(days):
            while days[j] <= d - 7:
                j += 1
            while days[k] <= d - 30:
                k += 1
            f[i + 1] = min(f[i] + costs[0], f[j] + costs[1], f[k] + costs[2])
        return f[-1]
''',
    call=f'Solution().mincostTickets({DAYS}, {COSTS})',
    expect=11,
    views=[
        dict(type='array', var='days', label='days（框 = days[j..i]：在 days[j] 买 7 天票能盖住的旅行日）', cell=96, h=240,
             pointers={'i': 'blue', 'j': 'pink', 'k': 'purple'}, window=('j', 'i')),
        dict(type='array', var='f', label='f[i+1]：完成 days[0..i] 的最小花费（f[0] = 0）', cell=96, h=170,
             pointers={'i + 1': 'green'},
             color=lambda S, x, v: 'green' if 'i' in S and x == S['i'] + 1 and S.get('_line') == 10 else
             ('cyan' if 'i' in S and x <= S['i'] else None)),
        dict(type='text', fn=_f_formula, h=70, size=26),
    ],
    watch=[('i', 'i', 'blue'), ('d', 'd'), ('j', 'j', 'pink'), ('k', 'k', 'purple'), ('costs', 'costs')],
    captions={
        'f = [0] * (len': '`f[i+1]`：完成 `days[0]` 到 `days[i]` 的最小花费；`f[0] = 0`（旅行 0 天不花钱）',
        'j = k = 0': '`j`/`k`：7 天票/30 天票==最早可以从哪个旅行日买==，只增不减',
        'for i, d in enumerate': _for_cap,
        'while days[j] <= d - 7': _wj,
        'j += 1': '`j` → {j}',
        'while days[k] <= d - 30': _wk,
        'k += 1': '`k` → {k}',
        'f[i + 1] = min(': _fcap,
        'return f[-1]': '答案 `f[{len(days)}] = {ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举最后一张票买哪种，双指针找它最早从哪天买',
        complexity='时间 `O(n)`，空间 `O(n)`（n 为 days 长度）',
        problem=['`days` 是要旅行的日子（严格递增），通行证有 1 / 7 / 30 天三种',
                 '价格分别为 `costs[0..2]`，求覆盖所有旅行日的==最低花费==',
                 '示例：`days = [1,4,6,7,8,20]`，`costs = [2,7,15]` → `11`'],
        quote='在第 days[j] 天购买为期 7 天的通行证，满足 days[j]+7 > days[i]（注意不是 ≥），'
              '接下来需要解决的问题为：完成 days[0] 到 days[j−1] 的最小花费，即 f[i+1] = f[j]+costs[1]。',
        quote_src='—— 灵茶山艾府题解（五、三指针优化）',
        idea=['「枚举选哪个」：最后一个旅行日 `days[i]` 用哪种票覆盖',
              '`j` = 满足 `days[j] > days[i] − 7` 的==最小==下标；`k` 同理（30 天）',
              '`days` 有序 → `j`、`k` 随 `i` 只增不减，三指针 `O(n)`'],
        summary=['时间 `O(n)`：`j`、`k` 总共只右移 `O(n)` 次；空间 `O(n)`',
                 '易错：7 天票覆盖 `[days[j], days[j]+6]`，条件是 `days[j] > d − 7`',
                 '`f` 下标偏移一位：`f[i+1]` 对应 `days[0..i]`，`f[0] = 0`',
                 '灵神的推导路线：记忆化搜索 `dfs(i)` → 按日期递推 `O(D)` → 三指针 `O(n)`'],
    ),
)
