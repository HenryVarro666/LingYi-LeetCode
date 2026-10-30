def _terms(S):
    i, f, nums = S['i'], S['f'], S['nums']
    return [(x, i - x) for x in nums if x <= i]


def _formula(S):
    if 'i' not in S or 'f' not in S:
        return '`f[i]` = 爬 `i` 个台阶的方案数；最后一步爬 `x` 级 → 加上 `f[i-x]`'
    ts = _terms(S)
    i = S['i']
    if S.get('_line') == 4:
        return f'`f[{i}] = ' + ' + '.join(f'f[{j}]' for _, j in ts) + '`'
    return f'`f[{i}] = ' + ' + '.join(str(S['f'][j]) for _, j in ts) + f'` = =={S["f"][i]}=='


def _color(S, k, v):
    if 'i' not in S or S.get('_line') != 5:
        return None
    if k == S['i']:
        return 'yellow'
    if k in [j for _, j in _terms(S)]:
        return 'green'
    return None


CONFIG = dict(
    num=377, title='组合总和 Ⅳ', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='爬楼梯式递推（排列数）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1600'],
    code='''
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        f = [1] + [0] * target
        for i in range(1, target + 1):
            f[i] = sum(f[i - x] for x in nums if x <= i)
        return f[target]
''',
    call='Solution().combinationSum4([1, 2, 3], 4)',
    expect=7,
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='f', label='f[i]：爬 i 个台阶的方案数（黄 = 正在算，绿 = 它依赖的 f[i-x]）', h=300, cell=110,
             pointers={'i': 'blue'}, color=_color),
        dict(type='array', var='nums', label='nums：每一步可以爬的台阶数', h=200, cell=110),
    ],
    watch=[('i', 'i', 'blue'), ('target', 'target', 'yellow'), ('f[i]', 'f[i]', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：爬 0 个台阶 = ==原地不动算一种方案==；其余先填 0',
        'for i in range': lambda S, B, r: ('开始算爬 `%d` 个台阶：==外层枚举台阶数 i==，内层才枚举 `x`，所以 `1,2` 和 `2,1` 都会被数到' % S.i if S.i != B.get('i') or B.get('i') is None
                                         else '`i` 枚举完了，退出循环'),
        'f[i] = sum': lambda S, B, r: ('最后一步爬 `x` 个台阶（`x ≤ i`），前面还剩 `i-x` 个：`f[%d] = %s` = ==%d==' % (
            S.i, ' + '.join(str(S.f[j]) for _, j in _terms(S)), S.f[S.i])),
        'return f[target]': '爬 `{target}` 个台阶的方案数 `f[{target}]` = =={ret}==',
    },
    cards=dict(
        one_liner='最后一步爬几个台阶？枚举 x，累加 f[i-x]',
        complexity='时间 `O(target·n)`，空间 `O(target)`',
        problem=['`nums` 是互不相同的正整数，从中每次选一个数，凑出总和 `target`，求==有多少种排列==',
                 '顺序不同算不同方案：`(1,2)` 和 `(2,1)` 是两种',
                 '示例：`nums=[1,2,3], target=4` → `7`'],
        quote='本质上是 70. 爬楼梯，每次从 nums 中选一个数，作为往上爬的台阶数，计算爬 target 个台阶有多少种方案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` 表示爬 `i` 个台阶的方案数；最后一步爬了 `x`，前面就是 `f[i-x]`',
              '`f[i] = sum(f[i-x])`，只加 `x ≤ i` 的项；70 题就是 `nums=[1,2]`',
              '`f[0] = 1`：什么也不选，也算一种方案'],
        summary=['时间 `O(target·n)`，空间 `O(target)`',
                 '易错：`f[0]` 必须是 1，否则所有 `f[i]` 都是 0',
                 '==外层体积、内层物品 = 排列==；外层物品、内层体积 = 组合（518 零钱兑换 II）',
                 '灵神原文还有记忆化搜索写法（`@cache`），递推是它 1:1 翻译的结果'],
    ),
)
