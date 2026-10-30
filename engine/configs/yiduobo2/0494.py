NUMS = [1, 2, 1]
TARGET = 2
SN = sum(NUMS)
COLS = list(range(-SN, SN + 1))


def _table(E):
    f = E.get('f')
    if f is None:
        return None
    rows = []
    for i in range(len(NUMS)):
        if i < len(f):
            rows.append([f[i].get(j, '') for j in COLS])
        else:
            rows.append([''] * len(COLS))
    return rows


def _color(E, r, c, v):
    j = COLS[c]
    if E.get('_line') == 16 and 'j' in E and 'i' in E:
        i, jj, x = E['i'], E['j'], NUMS[E['i']]
        if r == i and j == jj:
            return 'yellow'
        if r == i - 1 and j == jj - x:
            return 'blue'
        if r == i - 1 and j == jj + x:
            return 'pink'
    if E.get('_line') == 18 and r == len(NUMS) - 1 and j == TARGET:
        return 'green'
    return 'green' if isinstance(v, int) and v > 0 else None


def _text(E):
    if E.get('_line') == 16 and 'j' in E:
        i, j, f = E['i'], E['j'], E['f']
        x = NUMS[i]
        a, b = f[i - 1].get(j - x, 0), f[i - 1].get(j + x, 0)
        return f'`f[{i}][{j}]` = 加上 {x}：`f[{i - 1}][{j - x}]`={a} + 减去 {x}：`f[{i - 1}][{j + x}]`={b} = =={a + b}=='
    return '`f[i][j]`：前 `i+1` 个数（`nums[0..i]`）能得到 `j` 的情况总数'


def _cap_cell(E, B, ret):
    i, j, f = E.i, E.j, E.f
    x = E.nums[i]
    a, b = f[i - 1].get(j - x, 0), f[i - 1].get(j + x, 0)
    head = f'第 {i} 个数 `{x}`：' if j == -E.sum_nums else ''
    if a == 0 and b == 0:
        return head + f'`f[{i}][{j}]`：上一行得到 `{j - x}`、`{j + x}` 的都是 0 种 → `0`'
    return head + f'`f[{i}][{j}] = f[{i - 1}][{j - x}] + f[{i - 1}][{j + x}] = {a} + {b} = {a + b}`'


CONFIG = dict(
    num=494, title='目标和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='类背包 DP：f[i][j] 用 dict 存',
    tags=['热题173'],
    code='''
class Solution(object):
    def findTargetSumWays(self, nums, S):
        sum_nums = sum(nums)

        f = []
        f.append({})
        if nums[0] == 0:
            f[0][0] = 2
        else:
            f[0][nums[0]] = 1
            f[0][-nums[0]] = 1

        for i in range(1, len(nums)):
            f.append({})
            for j in range(-sum_nums, sum_nums + 1):
                f[i][j] = f[i - 1].get(j - nums[i], 0) + f[i - 1].get(j + nums[i], 0)

        return f[len(nums) - 1].get(S, 0)
''',
    call=f'Solution().findTargetSumWays({NUMS}, {TARGET})',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums', cell=84, h=140,
             color=lambda E, i, v: 'yellow' if i == (E['i'] if 'i' in E else (0 if 7 <= E.get('_line', 0) <= 11 else -1)) else None),
        dict(type='grid', var=_table, label='f（行 = i，列 = 能得到的和 j；黄 = 当前，蓝 = 加上 nums[i]，粉 = 减去 nums[i]）',
             rows=list(range(len(NUMS))), cols=COLS, cell=82, h=420, color=_color),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('nums[i]', 'nums[i]'), 'sum_nums'],
    skip=['for j in range', 'f.append({})', 'f = []'],
    captions={
        'sum_nums = sum': '`sum_nums = {sum_nums}`：能得到的和一定在 `[-{sum_nums}, {sum_nums}]` 之间',
        'if nums[0] == 0': '初始化 `f[0]`：要注意 `nums[0] = 0` 的情况（`+0` 和 `-0` 是两种）',
        'f[0][0] = 2': '`nums[0] = 0`：`+0`、`-0` 都得到 0 → 2 种',
        'f[0][nums[0]] = 1': '`nums[0] = {nums[0]}`：加上它得到 `{nums[0]}`，1 种',
        'f[0][-nums[0]] = 1': '减去它得到 `-{nums[0]}`，1 种',
        'for i in range(1': lambda E, B, ret: (f'处理第 `i = {E.i}` 个数 `{E.nums[E.i]}`：新建 `f[{E.i}]`'
                                               if 'i' not in B or B.i != E.i else '所有数处理完'),
        'f[i][j] = ': _cap_cell,
        'return f[len(nums) - 1]': '答案是 `f[{len(nums) - 1}][{S}]` = =={ret}==',
    },
    cards=dict(
        one_liner='每个数要么加要么减：f[i][j] = f[i-1][j-x] + f[i-1][j+x]',
        complexity='时间 `O(n · sum)`，空间 `O(n · sum)`',
        problem=['给每个数前面添 `+` 或 `-`，串起来得到表达式',
                 '求运算结果等于 `S` 的==不同表达式数目==',
                 '示例：`[1,1,1,1,1]`，`S = 3` → `5`',
                 '演示：`[1,2,1]`，`S = 2` → `2`（`+1+2-1`、`-1+2+1`）'],
        quote='可以将每个数字看成独立的个体，于是题目就与背包问题很类似了……f[i][j] = f[i - 1][j - nums[i]] + f[i - 1][j + nums[i]]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 `i` 个数能得到 `j` 的情况总数',
              '当前这次操作要么==加上== `nums[i]`，要么==减去== `nums[i]`',
              '`j` 可能是负数 → 用==一维数组套 dict==，`.get(key, 0)` 顺便处理边界'],
        summary=['时间 `O(n · sum)`，空间 `O(n · sum)`（只依赖上一轮，可以滚动）',
                 '易错：初始化 `f[0]` 时 `nums[0] = 0` 要记 2 种，否则会被覆盖成 1',
                 '原文：j 的数值大小是杂乱的，所以只能用 01 式滚动',
                 '原文为 Python 2 风格，参数名 `S` 未改，只删去了类型说明文档字符串',
                 '对比灵神：先推出 `q = (S − |target|) / 2`，转成 0-1 背包，状态更少'],
    ),
)
