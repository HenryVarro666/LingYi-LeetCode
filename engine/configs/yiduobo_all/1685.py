NUMS = [1, 4, 6, 8, 10]


def _parts(S):
    """(左段, 右段)：本轮 `p += num` 之后才有意义"""
    n, s, p, num, idx = S['n'], S['s'], S['p'], S['num'], S['index']
    return num * (idx + 1) - p, (s - p) - num * (n - idx - 1)


def _formula(S):
    if 'index' not in S or 'p' not in S or 'num' not in S:
        return '`res[i]` = 所有 `|nums[i] − nums[j]|` 之和；数组有序，绝对值可以拆开'
    a, b = _parts(S)
    idx, num = S['index'], S['num']
    if S['_line'] <= PLUS_LINE:
        return f'第 `{idx}` 个数 `{num}`：先把它加进前缀和 `p`'
    return (f'左段 `{num}×{idx + 1} − {S["p"]}` = =={a}==　　右段 `({S["s"]} − {S["p"]}) − {num}×{S["n"] - idx - 1}` = =={b}==　　合计 =={a + b}==')


PLUS_LINE = 8


def _color(S, i, v):
    if 'index' not in S or S['_line'] <= PLUS_LINE:
        return 'yellow' if S.get('index') == i else None
    return 'blue' if i <= S['index'] else 'pink'


CONFIG = dict(
    num=1685, title='有序数组中差的绝对值之和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='有序数组拆绝对值 · 前缀和与后缀和',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def getSumAbsoluteDifferences(self, nums):

        s = sum(nums)
        p = 0
        n = len(nums)
        res = []
        for index, num in enumerate(nums):
            p += num
            res.append(num * (index + 1) - p + (s - p) - num * (n - index - 1))

        return res
''',
    call=f'Solution().getSumAbsoluteDifferences({NUMS})',
    expect=[24, 15, 13, 15, 21],
    views=[
        dict(type='array', var='nums', label='nums（已排序；蓝 = 左段 0..index，粉 = 右段 index+1..n-1）', h=230, cell=96,
             pointers={'index': 'yellow'}, color=_color),
        dict(type='text', fn=_formula, size=26, h=90),
        dict(type='array', var=lambda S: S['res'] + [None] * (S['n'] - len(S['res'])) if 'res' in S and 'n' in S else None, label='res（每个位置的答案，和 nums 一一对应）', h=190, cell=96,
             color=lambda S, i, v: 'green' if S.get('res') and i == len(S['res']) - 1 else None),
    ],
    watch=[('s 总和', 's', 'purple'), ('p 前缀和', 'p', 'blue'), ('index', 'index', 'yellow'), ('num', 'num')],
    captions={
        's = sum(nums)': '先算出数组总和 `s = {s}`：后缀和可以用 `s − p` 得到，不必再存后缀数组',
        'p = 0': '`p` 是当前前缀和，从 0 开始',
        'n = len(nums)': '`n = {n}`，右段有 `n − index − 1` 个数',
        'for index, num in enumerate(nums)': lambda S, B, r: ('每个数都处理完了，循环结束' if ('index' in B and S.index == B.index)
                                                              else '处理第 `{}` 个数 `num = {}`：数组有序，左边的不大于它，右边的不小于它'.format(S.index, S.num)),
        'p += num': '`p += {num}` → `p = {p}`：现在 `p` 是 `nums[0..{index}]` 的和（含自己）',
        'res = []': '`res` 存每个位置的答案',
        'res.append': lambda S, B, r: ('左段 =={}==：左边 `{}` 个数都不大于 `num`，差直接是 `num − nums[j]`；'
                                       '右段 =={}==：右边 `{}` 个数都不小于 `num`；合计 `res[{}]` = =={}=='
                                       ).format(_parts(S)[0], S.index + 1, _parts(S)[1], S.n - S.index - 1, S.index, sum(_parts(S))),
        'return res': '全部算完，返回 `{res}`',
    },
    cards=dict(
        one_liner='数组有序，绝对值能直接拆开：左段用前缀和，右段用后缀和',
        complexity='时间 `O(n)`，空间 `O(1)`（不算结果数组）',
        problem=['非递减数组 `nums`，求同长度数组 `res`：`res[i]` = `nums[i]` 与其他所有数差的绝对值之和',
                 '示例：`[2,3,5]` → `[4,3,5]`',
                 '本视频：`[1,4,6,8,10]` → `[24,15,13,15,21]`'],
        quote='由于题目给出的是排好序的数组，那么可以将计算result的式子中的绝对值符号拆出来，那么result[i]就可以拆分成为两个部分，分别是0到index这一段以及index + 1到n - 1这一段。',
        quote_src='—— yiduobo 题解原文',
        idea=['左段：`nums[i]*(i+1) − prefix_s[i]`（`prefix_s[i]` 含 `nums[i]` 自己，它那一项差为 0）',
              '右段：`suffix_s[i] − nums[i]*(n−i−1)`',
              '后缀和 = 总和 − 前缀和：先算总和 `s`，一趟扫描边走边累加 `p`，不用开前缀数组'],
        summary=['时间 `O(n)`，空间 `O(1)`（结果数组除外）',
                 '易错：`p` 要==先加上当前数==再用，左段才包含它自己（那一项为 0）',
                 '右段个数是 `n − index − 1`，别写成 `n − index`',
                 '前提是数组有序：无序时不能直接拆绝对值'],
    ),
)
