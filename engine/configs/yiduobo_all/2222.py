S0 = '001101'


def _idx(S):
    if 'zero' not in S or 'char' not in S:
        return -1
    n = S['zero'] + S['one']
    return n if S.get('_line', 0) <= 8 else n - 1


def _txt(S):
    if 'zero_one' not in S:
        return '一趟扫描，数「前面有多少个 01 / 10」：遇到 0 就能接成 010，遇到 1 就能接成 101'
    return (f"`zero`={S['zero']}　`one`={S['one']}　`zero_one`(01 的个数)={S['zero_one']}　"
            f"`one_zero`(10 的个数)={S['one_zero']}　答案 `res` = =={S['res']}==")


CONFIG = dict(
    num=2222, title='选择建筑的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='统计 01 / 10 子序列的 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1657'],
    code='''
class Solution(object):
    def numberOfWays(self, s):

        res = 0
        zero = one = 0
        zero_one = one_zero = 0
        for char in s:
            if char == '0':
                zero += 1
                one_zero += one
                res += zero_one
            else:
                one += 1
                zero_one += zero
                res += one_zero
        
        return res
''',
    call=f'Solution().numberOfWays({S0!r})',
    expect=6,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前建筑）', h=190, cell=90,
             color=lambda S, i, v: ('blue' if i == _idx(S) else None),
             dim=lambda S, i, v: 0 <= _idx(S) and i > _idx(S)),
        dict(type='text', fn=_txt, size=26, h=110),
        dict(type='text', fn=lambda S: ('遇到 `0`：`010` 的个数 += 前面的 `01` 个数；`10` 的个数 += 前面的 `1` 的个数' if S.get('char') == '0'
                                       else '遇到 `1`：`101` 的个数 += 前面的 `10` 个数；`01` 的个数 += 前面的 `0` 的个数' if S.get('char') == '1' else ''), size=24, h=70),
    ],
    watch=[('zero', 'zero', 'blue'), ('one', 'one', 'pink'), ('zero_one', 'zero_one', 'cyan'), ('one_zero', 'one_zero', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计合法的 `010` / `101` 个数',
        'zero = one = 0': '`zero`/`one`：目前 0 和 1 各出现几次',
        'zero_one = one_zero': '`zero_one`/`one_zero`：目前 `01` / `10` 子序列各有几个',
        'for char in s': lambda S, B, r: ('所有建筑都扫完了' if S['zero'] + S['one'] == len(S['s']) else f"处理第 `{S['zero'] + S['one']}` 栋：`{S['char']}`"),
        'if char ==': '`char = {char}` → ' + '{"当成 010 的结尾 / 10 的结尾" if char == "0" else "当成 101 的结尾 / 01 的结尾"}',
        'zero += 1': '`zero = {zero}`',
        'one += 1': '`one = {one}`',
        'one_zero += one': '这个 0 可以接在前面每个 1 后面组成 `10`：`one_zero += {one}` → ==`{one_zero}`==',
        'zero_one += zero': '这个 1 可以接在前面每个 0 后面组成 `01`：`zero_one += {zero}` → ==`{zero_one}`==',
        'res += zero_one': '这个 0 接在前面 `{zero_one}` 个 `01` 后面，就是 `{zero_one}` 个 `010`：`res` = =={res}==',
        'res += one_zero': '这个 1 接在前面 `{one_zero}` 个 `10` 后面，就是 `{one_zero}` 个 `101`：`res` = =={res}==',
        'return res': '全部扫完，合法方案数 = =={ret}==',
    },
    cards=dict(
        one_liner='010 = 在 01 后面加 0，101 = 在 10 后面加 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 是一排建筑，`0` 是办公楼，`1` 是餐厅',
                 '选 3 栋，要求相邻两栋类型不同，即只能是 `010` 或 `101`',
                 '示例：`s = "001101"` → `6`；`s = "11100"` → `0`'],
        quote='对于010，可以认为是在01这种子序列的基础上添加一个0，同样的，对于101则可以认为是在10的基础上添加一个1。',
        quote_src='—— yiduobo 题解',
        idea=['从左到右扫，维护 `zero`、`one`、`zero_one`（01 的个数）、`one_zero`（10 的个数）',
              '遇到 `0`：`one_zero += one`，并且前面的每个 `01` 都能变成 `010`，`res += zero_one`',
              '遇到 `1`：对称。所有状态只依赖上一轮，四个变量就够，不需要数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`res` 累加的是「不含当前字符」的 `zero_one` / `one_zero`，所以当前字符只能当结尾，不能同时当 01 的中间',
                 '题目没说方案数多大，Python 不会溢出；其他语言要用 64 位',
                 '同类：前后缀分解统计法（枚举中间字符，左右各数一遍）'],
    ),
)
