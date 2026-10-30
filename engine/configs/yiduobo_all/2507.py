def _ph2(S):
    return S.get('_line', 0) >= 14


def _px(S):
    return S['x'] if 'x' in S and not _ph2(S) else None


def _pn(S):
    return S['now'] if 'now' in S and 0 <= S['now'] < len(S['f']) else None


CONFIG = dict(
    num=2507, title='使用质因数之和替换后可以取到的最小值', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛出最大质因子 · 反复分解',
    tags=['灵神题单·数学算法', '难度分 1500'],
    code='''
class Solution(object):
    def smallestValue(self, n):

        f = list(range(n + 1))
        x = 2
        while x * x <= n:
            if f[x] == x:
                now = x + x
                while now <= n:
                    f[now] = x
                    now += x
            x += 1

        now = n
        while True:
            pre = now
            s = 0
            while f[now] != now:
                s += f[now]
                now //= f[now]
            
            s += now
            now = s
            if s == pre:
                break

        return now
''',
    call='Solution().smallestValue(15)',
    expect=5,
    views=[
        dict(type='text', size=27, h=60, fn=lambda S: (
            ('筛法：`x = %d` 是质数，把它的倍数的 `f` 都标成 %d' % (S['x'], S['x'])) if 'x' in S and not _ph2(S) and S['x'] * S['x'] <= S['n'] and S['f'][S['x']] == S['x']
            else ('分解：`now = %d`，`f[now] = %d`' % (S['now'], S['f'][S['now']])) if _ph2(S) and 'now' in S and 0 <= S['now'] < len(S['f'])
            else '')),
        dict(type='array', var='f', label='f[i]：i 的一个质因子（f[i] = i 说明 i 是质数）', h=300, cell=62,
             pointers={_px: 'blue', _pn: 'pink'}, pointer_labels={_px: 'x', _pn: 'now'},
             color=lambda S, i, v: ('orange' if v != i else 'green' if i >= 2 else None)),
    ],
    watch=['n', ('x', 'x', 'blue'), ('now', 'now', 'pink'), ('s', 's', 'green'), 'pre'],
    skip=['now += x', 'while now <= n'],
    captions={
        'f = list(range': '`f[i]` 先全部设为自己：`f = [0,1,2,...,{n}]`，之后会被改成 `i` 的质因子',
        'while x * x <= n': lambda S, B, r: (f'`x*x = {S.x * S.x} <= n = {S.n}`：还要用 `x` 去筛' if S.x * S.x <= S.n
                                              else f'`x*x = {S.x * S.x} > n`：筛完了，合数都被标上了质因子'),
        'if f[x] == x': lambda S, B, r: (f'`f[{S.x}] == {S.x}`：没被更小的数改过 → ==质数==，筛它的倍数' if S.f[S.x] == S.x
                                          else f'`f[{S.x}] = {S.f[S.x]}`：已被标过，是合数 → 跳过'),
        'now = x + x': '从 `{x}` 的 2 倍开始，`{x}` 的倍数都不是质数',
        'f[now] = x': '`f[{now}] = {x}`：`{now}` 有质因子 `{x}`（后面的更大质数会覆盖，留下较大的）',
        'x += 1': '`x` → {x}',
        'now = n': '筛法做完。回到 `n = {n}` 开始替换：`now` 记当前数',
        'pre = now': '记下替换前的值 `pre = {pre}`，之后用来判断有没有变',
        's = 0': '`s` 累加质因数之和',
        'while f[now] != now': lambda S, B, r: (f'`f[{S.now}] = {S.f[S.now]} != {S.now}`：{S.now} 是合数，还能拆' if S.f[S.now] != S.now
                                                 else f'`f[{S.now}] = {S.now}`：{S.now} 是质数，拆完了'),
        's += f[now]': '取出质因子 `f[{B.now}] = {B.f[B.now]}`，`s` → =={s}==',
        'now //= f[now]': '除掉这个质因子：`now` → =={now}==（重复的因子下一轮会再取一次）',
        's += now': '剩下的 `now = {now}` 本身是质数，也加进去：`s` → =={s}==',
        'now = s': '`now` 换成质因数之和 `{now}`',
        'if s == pre': lambda S, B, r: (f'`s = {S.s} == pre = {S.pre}`：不再变小 → 结束' if S.s == S.pre
                                         else f'`s = {S.s} != pre = {S.pre}`：还在变，继续下一轮'),
        'break': '跳出循环',
        'return now': '最小值就是 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='先筛出每个数的质因子，再顺着 f 一路拆下去',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['把 `n` 换成它的质因数之和（重复的质因数算多次），一直重复',
                 '求 `n` 能取到的最小值',
                 '示例：`15 → 8 → 6 → 5`，返回 `5`'],
        quote='另外如果本题有多组询问，则可以先通过筛法找出每个数最大的质因子，然后通过这个质因子做分解质因数后形成类似并查集的结构。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模不大，暴力就够；他的写法是先用筛法为每个数记一个质因子 `f[i]`',
              '分解时 `now` 不断除以 `f[now]`，直到 `f[now] == now`（质数）',
              '每轮把质因子累加成 `s`，`s == pre` 时说明不再变化'],
        summary=['时间 `O(n log log n)` 的筛 + 每轮 `O(log n)` 的分解',
                 '`f[now] != now` 才是合数；最后剩的 `now` 要单独加进 `s`',
                 '原文为 Python 2 写法，`range` 直接当列表用、`/=` 做整除，已改为 `list(range(...))` 和 `//=`',
                 '对比灵神：灵神每轮试除到根号，不需要筛；yiduobo 筛一次、适合多组询问'],
    ),
)
