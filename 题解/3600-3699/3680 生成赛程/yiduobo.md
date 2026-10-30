---
title: "3680. 生成赛程"
aliases: ["yiduobo的每日leetcode 3680.生成赛程"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/random", "leetcode/randomized", "题单/数学算法", "题单/贪心算法", "题单/数学算法/六-随机算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953220889404508065"
zhihu_id: "1953220889404508065"
zhihu_title: "yiduobo的每日leetcode 3680.生成赛程"
question_id: "3680"
question: "生成赛程"
problem_url: "https://leetcode.cn/problems/generate-schedule/"
difficulty: "Medium"
rating: 2378
created: "2025-09-24T21:49:43+08:00"
updated: "2025-09-24T21:49:45+08:00"
upvotes: 2
comments: 0
---

# 3680. 生成赛程

> **[yiduobo的每日leetcode 3680.生成赛程](https://zhuanlan.zhihu.com/p/1953220889404508065) · 知乎 · 2025-09-24 · 赞同 2**
> 力扣：[3680. 生成赛程](https://leetcode.cn/problems/generate-schedule/) · Medium · 灵茶山艾府：[两种方法：构造 / 随机（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3680.生成赛程

<https://leetcode.cn/problems/generate-schedule/description/>

题目给出一个整数n，表示有n支队伍。现在要求生成一个赛程，使得每支队伍与其他队伍正好比赛两次，一次主场一次客场。每天只能进行一场比赛，且没有队伍在连续两天进行比赛。

要求返回一个二维数组schedule，其中schedule[index][0]表示主队，schedule[index][1]表示客队。如果有多个符合条件的赛程，返回其中任意一个。若没有，则返回空数组。

没有什么特别好的思路，不过按照题目中给出的样例来看，似乎每一轮都安排目前进行比赛最少，且上一轮没有安排过比赛，同时之前也没有进行过比赛的两只队伍进行比赛就是可行的处理方法。

沿着这个思路往下，只需要使用一个堆来维护每支队伍进行过的比赛次数，堆中记录的是二元组(tx, x)，表示x这只队伍目前已经进行过了tx场比赛。除此之外，还需要使用一个集合记录已经进行过比赛的队伍对，另外使用两个变量记录上一轮比赛的两个队伍。

接下来每一轮，先从堆中选出上一轮没有参加过比赛，且参加比赛次数最少的队伍x。具体的做法是判断堆顶的队伍是否为上一轮比赛的两个队伍之一，若是，则将其加入到一个等待数组pending_same中，这个数组中的队伍在本轮中是无法使用的，在本轮之后则需要将这些队伍加回到堆中；反之，则直接选取当前队伍作为x。

若无法选出可用的x，则直接返回空数组。

选出x之后，按相同的方法选择队伍y，同样是不断从堆中取出堆顶的队伍，要求是这只队伍上一轮没有参加比赛，同时这只队伍与x最多只进行过一场比赛。若不满足，且这只队伍在上一轮参加了比赛，则将其加入到pending_same中，否则将其加入到另一个等待数组pending_y中，需要注意这里的pending_y是因为选取了x，所以不能再进行选取，但是一旦x无法成行，那么就需要选取另一个x，此时pending_y中的队伍就可以放出来再次尝试配对了。

若无法选出可用的y，则将堆直接重置为pending_y，因为pending_y是按顺序取出来的，所以可以直接覆盖回去。接下来，将当前选出的x加入到第三个等待数组pending_x中，因为当前的x这一轮是无法再使用的。当然，如果无视数组的语义的话，直接加入到pending_same也没问题。

接下来回到第一步，重新选取x。重复此过程直到选出可用的队伍对x与y，或者没有合法的x为止。

如果能选出合法的队伍对(x, y)，接下来需要为这两只队伍安排比赛。若(x, y)已经安排过比赛，那么就交换x和y，然后安排一场(x, y)的比赛。接下来，更新x和y参加比赛的数量，然后加回到堆中，同时将三个等待数组中的队伍也都加回到堆中，最后将记录上一轮比赛两只队伍的两个变量分别更新为x和y即可。

以上方法的时间复杂度不好计算，而且直观感觉上构造得并不优美，不过好在本题的数据规模不大，处理起来还是没有问题的。

最后附上python代码：

```python
class Solution(object):
    def generateSchedule(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """
        
        heap = [(0, index) for index in range(n)]
        pre_x, pre_y = None, None
        using_pair = set()
        res = []

        while len(res) < n * (n - 1):
            pending_same = []
            pending_x = []
            x, y = None, None
            while y is None:
                while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y):
                    pending_same.append(heapq.heappop(heap))
            
                if heap:
                    tx, x = heapq.heappop(heap)
                else:
                    return []
            
                pending_y = []
                while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y or ((x, heap[0][1]) in using_pair and (heap[0][1], x) in using_pair)):
                    if heap[0][1] == pre_x or heap[0][1] == pre_y:
                        pending_same.append(heapq.heappop(heap))
                    else:
                        pending_y.append(heapq.heappop(heap))
            
                if heap:
                    ty, y = heapq.heappop(heap)
                else:
                    heap = pending_y[:]
                    pending_x.append((tx, x))
            
            if (x, y) in using_pair:
                x, y = y, x
                tx, ty = ty, tx
            
            res.append([x, y])
            using_pair.add((x, y))
            heapq.heappush(heap, (tx + 1, x))
            heapq.heappush(heap, (ty + 1, y))
            for p in pending_same:
                heapq.heappush(heap, p)
            for p in pending_x:
                heapq.heappush(heap, p)
            for p in pending_y:
                heapq.heappush(heap, p)

            pre_x, pre_y = x, y
        
        return res
```
