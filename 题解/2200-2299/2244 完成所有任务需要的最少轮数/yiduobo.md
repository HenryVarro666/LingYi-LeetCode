---
title: "2244. 完成所有任务需要的最少轮数"
aliases: ["yiduobo的每日leetcode 2244.完成所有任务需要的最少轮数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545564342"
zhihu_id: "545564342"
zhihu_title: "yiduobo的每日leetcode 2244.完成所有任务需要的最少轮数"
question_id: "2244"
question: "完成所有任务需要的最少轮数"
problem_url: "https://leetcode.cn/problems/minimum-rounds-to-complete-all-tasks/"
difficulty: "Medium"
rating: 1372
created: "2022-07-24T18:18:48+08:00"
updated: "2022-07-24T18:18:48+08:00"
upvotes: 0
comments: 1
---

# 2244. 完成所有任务需要的最少轮数

> **[yiduobo的每日leetcode 2244.完成所有任务需要的最少轮数](https://zhuanlan.zhihu.com/p/545564342) · 知乎 · 2022-07-24 · 赞同 0**
> 力扣：[2244. 完成所有任务需要的最少轮数](https://leetcode.cn/problems/minimum-rounds-to-complete-all-tasks/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2244.完成所有任务需要的最少轮数

[力扣](https://leetcode.cn/problems/minimum-rounds-to-complete-all-tasks/)

题目中每种任务的执行都是互不相关的，因此首先可以分别统计每种任务的数量。根据样例2的提示，当某种任务仅出现一次时，是无法完成的，此时直接返回-1。

接下来考虑一般情况。为了使得轮数尽量少，就应该尽可能多地3个3个一轮来执行任务。对于某种任务，设其出现了cnt次，那么就有三种情况：

1、cnt是3的倍数。此时3个3个一轮安排就行了，一共需要安排cnt / 3轮。

2、cnt模3余1。由于一开始已经处理了cnt等于1的情况，此时的cnt必然是大于等于4的。如果按3个3个一轮安排，一共将安排k \= cnt / 3轮，这里的k必然大于等于1。此时还有一个落单的任务没有完成，那么可以从这k轮里面拿出来一轮，只安排两个任务，多出来的另一个任务则与这个落单的任务放到另一轮执行，因此一共需要cnt / 3 + 1轮。

3、cnt模3余2。此时同样是3个3个一轮安排，多出来的两个任务再额外安排一轮就行了，因此需要的轮数也是cnt / 3 + 1。

综合起来，对于每个cnt，都是先安排cnt / 3轮，如果cnt % 3不为0，那么还需要额外一轮。

最后附上python代码：

```python
class Solution(object):
    def minimumRounds(self, tasks):
        """
        :type tasks: List[int]
        :rtype: int
        """

        cnt_dict = {}
        for task in tasks:
            cnt_dict[task] = cnt_dict.get(task, 0) + 1
        
        res = 0
        for cnt in cnt_dict.values():
            if cnt == 1:
                return -1
            
            res += cnt / 3
            if cnt % 3 > 0:
                res += 1
        
        return res
```
