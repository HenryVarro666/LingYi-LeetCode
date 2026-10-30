CONFIG = dict(
    num=1580, title='把箱子放进仓库里 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='正反前缀最小 · 排序双指针',
    code='''
class Solution(object):
    def maxBoxesInWarehouse(self, boxes, warehouse):

        now = warehouse[0]
        left = [now]
        for w in warehouse[1:]:
            now = min(now, w)
            left.append(now)
        
        n = len(warehouse)
        now = warehouse[n - 1]
        right = [now]
        for index in range(n - 2, -1, -1):
            w = warehouse[index]
            now = min(now, w)
            right.append(now)
        
        right.reverse()

        h_list = sorted([max(left[index], right[index]) for index in range(n)])
        p = 0
        boxes.sort()

        res = 0
        for h in h_list:
            if boxes[p] <= h:
                res += 1
                p += 1
                if p == len(boxes):
                    break
        
        return res
''',
    call='Solution().maxBoxesInWarehouse([1,2,2,3,4], [3,4,1,2])',
    expect=4,
    views=[
        dict(type='array', var='warehouse', label='warehouse（每个房间的高度）', cell=80, h=140),
        dict(type='array', var=lambda S: S.get('left'), label='left（从左边进，每列能放的最高箱子）', cell=80, h=140,
             color=lambda S, i, v: 'cyan'),
        dict(type='array', var=lambda S: S.get('right'), label='right（从右边进；先倒着算，最后 reverse）', cell=80, h=140,
             color=lambda S, i, v: 'orange'),
        dict(type='array', var=lambda S: S.get('h_list'), label='h_list（每列取左右较大值后排序）', cell=80, h=140,
             pointers={}, color=lambda S, i, v: 'green' if 'res' in S and i < S.get('res', 0) else None),
        dict(type='array', var=lambda S: S.get('boxes') if 'h_list' in S else None, label='boxes（排序后，p 指向下一个要放的箱子）',
             cell=80, h=140, pointers={'p': 'pink'}, dim=lambda S, i, v: i < S.get('p', 0)),
    ],
    watch=[('now', 'now', 'cyan'), ('p', 'p', 'pink'), ('h', 'h', 'blue'), ('res', 'res', 'green')],
    captions={
        'now = warehouse[0]': '从左边进：第 0 列最高就是 `warehouse[0] = {now}`',
        'now = min(now, w)': '箱子要一路挤过去，高度 ≤ 沿途最矮的房间：`now = min({B.now}, {w}) = {now}`',
        'left.append': '`left` 记下这一列从左边能放的最高 `{now}`',
        'n = len': '`n = {n}`',
        'now = warehouse[n - 1]': '从右边进：最右列最高就是 `{now}`',
        'w = warehouse[index]': '倒着看第 `{index}` 列，房间高 `{w}`',
        'right.append': '`right` 记下从右边进能放的最高 `{now}`',
        'right.reverse': '`right` 是倒着算的，反转后下标就和 `warehouse` 对齐：`{right}`',
        'h_list = sorted': '每列从左或右进都行，取较大的：排序后 `h_list` = =={h_list}==',
        'p = 0': '`p` 指向最小的还没放的箱子',
        'boxes.sort': '箱子也从小到大排：`{boxes}`',
        'res = 0': '`res` 统计放进去的箱子数',
        'for h in h_list': '看可放高度 `{h}` 的这一列',
        'if boxes[p] <= h': lambda S, B, r: (f"最小的箱子 `{S.boxes[S.p]}` ≤ `{S.h}` → 能放进这一列" if S.boxes[S.p] <= S.h
                                              else f"最小的箱子 `{S.boxes[S.p]}` > `{S.h}` → 放不下，这一列作废，看下一列"),
        'res += 1': '放进去一个，`res` = {res}',
        'p += 1': '`p` 后移到 {p}，下一个更大的箱子',
        'if p == len': lambda S, B, r: ('箱子都放完了 → 提前结束' if S.p == len(S.boxes) else f'还剩箱子（`p = {S.p}` < {len(S.boxes)}），继续'),
        'return res': '最多放进 `{res}` 个箱子',
    },
    cards=dict(
        one_liner='先算每列能放多高，再让小箱子配矮房间',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n)`',
        problem=['`boxes[i]` 是箱子高度，`warehouse[j]` 是仓库第 `j` 个房间高度，房间并排成一行',
                 '箱子可以==从左或右==推进去，遇到比它矮的房间就被挡住；箱子不能叠放，顺序随意',
                 '求最多能放几个箱子；本视频：`boxes=[1,2,2,3,4]`，`warehouse=[3,4,1,2]` → `4`'],
        quote='如果箱子从左侧进去，那么每一列可以放置的最高的箱子就可以按照之前相同的方式进行计算，推广到从右侧进去，就可以通过正反两趟遍历得到每一列可能放置的最高的箱子是多高。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左进：每列能放的最高 = 左边（含自身）房间高度的前缀最小值；从右进同理',
              '每列取左右两边较大的那个，就是这列的可放高度',
              '可放高度和箱子高度都从小到大排序，用单调性一趟配对：放不下就换下一列'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(n)`',
                 '`right` 是倒着算的，必须 `reverse()` 才能和下标对齐',
                 '箱子和房间都排序后，矮房间放不下最小箱子，就不可能放下更大的',
                 '本题是 1564（只能从一侧进）的强化版',
                 '代码与原文一致，无需修改'],
    ),
)
