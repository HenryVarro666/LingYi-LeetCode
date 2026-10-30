CONFIG = dict(
    num=885, title='螺旋矩阵 III', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按步长模拟螺旋行走',
    tags=[],
    code='''
class Solution(object):
    def spiralMatrixIII(self, R, C, r0, c0):

        step = 0
        nowx = r0
        nowy = c0
        res = [[nowx, nowy]]
        while len(res) < R * C:
            step += 1
            for _ in range(step):
                nowy += 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            for _ in range(step):
                nowx += 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            step += 1
            for _ in range(step):
                nowy -= 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            for _ in range(step):
                nowx -= 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
        
        return res
''',
    call='Solution().spiralMatrixIII(2, 3, 0, 1)',
    expect=[[0, 1], [0, 2], [1, 2], [1, 1], [1, 0], [0, 0]],
    views=[
        dict(type='grid', var=lambda S: [[next((k + 1 for k, p in enumerate(S['res']) if p == [i, j]), 0) for j in range(S['C'])] for i in range(S['R'])],
             cursors=[('nowx', 'nowy', 'yellow', '当前')], h=300, label='访问顺序（0 = 还没走到）',
             color=lambda S, i, j, v: 'green' if v else None),
        dict(type='text', fn=lambda S: f"当前步长 `step = {S['step']}`，位置 `({S['nowx']}, {S['nowy']})`，已收集 =={len(S['res'])}== / {S['R'] * S['C']}" if 'step' in S else '', h=60),
    ],
    watch=['step', 'nowx', 'nowy', ('收集数', 'len(res)', 'green')],
    captions={
        'step = 0': '`step` 是当前方向要走的步数，从 0 开始',
        'nowx = r0': '起点 `({r0}, {c0})`，第一个就加入答案',
        'res = [[': '起点是第 1 个访问的格子：`res = {res}`',
        'while len(res)': '已收集 `{len(res)}` 个，共 `{R * C}` 个 → {"继续走" if len(res) < R * C else "收集完毕，结束"}',
        'step += 1': '每转两次方向步长加 1：`step` → =={step}==',
        'nowy += 1': '向右走一步：`nowy` → {nowy}',
        'nowx += 1': '向下走一步：`nowx` → {nowx}',
        'nowy -= 1': '向左走一步：`nowy` → {nowy}',
        'nowx -= 1': '向上走一步：`nowx` → {nowx}',
        'if nowx >= 0': '`({nowx}, {nowy})` 在 {R}×{C} 矩阵内吗？→ {"在，要记录" if 0 <= nowx < R and 0 <= nowy < C else "==出界==，只走不记"}',
        'res.append': '记录 `[{nowx}, {nowy}]`，已收集 {len(res)} 个',
        'return res': '按访问顺序返回 `{ret}`',
    },
    cards=dict(
        one_liner='右、下、左、上走螺旋，步长每转两次方向加 1',
        complexity='时间 `O(max(R,C)^2)`，空间 `O(R*C)`',
        problem=['`R×C` 网格，从 `(r0, c0)` 出发面朝东，顺时针螺旋走',
                 '走出网格外也继续走，按访问顺序返回网格内所有格子的坐标',
                 '本视频：`R=2, C=3, (r0,c0)=(0,1)` → 6 个坐标'],
        quote='每变换两次方向之后走的步长将加1。于是我们可以从1开始模拟整个行走过程，按照右、下、左、上的顺序行走，同时维护当前应该走的步长。',
        quote_src='—— yiduobo 题解原文',
        idea=['步长序列：右 1、下 1、左 2、上 2、右 3、下 3……',
              '每走一步先移动，再判断是否在矩阵内，在才记录',
              '收集满 `R*C` 个格子就停'],
        summary=['时间 `O(max(R,C)^2)`（螺旋可能走出网格很远），空间 `O(R*C)`',
                 '易错：==出界的格子也要继续走==，只是不加入答案',
                 '易错：`step += 1` 放在「右、下」之后和「左、上」之前，各一次',
                 '原文代码已是 Python 3 写法，未做修改'],
    ),
)
