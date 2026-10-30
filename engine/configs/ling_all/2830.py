OFFERS = [[0, 0, 1], [0, 2, 2], [1, 3, 2], [3, 5, 4]]


def _groups_txt(S):
    g = S.get('groups')
    if g is None:
        return '把买家按 `end` 分组：`groups[end]` 里存 `(start, gold)`'
    parts = []
    for e, lst in enumerate(g):
        if lst:
            parts.append(f'end={e}: ' + ' '.join(f'({s},{w})' for s, w in lst))
    return '  |  '.join(parts)


def _cur_txt(S):
    if 'end' not in S or 'g' not in S:
        return ''
    e = S['end']
    if 'start' in S and S['_line'] in (11, 12):
        return f'买家 `[{S["start"]}, {e}]` 出价 {S["gold"]}：卖它 = `f[{S["start"]}] + {S["gold"]}` = =={S["f"][S["start"]] + S["gold"]}=='
    return f'枚举到第 `{e}` 号房屋：`f[{e + 1}]` = 销售编号不超过 {e} 的房屋的最大盈利'


CONFIG = dict(
    num=2830, title='销售利润最大化', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='按 end 分组 · 线性 DP',
    tags=['灵神题单', '难度分 1851'],
    code='''
class Solution:
    def maximizeTheProfit(self, n: int, offers: List[List[int]]) -> int:
        groups = [[] for _ in range(n)]
        for start, end, gold in offers:
            groups[end].append((start, gold))

        f = [0] * (n + 1)
        for end, g in enumerate(groups):
            f[end + 1] = f[end]
            for start, gold in g:
                f[end + 1] = max(f[end + 1], f[start] + gold)
        return f[n]
''',
    call=f'Solution().maximizeTheProfit(6, {OFFERS!r})',
    expect=6,
    skip=['groups[end].append', 'for start, end, gold in offers'],
    views=[
        dict(type='text', fn=_groups_txt, size=26, h=70),
        dict(type='array', var='f', label='f[i]：只卖编号 < i 的房屋能赚的最多（黄 = 正在算）', h=300, cell=100,
             pointers={'end + 1': 'blue', 'start if _line in (10, 11) else None': 'pink'},
             pointer_labels={'start if _line in (10, 11) else None': 'start'},
             color=lambda S, i, v: ('yellow' if 'end' in S and i == S['end'] + 1 and S.get('_line', 0) >= 9 else None)),
        dict(type='text', fn=_cur_txt, size=28, h=90),
    ],
    watch=['end', ('start', "start if _line in (10, 11) else '-'", 'pink'), ('gold', "gold if _line in (10, 11) else '-'"), ('f[end+1]', "f[end + 1]", 'green')],
    captions={
        'groups = [[]': '`groups[i]` 收集所有 `end = i` 的买家，方便按右端点枚举',
        'f = [0] * (n + 1)': '`f[i+1]` = 销售编号不超过 `i` 的房屋的最大盈利；==`f[0] = 0`==',
        'for end, g in enumerate': lambda S, B, r: ('所有房屋都处理完了' if S.end == B.get('end') else f'算 `f[{S.end + 1}]`：先看房屋 `{S.end}` 卖不卖'),
        'f[end + 1] = f[end]': '==不卖==房屋 `{end}`：`f[{end + 1}] = f[{end}]` = {f[end]}',
        'for start, gold in g': lambda S, B, r: (f'`end = {S.end}` 的买家都枚举完了' if S.g and 'start' in B and B.get('end') == S.end and (S.start, S.gold) == (B.start, B.gold) else (f'没有以 `{S.end}` 结尾的买家，只能不卖' if not S.g else f'枚举 `end = {S.end}` 的买家 `[start, {S.end}]`：买下它，前面只能用 `f[start]`')),
        'f[end + 1] = max(': '`max({B.f[end + 1]}, f[{start}] + {gold})` = `max({B.f[end + 1]}, {f[start] + gold})` → =={f[end + 1]}==',
        'return f[n]': '答案 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='房屋 i 卖或不卖：不卖继承 f[i]，卖则枚举 end=i 的买家',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 所房屋排成一排，`offers[i] = [start, end, gold]` 表示买家要买 `[start, end]` 的所有房屋',
                 '同一所房屋不能卖给两人，求最多赚多少金币',
                 '示例：`n=5, offers=[[0,0,1],[0,2,2],[1,3,2]]` → `3`'],
        quote='不卖，有 f[i+1]=f[i]。卖，那么遍历所有 end_j=i 的购买请求，有 f[i+1] = max(f[start_j]+gold_j)。为了方便遍历，可以先把所有 end 相同的数据归类。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i+1]` 表示只考虑编号不超过 `i` 的房屋的最大盈利',
              '卖房屋 `i` 时，买家区间必须以 `i` 结尾，所以先按 `end` 分组',
              '买家 `[start, i]` 占掉 `start..i`，左边只剩 `f[start]`'],
        summary=['时间 `O(n+m)`：每个买家只在自己的 `end` 组里被枚举一次',
                 '空间 `O(n+m)`：`groups` 和 `f`',
                 '易错：`f` 下标整体 +1，`f[start]` 就是 `start` 之前的最优，不要写成 `f[start-1]`',
                 '同类：2008 出租车的最大盈利（几乎一样）、1235、1751、2054'],
    ),
)
