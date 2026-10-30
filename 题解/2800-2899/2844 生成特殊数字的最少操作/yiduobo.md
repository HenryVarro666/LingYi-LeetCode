---
title: "2844. 生成特殊数字的最少操作"
aliases: ["yiduobo的每日leetcode 2844.生成特殊数字的最少操作"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660002622"
zhihu_id: "660002622"
zhihu_title: "yiduobo的每日leetcode 2844.生成特殊数字的最少操作"
question_id: "2844"
question: "生成特殊数字的最少操作"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-a-special-number/"
difficulty: "Medium"
rating: 1588
created: "2023-10-08T03:05:50+08:00"
updated: "2023-10-08T03:05:50+08:00"
upvotes: 0
comments: 0
---

# 2844. 生成特殊数字的最少操作

> **[yiduobo的每日leetcode 2844.生成特殊数字的最少操作](https://zhuanlan.zhihu.com/p/660002622) · 知乎 · 2023-10-08 · 赞同 0**
> 力扣：[2844. 生成特殊数字的最少操作](https://leetcode.cn/problems/minimum-operations-to-make-a-special-number/) · Medium · 灵茶山艾府：[两种方法：枚举末尾 / 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2844.生成特殊数字的最少操作

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-operations-to-make-a-special-number/)

题目中的特殊数字指的是25的倍数，由于100是25的倍数，那么在这里只需让数字的最后两位是25的倍数就行了，也就是说本题实际上是要求删除最少的数字，使得最后两位变为00、25、50、75这四种情况之一。于是可以检测以上四种情况，从后往前遍历，使用贪心法找到最靠后的两个对应的数字并执行删除操作。

另外需要注意的是，如果上面四种情况都无法达成，那么还有一种保底做法是将所有数字都删除变为0，不过如果数字中有一个单独的0，那么就可以留下这个单独的0而不用将所有数字都删掉，对于这种情况需要特殊处理。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, num):
        """
        :type num: str
        :rtype: int
        """

        def check(first, second):
            p = len(num_list) - 1
            res = len(num_list)
            while p >= 0 and num_list[p] != first:
                p -= 1

            if p == -1:
                return res
            
            if first == 0:
                res -= 1
            
            p -= 1
            while p >= 0 and num_list[p] != second:
                p -= 1

            if p == -1:
                return res
            
            return len(num_list) - p - 2

        num_list = list([int(x) for x in str(num)])
        res = len(num_list)
        res = min(res, check(0, 0))
        res = min(res, check(5, 2))
        res = min(res, check(0, 5))
        res = min(res, check(5, 7))
        return res
```
