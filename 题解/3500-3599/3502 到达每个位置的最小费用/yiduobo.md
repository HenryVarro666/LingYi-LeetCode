---
title: "3502. 到达每个位置的最小费用"
aliases: ["yiduobo的每日leetcode 3502.到达每个位置的最小费用"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901382865456988651"
zhihu_id: "1901382865456988651"
zhihu_title: "yiduobo的每日leetcode 3502.到达每个位置的最小费用"
question_id: "3502"
question: "到达每个位置的最小费用"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-reach-every-position/"
difficulty: "Easy"
created: "2025-05-01T22:04:42+08:00"
updated: "2025-05-01T22:04:42+08:00"
upvotes: 1
comments: 0
---

# 3502. 到达每个位置的最小费用

> **[yiduobo的每日leetcode 3502.到达每个位置的最小费用](https://zhuanlan.zhihu.com/p/1901382865456988651) · 知乎 · 2025-05-01 · 赞同 1**
> 力扣：[3502. 到达每个位置的最小费用](https://leetcode.cn/problems/minimum-cost-to-reach-every-position/) · Easy · 灵茶山艾府：[本质是前缀最小值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3502.到达每个位置的最小费用

[3502. 到达每个位置的最小费用 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-reach-every-position/description/)

题目给出一个长度为n + 1的队伍，标号从0到n，一开始的位置处于队伍的末尾，即位置n。另外给出一个长度为n的整数数组cost，其中元素的大小在1到100之间。

现在可以与队伍中的其他人交换位置，若交换的对象所在的位置index在更前面，那么需要支付cost[index]才能进行交换；若index在更后面，则可以免费与其交换位置。

现在要求返回一个长度为n的数组answer，其中answer[index]表示交换到index所需的最小代价。

首先对于index \= 0的情况，应该直接与0进行交换，因为无论中途如何交换，最后这一步交换必然是与更前面的0进行交换，也就是说这个cost[0]是必须要支付的。为了使得代价最小，中途就不应该有其他额外的操作。

接下来对于index > 0的情况，有两种交换的方法。

第一种依然是直接与index进行交换，代价为cost[index]。在这个过程中不应该与所有大于index的位置进行交换，这些交换是没有必要的。

第二种则是先与index之前的某个位置交换，然后再免费交换到index。对于这种情况，就应该选择cost[0]到cost[index - 1]中最小的值对应的那个下标进行交换。

综合起来，就可以趟遍历，使用一个变量维护cost前缀的最小值，若这个最小值小于当前index对应的cost，就选择第二种交换的方法，所需的代价就是前缀最小值，反之则应该直接进行交换，代价为cost[index]。

另外，由于answer数组实际上储存的就是前缀最小值，因此无需额外维护前缀最小值，使用answer数组的最后一项与cost[index]进行比较就行了。

最后附上python代码：

```python
class Solution(object):
    def minCosts(self, cost):
        """
        :type cost: List[int]
        :rtype: List[int]
        """
        
        res = [cost[0]]
        for v in cost[1:]:
            res.append(min(res[-1], v))
        return res
```
