def _color(S, i, v):
    if i < 2:
        return None
    if v == 0:
        return 'red'
    if 'now' in S and i == S['now']:
        return 'orange'
    if 'now' in S and (i < S['now'] or S['now'] > S.get('max_l', 10 ** 9)):
        return 'green'          # 小于 now 且未被划掉 → 已确定是质数
    return None


def _tmp(S):
    t = S.get('tmp')
    if t is None or t > S['n']:
        return None
    return t


CONFIG = dict(
    num=204, title='计数质数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='埃氏筛 · 从 x² 开始划合数',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def countPrimes(self, n):

        if n < 2:
            return 0

        max_l = int(n ** 0.5)
        f = [1] * (n + 1)

        now = 2
        cnt = 0
        while now <= max_l:
            if f[now] == 1:
                tmp = now * now
                while tmp <= n:
                    f[tmp] = 0
                    tmp += now
            now += 1

        return sum(f[2 : n])
''',
    call='Solution().countPrimes(20)',
    expect=8,
    views=[
        dict(type='array', var='f', label='f[x]（1 = 还没被划掉；绿 = 确定是质数，红 = 合数，橙 = now）', h=260, cell=60,
             pointers={'now': 'orange', _tmp: 'pink'}, pointer_labels={_tmp: 'tmp'},
             color=_color, dim=lambda S, i, v: i < 2),
        dict(type='text', h=120, size=30,
             fn=lambda S: (f"`now = {S['now']}` 的倍数从 `now² = {S['now'] ** 2}` 开始划：{', '.join(str(x) for x in range(S['now'] ** 2, S['n'] + 1, S['now']))}"
                           if 'now' in S and S['now'] <= S.get('max_l', 0) and S['f'][S['now']] == 1
                           else (f"只需枚举到 `max_l = floor(sqrt({S['n']})) = {S['max_l']}`" if 'max_l' in S
                                 else '==埃氏筛==：每找到一个质数，就把它的倍数全部划掉'))),
    ],
    watch=[('max_l', 'max_l'), ('now', 'now', 'orange'), ('tmp', 'tmp', 'pink')],
    skip=['cnt = 0'],
    captions={
        'if n < 2': '`n = {n} ≥ 2`，开始筛',
        'max_l = int(n ** 0.5)': '`max_l = floor(sqrt({n})) = {max_l}`：比它大的合数，==一定有不超过 sqrt(n) 的因子==，早已被划掉',
        'f = [1] * (n + 1)': '`f[x] = 1` 表示 x 暂时还可能是质数',
        'now = 2': '从最小的质数 `2` 开始',
        'while now <= max_l': lambda S, B, r: (f'`now = {S.now} ≤ {S.max_l}`，继续' if S.now <= S.max_l
                                               else f'`now = {S.now} > max_l = {S.max_l}`：筛完了'),
        'if f[now] == 1': lambda S, B, r: (f'`f[{S.now}] = 1`：{S.now} 没被更小的质数划掉 → =={S.now} 是质数==' if S.f[S.now] == 1
                                           else f'`f[{S.now}] = 0`：{S.now} 是合数，它的倍数早被它的质因子划过了，跳过'),
        'tmp = now * now': lambda S, B, r: (f'从 `{S.now} × {S.now} = {S.tmp}` 开始划' + (
            '' if S.now == 2 else f'：更小的倍数 `{S.now}×2' + (f'…{S.now}×{S.now - 1}' if S.now > 3 else '') + '` ==已被更小的质数划过==')),
        'while tmp <= n': lambda S, B, r: (f'`tmp = {S.tmp} ≤ {S.n}`' if S.tmp <= S.n else f'`tmp = {S.tmp} > {S.n}`：{S.now} 的倍数划完了'),
        'f[tmp] = 0': '`{tmp} = {now} × {tmp // now}` 是合数，划掉',
        'tmp += now': '下一个倍数 `tmp = {tmp}`',
        'now += 1': '`now` → {now}',
        'return sum(f[2 : n])': '`sum(f[2:{n}])`：小于 {n} 的质数共 `{ret}` 个',
    },
    max_steps=70,
    cards=dict(
        one_liner='每找到一个质数，就把它从平方开始的倍数全部划掉',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['给定整数 `n`，返回==小于 n== 的质数个数',
                 '示例：`n = 10` → `4`（2、3、5、7）',
                 '本视频：`n = 20` → `8`'],
        quote='令变量x从2开始循环到根号n：1、若x为质数，那么将x * 2，x * 3，...，x * k全部标记为合数。2、若x为合数，则不进行任何操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历到 `now` 时 `f[now]` 还是 1，说明没有更小的因子 → 它是质数',
              '代码从 `now * now` 开始划：更小的倍数已被更小的质数划过',
              '`now` 只需枚举到 `sqrt(n)`，最后数一数 `f[2:n]` 里的 1'],
        summary=['时间 `O(n log log n)`（原文估计为 `n log n` 量级，实际更小），空间 `O(n)`',
                 '题目要的是==严格小于 n==：所以是 `sum(f[2 : n])`，不含 `f[n]`',
                 '`n < 2` 要特判：此时没有质数',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未作改动；变量 `cnt` 未使用'],
    ),
)
