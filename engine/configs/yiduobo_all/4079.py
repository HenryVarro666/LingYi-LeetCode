N = 20


def _nums(S):
    return list(range(N + 1))


def _dim(S, i, v):
    f = S.get('f')
    return f is not None and (i < 2 or not f[i])


def _col(S, i, v):
    res = S.get('res')
    if res is not None and i in res:
        return 'green'
    return None


CONFIG = dict(
    num=4079, title='选择质数子集 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='埃氏筛 + 从小到大贪心', tags=[],
    code='''
class Solution(object):
    def maxPrimes(self, n, s):
        
        f = [True] * (n + 1)
        v = 2
        p_s = 0
        res = []
        while v <= n:
            if f[v]:
                if p_s + v > s:
                    break
                res.append(v)
                p_s += v

                for x in range(v + v, n + 1, v):
                    f[x] = False
            v += 1
        
        return res
''',
    call='Solution().maxPrimes(20, 30)',
    expect=[2, 3, 5, 7, 11],
    skip=['for x in range', 'f[x] = False'],
    views=[
        dict(type='array', var=_nums, label='0 ~ n（灰 = 已被筛掉 / 不是质数，绿 = 已选中，蓝箭头 = v）', h=260,
             pointers={'v': 'blue'}, dim=_dim, color=_col, cell=70),
        dict(type='text', size=34, h=120, fn=lambda S: (f"已选 `res` = =={S['res']}==，总和 `{S['p_s']}`，上限 `s = {S['s']}`" if 'res' in S and 'p_s' in S else '')),
    ],
    watch=[('v', 'v', 'blue'), ('p_s', 'p_s', 'orange'), ('s', 's', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = [True]': '`f[i]` 表示 `i` 还没被筛掉（可能是质数），先全部设为 `True`',
        'v = 2': '从最小的质数 `2` 开始往上看',
        'p_s = 0': '`p_s` 记录已选质数的总和',
        'res = []': '`res` 存已选的质数，要选得尽量多',
        'while v <= n': '`v = {v}`，还在 `n = {n}` 以内 → 继续' ,
        'if f[v]': '`f[{v}]` 是 {"True，没被筛掉，是质数" if f[v] else "False，被更小的质数筛掉了，跳过"}',
        'if p_s + v > s': '想选 `{v}`：`{p_s} + {v} = {p_s + v}`，{"超过 s = " + str(s) + "，更大的质数更放不下，直接 break" if p_s + v > s else "不超过 s = " + str(s) + "，放得下"}',
        'res.append(v)': '贪心：个数要最多，就先拿小的。选中 `{v}`',
        'p_s += v': '总和变为 `{p_s}`，离上限 `{s}` 还剩 `{s - p_s}`',
        'v += 1': '`{v-1}` 处理完（质数的倍数已筛掉，变灰）。看下一个数：`v = {v}`',
        'return res': '最多选 `{len(res)}` 个质数：`{res}`',
    },
    cards=dict(
        one_liner='要选得多，就从最小的质数开始拿',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['给 `n` 和 `s`：从 `n` 以内的质数里选若干个，每个最多选一次',
                 '总和不超过 `s`，数量尽量多，按递增顺序返回',
                 '本视频：`n = 20, s = 30` → `[2,3,5,7,11]`'],
        quote='题目要求选择的质数尽量多，那么就应该按照大小顺序，从小到大开始选取。',
        quote_src='—— yiduobo 题解原文',
        idea=['数量最多 → 每次拿还没选的最小质数，这是最划算的',
              '用筛法边找质数边选：筛出一个质数，就判断能否放进总和',
              '放不下就 `break`：后面的质数只会更大，更放不下'],
        summary=['时间 `O(n log log n)`，空间 `O(n)`',
                 '易错：`p_s + v > s` 是 `>`，刚好等于 `s` 仍可选',
                 '放不下立刻 `break`，不要继续往后找',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
