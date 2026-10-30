N = 20


def _prime_line(S):
    return list(range(0, N + 1))


def _col(S, i, v):
    pr = S.get('prime')
    if pr is None:
        return None
    s = S.get('s')
    if s is not None and i == s and s <= N and pr[s] and s >= 2:
        return 'yellow'
    return 'green' if pr[i] and i >= 2 else None


def _dim(S, i, v):
    pr = S.get('prime')
    return pr is not None and (i < 2 or not pr[i])


def _txt(S):
    if 'prime' not in S:
        return f'目标 `n = {N}`：先筛质数，再从 2 开始累加'
    if 'res' not in S:
        return '先用筛法把合数划掉'
    return f'依次累加质数：`s = {S["s"]}`；最近一次和是质数的 `res = {S["res"]}`'


CONFIG = dict(
    num=3770, title='可表示为连续质数和的最大质数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法 + 从小到大累加质数',
    tags=['灵神题单·数学算法', '难度分 1547'],
    code='''
class Solution(object):
    def largestPrime(self, n):
        
        prime = [True] * (n + 1)
        p_list = []
        x = 2
        while x * x <= n:
            if prime[x]:
                for v in range(x + x, n + 1, x):
                    prime[v] = False
            x += 1
        
        s = 0
        res = 0
        for v in range(2, n + 1):
            if prime[v]:
                s += v
                if s > n:
                    break
                
                if prime[s]:
                    res = s
        
        return res
''',
    call=f'Solution().largestPrime({N})',
    expect=17,
    max_steps=130,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=_prime_line, color=_col, dim=_dim, cell=46, h=300,
             pointers={'v': 'blue', 's': 'pink'},
             label=f'数轴 0..{N}（灰 = 合数；绿 = 质数；黄 = 当前和 s；蓝 = v）'),
    ],
    watch=['n', ('x', 'x', 'blue'), ('v', 'v', 'blue'), ('s', 's', 'pink'), ('res', 'res', 'green')],
    captions={
        'prime = [True]': '`prime[i]` 表示 `i` 是否质数，先假设 `0..{n}` 全是（`0`、`1` 其实不是，但后面不会用到）',
        'p_list = []': '这个列表原文声明了但没有用到',
        'x = 2': '从 `x = 2` 开始筛',
        'while x * x <= n': '`{x}×{x} = {x*x}` 与 `{n}` 比较：只筛到 `√n`',
        'if prime[x]': lambda S, B, r: (f'`prime[{S.x}]` 为真：`{S.x}` 是质数，划掉它的倍数' if S.prime[S.x]
                                        else f'`prime[{S.x}]` 为假：`{S.x}` 是合数，跳过'),
        'for v in range(x + x': lambda S, B, r: ('`' + str(S.x) + '` 的倍数划完了' if 'v' in B and B.v == S.v
                                                 else f'划掉 `{S.x}` 的倍数：`v = {S.v}`'),
        'prime[v] = False': '`{v}` 是 `{x}` 的倍数 → 合数',
        'x += 1': '`x` → {x}',
        13: '`s` 保存「从 2 开始连续质数之和」',
        14: '`res` 记录目前最大的「和是质数」，没有就是 0',
        'for v in range(2': lambda S, B, r: ('`v` 枚举完了' if 'v' in B and 's' in B and B.v == S.v and S.v == S.n
                                             else f'`v = {S.v}`'),
        'if prime[v]': lambda S, B, r: (f'`{S.v}` 是质数：把它加进 `s`' if S.prime[S.v] else f'`{S.v}` 是合数：不能参与累加，跳过'),
        's += v': '`s` = `{B.s} + {v}` = =={s}==',
        'if s > n': lambda S, B, r: (f'`s = {S.s} > n = {S.n}`：超过范围，再加只会更大 → break' if S.s > S.n
                                     else f'`s = {S.s} <= n = {S.n}`：还在范围内'),
        'break': '后面的和只会更大，直接结束',
        'if prime[s]': lambda S, B, r: (f'`prime[{S.s}]` 为真：`{S.s}` 本身是质数 → 满足' if S.prime[S.s]
                                        else f'`prime[{S.s}]` 为假：和 `{S.s}` 不是质数，不算'),
        'res = s': '更新答案：`res = {s}`（和越来越大，所以最后一个满足的就是最大的）',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='筛出质数，从 2 开始一路累加，和是质数就更新答案',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['找 `<= n` 的最大质数，且它是 ==从 2 开始的连续质数== 之和，没有返回 0',
                 '示例：`n = 20` → `17`（`2+3+5+7`）',
                 f'本视频：`n = {N}`'],
        quote='接下来从小到大遍历这些质数，并累加到一个变量s中，直到s大于等于n为止。若当前的s也是质数，则使用s更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用筛法找出 `n` 以内的所有质数（标记数组 `prime`）',
              '从小到大累加质数到 `s`，`s` 越来越大',
              '每次 `s` 是质数就更新 `res = s`，超过 `n` 就停'],
        summary=['原文为 Python 2 风格，本题代码无需改动即可运行',
                 '累加时只加质数；`s` 随加数增大，所以最后更新的 `res` 就是最大值',
                 '作者说最优做法其实是打表（`n ≤ 5×10^5` 时只有 40 个答案）',
                 '对比灵神：灵神预处理全局表后二分，yiduobo 每次现筛现加'],
    ),
)
