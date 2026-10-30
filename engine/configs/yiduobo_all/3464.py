CONFIG = dict(
    num=3464, title='正方形上的点之间的最大距离', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='拉直成环 + 二分 + 动态规划',
    tags=['二分算法', '难度分 2806'],
    code='''
class Solution(object):
    def maxDistance(self, side, points, k):
        
        dis = []
        for x, y in points:
            if x == 0:
                dis.append(y)
            elif y == side:
                dis.append(side + x)
            elif x == side:
                dis.append(side * 2 + side - y)
            else:
                dis.append(side * 3 + side - x)
        
        dis.sort()

        left = 1
        right = side
        while left < right:
            mid = (left + right + 1) // 2
            f = [1]
            start = [0]
            pre = 0
            flag = False
            for index in range(1, len(points)):
                while dis[index] - dis[pre] >= mid:
                    pre += 1
                
                if pre > 0:
                    f.append(f[pre - 1] + 1)
                    start.append(start[pre - 1])
                    if f[-1] >= k and side * 4 - dis[index] + dis[start[index]] >= mid:
                        flag = True
                        break
                else:
                    f.append(1)
                    start.append(index)

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maxDistance(3, [[0,0],[0,2],[2,3],[3,3],[3,0]], 4)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"二分答案 `mid` = =={S['mid']}==：能否选 `{S['k']}` 个点，相邻（含首尾）距离都 ≥ `{S['mid']}`" if 'mid' in S else f"二分区间 `[{S.get('left')}, {S.get('right')}]`")),
        dict(type='array', var='dis', label='dis：周长拉直后的坐标（周长 = side×4 = 12，环形）', h=170,
             pointers={'index': 'blue', 'pre': 'pink'},
             color=lambda S, i, v: 'green' if 'f' in S and i < len(S['f']) and S['f'][i] >= S['k'] else None),
        dict(type='array', var='f', label='f[i]：以 dis[i] 结尾最多能选几个点', h=150, pointers={}),
        dict(type='array', var='start', label='start[i]：那串点的第一个点的下标', h=150, pointers={}),
    ],
    watch=['left', 'right', ('mid', 'mid', 'yellow'), ('index', 'index', 'blue'), ('pre', 'pre', 'pink'), ('flag', 'flag', 'green')],
    captions={
        'dis = []': '把点顺时针拉直成直线上的下标，存进 `dis`',
        'dis.append(y)': '左边的点 `(0, y)`：下标就是 `y`',
        'dis.append(side + x)': '上边的点：先走完左边 `side`，再往右走 `x`',
        'dis.append(side * 2 + side - y)': '右边的点：已走 `side*2`，再从右上角向下走 `side - y`',
        'dis.append(side * 3 + side - x)': '下边的点：已走 `side*3`，再从右下角向左走 `side - x`',
        'dis.sort()': '排序后 `dis = {dis}`：问题变成在环形数组里选 k 个点，使相邻距离最小值最大',
        'left = 1': '答案下界 `left = 1`',
        'right = side': '答案上界 `right = side`（k ≥ 4 时答案不会超过边长）',
        'while left < right': lambda S, B, r: (f'答案在 `[{S.left}, {S.right}]`（下界 1，上界 side：k ≥ 4 时答案不超过边长）→ 继续二分' if S.left < S.right else f'`left = {S.left} ≥ right = {S.right}` → 答案确定'),
        'mid = (left + right + 1) // 2': '猜 `mid = {mid}`（上取整，保证 `left = mid` 时区间会缩小）。每个 mid 重新建 `f`（以 i 结尾最多选几个点）和 `start`（首点下标）',
        'f = [1]': '`f[i]`：以第 i 个点结尾最多能选几个点，`f[0] = 1`（选最左的点）',
        'start = [0]': '`start[i]`：那一串点里第一个点的下标，用来检查首尾距离',
        'pre = 0': '`pre` 指针：dis[pre] 之前的点离当前点都 ≥ mid',
        'flag = False': '`flag` 记录这个 `mid` 能否做到',
        'for index in range': '考虑第 `{index}` 个点，`dis[{index}] = {dis[index]}`',
        'while dis[index] - dis[pre] >= mid': lambda S, B, r: (f'考虑 `dis[{S.index}] = {S.dis[S.index]}`：`{S.dis[S.index]} - {S.dis[S.pre]} = {S.dis[S.index] - S.dis[S.pre]} ≥ mid = {S.mid}` → `pre` 这个点够远，试试更靠后的'
                                                              if S.dis[S.index] - S.dis[S.pre] >= S.mid else f'`{S.dis[S.index]} - {S.dis[S.pre]} < mid = {S.mid}` → `pre` 停在 {S.pre}：它是最靠后的够远点的后一个'),
        'pre += 1': '`pre` 右移到 {pre}（单调不减，所以整体只走一遍）',
        'if pre > 0': lambda S, B, r: ('x `pre - 1`，可以接在它后面' if S.pre > 0 else '`pre = 0`：前面没有够远的点，只能自己开头'),
        'f.append(f[pre - 1] + 1)': '第 `{index}` 个点：`f[{index}] = f[{pre - 1}] + 1 = {f[-1]}`，接在最靠后的够远点后面，首点同它 `start = {start[-1]}`',
        'start.append(start[pre - 1])': '首点跟着前驱走：`start[{index}] = {start[-1]}`',
        'if f[-1] >= k and': lambda S, B, r: (f"`f = {S.f[-1]}`，首尾距离 `side*4 - {S.dis[S.index]} + {S.dis[S.start[S.index]]} = {S.side * 4 - S.dis[S.index] + S.dis[S.start[S.index]]}`，"
                                              f"与 `mid = {S.mid}` 比：" + ('选够 k 个且首尾也够远 → ==成功==' if S.f[-1] >= S.k and S.side * 4 - S.dis[S.index] + S.dis[S.start[S.index]] >= S.mid else '还不满足')),
        'flag = True': '找到一组最小距离 ≥ mid 的点，`flag = True`',
        'f.append(1)': '第 `{index}` 个点：`f[{index}] = 1`，自己做第一个点，`start[{index}] = {index}`',
        'start.append(index)': '`start[{index}] = {index}`：首点就是自己',
        'if flag': lambda S, B, r: (f'`mid = {S.mid}` 可行 → 答案至少 mid：`left = mid` = {S.mid}' if S.flag else f'`mid = {S.mid}` 不可行 → 答案小于 mid：`right = mid - 1` = {S.mid - 1}'),
        'left = mid': '`left` → {left}',
        'right = mid - 1': '`right` → {right}',
        'return left': '`left = {left}`：最小距离的最大值',
    },
    skip=['if x == 0', 'elif y == side', 'elif x == side', 'break', 'f = [1]', 'start = [0]', 'pre = 0', 'flag = False', 'start.append', 'for index in range', 'for x, y in points', 'left = 1', 'right = side', 'pre += 1', 'if pre > 0', 'flag = True', 'left = mid', 'right = mid - 1'],
    max_steps=140,
    cards=dict(
        one_liner='拉直成环，二分答案，用 DP 数出最多能选几个点',
        complexity='时间 `O(n log side)`，空间 `O(n)`',
        problem=['正方形边长 `side`，`points` 是边界上互不相同的点，选 `k` 个点',
                 '使任意两点的==最小曼哈顿距离==最大，返回这个最大值',
                 '本视频：`side=3`，5 个点，`k=4` → `2`'],
        quote='将这些点从正方形左下角开始，按顺时针顺序拉直成一直线，问题就变成了给出一个循环的下标数组，需要从中选出k个点。',
        quote_src='—— yiduobo 题解原文',
        idea=['反证法：最小距离必出现在顺时针相邻的两点之间 → 拉直成环',
              '二分 `mid`；`f[i]` = 以 i 结尾最多选几个点，从最靠后的够远点转移',
              '`start[i]` 记首点，检查绕一圈的首尾距离 ≥ mid'],
        summary=['时间 `O(n log side)`：`pre` 指针单调，每个 mid 只扫一遍',
                 '易错点：环形要检查首尾距离；`f` 单调不减，所以取最靠后的够远点',
                 '二分用上取整 `mid = (left + right + 1) // 2`，对应 `left = mid`',
                 '对比灵神：灵神二分后用 bisect 贪心找下一个点，yiduobo 用 DP + 指针'],
    ),
)
