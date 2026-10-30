---
title: "1488. 避免洪水泛滥"
aliases: ["yiduobo的每日leetcode 1488.避免洪水泛滥"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/union-find", "leetcode/ordered-set", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/七-并查集", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416462704"
zhihu_id: "416462704"
zhihu_title: "yiduobo的每日leetcode 1488.避免洪水泛滥"
question_id: "1488"
question: "避免洪水泛滥"
problem_url: "https://leetcode.cn/problems/avoid-flood-in-the-city/"
difficulty: "Medium"
rating: 1974
created: "2021-10-02T23:50:45+08:00"
updated: "2021-10-02T23:50:45+08:00"
upvotes: 1
comments: 0
---

# 1488. 避免洪水泛滥

> **[yiduobo的每日leetcode 1488.避免洪水泛滥](https://zhuanlan.zhihu.com/p/416462704) · 知乎 · 2021-10-02 · 赞同 1**
> 力扣：[1488. 避免洪水泛滥](https://leetcode.cn/problems/avoid-flood-in-the-city/) · Medium · 灵茶山艾府：[贪心 + 有序集合 / 并查集（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1488.避免洪水泛滥

[力扣](https://leetcode-cn.com/problems/avoid-flood-in-the-city/)

贪心法的题目。对于两个湖泊x和y，不妨设这两个湖泊当前都装满了水，且下一次下雨的时间分别为next[x]以及next[y]。假设现在有一天可以抽水，那么必然应该先抽next[x]及next[y]中较小值对应的那个湖泊。换言之，对于每次抽水，都应该抽一个泛滥时间最近的湖泊，于是可以使用一个堆来维护当前有水的湖泊下一次泛滥的时间。

为了得到这个泛滥的时间，则需要先进行一趟扫描，求出每个湖泊下一次下雨的时间。除此之外，还需要使用过一个set表示当前哪儿湖泊中有水。接下来一趟扫描，对于当前这一天index，设rains[index]为num：

1、若num为0，说明这一天可以抽水。若此时存在有水的湖泊，即堆不为空，那么应该抽堆顶元素heap\[0\]对应的rains\[heap\[0\]\]中的水，于是此时应该将堆顶弹出，并将其对应的rains\[heap\[0\]\]从set中移除，同时将其加入到答案中。若此时所有湖泊都是空的，即堆为空，那么在答案中随便加入一个数即可

2、若num不为0，说明这一天num这个湖泊将会下雨，此时首先在答案中加入-1。接下来，若num在set中出现过，说明num这个湖泊中原先就有水，于是此时应该返回空数组。最后，若next[index]为-1，说明num这个湖泊以后都不会再下雨，也就没有抽水的必要，否则应该将num加入到set中，并将next[index]加入到堆中，表示湖泊num下一次下雨的时间为next[index]。

最后附上python代码：

```python
class Solution(object):
    def avoidFlood(self, rains):
        """
        :type rains: List[int]
        :rtype: List[int]
        """

        n = len(rains)
        rain_dict = {}
        next_rain = [-1] * n
        for index, num in enumerate(rains):
            if num > 0:
                if num in rain_dict:
                    next_rain[rain_dict[num]] = index
                rain_dict[num] = index
        
        heap = []
        res = []
        rain_set = set()
        for index, num in enumerate(rains):
            if num == 0:
                if heap:
                    deal = heapq.heappop(heap)
                    rain_set.remove(rains[deal])
                    res.append(rains[deal])
                else:
                    res.append(1)
            else:
                res.append(-1)
                if num in rain_set:
                    return []
                if next_rain[index] != -1:
                    rain_set.add(num)
                    heapq.heappush(heap, next_rain[index])
        
        return res
```
