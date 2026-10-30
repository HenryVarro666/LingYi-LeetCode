---
title: "1441. 用栈操作构建数组"
aliases: ["yiduobo的每日leetcode 1441.用栈操作构建数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/410057634"
zhihu_id: "410057634"
zhihu_title: "yiduobo的每日leetcode 1441.用栈操作构建数组"
question_id: "1441"
question: "用栈操作构建数组"
problem_url: "https://leetcode.cn/problems/build-an-array-with-stack-operations/"
difficulty: "Medium"
rating: 1180
created: "2021-09-13T23:38:39+08:00"
updated: "2021-09-13T23:38:39+08:00"
upvotes: 0
comments: 0
---

# 1441. 用栈操作构建数组

> **[yiduobo的每日leetcode 1441.用栈操作构建数组](https://zhuanlan.zhihu.com/p/410057634) · 知乎 · 2021-09-13 · 赞同 0**
> 力扣：[1441. 用栈操作构建数组](https://leetcode.cn/problems/build-an-array-with-stack-operations/) · Medium · 灵茶山艾府：[阅读理解，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1441.用栈操作构建数组

[力扣](https://leetcode-cn.com/problems/build-an-array-with-stack-operations/)

一趟扫描，对于target中出现的数字，需要在答案中加入一个push，否则需要在答案中加入一个push和一个pop。于是可以统计两个相邻数字之间空白数字的数目，也就是target[index] - target[index - 1] - 1，然后一次性加入批量的push和pop。对于target[index]，还需要额外加入一次push。

最后附上python代码：

```python
class Solution(object):
    def buildArray(self, target, n):
        """
        :type target: List[int]
        :type n: int
        :rtype: List[str]
        """

        last = 0
        res = []
        for num in target:
            res.extend(["Push", "Pop"] * (num - last - 1))
            res.append("Push")
            last = num
            
        return res
```
