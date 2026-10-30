CONFIG = dict(
    num=1103, title='分糖果 II', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='配方求轮数 · 等差数列',
    code='''
class Solution(object):
    def distributeCandies(self, candies, num_people):

        p = int(sqrt(candies * 2 + 0.25) - 0.5)
        rnd = p // num_people
        rest = p % num_people
        res = [(index + 1) * rnd + num_people * (rnd - 1) * rnd // 2 for index in range(num_people)]
        for index in range(rest):
            res[index] += index + 1 + num_people * rnd
        res[rest] += candies - p * (1 + p) // 2
        return res
''',
    setup='from math import sqrt',
    call='Solution().distributeCandies(7, 4)',
    expect=[1, 2, 3, 1],
    max_steps=40,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"完整发了 `p = {S['p']}` 次" if 'p' in S else '')),
        dict(type='text', size=30, fn=lambda S: (f"每人 `rnd = {S['rnd']}` 轮，前 `rest = {S['rest']}` 人多一次" if 'rest' in S else '')),
        dict(type='array', var='res', label='res（每个小朋友的糖果数）', pointers={'index': 'blue'}, h=260,
             color=lambda S, i, v: 'green' if 'rest' in S and i == S['rest'] else None),
    ],
    watch=['candies', 'num_people', ('p', 'p', 'blue'), ('rnd', 'rnd', 'cyan'), ('rest', 'rest', 'pink')],
    captions={
        'p = int': '配方：`p(p+1)/2 ≤ {candies}` → `p = {p}`，一共完整发了 `{p}` 次',
        'rnd =': '每人完整拿 `rnd = {p} // {num_people} = {rnd}` 轮',
        'rest =': '余下 `rest = {rest}`：前 `{rest}` 个人还要多拿一次',
        'res = [': '第 `i` 人每轮拿 `i, i+n, i+2n…`，`rnd` 轮求和 → `{res}`',
        'for index': '第 `{index}` 个人多拿一次',
        'res[index] +=': '多拿 `{index + 1} + {num_people}×{rnd}` → `res[{index}] = {res[index]}`',
        'res[rest] +=': '最后剩的 `{candies} - {p}×{p+1}/2 = {candies - p * (1 + p) // 2}` 颗，全给第 `rest + 1` 个人 → `{res}`',
        'return': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='配方求出发满几次，每人几轮用等差数列求和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`candies` 颗糖分给 `num_people` 个人，第 `i` 次发 `i` 颗，循环往复',
                 '最后不够的就全部发给当前的人',
                 '本视频：`candies=7, num_people=4` → `[1,2,3,1]`'],
        quote='设最终完整地分了p次，那么一共就分出去了 s = (1 + p) * p / 2 颗糖果，这里的s小于等于candies，同时p要最大。通过配方法可以很快得到 p = int(sqrt(candies * 2 + 0.25) - 0.5)',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 次完整发放 → 每人 `rnd = p // n` 轮，前 `rest = p % n` 人多一轮',
              '第 `i` 人每轮拿 `i, i+n, i+2n, …`，等差数列直接求和',
              '剩下的 `candies - p(1+p)/2` 颗全给第 `rest + 1` 个人'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：下标从 0 开始，第 `index` 个人第一轮拿 `index + 1` 颗',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并在 setup 里 `from math import sqrt`'],
    ),
)
