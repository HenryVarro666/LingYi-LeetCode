
CONFIG = dict(
    num=1912, title='设计电影租借系统', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='堆 + 延迟删除',
    tags=['堆（优先队列）', '难度分 2182'],
    code='''
class MovieRentingSystem(object):

    def __init__(self, n, entries):
        self.movie_shop_heap = {}
        self.report_heap = []
        self.in_movie_heap = set()
        self.in_report_heap = set()
        self.rented_set = set()
        self.price_dict = {}
        for shop, movie, price in entries:
            self.price_dict[(shop, movie)] = price
            if movie not in self.movie_shop_heap:
                self.movie_shop_heap[movie] = [[price, shop]]
            else:
                heapq.heappush(self.movie_shop_heap[movie], [price, shop])
            self.in_movie_heap.add((price, shop, movie))

    def search(self, movie):
        if movie not in self.movie_shop_heap:
            return []

        top5 = []
        while len(top5) < 5 and self.movie_shop_heap[movie]:
            price, shop = heapq.heappop(self.movie_shop_heap[movie])
            if (price, shop, movie) not in self.rented_set:
                top5.append([price, shop])
            else:
                self.in_movie_heap.remove((price, shop, movie))

        for info in top5:
            heapq.heappush(self.movie_shop_heap[movie], info)
        
        return [info[1] for info in top5]

    def rent(self, shop, movie):
        price = self.price_dict[(shop, movie)]
        self.rented_set.add((price, shop, movie))
        if (shop, movie) not in self.in_report_heap:
            self.in_report_heap.add((shop, movie))
            heapq.heappush(self.report_heap, [price, shop, movie])

    def drop(self, shop, movie):
        price = self.price_dict[(shop, movie)]
        self.rented_set.remove((price, shop, movie))
        if (price, shop, movie) not in self.in_movie_heap:
            self.in_movie_heap.add((price, shop, movie))
            heapq.heappush(self.movie_shop_heap[movie], [price, shop])

    def report(self):

        top5 = []
        while len(top5) < 5 and self.report_heap:
            price, shop, movie = heapq.heappop(self.report_heap)
            if (price, shop, movie) in self.rented_set:
                top5.append([price, shop, movie])
            else:
                self.in_report_heap.remove((shop, movie))
        
        for info in top5:
            heapq.heappush(self.report_heap, info)
        
        return [[info[1], info[2]] for info in top5]

''',
    call="""m = MovieRentingSystem(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]])
m.rent(1, 1)
res = [m.search(1)]
m.rent(0, 1)
res.append(m.report())
m.drop(1, 1)
res.append(m.search(1))
res.append(m.report())
res""",
    expect=[[0, 2], [[1, 1], [0, 1]], [1, 2], [[0, 1]]],
    skip=list(range(3, 17)) + ['for info in top5', 'heapq.heappush(self.movie_shop_heap[movie], info)', 'heapq.heappush(self.report_heap, info)'],
    max_steps=90,
    views=[
        dict(type='map', var='self.movie_shop_heap', label='movie_shop_heap：电影 → (price, shop) 堆', font=20,
             fmt=lambda k, v: f'{k}: {[tuple(x) for x in sorted(v)]}', h=100),
        dict(type='heap', var='self.report_heap', label='report_heap (price, shop, movie)', fmt=lambda x: f'({x[0]},{x[1]},{x[2]})', top_color='yellow', h=120),
        dict(type='set', var='self.rented_set', label='rented_set：真正借出的', font=20, fmt=lambda x: f'({x[0]},{x[1]},{x[2]})', h=100),
        dict(type='set', var='self.in_movie_heap', label='in_movie_heap：还在 movie_shop_heap 里的', font=18, fmt=lambda x: f'({x[0]},{x[1]},{x[2]})', h=115),
        dict(type='set', var='self.in_report_heap', label='in_report_heap：还在 report_heap 里的 (shop, movie)', font=20, fmt=lambda x: f'({x[0]},{x[1]})', h=105),
        dict(type='calls', label='正在执行', h=70),
    ],
    watch=[('movie', 'movie', 'cyan'), ('price', 'price', 'yellow'), ('shop', 'shop', 'blue'), ('top5', 'top5', 'green')],
    captions={
        'if movie not in self.movie_shop_heap': '先看有没有这部电影的堆：有，往下取前 5',
        'return []': '没有这部电影的记录，返回空列表',
        'top5 = []': '`top5` 存这次真正有效的前 5 个',
        'while len(top5) < 5 and self.movie_shop_heap[movie]': lambda S, B, ret: ('还没凑够 5 个，堆里还有，继续弹' if len(S.top5) < 5 and S['self.movie_shop_heap'][S.movie] else '凑够 5 个或堆空了，停止'),
        'price, shop = heapq.heappop(self.movie_shop_heap[movie])': '弹出堆顶 `({price}, {shop})`，看它还在不在架上',
        'if (price, shop, movie) not in self.rented_set': lambda S, B, ret: ('不在 `rented_set` → 是有效的（没被借走）' if (S.price, S.shop, S.movie) not in S['self.rented_set'] else '在 `rented_set` 里：==已经被借走了，却还躺在堆里=='),
        'top5.append([price, shop])': '有效：记入 `top5`',
        'self.in_movie_heap.remove': '==延迟删除==：顺便把借走的这条丢掉，并从 `in_movie_heap` 去掉标记',
        'return [info[1] for info in top5]': lambda S, B, ret: '有效的几条已 ==push 回堆==（不能丢），只返回店号：`{}`'.format(ret),
        'price = self.price_dict[(shop, movie)]': '查到价格 `price = {price}`',
        'self.rented_set.add': '登记「已借出」：`({price}, {shop}, {movie})`（不动 movie_shop_heap，等 search 时再清）',
        'if (shop, movie) not in self.in_report_heap': lambda S, B, ret: ('`report_heap` 里没有它 → 要加进去' if (S.shop, S.movie) not in S['self.in_report_heap'] else '它还留在 `report_heap` 里（归还时没清）→ 不用重复加'),
        'self.in_report_heap.add': '记住它在 `report_heap` 里',
        'heapq.heappush(self.report_heap': '压入 `report_heap`：`[{price}, {shop}, {movie}]`',
        'self.rented_set.remove': '归还：从 `rented_set` 删掉（不动 report_heap，等 report 时再清）',
        'if (price, shop, movie) not in self.in_movie_heap': lambda S, B, ret: ('之前 search 已把它弹出过 → 要重新压回 `movie_shop_heap`' if (S.price, S.shop, S.movie) not in S['self.in_movie_heap'] else '它还留在 `movie_shop_heap` 里 → 不能重复压，否则会有两份'),
        'self.in_movie_heap.add((price, shop, movie))': '重新标记：它又在 `movie_shop_heap` 里了',
        'heapq.heappush(self.movie_shop_heap[movie], [price, shop])': '压回电影 `{movie}` 的堆：`[{price}, {shop}]`',
        'while len(top5) < 5 and self.report_heap': lambda S, B, ret: ('还没凑够 5 个，继续弹 `report_heap`' if len(S.top5) < 5 and S['self.report_heap'] else '停止'),
        'price, shop, movie = heapq.heappop(self.report_heap)': '弹出 `({price}, {shop}, {movie})`',
        'if (price, shop, movie) in self.rented_set': lambda S, B, ret: ('仍在 `rented_set` → 有效的已借出' if (S.price, S.shop, S.movie) in S['self.rented_set'] else '不在 `rented_set`：==早就归还了，延迟到现在才清掉=='),
        'top5.append([price, shop, movie])': '有效：记入 `top5`',
        'self.in_report_heap.remove': '清理：从 `in_report_heap` 去掉标记',
        'return [[info[1], info[2]]': lambda S, B, ret: '有效的几条已 ==push 回堆==，返回 `[shop, movie]`：`{}`'.format(ret),
    },
    cards=dict(
        one_liner='用堆取前 5；删不了中间元素，就先标记，等弹到时再清（延迟删除）',
        complexity='每次 `search` / `report` 最多弹 5 + 过期条数，均摊 `O(log m)`',
        problem=['`search(movie)`：未借出该电影的最便宜 5 家店',
                 '`rent` / `drop`：借出 / 归还；`report()`：已借出电影里最便宜的 5 部',
                 '本视频：借 (1,1)、搜 1、借 (0,1)、report、还 (1,1)、搜 1、report'],
        quote='python的堆不支持直接从堆中删去指定元素，因此在这里需要用到延迟更新的技巧。当一部电影被借出时，按理说应该将其从movie_shop_heap删去。不过在这里并不直接执行删除操作，而是等到下一次search操作时，如果pop堆顶的过程中发现该电影已经被借走，那么就顺便将其删去。',
        quote_src='—— yiduobo 题解原文',
        idea=['每部电影一个 `(price, shop)` 堆，另一个全局 `report_heap`；取前 5 = 弹 5 次再压回去',
              '借 / 还只改 `rented_set`；堆里的过期元素等 `search` / `report` 弹到时才清掉',
              '`in_movie_heap` / `in_report_heap` 记录谁还在堆里，防止同一条被压两次'],
        summary=['均摊 `O(log m)`；堆里可能暂存过期元素，空间 `O(m)`',
                 '易错：借出时不用动 `in_movie_heap`；归还时先看是否还在堆里，在就不能重复压',
                 '`search` / `report` 弹出的有效元素必须 push 回去',
                 '原文本身已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：有序集合直接增删改；这里用堆 + 延迟删除'],
    ),
)
