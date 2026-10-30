def _f(S):
    return [1.0] + [0.5] * (S['n'] - 1)


def _txt1(S):
    n = S['n']
    return f'`f[k]` = 有 k 个人时，第 k 个人坐对的概率；本例 `n = {n}`'


def _txt2(S):
    n = S['n']
    return f'递推推到最后：`f[2] = 0.5`，之后 `f[k+1] = f[k]`，所以 `f[{n}]` = ==0.5=='


CONFIG = dict(
    num=1227, title='飞机座位分配概率', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='递推式相减 · 结论恒为 0.5',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def nthPersonGetsNthSeat(self, n):

        if n == 1:
            return 1.0
        
        return 0.5
''',
    call='Solution().nthPersonGetsNthSeat(4)',
    expect=0.5,
    views=[
        dict(type='text', fn=_txt1, size=28, h=90),
        dict(type='array', var=_f, label='f[1], f[2], ... , f[n]（从左到右）', h=230,
             color=lambda S, i, v: 'green' if i == S['n'] - 1 else None, index=False),
        dict(type='text', fn=_txt2, size=28, h=110),
    ],
    watch=['n'],
    captions={
        'if n == 1': '`n == 1`（{n} == 1）→ {"成立：只有一个人，一定坐在自己的位子上" if n == 1 else "不成立，进入 n ≥ 2 的情况，答案恒为 0.5"}',
        'return 1.0': '只有 1 个人，概率 =={ret}==',
        'return 0.5': '`n = {n} ≥ 2`：由 `f[n+1] = f[n]` 和 `f[2] = 0.5`，所有 `n ≥ 2` 都是 =={ret}==',
    },
    cards=dict(
        one_liner='设 f[n] 列递推式，两式相减后发现 f 恒为 0.5',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 位乘客、`n` 个座位，第 1 位随便坐；其余人先坐自己的座位，被占了才随机坐',
                 '求第 `n` 位乘客坐到自己座位的概率',
                 '本视频：`n = 4` → `0.5`'],
        quote='不妨设f[n]表示有n个人时，第n个人坐到自己位子上的概率，那么对于n=1的情况，答案就是1。当n大于1时，则有两种可能。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 1 人坐自己位子（概率 `1/n`）→ 后面都坐对，答案 1',
              '第 1 人坐了第 `k` 人的位子 → 第 `k` 人变成新的「丢票者」，剩 `n−k` 人 → `f[n−k]`',
              '得 `n·f[n] = 1 + f[n−1] + … + f[1]`，与 `n+1` 的式子相减 → `f[n+1] = f[n]`'],
        after=[dict(heading='递推式怎么变出来的', lines=['`f[n] = 1/n + 1/n·f[n−1] + … + 1/n·f[1]`',
                                                       '两边乘 `n`：`n·f[n] = 1 + f[n−1] + … + f[1]`',
                                                       '再写 `(n+1)·f[n+1] = 1 + f[n] + … + f[1]`，两式相减',
                                                       '得 `(n+1)·f[n+1] − n·f[n] = f[n]`，即 ==f[n+1] = f[n]==，且 `f[2] = 0.5`'])],
        summary=['时间、空间 `O(1)`，不需要真的算递推',
                 '`n = 1` 要单独返回 1.0，其余一律 0.5',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神用「后面的人分不清谁坐错」的等价思想，yiduobo 用递推相减'],
    ),
)
