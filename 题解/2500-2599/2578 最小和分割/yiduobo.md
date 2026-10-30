---
title: "2578. 最小和分割"
aliases: ["yiduobo的每日leetcode 2578.最小和分割"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642243641"
zhihu_id: "642243641"
zhihu_title: "yiduobo的每日leetcode 2578.最小和分割"
question_id: "2578"
question: "最小和分割"
problem_url: "https://leetcode.cn/problems/split-with-minimum-sum/"
difficulty: "Easy"
rating: 1351
created: "2023-07-08T03:32:56+08:00"
updated: "2023-07-08T03:32:56+08:00"
upvotes: 0
comments: 0
---

# 2578. 最小和分割

> **[yiduobo的每日leetcode 2578.最小和分割](https://zhuanlan.zhihu.com/p/642243641) · 知乎 · 2023-07-08 · 赞同 0**
> 力扣：[2578. 最小和分割](https://leetcode.cn/problems/split-with-minimum-sum/) · Easy · 灵茶山艾府：[贪心：排序+奇偶分组（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2578.最小和分割

[力扣](https://leetcode.cn/problems/split-with-minimum-sum/)

为了使得最终的和最小，就应该让参与加法的两个数位数尽量少，也就是这两个数的位数应该尽量接近。另一方面，对于这两个数而言，则应该将较小的数字放在高位上，将较大的数字放在低位上。

根据这个结论，就可以先将num中的数字分离出来并从小到大排序，接下来遍历排序后的数字，交替分配个第一个数和第二个数。分配完成后，返回二者之和即可。

最后附上python代码：

```python
class Solution(object):
    def splitNum(self, num):
        """
        :type num: int
        :rtype: int
        """

        first = second = 0
        for index, digit in enumerate(sorted(list(str(num)))):
            if index % 2 == 0:
                first = first * 10 + int(digit)
            else:
                second = second * 10 + int(digit)
        
        return first + second
```
