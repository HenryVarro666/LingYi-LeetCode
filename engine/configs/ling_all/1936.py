CONFIG = dict(
    num=1936, title='新增的最少台阶数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='贪心 · 相邻差 ceil(d/dist)-1（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def addRungs(self, rungs: List[int], dist: int) -> int:
        ans = 0
        pre = 0
        for h in rungs:
            d = h - pre
            if d > dist:
                ans += (d - 1) // dist  # 等价于 ceil(d / dist) - 1
            pre = h
        return ans
''',
    call='Solution().addRungs([1,3,5,10,11], 2)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"这一级 `{S['h']}` − 上一级 `{S['pre']}` = 差 `{S['h'] - S['pre']}`，`dist = {S['dist']}`" if 'h' in S and 'pre' in S else ''), h=90),
        dict(type='array', var='rungs', pointers={'rungs.index(h)': 'blue'}, pointer_labels={'rungs.index(h)': 'h'}, label='rungs（地板高度 0 为起点）', h=300,
             color=lambda S, i, v: 'blue' if 'h' in S and S['rungs'][i] == S['h'] else ('green' if 'h' in S and S['rungs'][i] < S['h'] else None)),
        dict(type='text', fn=lambda S: f"已新增 ==`{S['ans']}`== 个台阶", h=80),
    ],
    watch=[('pre', 'pre', 'pink'), ('h', 'h', 'blue'), 'd', 'dist', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '答案从 `0` 开始累加',
        'pre = 0': '`pre` 是上一个落脚点，一开始站在==地板 0==',
        'for h in rungs': '下一级台阶高度 `h = {h}`',
        'd = h - pre': '要爬的高度差 `d = {h} - {pre}` = =={d}==',
        'if d > dist': lambda S, B, ret: (f"`d = {S.d}` > `dist = {S.dist}`：一步够不着，==要补台阶==" if S.d > S.dist
                                          else f"`d = {S.d}` ≤ `dist = {S.dist}`：一步就能爬上去，不用补"),
        'ans += ': '间隔 `{d}`，每步最多 `{dist}`：==补 ceil({d}/{dist}) − 1 = ({d}−1)//{dist} = {(d - 1) // dist}== 个，`ans = {ans}`',
        'pre = h': '落脚到 `h`：`pre = {pre}`，继续看下一级',
        'return ans': '所有间隔处理完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='每个间隔 d 补 ceil(d/dist)−1 个台阶',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['梯子高度 `rungs` 严格递增，每次最多爬 `dist`，可在任意整数高度补台阶',
                 '从地板 0 出发，求爬到最后一级最少补几个台阶',
                 '示例：`rungs = [1,3,5,10]`，`dist = 2` → `2`'],
        quote='`ans += (d - 1) / dist // 等价于 ceil(d / dist) - 1`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['间隔 `d` 被各台阶分段，互不影响，逐段独立计算',
              '一段间隔 `d > dist` 时，最少要走 `ceil(d/dist)` 步，其中最后一步落在原有台阶上',
              '所以要补 `ceil(d/dist) - 1`，整数写法 `(d-1)//dist`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：起点是地板 `0`，第一级也要算间隔',
                 '`d == dist` 时 `(d-1)//dist = 0`，不用补；向上取整技巧 `(d-1)//dist`'],
    ),
)
