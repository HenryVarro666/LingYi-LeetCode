CONFIG = dict(
    num=1620, title='网络信号最好的坐标', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力枚举坐标',
    code='''
class Solution(object):
    def bestCoordinate(self, towers, radius):
        res = [0, 0]
        max_c = 0
        for x in range(0, 101):
            for y in range(0, 101):
                tot = 0
                for tx, ty, q in towers:
                    tmp = (x - tx) ** 2 + (y - ty) ** 2
                    if tmp > radius ** 2:
                        continue
                    
                    tot += int(q / (1 + sqrt(tmp)))

                if tot > max_c:
                    max_c = tot
                    res = [x, y]
        
        return res
''',
    setup='''from math import sqrt
_range = range
def range(a, b):
    return _range(a, 3 if b == 101 else b)
''',
    call='Solution().bestCoordinate([[1,2,5],[2,1,7]], 2)',
    expect=[2, 1],
    views=[
        dict(type='table', var='towers', rows=['塔 0', '塔 1', '塔 2'], cols=['x', 'y', '质量 q'], h=170, cell=110),
        dict(type='text', fn=lambda S: (f"枚举坐标 `({S['x']}, {S['y']})`，当前信号 `tot = {S.get('tot', 0)}`" if 'x' in S and 'y' in S else ''), size=28),
        dict(type='text', fn=lambda S: (f"最优：坐标 `{S['res']}`，信号 ==`{S['max_c']}`==" if 'res' in S and 'max_c' in S else ''), size=28),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'tx', 'ty', 'tmp', 'tot', ('max_c', 'max_c', 'green'), ('res', 'res', 'green')],
    captions={
        'res = [0, 0]': '答案坐标先设 `[0, 0]`',
        'max_c = 0': '`max_c` 记录目前最大信号，初始 0',
        'for x in range': lambda S, B, r: ('所有横坐标都枚举完了' if B.get('x') == S.x and B.get('x') is not None else '') or f'枚举横坐标 `x = {S.x}`（真实范围 0..100，视频里缩成 0..2）',
        'for y in range': lambda S, B, r: (f'枚举纵坐标 `y = {S.y}`，位置 `({S.x}, {S.y})`' if B.get('y') != S.y or B.get('x') != S.x else f'`x = {S.x}` 这一列的 y 都枚举完了'),
        'tot = 0': '新位置，信号总和清零',
        'for tx, ty, q in towers': lambda S, B, r: (f'看信号塔：位置 `({S.tx}, {S.ty})`，质量 `{S.q}`' if B.get('tx') != S.tx or B.get('tmp') is None or B.get('q') != S.q or B.get('x') != S.x or B.get('y') != S.y else f'所有塔都看完了，累计信号 `tot = {S.tot}`'),
        'tmp = (x - tx)': '到塔的距离平方 `tmp` = `({x}-{tx})^2 + ({y}-{ty})^2` = =={tmp}==，不开根号先比较半径',
        'if tmp > radius ** 2': lambda S, B, r: (f'`{S.tmp} > {S.radius}^2 = {S.radius ** 2}` → 超出半径，信号塔不可达，跳过' if S.tmp > S.radius ** 2 else f'`{S.tmp} <= {S.radius}^2 = {S.radius ** 2}` → 在半径内，塔有信号'),
        'continue': '超出半径，这座塔对该点没有贡献',
        'tot += int(q / (1 + sqrt(tmp)))': '塔在范围内：贡献 `floor(q / (1 + d))` = `int({q} / (1 + {sqrt(tmp):.2f}))`，`tot` → =={tot}==',
        'if tot > max_c': lambda S, B, r: (f'`tot = {S.tot} > max_c = {S.max_c}` → 比目前最好的强，更新' if S.tot > S.max_c else f'`tot = {S.tot} <= max_c = {S.max_c}` → 不更优（相等时保留字典序更小的，所以不更新）'),
        'max_c = tot': '最大信号更新为 =={max_c}==',
        'res = [x, y]': '最佳坐标更新为 `{res}`',
        'return res': '全部坐标枚举完：答案 `{res}`',
    },
    skip=['continue', 'tot = 0'],
    max_steps=62,
    cards=dict(
        one_liner='坐标范围很小，直接枚举每个整数点算信号',
        complexity='时间 `O(101 × 101 × m)`，空间 `O(1)`',
        problem=['给出信号塔 `[x, y, q]` 和有效半径 `radius`，距离 `d <= radius` 的塔在该点贡献 `floor(q / (1 + d))`',
                 '求信号总和最大的整数坐标；并列时取字典序最小',
                 '示例：`[[1,2,5],[2,1,7]]`，`radius = 2` → `[2,1]`'],
        quote='这里有向下取整的操作，同时要求坐标为正数，看样子是不能这么做。不过注意到题目数据的规模比较小，那么可以直接枚举坐标系里面的每一个整数坐标，然后计算该位置的网络信号，取其中最大值作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['乍看是最优化问题，但有取整、坐标必须是整数，不能用连续方法',
              '数据规模小：枚举 `0..100` 的每个整数点',
              '每个点累加范围内各塔的信号，用 `tot > max_c`（严格大于）保证并列时坐标靠前'],
        summary=['时间 `O(101² × m)`，空间 `O(1)`',
                 '易错：先比较距离平方与 `radius²`，避免开方；取整要对单个塔的信号取整，不是对总和',
                 '严格大于才更新，所以并列时保留字典序更小的坐标',
                 '原文用到 `sqrt`，视频 setup 里补了 `from math import sqrt`；为控制步数，setup 把 `range(0, 101)` 缩成 `range(0, 3)`，作者代码一字未改'],
    ),
)
