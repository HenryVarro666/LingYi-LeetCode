CONFIG = dict(
    num=1564, title='把箱子放进仓库里 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前缀最小值 + 排序 + 从右放起',
    code='''
class Solution(object):
    def maxBoxesInWarehouse(self, boxes, warehouse):

        now = warehouse[0]
        h_list = [now]
        for w in warehouse[1:]:
            now = min(now, w)
            h_list.append(now)
            
        boxes.sort()
        p = 0
        res = 0
        for h in h_list[::-1]:
            if boxes[p] <= h:
                res += 1
                p += 1
                if p == len(boxes):
                    break
        
        return res
''',
    call='Solution().maxBoxesInWarehouse([4, 3, 4, 1], [5, 3, 3, 4, 1])',
    expect=3,
    views=[
        dict(type='array', var='warehouse', label='warehouse：每列的天花板高度', cell=90, h=190),
        dict(type='array', var='h_list', label='h_list：每列真正能放的最大高度（前缀最小值）', cell=90, h=190),
        dict(type='array', var='boxes', label='boxes（从矮到高排序），p = 下一个要放的箱子', cell=90, h=200,
             pointers={'p': 'blue'}, color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None),
        dict(type='text', fn=lambda S: f"当前列高度 `h = {S['h']}`" if 'h' in S and S.get('_line', 0) >= 14 else '', size=32, h=70),
    ],
    watch=['now', 'p', ('h', 'h', 'yellow'), ('res', 'res', 'green')],
    captions={
        'now = warehouse[0]': '最左边的列最先进入，它的高度 `{now}` 就是它能放的上限',
        'h_list = [now]': '`h_list` 记录每一列实际能放的高度',
        'for w in warehouse[1:]': '箱子只能从左往右推，要经过左边所有的列',
        'now = min(now, w)': '这一列能放多高，取决于它和左边所有列的==最小值==：`min` → =={now}==',
        'h_list.append(now)': '`h_list` = {h_list}（从左到右不增，所以反过来看就是递增）',
        'boxes.sort()': '要放尽量多的箱子 → ==先放矮的==：`boxes` 排序后 = {boxes}',
        'p = 0': '`p` 指向下一个要放的、最矮的箱子',
        'for h in h_list[::-1]': '从右往左扫每一列：右边的列更矮，用来放矮箱子，把高的列留给后面的高箱子',
        'if boxes[p] <= h': lambda S, B, r: (f'箱子 `{S.boxes[S.p]}` <= 列高 `{S.h}`：放得下' if S.boxes[S.p] <= S.h else f'箱子 `{S.boxes[S.p]}` > 列高 `{S.h}`：这一列放不下，看更靠左（更高）的一列'),
        'res += 1': '放进去一个：`res` → =={res}==',
        'p += 1': '换下一个更高的箱子：`p` → {p}',
        'if p == len(boxes)': lambda S, B, r: (f'`p = {S.p}` 等于箱子总数：箱子全放完了 → 提前结束' if S.p == len(S.boxes) else f'`p = {S.p}`，还有箱子没放，继续'),
        'return res': '最多放进 `{res}` 个箱子',
    },
    cards=dict(
        one_liner='每列的上限是左侧最小值，矮箱子先放、从右往左放',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`boxes[i]` 是箱子高度，`warehouse[j]` 是第 j 个房间的高度',
                 '箱子不能叠放，只能从左边进入仓库、向右推，被矮房间挡住就进不去',
                 '本视频：`boxes = [4,3,4,1]`，`warehouse = [5,3,3,4,1]` → `3`'],
        quote='仓库中的每一列可以放置的最大高度取决于该列以及其左侧所有列中的最小高度。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟从左到右做前缀最小值 `h_list`，得到每列真实可放高度',
              '只要求个数最多 → ==先放矮箱子==，箱子从小到大排序',
              '`h_list` 从右往左是递增的：遇到能放下当前箱子的最右一列就放，不行再看左边'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：必须用前缀最小值，不能直接用 `warehouse`',
                 '从右往左扫时列高只增不减，所以放不下当前箱子的列直接跳过即可',
                 '原文已是 Python 3 可运行，仅删去了类型说明文档字符串'],
    ),
)
