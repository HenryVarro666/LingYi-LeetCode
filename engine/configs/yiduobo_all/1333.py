def _cur(S):
    return S.get('id')


def _color(S, i, j, v):
    if 'id' not in S:
        return None
    if S['restaurants'][i][0] == S['id']:
        return 'blue'
    return None


def _dim(S, i, j, v):
    return False


CONFIG = dict(
    num=1333, title='餐厅过滤器', difficulty='Medium', category='模拟',
    author='yiduobo', technique='筛选 + 自定义排序',
    tags=[],
    code='''
class Solution(object):
    def filterRestaurants(self, restaurants, veganFriendly, maxPrice, maxDistance):

        candidate = []
        for id, r, v, p, d in restaurants:
            if veganFriendly and not v:
                continue
            if p > maxPrice:
                continue
            if d > maxDistance:
                continue
            candidate.append([r, id])
        
        return [x[1] for x in sorted(candidate, key=lambda d:(-d[0], -d[1]))]
''',
    call='Solution().filterRestaurants([[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]], 1, 50, 10)',
    expect=[3, 1, 5],
    views=[
        dict(type='table', var='restaurants', rows=lambda S: [f'#{r[0]}' for r in S['restaurants']],
             cols=['id', 'rating', 'vegan', 'price', 'dist'], color=_color, h=330),
        dict(type='array', var='candidate', label='candidate（[rating, id]）', h=150),
    ],
    watch=[('id', 'id', 'blue'), ('rating', 'r', 'yellow'), ('vegan', 'v', 'green'), ('price', 'p', 'orange'), ('dist', 'd', 'pink')],
    captions={
        'candidate = []': '`candidate` 存通过筛选的 `[rating, id]`',
        'for id, r, v, p, d': '看餐厅 `{id}`：rating `{r}`，vegan `{v}`，价格 `{p}`，距离 `{d}`',
        'if veganFriendly and not v': lambda S, B, r: (f'要求素食友好，但餐厅 {S.id} 的 `v = 0` → ==排除==' if S.veganFriendly and not S.v
                                                       else '不要求素食或它是素食友好 → 通过这一关'),
        'if p > maxPrice': lambda S, B, r: (f'价格 `{S.p} > {S.maxPrice}` → ==排除==' if S.p > S.maxPrice
                                            else f'价格 `{S.p} <= {S.maxPrice}` → 通过'),
        'if d > maxDistance': lambda S, B, r: (f'距离 `{S.d} > {S.maxDistance}` → ==排除==' if S.d > S.maxDistance
                                               else f'距离 `{S.d} <= {S.maxDistance}` → 通过'),
        'continue': '不满足条件，直接看下一家',
        'candidate.append': '三关都通过：加入候选 `[{r}, {id}]`',
        'return [x[1]': '按 rating 降序、rating 相同按 id 降序：key 取 `(-rating, -id)`，输出 id → `{ret}`',
    },
    cards=dict(
        one_liner='先一趟筛掉不合格的，再按 rating、id 降序排',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每家餐厅是 `[id, rating, veganFriendly, price, distance]`',
                 '只保留满足素食、价格、距离限制的；按 rating 降序，rating 相同按 id 降序，返回 id',
                 '示例：素食要求 1，最高价 50，最远 10 → `[3,1,5]`'],
        quote='首先一趟扫描，按照素食友好、价格以及距离筛选出候选餐厅，并将其对应的rating和id加入到候选数组candidate当中，接下来按照rating为第一关键字，id为第二关键字对candidate排序',
        quote_src='—— yiduobo 题解原文',
        idea=['题目文字多，但本质是过滤加排序',
              '`veganFriendly` 为 0 时不看素食；为 1 才要求 `v` 为真',
              '候选里存 `[rating, id]`，排序键取负数就能降序'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`veganFriendly = 0` 时素食和非素食都要保留',
                 '价格和距离都是 `<=` 才合格，超过才排除',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
