NEEDS = [2, 2]
INF = '∞'


def _slice(S):
    f = S.get('f')
    if f is None:
        return None
    return [[(INF if f[a][b][0][0][0][0] is None else f[a][b][0][0][0][0]) for b in range(NEEDS[1] + 1)]
            for a in range(NEEDS[0] + 1)]


def _cell(S, r, c, v):
    line = S.get('_line')
    if line not in (28, 29, 30, 31) or 'y0' not in S or 'x0' not in S:
        return None
    if (r, c) == (S['y0'], S['y1']):
        return 'yellow'
    if (r, c) == (S['y0'] - S['x0'], S['y1'] - S['x1']):
        return 'green'
    return None


def _cases(S):
    if 'case' not in S or 'cost' not in S:
        return None
    return [[c[0], c[1], S['cost'][k] if k < len(S['cost']) else '?'] for k, c in enumerate(S['case'])]


def _case_color(S, r, c, v):
    if 'index' in S and S.get('_line', 0) >= 20 and r == S['index']:
        return 'yellow'
    return None


def _formula(S):
    line = S.get('_line', 0)
    if line >= 28 and line <= 31 and 'y0' in S:
        return (f'目标 `({S["y0"]}, {S["y1"]})` ← 来源 `({S["y0"] - S["x0"]}, {S["y1"] - S["x1"]})` + 价格 `{S["cost"][S["index"]]}`'
                f'（物品 `{S["index"]}` = ({S["x0"]}, {S["x1"]})）')
    return '`f[y0][y1]` = 买到 y0 件 A、y1 件 B 的最少花费（`∞` = 还没算出）；其余 4 维恒为 0'


def _cap_if1(S, B, ret):
    src = S.f[S.y0 - S.x0][S.y1 - S.x1][S.y2 - S.x2][S.y3 - S.x3][S.y4 - S.x4][S.y5 - S.x5]
    if src is None:
        return f'来源状态 `({S.y0 - S.x0}, {S.y1 - S.x1})` 还凑不出（`None`）→ ==没法转移==，跳过'
    return f'来源状态 `({S.y0 - S.x0}, {S.y1 - S.x1})` 已有最小花费 `{src}`，再加物品 {S.index}（价格 {S.cost[S.index]}）→ `{src + S.cost[S.index]}`'


def _cap_if2(S, B, ret):
    cur = S.f[S.y0][S.y1][S.y2][S.y3][S.y4][S.y5]
    if cur is None:
        return f'`tmp = {S.tmp}`：目标 `({S.y0}, {S.y1})` 还是 `None`（没凑过）→ ==直接更新=='
    if cur > S.tmp:
        return f'`tmp = {S.tmp}`，`{cur} > {S.tmp}`：新方案更便宜 → ==更新=='
    return f'`tmp = {S.tmp}`，`{cur} <= {S.tmp}`：已有方案不贵于新方案 → 保持不变'


