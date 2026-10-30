---
title: "679. 24点游戏"
aliases: ["yiduobo的每日leetcode 679.24点游戏"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/301761729"
zhihu_id: "301761729"
zhihu_title: "yiduobo的每日leetcode 679.24点游戏"
question_id: "679"
question: "24 点游戏"
problem_url: "https://leetcode.cn/problems/24-game/"
difficulty: "Hard"
created: "2020-11-19T23:59:13+08:00"
updated: "2020-11-19T23:59:13+08:00"
upvotes: 0
comments: 0
---

# 679. 24点游戏

> **[yiduobo的每日leetcode 679.24点游戏](https://zhuanlan.zhihu.com/p/301761729) · 知乎 · 2020-11-19 · 赞同 0**
> 力扣：[679. 24 点游戏](https://leetcode.cn/problems/24-game/) · Hard · 灵茶山艾府：[每次合并两张牌，递归写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

679\. 24点游戏

[力扣](https://leetcode-cn.com/problems/24-game/)

经典问题，我在这里的做法是先两两配对，用set记录下某两个数通过加减乘除可以形成的所有结果，然后枚举这些数对看是否存在两个结果可以构成24。若不能，将第三个数加入到这些数对中，依然是用set记录下来所有可能的结果，然后看这些结果能否与第四个数构成24。

最后附上python代码，其中res_dict记录每种组合的结果，使用状态压缩的方式储存。由于这里涉及到除法运算，因此我采用的是同时保存分子和分母的做法，从而避免实数运算：

```python
class Solution(object):
    def judgePoint24(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        res_dict = {}
        for i in range(3):
            for j in range(i + 1, 4):
                k = (1 << i) + (1 << j)
                x, y = nums[i], nums[j]
                res_dict[k] = set()
                res_dict[k].add((x + y, 1))
                res_dict[k].add((x - y, 1))
                res_dict[k].add((y - x, 1))
                res_dict[k].add((x * y, 1))
                res_dict[k].add((x, y))
                res_dict[k].add((y, x))

        for i in range(3):
            for j in range(i + 1, 4):
                k = (1 << i) + (1 << j)
                for (x1, y1) in res_dict[k]:
                    for (x2, y2) in res_dict[15 - k]:
                        if x1 * y2 + x2 * y1 == 24 * y1 * y2:
                            return True
                        elif x1 * y2 - x2 * y1 == 24 * y1 * y2:
                            return True
                        elif x2 * y1 - x1 * y2 == 24 * y1 * y2:
                            return True
                        elif x1 * x2 == 24 * y1 * y2:
                            return True
                        elif x1 != 0 and x1 * y2 * 24 == x2 * y1:
                            return True
                        elif x2 != 0 and x1 * y2 == x2 * y1 * 24:
                            return True
                
                for l in range(4):
                    if k & (1 << l) == 0:
                        tmp = k + (1 << l)
                        if tmp not in res_dict:
                            res_dict[tmp] = set()
                        for (x, y) in res_dict[k]:
                            res_dict[tmp].add((x + nums[l] * y, y))
                            res_dict[tmp].add((x - nums[l] * y, y))
                            res_dict[tmp].add((nums[l] * y - x, y))
                            res_dict[tmp].add((x * nums[l], y))
                            res_dict[tmp].add((x, y * nums[l]))
                            if x != 0:
                                res_dict[tmp].add((y * nums[l], x))

        for i in range(4):
            j = 15 - (1 << i)
            for (x, y) in res_dict[j]:
                if nums[i] * y + x == 24 * y:
                    return True
                elif nums[i] * y - x == 24 * y:
                    return True
                elif x - nums[i] * y == 24 * y:
                    return True
                elif x * nums[i] == 24 * y:
                    return True
                elif x == 24 * y * nums[i]:
                    return True
                elif x != 0 and nums[i] * y == 24 * x:
                    return True

        
        return False
```
