NUMS = [0, 2, 3, 9]
QS = [[3, 0], [1, 2], [2, 0]]
QI = "len(res) if _line >= 33 else None"


def _q(S):
    if 'res' not in S:
        return '先算每个位置向左、向右走一步的代价，再做前缀和 / 后缀和'
    return '询问：' + '，'.join(f'`{q[0]}→{q[1]}`' for q in S['queries'])


CONFIG = dict(
    num=3919, title='在下标间移动的最小代价', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='不走回头路 · 一步步走 + 前后缀和',
    tags=['前缀和', '进阶', '难度分 1777'],
    code='''
class Solution(object):
    def minCost(self, nums, queries):
        
        n = len(nums)
        to_left = [0] * n
        to_right = [0] * n

        for index in range(n):
            if index == 0:
                to_left[index] = 0
                to_right[index] = 1
            elif index == n - 1:
                to_right[index] = 0
                to_left[index] = 1
            else:
                left_dis = nums[index] - nums[index - 1]
                right_dis = nums[index + 1] - nums[index]
                if left_dis <= right_dis:
                    to_left[index] = 1
                    to_right[index] = right_dis
                else:
                    to_left[index] = left_dis
                    to_right[index] = 1

        suffix = [0]
        for index in range(n - 1, 0, -1):
            suffix.append(suffix[-1] + to_left[index])
        suffix.reverse()

        prefix = [0]
        for index in range(n - 1):
            prefix.append(prefix[-1] + to_right[index])
        
        res = []
        for x, y in queries:
            if x < y:
                res.append(prefix[y] - prefix[x])
            elif x == y:
                res.append(0)
            else:
                res.append(suffix[y] - suffix[x])
        
        return res
''',
    call=f'Solution().minCost({NUMS!r}, {QS!r})',
    expect=[4, 1, 3],
    views=[
        dict(type='table', var=lambda S: [S['nums'], S['to_left'], S['to_right']] if 'to_right' in S else [S['nums']],
             rows=['nums', '左一步', '右一步'], cols=lambda S: list(range(len(S['nums']))), cell=90, h=260,
             label='nums；to_left / to_right = 每个位置向左 / 向右走一步的代价',
             color=lambda S, i, j, v: 'blue' if i > 0 and S.get('_line', 0) < 25 and j == S.get('index') else None),
        dict(type='table', var=lambda S: [S.get('suffix', []), S.get('prefix', [])],
             rows=['后缀', '前缀'], cols=lambda S: list(range(len(S['nums']))), cell=90, h=200,
             label='suffix[i]：i 一步步走到 0；prefix[i]：0 一步步走到 i'),
        dict(type='text', h=60, size=26, fn=_q),
        dict(type='text', h=60, size=28, fn=lambda S: ('res = `' + str(S['res']) + '`') if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'to_left = [0]': '`to_left[i]`：从 `i` 往左走一步的代价',
        'to_right = [0]': '`to_right[i]`：从 `i` 往右走一步的代价',
        'if index == 0': lambda S, B, r: '`index = 0` 是左端：只能往右走，往右一步 closest 代价 1' if S.index == 0 else '`index != 0`，不是左端',
        'elif index == n - 1': lambda S, B, r: f'`index = {S.index}` 是右端：只能往左走，往左一步代价 1' if S.index == S.n - 1 else f'`index = {S.index}` 不是右端，是中间位置，两边都有邻居',
        'left_dis =': '`left_dis` = 左邻差 {left_dis}',
        'right_dis =': '`right_dis` = 右邻差 {right_dis}',
        'if left_dis <= right_dis': '`{left_dis} <= {right_dis}`？相等取较小下标 → closest 是左边 → ==往左一步花 1，往右要付差值==',
        'to_left[index] = left_dis': '`closest` 指向右边：往左不能用方式二，付差值 `{left_dis}`；往右花 1',
        'to_right[index] = right_dis': '`closest` 是左边：往右付差值 `{right_dis}`；往左花 1',
        'suffix.append': '`suffix` 从右往左累加 `to_left`：`{suffix}`',
        'suffix.reverse': '翻转后 `suffix[i]` = 从 `i` 一步步走到 0 的代价：`{suffix}`',
        'prefix.append': '`prefix` 累加 `to_right`：`{prefix}`',
        'res.append(prefix': '`x < y` 向右走：`prefix[{y}] − prefix[{x}]` = =={res[-1]}==',
        'res.append(0)': '`x == y`，不用走：=={res[-1]}==',
        'res.append(suffix': '`x > y` 向左走：`suffix[{y}] − suffix[{x}]` = =={res[-1]}==',
    },
    cards=dict(
        one_liner='不走回头路、不跳跃：从 l 一步步走到 r',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['递增数组：可以直接跳（付差值），或者走到最近下标（付 1）',
                 '每个询问 `[l, r]` 求 `l` 到 `r` 的最小代价',
                 '示例：`[0,2,3,9]`，`[[3,0],[1,2],[2,0]]` → `[4,1,3]`'],
        quote='综合起来，就可以得到的结论，不走回头路。……对于每组询问最优的走法就是从l出发一步一步走到r。',
        quote_src='—— yiduobo 题解原文',
        idea=['走回头路必有往返的无用功；跳跃的差值等于一步步的差值之和',
              '先算每个位置向左、向右走一步的代价（closest 只要 1）',
              '正反各做前缀和，`l<r` 用 `prefix`，`l>r` 用 `suffix`'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '相邻差相等时 closest 取左边，所以往右要付差值',
                 '两端位置只有一个方向，代价单独处理',
                 '对比灵神：灵神在一个循环里同时算两个前缀和；这里先分别算单步代价'],
    ),
)
