def _terms(S):
    i, nums = S['i'], S['nums']
    return [i - x for x in nums if x <= i]


def _color(S, k, v):
    if 'i' not in S or S.get('_line') not in (6, 7, 8, 9):
        return None
    if k == S['i']:
        return 'yellow'
    if S.get('num') is not None and S.get('_line') in (8, 9) and k == S['i'] - S['num']:
        return 'green'
    return None


def _formula(S):
    if 'i' not in S or 'f' not in S:
        return '`f[i]` = 凑出 `i` 的方案数；`f[i] = sum(f[i - nums[j]])`'
    i, f = S['i'], S['f']
    ts = _terms(S)
    return f'`f[{i}] = ' + ' + '.join(f'f[{j}]' for j in ts) + '`' + (f' = ' + ' + '.join(str(f[j]) for j in ts) if ts else '')


CONFIG = dict(
    num=377, title='组合总和 Ⅳ', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP（完全背包·排列）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1600'],
    code='''
class Solution(object):
    def combinationSum4(self, nums, target):

        f = [0] * (target + 1)
        f[0] = 1
        for i in range(1, target + 1):
            for num in nums:
                if i >= num:
                    f[i] += f[i - num]

        return f[target]
''',
    call='Solution().combinationSum4([1, 3, 4], 6)',
    expect=9,
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='f', label='f[i]：组合出 i 有多少种（黄 = 正在算，绿 = 刚加进来的 f[i-num]）', h=300, cell=100,
             pointers={'i': 'blue'}, color=_color),
        dict(type='array', var='nums', label='nums', h=200, cell=100, pointers={'num': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('num', 'num', 'pink'), ('f[i]', 'f[i]', 'green')],
    captions={
        'f = [0]': '开一个长度 `target + 1` 的数组，初值都是 0',
        'f[0] = 1': '边界 `f[0] = 1`：==什么数都不选==，凑出 0 只有这一种',
        'for i in range': lambda S, B, r: ('现在求凑出 `%d` 的方案数 `f[%d]`' % (S.i, S.i) if S.i != B.get('i') or B.get('i') is None else '`i` 都算完了，退出循环'),
        'if i >= num': lambda S, B, r: ('`%d >= %d` → 可以先凑出 `i-num = %d`，再加上 `num` 得到 `i`' % (S.i, S.num, S.i - S.num)
                                       if S.i >= S.num else '`%d < %d`：这个数比 i 还大，用不了' % (S.i, S.num)),
        'f[i] += f[i - num]': '`f[{i}] += f[{i - num}]`（{f[i - num]}）→ 目前 `f[{i}]` = =={f[i]}==',
        'return f[target]': '凑出 `{target}` 的方案数 `f[{target}]` = =={ret}==',
    },
    cards=dict(
        one_liner='凑 i = 先凑 i-num，再补上 num',
        complexity='时间 `O(target·n)`，空间 `O(target)`',
        problem=['给不同的整数数组 `nums` 和目标 `target`，求总和为 `target` 的元素组合个数',
                 '顺序不同算不同的组合',
                 '示例：`nums=[1,3,4], target=6`（演示用）→ `9`'],
        quote='设f[i]表示组合达成i有多少种可能性，那么对于i，若i大于等于nums中的任意数nums[j]，那么就可以通过i - nums[j]再加上nums[j]达成i',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = sum(f[i - nums[j]])`，只统计 `i >= nums[j]` 的项',
              '边界 `f[0] = 1`，表示什么数都不选这一种情况',
              '外层枚举 `i`、内层枚举 `num`，所以不同顺序都会被数到'],
        summary=['时间 `O(target·n)`，空间 `O(target)`',
                 '易错：`f[0]` 要设成 1；`i >= num` 才能转移',
                 '进阶（有负数）：正负数同时存在时能凑出 0 的方式有无数种，所以任何能凑出的数都有无数种组合',
                 '循环顺序决定排列还是组合：外层 `i` = 排列'],
    ),
)
