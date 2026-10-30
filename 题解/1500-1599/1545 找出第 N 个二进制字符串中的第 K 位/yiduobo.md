---
title: "1545. 找出第N个二进制字符串中的第K位"
aliases: ["yiduobo的每日leetcode 1545.找出第N个二进制字符串中的第K位"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/math", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/五-其他递归/分治", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424981294"
zhihu_id: "424981294"
zhihu_title: "yiduobo的每日leetcode 1545.找出第N个二进制字符串中的第K位"
question_id: "1545"
question: "找出第 N 个二进制字符串中的第 K 位"
problem_url: "https://leetcode.cn/problems/find-kth-bit-in-nth-binary-string/"
difficulty: "Medium"
created: "2021-10-24T11:26:18+08:00"
updated: "2021-10-24T11:26:18+08:00"
upvotes: 0
comments: 0
---

# 1545. 找出第N个二进制字符串中的第K位

> **[yiduobo的每日leetcode 1545.找出第N个二进制字符串中的第K位](https://zhuanlan.zhihu.com/p/424981294) · 知乎 · 2021-10-24 · 赞同 0**
> 力扣：[1545. 找出第 N 个二进制字符串中的第 K 位](https://leetcode.cn/problems/find-kth-bit-in-nth-binary-string/) · Medium · 灵茶山艾府：[从递归到 O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1545.找出第N个二进制字符串中的第K位

[力扣](https://leetcode-cn.com/problems/find-kth-bit-in-nth-binary-string/)

观察这些字符串的长度，那么可以得出s[n]的长度等于s[n - 1]的长度，加上正中间的1，再加上s[n - 1]的长度。由于s1的长度为1，那么就可以得出s[n]的长度为2^n - 1

有了这个结论，那么可以找出最大的m，满足2^m \<\= K：

1、若此时的k恰好等于2^m，其中m > 0，那么说明第k位对应的字符就是某次拼接操作时夹在正中间的那个1，若m \= 0，说明K \= 1，也就是字符串最开头的那个0

2、若此时的k大于2^m，当前总的s组成是

s[m] + '1' + reverse(invert(s[m])) + ...

其中这个'1'的位置位2^m，而K位于reverse(invert(s[m]))这一段

其距离'1'的长度位k - 2^m，那么其对应回s[m]的位置就是2^m - (K - 2^m) \= 2^m + 2^m - k。此时问题就转化为了s中第2^m + 2^m - k这个位置的字符是什么。重复这个过程直到某一时刻2^m \= k。

可以发现，每一轮k的规模是在不断缩小的，因为每次操作都可以让m至少减少1。

最后附上python代码：

```python
class Solution(object):
    def findKthBit(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """

        pow2 = [1]
        while pow2[-1] < k:
            pow2.append(pow2[-1] + pow2[-1])
        
        now = len(pow2) - 1
        flag = 0
        while k > 0:
            while pow2[now] > k:
                now -= 1

            if k == pow2[now]:
                if k == 1:
                    return str(flag ^ 0)
                else:
                    return str(flag ^ 1)
            else:
                k = pow2[now] + pow2[now] - k
                flag ^= 1
```
