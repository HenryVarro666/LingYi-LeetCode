CONFIG = dict(
    num=3645, title='最优激活顺序得到的最大总和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='按 limit 分组 · 组内取最大的 lim 个',
    tags=['贪心与思维', '难度分 2019'],
    code='''
class Solution:
    def maxTotal(self, value: List[int], limit: List[int]) -> int:
        groups = defaultdict(list)
        for lim, v in zip(limit, value):
            groups[lim].append(v)

        ans = 0
        for lim, a in groups.items():
            # lim >= len(a) 的情况不需要排序
            if lim < len(a):
                a.sort()
                a = a[-lim:]
            ans += sum(a)
        return ans
''',
    call='Solution().maxTotal([4,1,5,2,7], [3,3,2,3,3])',
    expect=18,
    views=[
        dict(type='array', var='value', label='value', pointers={}, h=150),
        dict(type='array', var='limit', label='limit', pointers={}, h=150),
        dict(type='map', var='groups', fmt=lambda k, v: f'{k}: {v}', h=220),
        dict(type='array', var='a', label='当前组 a（取最大的 lim 个）', h=170),
        dict(type='text', fn=lambda S: (f"组 limit=`{S['lim']}`：最多取 `{S['lim']}` 个，组内共 `{len(S['a'])}` 个" if 'lim' in S and 'a' in S and 'ans' in S else ''), size=30, h=70),
    ],
    watch=['lim', ('ans', 'ans', 'green')],
    captions={
        'groups[lim].append(v)': '`limit = {lim}` 的价值放进同一组：`groups[{lim}]` = {groups[lim]}',
        'ans = 0': '按组累加答案，各组之间互不影响',
        'for lim, a in groups.items()': '处理 `limit = {lim}` 这一组，价值是 {a}',
        'if lim < len(a)': lambda S, B, r: (f'组里有 `{len(S.a)}` 个，但最多只能选 `{S.lim}` 个 → ==需要挑最大的=={S.lim}==个==' if S.lim < len(S.a)
                                          else f'组里只有 `{len(S.a)}` 个，不超过 `{S.lim}` → 全都能选，不用排序'),
        'a.sort()': '从小到大排序，最大的几个在末尾：`a` = {a}',
        'a = a[-lim:]': '只留最大的 `{lim}` 个：`a` = =={a}==',
        'ans += sum(a)': '这组贡献 `sum(a)` = {sum(a)}，`ans` = =={ans}==',
        'return ans': '各组独立，总和就是答案 `{ans}`',
    },
    cards=dict(
        one_liner='limit 相同的分一组，每组选最大的 limit 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['激活元素 `i` 要求当前活跃数 `< limit[i]`，激活得 `value[i]`',
                 '激活后活跃数为 x，所有 `limit[j] <= x` 的元素永久失效',
                 '示例：`value=[4,1,5,2], limit=[3,3,2,3]` → `12`'],
        quote='所以按照 limit[i] 从小到大选是最优的。……所以本题只需把 limit[i] 相同的价值分到同一组。同一组内取最大的 limit[i] 个价值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先选 limit 大的，limit 小的可能就没法选了 → ==从小到大选==',
              '选了 lim 个后，同组剩下的也会失效，所以每组最多选 `lim` 个',
              '不同组之间无关：==组内取最大的 lim 个==即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；用快速选择可到 `O(n)`',
                 '`lim >= len(a)` 时整组都能选，不用排序（Python3 优化写法）',
                 '切片 `a[-lim:]` 取末尾 lim 个，lim 不会为 0（`limit >= 1`）',
                 '另有写法：直接 `sum(nlargest(lim, a))`'],
    ),
)
