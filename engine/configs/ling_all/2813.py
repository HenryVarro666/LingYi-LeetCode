CONFIG = dict(
    num=2813, title='子序列最大优雅度', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='利润排序 + 反悔贪心（重复类别栈）',
    tags=['堆（优先队列）', '反悔贪心', '难度分 2640'],
    code='''
class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda p: -p[0])  # 把利润从大到小排序
        ans = total_profit = 0
        vis = set()
        duplicate = []  # 重复类别的利润
        for i, (profit, category) in enumerate(items):
            if i < k:
                total_profit += profit  # 累加前 k 个项目的利润
                if category not in vis:
                    vis.add(category)
                else:  # 重复类别
                    duplicate.append(profit)
            elif duplicate and category not in vis:  # 之前没有的类别
                vis.add(category)  # len(vis) 变大
                total_profit += profit - duplicate.pop()  # 用最小利润替换
            # else: 比前面的利润小，而且类别还重复了，选它只会让 total_profit 变小，len(vis) 不变，优雅度不会变大
            ans = max(ans, total_profit + len(vis) * len(vis))
        return ans
''',
    call='Solution().findMaximumElegance([[5,3],[9,1],[6,2],[7,1],[8,1]], 3)',
    expect=29,
    views=[
        dict(type='text', fn=lambda S: (f"优雅度 = 总利润 `{S['total_profit']}` + 类别数² `{len(S['vis'])}²` = ==`{S['total_profit'] + len(S['vis'])**2}`==" if 'vis' in S and 'total_profit' in S else '优雅度 = 总利润 + 不同类别数²'), size=26),
        dict(type='array', var="[f'{p}/{c}' for p, c in items]", label='items（利润/类别，按利润从大到小；前 k 个先选上）', h=220, cell=96,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if 'i' in S and i < S['k'] else None)),
        dict(type='set', var='vis', label='vis：已选的类别', h=150),
        dict(type='stack', var='duplicate', label='duplicate：重复类别的利润（栈顶最小，可被替换）', h=200),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'pink'), ('total_profit', 'total_profit', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'items.sort': '利润从大到小排序：先选前 `k` 个，之后再靠“反悔”换类别 → {items}',
        'ans = total_profit': '`ans` 记最大优雅度，`total_profit` 是已选利润和',
        'vis = set()': '`vis` 记已选项目出现过的类别',
        'duplicate = []': '`duplicate` 栈：已选项目里「类别重复」的利润，越靠后越小',
        'for i, (profit': '看第 `{i}` 个项目：利润 `{profit}`，类别 `{category}`',
        'if i < k': lambda S, B, r: (f'`i = {S.i} < k = {S.k}`：还在前 k 个里 → 先全选上' if S.i < S.k else f'`i = {S.i} ≥ k = {S.k}`：已选满 k 个，要选它就得先移除一个'),
        'total_profit += profit  # 累加': '前 k 个全选：`total_profit` → =={total_profit}==',
        'if category not in vis': lambda S, B, r: (f'类别 `{S.category}` 没出现过 → 加入 `vis`' if S.category not in S.vis else f'类别 `{S.category}` 已经有了 → 它是重复类别'),
        'vis.add(category)\n': '`vis` 现在是 {vis}',
        'duplicate.append': '重复类别的利润 `{profit}` 入栈：{duplicate}',
        'elif duplicate and': lambda S, B, r: (f'有重复可换，且类别 `{S.category}` 是新类别 → ==选它，类别数 +1==' if S.duplicate and S.category not in S.vis else ('没有可换的重复项目 → 跳过' if not S.duplicate else f'类别 `{S.category}` 已有：利润更小、类别数不变 → 选它没意义')),
        'vis.add(category)  # len': '类别数变大：`len(vis) = {len(vis)}`',
        'total_profit += profit - duplicate.pop()': '弹出最小的重复利润 `{B.duplicate[-1]}`，换成 `{profit}`：`total_profit` → =={total_profit}==',
        'ans = max': '当前优雅度 `{total_profit} + {len(vis)}² = {total_profit + len(vis)**2}`，`ans` → =={ans}==',
        'return ans': '最大优雅度 =={ans}==',
    },
    cards=dict(
        one_liner='先选利润最大的 k 个，再用新类别换掉重复项里最小的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`items[i] = [利润, 类别]`，选 `k` 个项目作为子序列',
                 '优雅度 = ==总利润 + 不同类别数的平方==，求最大值',
                 '本视频：`[[5,3],[9,1],[6,2],[7,1],[8,1]]`，`k=3` → `29`'],
        quote='如果第 k+1 个项目和前面任何已选项目的类别都不一样……如果移除的项目的类别重复出现多次，那么选第 k+1 个项目后，distinctCategories 会增加一……能让 distinctCategories 增加就立刻选上！',
        quote_src='—— 灵茶山艾府题解',
        idea=['按利润降序，先选前 `k` 个：总利润此时最大',
              '之后的利润只会更小，只有==带来新类别==才值得换',
              '换掉谁？类别重复的里利润最小的，用栈 `duplicate` 取栈顶',
              '每步都算一次优雅度，取最大'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：被移除的必须是重复类别的项目，否则类别数一减一增没收益',
                 '前 k 个遇到重复类别入栈 `duplicate`，之后换一个就弹一个',
                 '每处理完一个项目都要更新 `ans`，包括没选的那一步（不影响结果）',
                 '同类：§1.9 反悔贪心；思考题是类别数恰为 1..k 的最大优雅度'],
    ),
)
