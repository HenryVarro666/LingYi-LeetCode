def _idx(S):
    if 'x' not in S or 'lane1' not in S:
        return None
    for i, (a, b) in enumerate(zip(S['lane1'], S['lane2'])):
        if a == S['x'] and b == S['y']:
            return i
    return None


def _cur(S, i, v):
    return 'yellow' if _idx(S) == i else None


def _txt(S):
    if 'x' not in S:
        return '`f`/`g`/`h` = 变道 0 / 1 / 2 次、刚好走到当前英里时的最大收益'
    return (f"`f`（还在车道1）= =={S['f']}==　`g`（已变道1次，在车道2）= =={S['g']}==　"
            f"`h`（已变道2次，回车道1）= =={S['h']}==")


CONFIG = dict(
    num=3466, title='最大硬币收集量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三状态 DP（变道 0/1/2 次）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def maxCoins(self, lane1, lane2):
        
        f, g, h = 0, 0, 0
        res = None

        for x, y in zip(lane1, lane2):
            h = max(g, h) + x
            g = max(f, g, 0) + y
            f = max(f, 0) + x
            max_v = max(f, g, h)
            if res is None or res < max_v:
                res = max_v
        
        return res
''',
    call='Solution().maxCoins([4,-3,-2,5,1], [-1,6,5,-4,-2])',
    expect=21,
    views=[
        dict(type='array', var='lane1', label='lane1（车道 1：只能从这里上高速）', h=190, cell=96,
             pointers={'index': lambda S: _idx(S)}, color=_cur),
        dict(type='array', var='lane2', label='lane2（车道 2）', h=190, cell=96,
             pointers={'index': lambda S: _idx(S)}, color=_cur),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('f', 'f', 'cyan'), ('g', 'g', 'orange'),
           ('h', 'h', 'purple'), ('res', 'res', 'green')],
    captions={
        'f, g, h = 0, 0, 0': '三个状态都从 0 开始：`f` 变道 0 次、`g` 变道 1 次、`h` 变道 2 次',
        'res = None': '`res` 记录见过的最大收益；收益可能全为负，所以不能从 0 起算',
        'for x, y in zip': lambda S, B, r: ('所有英里都走完了，循环结束' if 'x' in B and B.x == S.x and B.y == S.y
                                            else f'同时看下一英里：车道1 是 `{S.x}`，车道2 是 `{S.y}`'),
        'h = max(g, h) + x': '`h`：从车道2变回来（`g`={B.g}）或一直在车道1第二段（`h`={B.h}），取大者再吃车道1的 `{x}` → ==`{h}`==',
        'g = max(f, g, 0) + y': '`g`：从车道1变道过来（`f`={B.f}）、继续留在车道2（`g`={B.g}）、或这里上高速立刻变道（0），再吃车道2的 `{y}` → ==`{g}`==',
        'f = max(f, 0) + x': '`f`：接着上一英里（`f`={B.f}）或这里才上高速（0），取大者加 `{x}` → ==`{f}`==；==先算 h、g，再算 f==，它们都要用旧值',
        'max_v = max': '这一英里结束时三种状态的最好成绩：`max({f}, {g}, {h})` = ==`{max_v}`==',
        'if res is None or res < max_v': lambda S, B, r: (
            '`res` 还是 None，直接取' if B.get('res') is None
            else f'`res = {B.get("res")}` {"<" if B.get("res") < S.max_v else "≥"} `max_v = {S.max_v}` → ' + ('==刷新答案==' if B.get('res') < S.max_v else '不更新')),
        'res = max_v': '最优收益更新为 ==`{res}`==',
        'return res': '全程最多硬币 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='用三个变量记「变道 0/1/2 次」，每英里滚动一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两条车道，每英里有硬币：正数得硬币，负数扣硬币',
                 '只能从车道 1 上高速，至少开一英里；最多变道两次，上高速和下高速时可立即变道',
                 '本视频：`[4,-3,-2,5,1]` 与 `[-1,6,5,-4,-2]` → ==21=='],
        quote='经典的子段和问题，不过在这里有两个数组且可以进行切换，那么在这里使用动态规划会更直观点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：变道 0 次、在车道 1：`max(f[i-1], 0) + lane1[i]`，0 表示这里才上高速',
              '`g[i]`：变道 1 次、必在车道 2：`max(f[i-1], g[i-1], 0) + lane2[i]`',
              '`h[i]`：变道 2 次、回车道 1：`max(h[i-1], g[i-1]) + lane1[i]`，答案取三者最大'],
        summary=['时间 `O(n)`，空间 `O(1)`：三个状态只依赖上一英里，滚动变量即可',
                 '更新顺序要 ==h → g → f==，否则 g、h 会读到已被改写的 `f`',
                 '`res` 初值为 None 而不是 0：至少要走一英里，全负时也得选一个',
                 '本质是「最大子段和」的三状态版：每多一次变道多一个状态'],
    ),
)
