---
title: "1863. 找出所有子集的异或总和再求和"
aliases: ["yiduobo的每日leetcode 1863.找出所有子集的异或总和再求和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/四-回溯", "题单/位运算/四-拆位-/-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473226139"
zhihu_id: "473226139"
zhihu_title: "yiduobo的每日leetcode 1863.找出所有子集的异或总和再求和"
question_id: "1863"
question: "找出所有子集的异或总和再求和"
problem_url: "https://leetcode.cn/problems/sum-of-all-subset-xor-totals/"
difficulty: "Easy"
rating: 1372
created: "2022-02-27T17:55:07+08:00"
updated: "2022-02-27T17:55:07+08:00"
upvotes: 1
comments: 0
---

# 1863. 找出所有子集的异或总和再求和

> **[yiduobo的每日leetcode 1863.找出所有子集的异或总和再求和](https://zhuanlan.zhihu.com/p/473226139) · 知乎 · 2022-02-27 · 赞同 1**
> 力扣：[1863. 找出所有子集的异或总和再求和](https://leetcode.cn/problems/sum-of-all-subset-xor-totals/) · Easy · 灵茶山艾府：[O(n) 数学做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1863.找出所有子集的异或总和再求和

[力扣](https://leetcode-cn.com/problems/sum-of-all-subset-xor-totals/)

由于题目的数据规模比较小，那么在这里采用暴力算法也是可以的，不过在这里有更好的做法。

对于异或相关的问题，自然是想到从位上去剖析。

在这里不妨设当前考虑的是所有数的第i位，一共有n个数，那么：

1、若所有数的第i位都是0，那么无论是哪个子集，异或的结果全都是0，因此这一位为最终答案提供的值就是0

2、若所有数的第i位中有cnt个1，那么只有当某个子集中有奇数个1时，异或结果才为1，才会被累加到最终结果当中。

在这里，若cnt为奇数，那么有奇数个1的子集数目就是

(C(cnt, 1) + C(cnt, 3) + ... + C(cnt, cnt)) \* 2^(n - cnt)

式子的前半部分表示的是从cnt个第i位为1的数中选出奇数个，后面的幂次表示的是剩下第i位为0的数中可以选或者不选。

相对的，当cnt为偶数时，这个式子就是

(C(cnt, 1) + C(cnt, 3) + ... + C(cnt, cnt - 1)) \* 2^(n - cnt)

分别考察这两个式子。

首先是cnt等于奇数时：

C(cnt, 1) \= C(cnt - 1, 0) + C(cnt - 1, 1)

C(cnt, 3) \= C(cnt - 1, 2) + C(cnt - 1, 3)

...

C(cnt, cnt - 2) \= C(cnt - 1, cnt - 3) + C(cnt - 1, cnt - 2)

而最后

C(cnt, cnt) \= 1 \= C(cnt - 1, cnt - 1)

也就是说

C(cnt, 1) + C(cnt, 3) + ... + C(cnt, cnt) \= C(cnt - 1, 0) + C(cnt - 1, 1) + ... + C(cnt - 1, cnt - 1) \= 2^(cnt - 1)

于是就有

(C(cnt, 1) + C(cnt, 3) + ... + C(cnt, cnt)) \* 2^(n - cnt) \= 2^(cnt - 1) \* 2^(n - cnt) \= 2^(n - 1)

接下来是cnt为偶数时：

C(cnt, 1) \= C(cnt - 1, 0) + C(cnt - 1, 1)

C(cnt, 3) \= C(cnt - 1, 2) + C(cnt - 1, 3)

...

C(cnt, cnt - 1) \= C(cnt - 1, cnt - 2) + C(cnt - 1, cnt - 1)

也就是说

C(cnt, 1) + C(cnt, 3) + ... + C(cnt, cnt - 1) \= C(cnt - , 0) + C(cnt - 1, 1) + ... + C(cnt - 1, cnt -1) \= 2^(cnt - 1)

与上面相同，此时最终结果也是2^(n - 1)

换言之，只需要这些数中的第i位上有1，最终这一位上的和就是2^(n - 1)，需要将2^(n - 1) \* 2^i累加到答案中。此时就只需要遍历每一位，对于当前遍历到的位i，若nums中存在一个数在i这一位为1，那么就将2^(n - 1) \* 2^i累加到答案中。

具体实现上，则可以利用或运算将nums中的数全部取或，对于其中的某一位，若nums存在一个数这一位为1，那么或运算结果的这一位就必然是1，那么最后只需要将这个或运算的结果再乘以2^(n - 1)就行了。

最后附上python代码：

```python
class Solution(object):
    def subsetXORSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        res = 0
        for num in nums:
            res |= num
        
        return res << (n - 1)
```
