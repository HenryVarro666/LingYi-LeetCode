CONFIG = dict(
    num=1272, title='删除区间', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='差分 · 扫描边界点',
    code='''
class Solution(object):
    def removeInterval(self, intervals, toBeRemoved):

        points = []
        for x, y in intervals:
            points.append([x, 1])
            points.append([y, -1])
        
        points.append([toBeRemoved[0], -1])
        points.append([toBeRemoved[1], 1])
        points.sort()

        last = None
        now = 0
        res = []
        for x, v in points:
            now += v
            if v == -1 and now == 0:
                res.append([last, x])
            last = x
        
        return res
''',
    call='Solution().removeInterval([[0,2],[3,4],[5,7]], [1,6])',
    expect=[[0, 1], [6, 7]],
    views=[
        dict(type='array', var=lambda S: [f"{p[0]}:{'+' if p[1] > 0 else '-'}1" for p in S['points']] if 'points' in S else None,
             label='points（边界点:增减；输入区间 +1/−1，删除区间反过来）', cell=100, h=190,
             color=lambda S, i, v: 'blue' if 'x' in S and 'v' in S and S['points'].index([S['x'], S['v']]) == i else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"累加 `now` = =={S['now']}==，上一个边界 `last` = {S['last']}" if 'now' in S and 'last' in S else '')),
        dict(type='array', var=lambda S: [f'[{a},{b}]' for a, b in S['res']] if 'res' in S else None,
             label='res（幸存区间）', cell=110, h=170),
    ],
    watch=[('x', 'x'), ('v', 'v'), ('now', 'now', 'blue'), ('last', 'last', 'pink'), ('res', 'res', 'green')],
    skip=['points = []', 'now = 0', 'res = []', 'last = None'],
    captions={
        'points.append([x, 1])': '区间左端 `{x}`：这里开始 +1',
        'points.append([y, -1])': '区间右端 `{y}`：这里 −1',
        'points.append([toBeRemoved[0], -1])': '删除区间 `{toBeRemoved}` 反过来：左端 `{toBeRemoved[0]}` 处 −1',
        'points.append([toBeRemoved[1], 1])': '删除区间右端 `{toBeRemoved[1]}` 处 +1，把它抵消掉的覆盖还回去',
        'points.sort()': '按坐标排序，同坐标时 −1 在前：`{points}`',
        'now += v': '走到边界 `{x}`，累加 `now` = =={now}==',
        'if v == -1 and now == 0': lambda S, B, r: (
            f"`v = -1` 且 `now = 0`：覆盖从 1 掉到 0 → `{S.x}` 是幸存区间的右端" if S.v == -1 and S.now == 0
            else f"`v = {S.v}`，`now = {S.now}`：不是「从 1 变成 0」，没有幸存区间结束"),
        'res.append': '幸存区间：左端是上一个边界 `{last}`，右端是 `{x}` → `[{last}, {x}]`',
        'last = x': '记下当前边界 `last = {x}`，下一个边界来了就是它的右端候选',
        'return res': '幸存区间：`{res}`',
    },
    cards=dict(
        one_liner='区间加一、删除区间减一，扫一遍看覆盖数何时从 1 掉到 0',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['`intervals` 是互不相交的半开区间 `[a, b)`，再给一个要删除的区间 `toBeRemoved`',
                 '删掉被覆盖的部分，按顺序返回剩下的区间',
                 '示例：`[[0,2],[3,4],[5,7]]` 删 `[1,6]` → `[[0,1],[6,7]]`'],
        quote='对于intervals中的区间[x, y)，需要将f[x]加上1，f[y]减去1，而对于toBeRemoved这个区间[x, y），则需要将f[x]减去1，f[y]加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['边界都是整数点，把问题当成「区间加减」的差分',
              '输入区间贡献 +1，删除区间贡献 −1，覆盖数 ==1 的地方才是幸存==',
              '覆盖数从 1 变 0 时，当前点是右端，上一个边界点是左端'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '排序时同一坐标 −1 在前，所以相接的区间不会被误合并',
                 '删除区间的 −1 把覆盖数压到 0 或负数，只有 `v == -1 and now == 0` 才收集区间',
                 '`last` 每个边界都要更新，别只在收集时更新'],
    ),
)
