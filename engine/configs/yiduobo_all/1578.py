def _top(S):
    if 'res' not in S:
        return ''
    return f"已删除的总成本 `res` = =={S['res']}==；当前留着的气球成本 `last_cost` = {S.get('last_cost')}"


def _col(S, i, v):
    if 'index' not in S:
        return None
    return 'blue' if i == S['index'] else ('green' if i < S['index'] and S['s'][i] == S['s'][S['index']] and
                                           all(S['s'][k] == S['s'][i] for k in range(i, S['index'] + 1)) else None)


def _cmp(S, B, r):
    c, lc = S.cost[S.index], S.last_cost
    if c < lc:
        return f'`{c} < {lc}`：新来的更便宜 → ==删新的==，`res` += {c}'
    return f'`{c} ≥ {lc}`：上一个更便宜（或相等）→ ==删上一个==，`res` += {lc}，新的成了留下的'


CONFIG = dict(
    num=1578, title='使绳子变成彩色的最短时间', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='相邻相同 · 删成本较小的',
    tags=['灵神题单', '难度分 1574'],
    code='''
class Solution(object):
    def minCost(self, s, cost):

        last = None
        last_cost = None
        n = len(cost)
        res = 0
        for index in range(n):
            if s[index] == last:
                if cost[index] < last_cost:
                    res += cost[index]
                else:
                    res += last_cost
                    last_cost = cost[index]
            else:
                last = s[index]
                last_cost = cost[index]
        
        return res
''',
    call='Solution().minCost("aabaac", [1,3,2,4,1,5])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前，绿 = 同色段前面的气球）', cell=84,
             pointers={'index': 'pink'}, color=_col),
        dict(type='array', var='cost', label='cost（删除成本）', cell=84, pointers={'index': 'pink'}, color=_col),
        dict(type='text', fn=lambda S: (f"上一个字符 `last = {S['last']!r}`" if 'last' in S else ''), size=26),
    ],
    watch=[('index', 'index', 'pink'), ('last', 'last', 'blue'), ('last_cost', 'last_cost', 'orange'), ('res', 'res', 'green')],
    captions={
        'last = None': '`last`：上一个气球的颜色，开头还没有',
        'last_cost = None': '`last_cost`：当前留着的那个气球的成本',
        'n = len': '`n = {n}` 个气球',
        'res = 0': '`res` 累计删除成本',
        'for index': lambda S, B, r: ('气球都扫完了，循环结束' if B.get('index') == S.index and 'index' in B
                                     else f"看第 `{S.index}` 个气球：颜色 `{S.s[S.index]}`，成本 `{S.cost[S.index]}`"),
        'if s[index] == last': lambda S, B, r: (f"`'{S.s[S.index]}' == '{S.last}'` → 和上一个同色，必须删掉一个"
                                                if S.s[S.index] == S.last
                                                else f"`'{S.s[S.index]}' ≠ {S.last!r}` → 颜色变了，不用删，它成为新的“留着的”"),
        'if cost[index] < last_cost': _cmp,
        'res += cost[index]': '删新的：`res` → =={res}==，`last_cost` 不变（仍是更贵的 {last_cost}）',
        'res += last_cost': '删上一个：`res` → =={res}==',
        'last_cost = cost[index]': '新的更贵，留下它：`last_cost = {last_cost}`',
        'last = s[index]': '记下新的颜色 `{last}`',
        'last_cost = cost[index]': lambda S, B, r: f'它成为当前留着的气球：`last_cost = {S.last_cost}`',
        'return res': '同色段都只剩最贵的一个，最少总成本 `{ret}`',
    },
    cards=dict(
        one_liner='遇到相邻同色，就删掉其中成本较小的那个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s[i]` 是第 i 个气球的颜色，`cost[i]` 是删掉它的成本',
                 '删若干个气球，使==相邻气球颜色都不同==，求最小总成本',
                 '示例：`s = "abaac"`，`cost = [1,2,3,4,5]` → `3`'],
        quote='为了使得成本最小，那么剩下的自然就是成本最大的那一个，换言之就是一旦遇到两个相同的相邻字符，那么必然是删去其中成本较小的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻相同的字符要删到只剩一个，剩下的当然选成本最大的',
              '一趟扫描：用 `last` / `last_cost` 记住“目前留着的那个”',
              '遇到同色：删较便宜的，较贵的继续留着，等待下一个同色的比较'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`last_cost` 始终是当前同色段里留下的最大成本',
                 '颜色变了就重置 `last` 与 `last_cost`，不会误删',
                 '对比灵神：灵神“总和减去每段最大”，这里边扫边累加被删的',
                 '题目名与简报略有不同，内容一致；原文已是可直接运行的写法'],
    ),
)
