def _rented(S):
    r = S.get('self.rented_movies')
    return None if r is None else [f'({p},{s},{m})' for p, s, m in r]


def _info(S):
    m = S.get('movie')
    if m is None:
        return ''
    u = S.get('self.unrented_movie_to_price_shop')
    if u is None or m not in u:
        return ''
    return f"电影 `{m}` 未借出的 `(price, shop)`：`{list(u[m])}`"


CONFIG = dict(
    num=1912, title='设计电影租借系统', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 有序集合',
    tags=['堆（优先队列）', '难度分 2182'],
    setup='''
class SortedList(list):  # 演示用的最小实现，行为同 sortedcontainers.SortedList（本题只用到 add / discard / 切片）
    def add(self, x):
        bisect.insort(self, x)

    def discard(self, x):
        i = bisect.bisect_left(self, x)
        if i < len(self) and self[i] == x:
            del self[i]
''',
    code='''
class MovieRentingSystem:
    def __init__(self, _, entries: List[List[int]]):
        self.shop_movie_to_price = {}  # (shop, movie) -> price
        self.unrented_movie_to_price_shop = defaultdict(SortedList)  # movie -> [(price, shop)]
        self.rented_movies = SortedList()  # [(price, shop, movie)]

        for shop, movie, price in entries:
            self.shop_movie_to_price[(shop, movie)] = price
            self.unrented_movie_to_price_shop[movie].add((price, shop))

    # 获取 unrented_movie_to_price_shop[movie] 的前 5 个 shop
    def search(self, movie: int) -> List[int]:
        return [shop for _, shop in self.unrented_movie_to_price_shop[movie][:5]]

    # 借电影
    def rent(self, shop: int, movie: int) -> None:
        price = self.shop_movie_to_price[(shop, movie)]
        # 从 unrented_movie_to_price_shop 移到 rented_movies
        self.unrented_movie_to_price_shop[movie].discard((price, shop))
        self.rented_movies.add((price, shop, movie))

    # 还电影
    def drop(self, shop: int, movie: int) -> None:
        price = self.shop_movie_to_price[(shop, movie)]
        # 从 rented_movies 移到 unrented_movie_to_price_shop
        self.rented_movies.discard((price, shop, movie))
        self.unrented_movie_to_price_shop[movie].add((price, shop))

    # 获取 rented_movies 的前 5 个 shop 和 movie
    def report(self) -> List[List[int]]:
        return [[shop, movie] for _, shop, movie in self.rented_movies[:5]]
''',
    call="""m = MovieRentingSystem(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]])
res = [m.search(1)]
m.rent(0, 1)
m.rent(1, 2)
res.append(m.report())
m.drop(1, 2)
res.append(m.search(2))
res""",
    expect=[[1, 0, 2], [[0, 1], [1, 2]], [0, 1]],
    skip=['self.shop_movie_to_price = {}', 'self.shop_movie_to_price[(shop, movie)] = price'],
    max_steps=80,
    views=[
        dict(type='map', var='self.unrented_movie_to_price_shop', label='未借出：movie → 有序的 (price, shop)', font=22,
             fmt=lambda k, v: f'{k}: {list(v)}', h=190),
        dict(type='array', var=_rented, label='已借出 rented_movies：有序的 (price, shop, movie)', cell=130, min_slots=3, h=170),
        dict(type='map', var='self.shop_movie_to_price', label='(shop, movie) → price', font=18,
             fmt=lambda k, v: f'{k}→{v}', h=140),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('movie', 'movie', 'cyan'), ('shop', 'shop', 'blue'), ('price', 'price', 'yellow')],
    captions={
        4: '三张表：未借出（按电影分组的有序集合）、已借出（一个有序集合）、租价哈希表',
        'for shop, movie, price in entries': '逐个录入库存：商店 `{shop}`，电影 `{movie}`，价格 `{price}`',
        9: '一开始全部未借出：电影 `{movie}` 的有序集合里加入 `({price}, {shop})`，按价格、再按商店排序',
        'return [shop for _, shop in': lambda S, B, ret: '有序集合已按 (价格, 商店) 排好，==前 5 个==就是最便宜的：`{}`'.format(ret),
        'price = self.shop_movie_to_price': '先用哈希表查到租价 `price = {price}`：有序集合里存的是 `(price, shop)`，得知道 price 才删得掉',
        '.discard((price, shop))': '从「未借出」里删掉 `({price}, {shop})`',
        'self.rented_movies.add': '加入「已借出」：`({price}, {shop}, {movie})`，自动排好序',
        '.discard((price, shop, movie))': '从「已借出」里删掉 `({price}, {shop}, {movie})`',
        27: '还回去：重新加进电影 `{movie}` 的未借出集合 `({price}, {shop})`',
        'return [[shop, movie] for': lambda S, B, ret: '已借出的有序集合前 5 个就是最便宜的已借出电影：`{}`'.format(ret),
    },
    cards=dict(
        one_liner='三张表：未借出按电影分组有序，已借出一张有序，再加一张租价表',
        complexity='`rent` / `drop` `O(log m)`，`search` / `report` 取前 5 个，空间 `O(m)`',
        problem=['`search(movie)`：未借出该电影的最便宜 5 家店（价格升序，同价店号小优先）',
                 '`rent(shop, movie)` / `drop(shop, movie)`：借出 / 归还',
                 '`report()`：已借出电影里最便宜的 5 部 `[shop, movie]`（价格、店号、电影号升序）'],
        quote='为了实现 search，需要对每部未借出电影维护对应的 (price, shop) 有序集合。这可以用哈希表套有序集合维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`search`：哈希表套有序集合，每部电影一个 `(price, shop)` 集合，取前 5 个',
              '`report`：一个全局的 `(price, shop, movie)` 有序集合，取前 5 个',
              '`rent` / `drop` 要在两个集合间搬动元素，需要价格：用哈希表 `(shop, movie) → price` 查'],
        summary=['初始化 `O(m log m)`；`rent` / `drop` `O(log m)`；空间 `O(m)`',
                 '易错：有序集合的元组顺序要和题目排序一致，`report` 里是 `(price, shop, movie)`',
                 'Python 无内置有序集合：原题解用 sortedcontainers，视频里用等价的小 SortedList 代替',
                 '另一个思路（yiduobo）：用堆 + 延迟删除代替有序集合'],
    ),
)
