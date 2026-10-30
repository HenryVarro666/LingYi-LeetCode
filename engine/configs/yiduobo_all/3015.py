def _info(S):
    if 'circle_len' not in S:
        return '把图拆成三块：==环==（x 到 y）、==主链==（1 到 n）、==挂在环两端的小尾巴=='
    n, x, y, c = S['n'], S['x'], S['y'], S['circle_len']
    s = f'环：`{x}…{y}`，长度 `{c}`，环内最大距离 `{c // 2}`'
    if 'chain_len' in S:
        s += f'　链长 `{S["chain_len"]}`'
    return s


CONFIG = dict(
    num=3015, title='按距离统计房屋对数目 I', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拆成环+链+尾巴 · 差分数组',
    tags=['灵神题单·图论算法', '难度分 1658'],
    code='''
class Solution(object):
    def countOfPairs(self, n, x, y):

        if x > y:
            x, y = y, x
        
        if y - x <= 1:
            return [(index - 1) * 2 for index in range(n, 0, -1)]
        
        delta = [0] * (n + 1)
        circle_len = y - x + 1
        circle_dis_max = circle_len // 2
        delta[1] += circle_len * 2
        delta[circle_dis_max + 1] -= circle_len
        if circle_len % 2 == 0:
            delta[circle_dis_max] -= circle_len
        else:
            delta[circle_dis_max + 1] -= circle_len
        
        chain_len = x - 1 + n - y + 2
        for index in range(1, chain_len):
            delta[1] += 2
            delta[chain_len - index + 1] -= 2
        delta[1] -= 2
        delta[2] += 2

        for index in range(x - 1, 0, -1):
            delta[x - index + 1] += 2
            delta[x - index + circle_dis_max + 1] -= 2
            delta[x - index + 2] += 2
            if circle_len % 2 == 0:
                delta[x - index + circle_dis_max] -= 2
            else:
                delta[x - index + circle_dis_max + 1] -= 2

        for index in range(y + 1, n + 1):
            delta[index - y + 1] += 2
            delta[index - y + circle_dis_max + 1] -= 2
            delta[index - y + 2] += 2
            if circle_len % 2 == 0:
                delta[index - y + circle_dis_max] -= 2
            else:
                delta[index - y + circle_dis_max + 1] -= 2

        v = 0
        res = []
        for index in range(1, n + 1):
            v += delta[index]
            res.append(v)
        
        return res
''',
    call='Solution().countOfPairs(6, 2, 5)',
    expect=[12, 12, 6, 0, 0, 0],
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='delta', label='delta[d]：差分数组，下标 d = 距离（0 号位不用）', cell=100, h=240,
             color=lambda S, i, v: 'yellow' if v else None),
        dict(type='array', var='res', label='res[d-1]：距离为 d 的房屋对数（delta 前缀和）', cell=100, h=240,
             color=lambda S, i, v: 'green'),
    ],
    watch=[('index', 'index', 'blue'), ('circle_len', 'circle_len', 'cyan'), ('chain_len', 'chain_len', 'orange'), ('v', 'v', 'green')],
    skip=['circle_dis_max = ', 'res.append(v)', 'res = []'],
    captions={
        'if x > y': '规定 `x < y`，不满足就交换，不影响结果',
        'x, y = y, x': '交换后 `x = {x}`，`y = {y}`',
        'if y - x <= 1': lambda S, B, ret: ('`y - x <= 1`：近路等于没有 → 只是一条直线' if S.y - S.x <= 1
                                            else f'`y - x = {S.y - S.x} > 1`：近路有效，进入「环 + 链 + 尾巴」分类计算'),
        'return [(index - 1)': '直线 `n` 个点：距离 `d` 有 `n-d` 对，乘 2 是有序对，答案 `{ret}`',
        'delta = [0]': '`delta` 是差分数组：「距离 `1..k` 各加 1」只需改两个位置，最后前缀和求值',
        'circle_len = ': '第一块：环 `x…y`，长度 `{circle_len}`；环里最大距离 `circle_len // 2 = {circle_dis_max}`',
        'delta[1] += circle_len * 2': '环里每个点向两个方向走：距离 `1..` 各 `{circle_len*2}` 个有序对（先把 `1` 起的区间加上）',
        'delta[circle_dis_max + 1] -= circle_len': '先把超过最大距离的部分减掉：`delta[{circle_dis_max + 1}] -= {circle_len}`',
        'if circle_len % 2 == 0': lambda S, B, ret: (f'环长 `{S.circle_len}` 是==偶数==：每个点只有一个对角点，最大距离那档只有 `circle_len` 对，所以多扣一次' if S.circle_len % 2 == 0
                                                     else f'环长 `{S.circle_len}` 是==奇数==：两个方向都能走满最大距离，不用多扣'),
        'delta[circle_dis_max] -= circle_len': '偶数环：最大距离 `{circle_dis_max}` 这档少一半 → `delta[{circle_dis_max}] -= {circle_len}`',
        'chain_len = ': '第二块：主链 `1…x` 加 `y…n`，共 `{chain_len}` 个点（`x` 和 `y` 靠近路直连）',
        'for index in range(1, chain_len)': '把主链看成一条直线，按「还剩几个点在后面」一条条加',
        'delta[1] += 2': '主链上第 `{index}` 个点往后看：距离 `1…{chain_len - index}` 各加 2 对（有序）',
        'delta[chain_len - index + 1] -= 2': '区间到距离 `{chain_len - index}` 为止：`delta[{chain_len - index + 1}] -= 2`',
        'delta[1] -= 2': '`x` 和 `y` 这一对，环里数了一次、链里又数了一次 → 距离 1 要扣 2',
        'delta[2] += 2': '只扣距离 1 这一档，所以从 2 起加回去',
        'delta[x - index + 1] += 2': '尾巴点 `{index}` 先走 `{x - index}` 步到 `x`，再走环：距离从 `{x - index + 1}` 开始各加 2 对',
        'delta[x - index + circle_dis_max + 1] -= 2': '环内最远 `{circle_dis_max}` 步 → 到距离 `{x - index + circle_dis_max}` 为止',
        'delta[x - index + 2] += 2': '环的另一个方向：区间起点在 `{x - index + 2}`（`x`、`y` 本身已算过，跳过一档）：`+= 2`',
        'delta[x - index + circle_dis_max] -= 2': '偶数环：另一个方向的终点少一档，`delta[{x - index + circle_dis_max}] -= 2`',
        'delta[index - y + 1] += 2': '尾巴点 `{index}` 先走 `{index - y}` 步到 `y`，再走环：距离从 `{index - y + 1}` 开始各加 2 对',
        'delta[index - y + circle_dis_max + 1] -= 2': '环内最远 `{circle_dis_max}` 步 → 到距离 `{index - y + circle_dis_max}` 为止',
        'delta[index - y + 2] += 2': '环的另一个方向：区间起点在 `{index - y + 2}`（`x`、`y` 本身已算过，跳过一档）：`+= 2`',
        'delta[index - y + circle_dis_max] -= 2': '偶数环：另一个方向的终点少一档，`delta[{index - y + circle_dis_max}] -= 2`',
        'for index in range(x - 1, 0, -1)': '第三块：左尾巴的点 `index`：先走 `x - index` 步到 `x`，再走环',
        'for index in range(y + 1, n + 1)': '第三块：右尾巴的点 `index`：先走 `index - y` 步到 `y`，再走环',
        'v = 0': '三块都叠加好了，最后用前缀和还原每个距离的对数',
        'v += delta[index]': '`v += delta[{index}]` → `{v}`：距离 `{index}` 的有序对共 =={v}== 对，记入 `res`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='把图拆成「环、链、尾巴」三块，每块用差分数组区间加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['房屋 `1..n` 排成一条街，相邻房屋有街道，另有一条 `x - y` 的近路',
                 '对每个 `k`，求最短距离恰好为 `k` 的房屋对数（有序对）',
                 '示例：`n=5, x=2, y=4` → `[10,8,2,0,0]`',
                 '本视频：`n=6, x=2, y=5` → `[12,12,6,0,0,0]`'],
        quote='可以发现，从每个节点出发的距离都必然是连续的，那么对于从某个点出发的距离为1到k的结果，可以视为在答案数组中的1到k中每个数都加上1，这是一个非常典型的静态区间修改，最后单点求值的情况，是非常适合用差分数组的。',
        quote_src='—— yiduobo 题解原文',
        idea=['加上近路后，图 = ==环== `x…y` + ==链== + 挂在环两端的==尾巴==',
              '环里的距离靠环长奇偶分类：偶数环最大距离那档只有一半',
              '尾巴上的点：先走到 `x`（或 `y`）再走环 → 区间整体右移',
              '三块都用差分数组加好，最后一次前缀和得到答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（3017 题数据大，同一思路可过）',
                 '易错：`y - x <= 1` 时近路无效，直接返回直线结果',
                 '易错：环长奇偶不同，最大距离那档的个数不同',
                 '易错：`x→y` 这条边在环与链里各算一次，要扣掉重复',
                 '本题数据很小，也可以直接对每个点做 BFS（灵神题解思路）'],
    ),
)
