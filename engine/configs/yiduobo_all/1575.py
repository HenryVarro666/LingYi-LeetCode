def _cell(S, r, c, v):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if i is None or j is None or k is None or S.get('_line', 0) < 10:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    L = S['locations']
    src = i + abs(L[j] - L[k])
    if src <= S['fuel'] and (r, c) == (src, k):
        return 'blue'
    return None


def _fml(S):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if i is None or j is None or k is None or S.get('_line', 0) < 10:
        return '`f[i][j]`：油箱还剩 `i` 升、停在城市 `j` 的方案数'
    L = S['locations']
    d = abs(L[j] - L[k])
    return f'`f[{i}][{j}] += f[{i}+|{L[j]}−{L[k]}|][{k}] = f[{i + d}][{k}]`：从城市 {k} 走到 {j} 花 {d}'


CONFIG = dict(
    num=1575, title='统计所有可行路径', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[剩余油量][城市] 倒序枚举油量',
    tags=[],
    code='''
class Solution(object):
    def countRoutes(self, locations, start, finish, fuel):

        n = len(locations)
        f = [[0] * n for _ in range(fuel + 1)]
        f[fuel][start] = 1
        mod = 10 ** 9 + 7
        for i in range(fuel - 1, -1, -1):
            for j in range(n):
                for k in range(n):
                    if j != k and i + abs(locations[j] - locations[k]) <= fuel:
                        f[i][j] += f[i + abs(locations[j] - locations[k])][k]
                        f[i][j] %= mod
        
        res = 0
        for i in range(fuel, -1, -1):
            res += f[i][finish]
            res %= mod
        
        return res
''',
    call='Solution().countRoutes([4, 3, 1], 1, 0, 6)',
    expect=5,
    skip=['for j in range(n)', 'for k in range(n)', 'if j != k', 'f[i][j] %= mod', 'res %= mod', 'mod = '],
    max_steps=40,
    views=[
        dict(type='array', var='locations', label='locations（城市位置，粉 = j 目的地，蓝 = k 出发地）', h=230, cell=90,
             pointers={'j': 'pink', 'k': 'blue'},
             color=lambda S, i, v: 'green' if i == S.get('finish') and S.get('_line', 0) < 8 else None),
        dict(type='text', fn=_fml, size=22, h=60),
        dict(type='table', var='f', label='f[i][j]（行 = 剩余油量 i，列 = 城市 j；黄 = 正在算，蓝 = 来源）', h=380, cell=80,
             rows=lambda S: [f'油{r}' for r in range(len(S['f']))], cols=lambda S: [f'城{c}' for c in range(len(S['f'][0]))],
             color=_cell),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'pink'), ('k', 'k', 'blue'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}` 个城市',
        'f = [[0]': '`f[i][j]`：油箱剩 `i` 升、最后停在城市 `j` 的方案总数，先全 0',
        'f[fuel][start] = 1': '出发时油是满的 `{fuel}` 升，在城市 `{start}`：方案 1 种',
        'for i in range(fuel - 1': lambda S, B, r: (f'`i = {S.i}`：油量从大到小，因为每走一步油只会变少，来源都在更大的油量行' if 'i' in S and S.get('i') != B.get('i') else '油量枚举完了'),
        'f[i][j] += f': '城 `{k}` → 城 `{j}` 花 `{abs(locations[j] - locations[k])}` 升，加上 `f[{i + abs(locations[j] - locations[k])}][{k}] = {f[i + abs(locations[j] - locations[k])][k]}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'res = 0': '终点 `{finish}` 可以在任意剩余油量下停下，把所有行加起来',
        'res += f[i][finish]': '加上油 `{i}` 升停在终点的 `{f[i][finish]}` 种 → `res` = =={res}==',
        'return res': '一共 =={ret}== 条路径',
    },
    cards=dict(
        one_liner='f[i][j]：剩 i 升油停在城市 j，枚举上一个城市',
        complexity='时间 `O(fuel·n²)`，空间 `O(fuel·n)`',
        problem=['`locations[i]` 是城市位置，从 `start` 出发到 `finish`，从 i 去 j 花 `|locations[i] − locations[j]|` 升油',
                 '油量不能为负，可以多次经过任一城市（含起终点），求路径数，对 `10^9 + 7` 取模',
                 '示例：`[4,3,1], start=1, finish=0, fuel=6` → `5`（题面为我据题意补写）'],
        quote='令f[i][j]表示邮箱里还剩i升油，最后走到位置j的方案总数，那么首先就有f[fuel][start] = 1，其他的f则初始化为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 由「上一个城市 k、油更多」转移来：`f[i + |loc[j] − loc[k]|][k]`',
              '来源油量更大，所以油量从大到小枚举',
              '终点可在任意剩余油量停下，最后把 `f[·][finish]` 全加起来'],
        summary=['时间 `O(fuel·n²)`，空间 `O(fuel·n)`',
                 '`j != k` 不能漏：题目不允许原地不动',
                 '答案要累加所有剩余油量的 `f[i][finish]`，不是只看 `f[0]`',
                 '原文提到可拆成向左/向右两个方向用前缀和优化，但作者并未实现',
                 '简报缺少题面，题意按 LeetCode 原题补写；原文代码已是 Python 3 写法'],
    ),
)
