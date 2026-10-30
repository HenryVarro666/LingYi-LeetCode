---
title: "1345. 跳跃游戏IV"
aliases: ["yiduobo的每日leetcode 1345.跳跃游戏IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/hash-table", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397172645"
zhihu_id: "397172645"
zhihu_title: "yiduobo的每日leetcode 1345.跳跃游戏IV"
question_id: "1345"
question: "跳跃游戏 IV"
problem_url: "https://leetcode.cn/problems/jump-game-iv/"
difficulty: "Hard"
rating: 1810
created: "2021-08-06T22:48:34+08:00"
updated: "2021-08-06T22:48:34+08:00"
upvotes: 1
comments: 0
---

# 1345. 跳跃游戏IV

> **[yiduobo的每日leetcode 1345.跳跃游戏IV](https://zhuanlan.zhihu.com/p/397172645) · 知乎 · 2021-08-06 · 赞同 1**
> 力扣：[1345. 跳跃游戏 IV](https://leetcode.cn/problems/jump-game-iv/) · Hard · 灵茶山艾府：[BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1345.跳跃游戏IV

[力扣](https://leetcode-cn.com/problems/jump-game-iv/)

题目除了可以正常的向左或者向右移动一步之外，还可以直接跳转到数值相同的位置上，那么我们可以先一趟扫描，使用一个dict来储存所有数值相同的位置列表。另外，对于数值相同的跳转，只有执行一次的必要。于是一种可行的做法是从0开始进行bfs，对于当前处理的位置now：

1、尝试向左走，若now - 1没有出界，且now - 1没有被访问过，那么将now - 1加入到bfs队列中

2、尝试向右走，若now + 1没有出界，且now + 1没有被访问过，那么将now + 1加入到bfs队列中

3、若arr[now]对应的数值相同跳转没有被使用过，那么枚举所有值等于arr[now]的位置p，若p没有被访问过，则将p加入到bfs队列中。枚举完成后，就不应该再执行数值等于arr[now]的跳转，因此将arr[now]从dict中删去

由于存在向右走一步这个操作，因此题目必然是有解的。若某一时刻走到了n - 1，那么当前bfs的轮次就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def minJumps(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)
        if n == 1:
            return 0

        num_dict = {}
        for index, num in enumerate(arr):
            if num not in num_dict:
                num_dict[num] = []
            num_dict[num].append(index)
        
        
        q = [0]
        l = 0
        r = 1
        used = [False] * n
        used[0] = True

        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                if now >= 1 and not used[now - 1]:
                    q.append(now - 1)
                    used[now - 1] = True
                if now < n - 1 and not used[now + 1]:
                    q.append(now + 1)
                    used[now + 1] = True
                if arr[now] in num_dict:
                    for p in num_dict[arr[now]]:
                        if not used[p]:
                            q.append(p)
                            used[p] = True
                    num_dict.pop(arr[now])
                    
                if used[n - 1]:
                    return step

            l, r = r, len(q)
```