CONFIG = dict(
    num=638, title='大礼包', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='多维背包 DP（把礼包当物品）',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def shoppingOffers(self, price, special, needs):

        needs = needs + [0] * (6 - len(needs))
        case = []
        cost = []
        for index in range(len(price)):
            tmp = [0] * 6
            tmp[index] = 1
            case.append(tmp)
            cost.append(price[index])
        for index in range(len(special)):
            cost.append(special[index][-1])
            tmp = special[index][:-1]
            tmp += [0] * (6 - len(tmp))
            case.append(tmp)

        f = [[[[[[None] * 7 for _ in range(7)] for _ in range(7)] for _ in range(7)] for _ in range(7)] for _ in range(7)]
        f[0][0][0][0][0][0] = 0
        for index in range(len(case)):
            x0, x1, x2, x3, x4, x5 = case[index]
            for y0 in range(x0, needs[0] + 1):
                for y1 in range(x1, needs[1] + 1):
                    for y2 in range(x2, needs[2] + 1):
                        for y3 in range(x3, needs[3] + 1):
                            for y4 in range(x4, needs[4] + 1):
                                for y5 in range(x5, needs[5] + 1):
                                    if f[y0 - x0][y1 - x1][y2 - x2][y3 - x3][y4 - x4][y5 - x5] is not None:
                                        tmp = f[y0 - x0][y1 - x1][y2 - x2][y3 - x3][y4 - x4][y5 - x5] + cost[index]
                                        if f[y0][y1][y2][y3][y4][y5] is None or f[y0][y1][y2][y3][y4][y5] > tmp:
                                            f[y0][y1][y2][y3][y4][y5] = tmp

        return f[needs[0]][needs[1]][needs[2]][needs[3]][needs[4]][needs[5]]
''',
    call='Solution().shoppingOffers([2, 5], [[2, 0, 3], [1, 2, 10]], [2, 2])',
    expect=12,
    skip=['case = []', 'cost = []', 'tmp = f[y0', 'case.append(tmp)', 'cost.append(price', 'cost.append(special', 'tmp = [0] * 6', 'tmp[index] = 1', 'tmp = special', 'tmp += [0]', 'for y0', 'for y1', 'for y2', 'for y3', 'for y4', 'for y5'],
    max_steps=110, max_events=600000,
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var=_slice, label='f[y0][y1]：最少花费（黄 = 目标，绿 = 来源）', h=330, cell=90,
             rows=['A=0', 'A=1', 'A=2'], cols=['B=0', 'B=1', 'B=2'], color=_cell),
        dict(type='table', var=_cases, label='物品表：单品与礼包（A 件数, B 件数, 价格）', h=300, cell=80,
             rows=['单品 A', '单品 B', '礼包 1', '礼包 2'], cols=['A', 'B', '价格'], color=_case_color),
    ],
    watch=[('index', 'index', 'pink'), ('(y0,y1)', '(y0, y1)', 'yellow'), ('tmp', 'tmp', 'green'), ('needs', 'needs[:2]', 'blue')],
    captions={
        'needs = needs': '`needs` 补齐到 6 维（最多 6 种商品），后面几维全是 0',
        'for index in range(len(price))': lambda S, B, r: ('单买商品 `%d` 当成一个物品：数量向量 `%s`，价格 `%d`' % (S.index, S.case[S.index][:2] if False else [1 if k == S.index else 0 for k in range(2)], S.price[S.index])
                                                          if S.index != B.get('index') else '所有单品都放进物品表了'),
        'for index in range(len(special))': lambda S, B, r: ('礼包 `%d`：内容 `%s`，==最后一个数 %d 是价格==，补 0 到 6 维后也当成物品' % (S.index, S.special[S.index][:-1], S.special[S.index][-1])
                                                            if S.index != B.get('index') or B.get('index') is None else '礼包也都放进物品表了：共 `%d` 个物品' % len(S.case)),
        'f = [[[': '建一个 6 维表，`f[y0]..[y5]` = 这六样商品分别买 y0..y5 件的最少花费，初值 `None`（凑不出）',
        'f[0][0][0][0][0][0] = 0': '边界：一件都不买，花费 `0`',
        'for index in range(len(case))': lambda S, B, r: ('枚举物品 `%d`：内容 `%s`，价格 `%d`；==外层物品、内层状态==，正序枚举所以同一物品可重复买（完全背包）' % (
            S.index, S.case[S.index][:2], S.cost[S.index]) if S.index != B.get('index') or B.get('index') is None else '所有物品都处理完了'),
        'x0, x1, x2': '这个物品含 `({x0}, {x1})` 件 A、B；`y` 从 `x` 开始枚举（买得比物品还少就用不上它）',
        'is not None:': _cap_if1,
        'is None or': _cap_if2,
        'f[y0][y1][y2][y3][y4][y5] = tmp': '`f[{y0}][{y1}] = {tmp}`',
        'return f[needs': '目标 `f[{needs[0]}][{needs[1]}]` = =={ret}==：买 {needs[0]} 件 A、{needs[1]} 件 B 的最少花费',
    },
    cards=dict(
        one_liner='把礼包当物品，6 维状态做背包',
        complexity='时间 `O(物品数 × 7^6)`（按 needs 缩小），空间 `O(7^6)`',
        problem=['商店有若干商品及价格 `price`，还有一些大礼包 `special`（最后一个数是礼包价格）',
                 '每种商品要买的数量是 `needs`，不能多买；求最少花多少钱，礼包可以重复使用',
                 '示例：`price=[2,5], special=[[2,0,3],[1,2,10]], needs=[2,2]`（演示用）→ `12`'],
        quote='典型的背包问题，不过这里的状态维度很多，我选择的就是强行做一个7维的动态规划……状态f[y0][y1][y2][y3][y4][y5]表示这六样商品分别有y0、y1、y2、y3、y4、y5件最少要多少钱，然后枚举每个单个商品或者礼包进行状态转移。',
        quote_src='—— yiduobo 题解',
        idea=['单买一种商品、一个礼包都当成「物品」：一个数量向量 + 一个价格',
              '`f[y]` 表示凑出数量向量 `y` 的最少花费；用物品 `x` 转移：`f[y] = min(f[y-x] + 价格)`',
              '`y` 从 `x` 开始枚举，保证 `y - x` 不越界；正序枚举所以物品可重复使用'],
        summary=['商品种类最多 6 种，所以固定开 6 维；多出的维度 `needs` 补 0',
                 '`None` 表示凑不出：转移前要判断来源非 `None`，比较前要判断目标是否 `None`',
                 '易错：礼包最后一个数是价格，不是数量；`special[index][:-1]` 才是数量',
                 '本题没有 Python 2 专有写法，代码原样运行；视频只展示前 2 维的切片，其余维恒为 0'],
    ),
)
