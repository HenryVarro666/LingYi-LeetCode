---
title: "1502. 判断能否形成等差数列"
aliases: ["yiduobo的每日leetcode 1502.判断能否形成等差数列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/sorting", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416799231"
zhihu_id: "416799231"
zhihu_title: "yiduobo的每日leetcode 1502.判断能否形成等差数列"
question_id: "1502"
question: "判断能否形成等差数列"
problem_url: "https://leetcode.cn/problems/can-make-arithmetic-progression-from-sequence/"
difficulty: "Easy"
created: "2021-10-07T17:58:24+08:00"
updated: "2021-10-07T17:58:24+08:00"
upvotes: 0
comments: 0
---

# 1502. 判断能否形成等差数列

> **[yiduobo的每日leetcode 1502.判断能否形成等差数列](https://zhuanlan.zhihu.com/p/416799231) · 知乎 · 2021-10-07 · 赞同 0**
> 力扣：[1502. 判断能否形成等差数列](https://leetcode.cn/problems/can-make-arithmetic-progression-from-sequence/) · Easy · 灵茶山艾府：[两种方法：从 O(nlogn) 到 O(n)（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1502.判断能否形成等差数列

[力扣](https://leetcode-cn.com/problems/can-make-arithmetic-progression-from-sequence/)

比较基础的题目。直接一趟扫描，计算相邻项之间的差值，并对比这个差值是否相同即可。

最后附上python代码：

```python
class Solution(object):
    def canMakeArithmeticProgression(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        arr = sorted(arr)
        d = arr[1] - arr[0]
        for index in range(2, len(arr)):
            if arr[index] - arr[index - 1] != d:
                return False
        
        return True
```
