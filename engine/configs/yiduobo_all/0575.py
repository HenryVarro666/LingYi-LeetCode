CONFIG = dict(
    num=575, title='分糖果', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合去重 · 取较小值',
    code='''
class Solution(object):
    def distributeCandies(self, candies):

        candy_set = set()
        for candy in candies:
            candy_set.add(candy)
        
        return min(len(candy_set), len(candies) // 2)
''',
    call='Solution().distributeCandies([1,1,2,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='candies', pointers={}, h=220,
             color=lambda S, i, v: 'green' if 'candy_set' in S and 'candy' in S and v in S['candy_set'] and v != S['candy'] else ('yellow' if 'candy' in S and v == S['candy'] else None)),
        dict(type='set', var='candy_set', fmt=lambda x: str(x), h=200, label='candy_set（糖的种类）'),
        dict(type='text', fn=lambda S: f"种类数 `{len(S['candy_set'])}`，最多能吃 `{len(S['candies'])} // 2 = {len(S['candies'])//2}` 颗" if 'candy_set' in S and 'candies' in S else '', h=60),
    ],
    watch=['candy', ('len(candy_set)', 'len(candy_set)', 'green')],
    captions={
        'candy_set = set()': '先准备空集合，用来统计出现过的糖果种类',
        'candy_set.add': lambda S, B, r: f'`candy = {S.candy}`：' + (f'集合里已有 {S.candy}，重复种类不增加' if S.candy in B.candy_set else f'新种类，加入集合 → 共 =={len(S.candy_set)}== 种'),
        'return min': '种类数 `{len(candy_set)}` 与可吃数量 `{len(candies)} // 2 = {len(candies)//2}` 取较小：=={ret}==',
    },
    cards=dict(
        one_liner='种类数与 n/2 取较小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`candies[i]` 是第 `i` 颗糖的种类，只能吃掉一半（`n/2` 颗）',
                 '想吃到尽可能多的不同种类，求最多种类数',
                 '示例：`[1,1,2,3,3,3]` → `3`'],
        quote='通过set统计糖果的种类数，我们希望每种糖果都可以分给姐姐，而姐姐最多可以分到len(candies)/2个糖果，因此这两个数取较小值就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['用集合统计一共有几种糖',
              '数量上限是 `n/2` 颗，种类数多于上限也吃不完',
              '两者取较小值即为答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：上限是 `n // 2`，不是种类数的一半',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
