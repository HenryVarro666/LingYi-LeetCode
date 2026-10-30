---
title: "3488. 距离最小相等元素查询"
aliases: ["yiduobo的每日leetcode 3488.距离最小相等元素查询"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897436280654102532"
zhihu_id: "1897436280654102532"
zhihu_title: "yiduobo的每日leetcode 3488.距离最小相等元素查询"
question_id: "3488"
question: "距离最小相等元素查询"
problem_url: "https://leetcode.cn/problems/closest-equal-element-queries/"
difficulty: "Medium"
created: "2025-04-24T22:51:57+08:00"
updated: "2025-04-24T22:51:57+08:00"
upvotes: 1
comments: 0
---

# 3488. 距离最小相等元素查询

> **[yiduobo的每日leetcode 3488.距离最小相等元素查询](https://zhuanlan.zhihu.com/p/1897436280654102532) · 知乎 · 2025-04-24 · 赞同 1**
> 力扣：[3488. 距离最小相等元素查询](https://leetcode.cn/problems/closest-equal-element-queries/) · Medium · 灵茶山艾府：[两种方法：二分查找 / 预处理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3488.距离最小相等元素查询

[3488. 距离最小相等元素查询 - 力扣（LeetCode）](https://leetcode.cn/problems/closest-equal-element-queries/description/)

题目给出一个循环数组nums以及一个询问数组queries。对于每个询问queries\[index\]，需要找出满足与nums\[queirs\[index\]\]相等的nums\[p\]，且p与queries\[index\]的距离最近。若不存在这样的p，则本次查询的结果为-1。

首先可以明确的是，对于nums中的某个位置nums[index]而言，与其相等且距离index最近的p的必然是nums[index]这个数值在nums中上一次出现或者下一次出现的位置这二者之一，于是可以先对nums进行一趟遍历，使用一个哈希表pos_dict将nums中每个数值出现的所有位置都收集起来，其中pos_dict[v]是一个list，表示v在nums中出现的所有下标。由于是遍历计算得到的，因此pos_dict[v]天然是单调递增的。

接下来对于pos_dict[v]中的某个下标p \= pos_dict[v][index]，其在nums中上一次和下一次出现的位置就分别为pos_dict[v][(index - 1 + m) % m]以及pos_dict[v][(index + 1) % m]，其中m为pos_dict[v]的长度。基于这一点，就可以设置两个长度为n的数组pre和nxt，分别记录nums中的每个p对应的元素值nums[p]在nums中上一次和下一次出现的下标。

预处理完成后，再对queries进行一趟遍历。对于当前的询问q，若pre[q] \= q，说明数组中只有这唯一一个nums[q]，此时查询的结果为-1，否则答案就是q到pre[q]的距离，即(q + n - pre[q]) % n以及q到nxt[q]的距离，即(nxt[q] + n - q) % n这二者中的较小值。

最后附上python代码：

```python
class Solution(object):
    def solveQueries(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[int]
        :rtype: List[int]
        """
        
        pos_dict = {}
        for index, v in enumerate(nums):
            if v not in pos_dict:
                pos_dict[v] = []
            pos_dict[v].append(index)
        
        n = len(nums)
        pre = [None] * n
        nxt = [None] * n

        for v in pos_dict:
            m = len(pos_dict[v])
            for index, p in enumerate(pos_dict[v]):
                pre[p] = pos_dict[v][(index - 1 + m) % m]
                nxt[p] = pos_dict[v][(index + 1) % m]

        res = []
        for q in queries:
            if pre[q] == q:
                res.append(-1)
            else:
                res.append(min((q + n - pre[q]) % n, (nxt[q] + n - q) % n))
        
        return res
```
