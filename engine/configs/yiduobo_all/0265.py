def _cc(S, r, c, v):
    i = S.get('index')
    if i is None:
        return None
    return 'yellow' if r == i else None


def _cap_cur(S, B, ret):
    c = S.color
    if c == S.first_color:
        return f'`color = {c}` 恰好是上一轮最小值的颜色，不能用最小值 → 用次小 `{S.second_val}` + `{S.costs[S.index][c]}` = =={S.f[c]}=='
    return f'`color = {c}` 和上一轮最小值颜色 `{S.first_color}` 不同 → 用最小 `{S.first_val}` + `{S.costs[S.index][c]}` = =={S.f[c]}=='


def _cap_cmp(S, B, ret):
    v = S.f[S.color]
    if S.first_val is None or v < S.first_val:
        return f'`f[{S.color}] = {v}` 比最小值 `{S.first_val}` 还小（或还没有最小值）→ 成为新的最小'
    return f'`f[{S.color}] = {v}` 不比最小值 `{S.first_val}` 小，继续看是否更新次小'


def _cap_sec(S, B, ret):
    v = S.f[S.color]
    if S.second_val is None or v < S.second_val:
        return f'`f[{S.color}] = {v}` 比次小值 `{S.second_val}` 小（或还没有次小值）→ 更新次小'
    return f'`f[{S.color}] = {v}` 不比次小值 `{S.second_val}` 小，跳过'


CONFIG = dict(
    num=265, title='粉刷房子II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='线性 DP · 记录最小值与次小值',
    tags=['线性DP'],
    code='''
class Solution(object):
    def minCostII(self, costs):

        for index in range(len(costs)):
            if index == 0:
                f = costs[0][:]
            else:
                g = f[:]
                for color in range(len(g)):
                    if color == first_color:
                        f[color] = second_val + costs[index][color]
                    else:
                        f[color] = first_val + costs[index][color]
            
            first_val = None
            first_color = None
            second_val = None
            second_color = None
            for color in range(len(f)):
                if first_val is None or f[color] < first_val:
                    first_val, second_val = f[color], first_val
                    first_color, second_color = color, first_color
                elif second_val is None or f[color] < second_val:
                    second_val = f[color]
                    second_color = color
        
        return min(f)
''',
    call='Solution().minCostII([[1,5,3],[2,9,4],[7,1,8]])',
    expect=6,
    views=[
        dict(type='table', var='costs', rows=['房0', '房1', '房2'], cols=['色0', '色1', '色2'], color=_cc, h=220),
        dict(type='array', var='f', pointers={'color': 'blue'}, label='f：当前这栋房子刷完各颜色的最小代价', h=230),
        dict(type='text', fn=lambda S: (f"上一轮最小 ==`{S['first_val']}`==（色 {S['first_color']}），次小 ==`{S['second_val']}`==（色 {S['second_color']})" if 'first_val' in S and S['first_val'] is not None else '还没有最小值 / 次小值'), h=70),
    ],
    skip=['first_val = None', 'first_color = None', 'second_val = None', 'second_color = None'],
    watch=['index', 'color', ('first_val', 'first_val', 'green'), ('first_color', 'first_color', 'green'),
           ('second_val', 'second_val', 'orange'), ('second_color', 'second_color', 'orange')],
    captions={
        'if index == 0': lambda S, B, r: ('第 0 栋没有前一栋，`f` 直接等于它的代价' if S.index == 0 else f'第 `{S.index}` 栋：有前一栋，要用上一轮的最小/次小值转移'),
        'f = costs[0][:]': '`f = {f}`：第 0 栋各颜色的代价',
        'g = f[:]': '备份上一栋的结果：`g = {g}`',
        'if color == first_color': lambda S, B, r: (f'`color = {S.color}` 等于上一轮最小值的颜色 `{S.first_color}` → 不能接最小值，要接次小值' if S.color == S.first_color else f'`color = {S.color}` 不是最小值的颜色 `{S.first_color}` → 可以接最小值'),
        'f[color] = second_val': _cap_cur,
        'f[color] = first_val': _cap_cur,
        'if first_val is None': _cap_cmp,
        'first_val, second_val =': '新最小 `{first_val}`；原最小 `{second_val}` 退位成次小',
        'first_color, second_color': '颜色同步更新：最小色 {first_color}，次小色 {second_color}（None 表示还没有）',
        'elif second_val is None': _cap_sec,
        'second_val = f[color]': '次小值更新为 `{second_val}`',
        'second_color = color': '次小色更新为 {second_color}',
        'return min': '最后一栋颜色不限：`min({f})` = =={ret}==',
    },
    cards=dict(
        one_liner='转移只需要上一轮的最小值；撞色了就改用次小值',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['`n` 栋房子、`k` 种颜色，`costs[i][j]` 是第 `i` 栋刷颜色 `j` 的花费',
                 '==相邻两栋颜色不能相同==，求最小总花费',
                 '本视频：`[[1,5,3],[2,9,4],[7,1,8]]`'],
        quote='第i - 1轮中的次小值实际上就是f[i - 1][k]中的最小值，此时直接使用i - 1轮的次小值来进行状态转移就行了',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素转移 `f[i][j] = min(f[i-1][k]) + cost[i][j]`（`k ≠ j`）要 `O(nk²)`',
              '上一轮最小值的颜色与 `j` 不同 → 直接用最小值',
              '相同 → 必须用次小值，所以每轮扫描时同时记录最小、次小及其颜色'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错点：更新最小值时，旧的最小值要退位成次小值',
                 '`first_val` 初始为 `None`，所以比较前要先判断 `is None`',
                 '颜色数为 3 时就是第 256 题'],
    ),
)
