---
title: "2445. 值为1的节点数"
aliases: ["yiduobo的每日leetcode 2445.值为1的节点数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631688294"
zhihu_id: "631688294"
zhihu_title: "yiduobo的每日leetcode 2445.值为1的节点数"
question_id: "2445"
question: "值为1的节点数"
problem_url: "https://leetcode.cn/problems/number-of-nodes-with-value-one/"
created: "2023-05-24T00:07:35+08:00"
updated: "2023-05-24T00:07:35+08:00"
upvotes: 0
comments: 0
---

# 2445. 值为1的节点数

> **[yiduobo的每日leetcode 2445.值为1的节点数](https://zhuanlan.zhihu.com/p/631688294) · 知乎 · 2023-05-24 · 赞同 0**
> 力扣：[2445. 值为1的节点数](https://leetcode.cn/problems/number-of-nodes-with-value-one/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2445.值为1的节点数

[力扣](https://leetcode.cn/problems/number-of-nodes-with-value-one/)

由于题目的翻转操作是离线的，那么可以先一趟遍历，将queries中的节点都进行翻转，然后再计算树中有哪些节点被翻转过。在这里需要使用一个数组记录每个节点是否被翻转。另外需要特别注意queries中可能多次出现相同的节点。

接下来，从根节点，也就是1号节点开始向下进行dfs。对于当前节点now，若now被翻转，那么就将这个翻转信息向下传递，也就是将now + now以及now+ now + 1都翻转，同时将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def numberOfNodes(self, n, queries):
        """
        :type n: int
        :type queries: List[int]
        :rtype: int
        """

        reverse = [False] * (n + 1)
        for v in queries:
            reverse[v] = not reverse[v]

        res = 0
        for index in range(1, n + 1):
            if reverse[index]:
                res += 1
                left = index * 2
                right = index * 2 + 1
                if left <= n:
                    reverse[left] = not reverse[left]
                if right <= n:
                    reverse[right] = not reverse[right]

        return res
```
