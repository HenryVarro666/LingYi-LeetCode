---
title: "1963. 使字符串平衡的最小交换次数"
aliases: ["yiduobo的每日leetcode 1963.使字符串平衡的最小交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/494171553"
zhihu_id: "494171553"
zhihu_title: "yiduobo的每日leetcode 1963.使字符串平衡的最小交换次数"
question_id: "1963"
question: "使字符串平衡的最小交换次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-string-balanced/"
difficulty: "Medium"
rating: 1689
created: "2022-04-07T00:31:13+08:00"
updated: "2022-04-07T00:31:13+08:00"
upvotes: 0
comments: 0
---

# 1963. 使字符串平衡的最小交换次数

> **[yiduobo的每日leetcode 1963.使字符串平衡的最小交换次数](https://zhuanlan.zhihu.com/p/494171553) · 知乎 · 2022-04-07 · 赞同 0**
> 力扣：[1963. 使字符串平衡的最小交换次数](https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-string-balanced/) · Medium · 灵茶山艾府：[贪心，三种写法，一步步优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1963.使字符串平衡的最小交换次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/)

括号匹配的常规检测方法是从左向右一趟扫描，若某一时刻右括号的数量大于左括号的数量，那么就出现了不匹配，此时需要执行交换。

最具性价比的交换自然是让当前多出来的右括号与位置在最后面的左括号进行交换。为了顺利进行这个交换操作，可以使用一个指针r表示当前最右侧的左括号所在的位置，每次在交换后往前移动，找到新的最右侧的左括号，直到扫描的位置到达了r的位置。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, s):
        """
        :type s: str
        :rtype: int
        """

        r = len(s) - 1
        while s[r] != '[':
            r -= 1

        cnt = 0
        l = 0
        res = 0
        while l < r:
            if s[l] == '[':
                cnt += 1
            elif cnt > 0:
                cnt -= 1
            else:
                res += 1
                cnt += 1
                r -= 1
                while r > l and s[r] != '[':
                    r -= 1
        
            l += 1

        return res
```
