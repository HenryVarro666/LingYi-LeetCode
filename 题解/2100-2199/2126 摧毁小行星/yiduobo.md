---
title: "2126. 摧毁小行星"
aliases: ["yiduobo的每日leetcode 2126.摧毁小行星"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/贪心算法", "题单/位运算/九-其他", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/526186519"
zhihu_id: "526186519"
zhihu_title: "yiduobo的每日leetcode 2126.摧毁小行星"
question_id: "2126"
question: "摧毁小行星"
problem_url: "https://leetcode.cn/problems/destroying-asteroids/"
difficulty: "Medium"
rating: 1335
created: "2022-06-08T23:41:54+08:00"
updated: "2022-06-08T23:41:54+08:00"
upvotes: 0
comments: 0
---

# 2126. 摧毁小行星

> **[yiduobo的每日leetcode 2126.摧毁小行星](https://zhuanlan.zhihu.com/p/526186519) · 知乎 · 2022-06-08 · 赞同 0**
> 力扣：[2126. 摧毁小行星](https://leetcode.cn/problems/destroying-asteroids/) · Medium · 灵茶山艾府：[贪心证明，以及 O(n) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2126.摧毁小行星

[力扣](https://leetcode.cn/problems/destroying-asteroids/)

比较简单的贪心题，将小行星从小到大进行排序，然后一趟遍历尝试逐个摧毁。对于当前遍历到的小行星，若能摧毁，则将其质量累加到当前质量中，否则返回false。若能够成功完成遍历，则返回true。

最后附上python代码：

```python
class Solution(object):
    def asteroidsDestroyed(self, mass, asteroids):
        """
        :type mass: int
        :type asteroids: List[int]
        :rtype: bool
        """

        for ast in sorted(asteroids):
            if mass >= ast:
                mass += ast
            else:
                return False

        return True
```
