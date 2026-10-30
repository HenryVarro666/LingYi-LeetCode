def _fr(S, i):
    s = S.get('sorted_cost')
    return s is not None and i >= 2 and (i - 2) % 3 == 0


CONFIG = dict(
    num=2144, title='打折购买糖果的最小开销', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='排序 · 下标模 3 余 2 免费',
    tags=['灵神题单', '难度分 1261'],
    code='''
class Solution(object):
    def minimumCost(self, cost):

        res = sum(cost)
        sorted_cost = sorted(cost, reverse=True)
        for index in range(2, len(sorted_cost), 3):
            res -= sorted_cost[index]
        
        return res
''',
    call='Solution().minimumCost([6,5,7,9,2,2])',
    expect=23,
    views=[
        dict(type='array', var=lambda S: S['sorted_cost'] if 'sorted_cost' in S else S['cost'],
             label='糖果价格（排序后：每 3 个里第 3 个免费）', pointers={'index': 'blue'}, h=230, cell=100,
             color=lambda S, i, v: 'green' if 'sorted_cost' in S and i % 3 == 2 and ('index' not in S or i <= S['index']) else None),
        dict(type='text', h=90, size=32, fn=lambda S: f"`res` = `{S['res']}`" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = sum(cost)': '先假设全部购买：`res = {res}`',
        'sorted_cost = sorted': '从大到小排序：`{sorted_cost}`。最贵的两颗只能靠买',
        'for index in range': lambda S, B, r: (f'下标 `{S.index}`（模 3 余 2）的糖果是免费的' if 'index' not in B or S.index != B.index else '没有更多的免费糖果了'),
        'res -= sorted_cost[index]': '免费的价格 `{sorted_cost[index]}` 不用付：`res` → =={res}==',
        'return res': '最小开销 `{res}`',
    },
    cards=dict(
        after=[dict(heading='为什么这样送最划算', lines=['最贵的两颗没有别的颗可以白送，只能买', '买了它们，免费名额给第三贵的，价值最高', '之后每买两颗，同理送下一个最贵的', '免费的价格和最大 → 总开销最小'])],
        one_liner='买了最贵的两颗，就送第三贵的，依此类推',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['买两颗糖果可免费得一颗，免费的不能比买的两颗中较小者贵',
                 '求拿到所有糖果的最小总开销',
                 '本视频：`cost = [6,5,7,9,2,2]` → `23`'],
        quote='最贵的两颗糖果就只能靠买的。购买了最贵的两颗糖果之后，可以免费获得一颗糖果，此时显然就应该选择获得第三贵的糖果。',
        quote_src='—— yiduobo 题解原文',
        idea=['从大到小排序，三颗一组：买、买、送',
              '下标模 3 余 2 的糖果免费',
              '答案 = 总价 − 这些糖果的价格和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`range(2, len, 3)` 从下标 2 开始每隔 3 个取一个',
                 '不足 3 颗时没有免费糖果，全部购买',
                 '对比灵神：灵神用切片 `cost[2::3]` 并证明了上界可达'],
    ),
)
