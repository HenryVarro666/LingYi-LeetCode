---
title: "2353. 设计食物评分系统"
aliases: ["yiduobo的每日leetcode 2353.设计食物评分系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561611639"
zhihu_id: "561611639"
zhihu_title: "yiduobo的每日leetcode 2353.设计食物评分系统"
question_id: "2353"
question: "设计食物评分系统"
problem_url: "https://leetcode.cn/problems/design-a-food-rating-system/"
difficulty: "Medium"
rating: 1782
created: "2022-09-06T00:09:15+08:00"
updated: "2022-09-06T00:09:15+08:00"
upvotes: 1
comments: 0
---

# 2353. 设计食物评分系统

> **[yiduobo的每日leetcode 2353.设计食物评分系统](https://zhuanlan.zhihu.com/p/561611639) · 知乎 · 2022-09-06 · 赞同 1**
> 力扣：[2353. 设计食物评分系统](https://leetcode.cn/problems/design-a-food-rating-system/) · Medium · 灵茶山艾府：[两种方法：有序集合 / 懒删除堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2353.设计食物评分系统

[力扣](https://leetcode.cn/problems/design-a-food-rating-system/)

本题与之前的2349题大同小异，做法也是类似，对于每种cuisine都维护一个堆，储存这种烹饪方式下的所有食物以及评分。除此之外，还需要使用一个哈希表来记录每种食物当前的得分。对于题目给出的两种操作：

1、修改食物评分：

此时需要修改哈希表中对应食物的评分，同时将修改的(食物、新的评分)对加入到对应烹饪方式的堆中。由于题目只给出了食物和评分，那么还需要额外使用一个哈希表，记录每种食物对应的烹饪方式。

2、返回指定烹饪方式下的最高评分的食物：

找到该烹饪方式对应的堆，并通过哈希表检测当前堆顶食物的评分是否与堆中记录的一致。若不一致，说明这个食物的评分已经被修改过，不能作数，因此需要将该食物从堆顶弹出，然后重复此过程，直到出现某种得分在哈希表和堆中一致的食物，即为所求的答案。

最后附上python代码：

```python
class FoodRatings(object):

    def __init__(self, foods, cuisines, ratings):
        """
        :type foods: List[str]
        :type cuisines: List[str]
        :type ratings: List[int]
        """

        self.f_map = {}
        self.f_reverse_map = {}
        sorted_foods = sorted(foods)
        for index, f in enumerate(sorted_foods):
            self.f_map[f] = index
            self.f_reverse_map[index] = f

        self.c_map = {}
        self.heap_dict = {}
        self.cuisine_dict = {}
        self.rating_dict = {}
        n = len(foods)
        cnt = 0
        for index in range(n):
            f_id = self.f_map[foods[index]]

            if cuisines[index] not in self.c_map:
                self.c_map[cuisines[index]] = cnt
                cnt += 1
            
            c_id = self.c_map[cuisines[index]]

            r = ratings[index]

            if c_id not in self.heap_dict:
                self.heap_dict[c_id] = []
            heapq.heappush(self.heap_dict[c_id], [-r, f_id])
            self.cuisine_dict[f_id] = c_id
            self.rating_dict[f_id] = r

    def changeRating(self, food, newRating):
        """
        :type food: str
        :type newRating: int
        :rtype: None
        """
        f_id = self.f_map[food]
        if self.rating_dict[f_id] == newRating:
            return

        c_id = self.cuisine_dict[f_id]
        heappush(self.heap_dict[c_id], [-newRating, f_id])
        self.rating_dict[f_id] = newRating

    def highestRated(self, cuisine):
        """
        :type cuisine: str
        :rtype: str
        """
        c_id = self.c_map[cuisine]
        while True:
            r, f_id = self.heap_dict[c_id][0]
            r = -r
            if self.rating_dict[f_id] == r:
                return self.f_reverse_map[f_id]
            
            heapq.heappop(self.heap_dict[c_id])

# Your FoodRatings object will be instantiated and called as such:
# obj = FoodRatings(foods, cuisines, ratings)
# obj.changeRating(food,newRating)
# param_2 = obj.highestRated(cuisine)
```
