---
title: "1912. 设计电影租借系统"
aliases: ["yiduobo的每日leetcode 1912.设计电影租借系统"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/483481037"
zhihu_id: "483481037"
zhihu_title: "yiduobo的每日leetcode 1912.设计电影租借系统"
question_id: "1912"
question: "设计电影租借系统"
problem_url: "https://leetcode.cn/problems/design-movie-rental-system/"
difficulty: "Hard"
rating: 2182
created: "2022-03-19T00:10:30+08:00"
updated: "2022-03-19T00:10:31+08:00"
upvotes: 1
comments: 0
---

# 1912. 设计电影租借系统

> **[yiduobo的每日leetcode 1912.设计电影租借系统](https://zhuanlan.zhihu.com/p/483481037) · 知乎 · 2022-03-19 · 赞同 1**
> 力扣：[1912. 设计电影租借系统](https://leetcode.cn/problems/design-movie-rental-system/) · Hard · 灵茶山艾府：[有序集合（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1912.设计电影租借系统

[力扣](https://leetcode-cn.com/problems/design-movie-rental-system/)

除了常规的借和还操作之外，题目还要求提供查询指定电影现存价格最低的5个来源，以及已解出的电影中价格最低的五部电影及其来源。

对于这种动态top k问题，常规做法自然是平衡二叉树，不过在这里只需要找top 5，因此使用一个堆，从堆顶pop 5次也能达到同样的效果。我在这里就是采用的堆来实现。

具体的，对于每一部电影都维护一个堆movie_shop_heap，堆中元素为二元组(price, shop)，表示当前现存的来源。对于已借出的电影同样维护一个堆report_heap，堆中元素为三元组(price, shop, movie)，表示已解出电影的各种信息。

由于python的堆不支持直接从堆中删去指定元素，因此在这里需要用到延迟更新的技巧。当一部电影被借出时，按理说应该将其从movie_shop_heap删去。不过在这里并不直接执行删除操作，而是等到下一次search操作时，如果pop堆顶的过程中发现该电影已经被借走，那么就顺便将其删去。为了满足这个操作，就需要再维护一个集合rented_set来记录当前哪些电影已经被借出去了。

这样做的话可能出现一个问题，即某部电影被借出后，其可能一直都没有被弹出movie_shop_heap。而当这部电影被归还之后，其可能被重新加入到movie_shop_heap，这样一来movie_shop_heap里面就会有两条关于这部电影的信息。

一个可行的解决办法是再维护一个集合in_movie_heap来记录哪些电影目前在movie_shop_heap中。很明显，in_movie_heap初始情况下应该包含所有的电影，接下来：

1、对于每次search操作，如果某部电影因为被借走而被弹出movie_shop_heap，那么就需要同时将其从集合in_movie_heap中删去

2、对于每次归还操作，如果某部电影当前没有在集合in_movie_heap中，那么就需要将其重新加入到堆movie_shop_heap中，同时也需要将其加入到集合in_movie_heap中。否则的话，就说明其之前要么没被借走，要么被借走了还没被弹出movie_shop_heap，因此无需再次将其加入movie_shop_heap中

需要注意的是，在借操作时并不需要更新in_movie_heap

类似的，对于归还操作，也不是第一时间更新report_heap，而是等到report操作时，如果pop堆顶的过程中发现该电影已经被归还，那么就顺便将其删去。

当然，这样做也会遇到同样的问题，即某部电影被归还后，其可能一直都没有被弹出report_heap。而当这部电影再一次被借走时，其可能再次加入到report_heap中。解决方案与上面一样，也是再维护一个集合in_report_heap来记录哪些电影目前在report_heap中。in_report_heap初始值显然是空，接下来：

1、对于每次report操作，如果某部电影因为被归还而被弹出report_heap，那么就需要同时将其从集合in_report_heap中删去

2、对于每次借操作，如果某部电影当前没有在集合in_report_heap中，那么就需要将其加入到堆report_heap中，同时也需要将其加入到集合in_report_heap中。否则的话，就说明其之前被归还了但还没被弹出report_heap，因此无需再次将其加入report_heap中

最后附上python代码：

```python
class MovieRentingSystem(object):

    def __init__(self, n, entries):
        """
        :type n: int
        :type entries: List[List[int]]
        """
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
        """
        :type movie: int
        :rtype: List[int]
        """
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
        """
        :type shop: int
        :type movie: int
        :rtype: None
        """
        price = self.price_dict[(shop, movie)]
        self.rented_set.add((price, shop, movie))
        if (shop, movie) not in self.in_report_heap:
            self.in_report_heap.add((shop, movie))
            heapq.heappush(self.report_heap, [price, shop, movie])

    def drop(self, shop, movie):
        """
        :type shop: int
        :type movie: int
        :rtype: None
        """
        price = self.price_dict[(shop, movie)]
        self.rented_set.remove((price, shop, movie))
        if (price, shop, movie) not in self.in_movie_heap:
            self.in_movie_heap.add((price, shop, movie))
            heapq.heappush(self.movie_shop_heap[movie], [price, shop])

    def report(self):
        """
        :rtype: List[List[int]]
        """

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

# Your MovieRentingSystem object will be instantiated and called as such:
# obj = MovieRentingSystem(n, entries)
# param_1 = obj.search(movie)
# obj.rent(shop,movie)
# obj.drop(shop,movie)
# param_4 = obj.report()
```
