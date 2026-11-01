CONFIG = dict(
    num='LCP 39', title='无人机方阵', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 颜色计数抵消（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def minimumSwitchingTimes(self, source: List[List[int]], target: List[List[int]]) -> int:
        cnt = defaultdict(int)
        for i, row in enumerate(source):
            for j, v in enumerate(row):
                cnt[v] += 1
                cnt[target[i][j]] -= 1
        ans = 0
        for c in cnt.values():
            ans += abs(c)
        return ans // 2
''',
    call='Solution().minimumSwitchingTimes([[1,3],[5,4]], [[3,1],[6,5]])',
    expect=1,
    views=[
        dict(type='grid', var='source', label='source（蓝框 = 当前格）', cell=90, h=230,
             cursors=[('i', 'j', 'blue')]),
        dict(type='grid', var='target', label='target', cell=90, h=230,
             cursors=[('i', 'j', 'pink')]),
        dict(type='map', var='cnt', label='cnt（source 中次数 − target 中次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('c', 'c', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict(int)': '位置可以随便换，所以只看==每种颜色的数量==；`cnt[颜色]` = source 里的个数 − target 里的个数',
        'for i, row in enumerate(source)': lambda S, B, r: (f'第 `{S.i}` 行' if 'i' not in B or S.i != B.i else '所有行都扫完了'),
        'for j, v in enumerate(row)': lambda S, B, r: (f'看 `source[{S.i}][{S.j}] = {S.v}`' if 'j' not in B or S.j != B.j or S.i != B.i else '这一行扫完了'),
        'cnt[v] += 1': 'source 里有一架颜色 `{v}` 的无人机：`cnt[{v}] = {cnt[v]}`',
        'cnt[target[i][j]] -= 1': 'target 同一格需要一架颜色 `{target[i][j]}` 的，减一：`cnt[{target[i][j]}] = {cnt[target[i][j]]}`（正 = source 多，负 = source 缺，0 = 抵消）',
        'ans = 0': lambda S, B, r: ('两个方阵都统计完：`cnt` 里非 0 的就是数量对不上的颜色：'
                                    + '，'.join(f'{k}→{v}' for k, v in S.cnt.items() if v != 0)),
        'for c in cnt.values()': lambda S, B, r: (f'看这个颜色的差值 `c = {S.c}`' if 'c' in S else '差值都累加完了'),
        'ans += abs(c)': '`ans += |{c}|` → `{ans}`：正数是多出来的，负数是缺的，各算一次',
        'return ans // 2': '一架无人机换色会同时消掉一个“多”和一个“缺”，所以 `{ans} // 2` = =={ans // 2}==',
    },
    cards=dict(
        one_liner='位置随便换，只剩颜色数量不一致的部分需要换色；多和缺成对出现，除以 2',
        complexity='时间 `O(nm)`，空间 `O(nm)`（颜色种数）',
        problem=['`source`、`target` 是两个 `n×m` 的颜色矩阵，无人机位置可以任意调整',
                 '只有切换灯光颜色才耗能，求最少切换几架',
                 '本视频：`[[1,3],[5,4]]` → `[[3,1],[6,5]]`，答案 `1`'],
        quote='func minimumSwitchingTimes(source, target [][]int) (ans int) { cnt := map[int]int{} ...',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['既然位置任意，问题就是比较两个颜色的多重集',
              '`cnt[v]` 对 source 加一、对 target 减一，一遍扫完',
              '每种颜色 `|cnt|` 求和，再除以 2'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（命名返回值 `ans` → 显式 `ans = 0`，自定义 `abs` → 内置 `abs`）',
                 '时间 `O(nm)`，空间 `O(nm)`',
                 '易错：差值总和是“多出来的 + 缺的”，一架无人机同时解决一对，所以要除以 2',
                 '用 `defaultdict` 保证没出现过的颜色从 0 开始'],
    ),
)
