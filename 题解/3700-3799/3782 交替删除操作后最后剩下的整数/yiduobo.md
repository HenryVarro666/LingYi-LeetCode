---
title: "3782. 交替删除操作后最后剩下的整数"
aliases: ["yiduobo的每日leetcode 3782.交替删除操作后最后剩下的整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/simulation", "题单/位运算", "题单/数学算法", "题单/位运算/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986223716267480347"
zhihu_id: "1986223716267480347"
zhihu_title: "yiduobo的每日leetcode 3782.交替删除操作后最后剩下的整数"
question_id: "3782"
question: "交替删除操作后最后剩下的整数"
problem_url: "https://leetcode.cn/problems/last-remaining-integer-after-alternating-deletion-operations/"
difficulty: "Hard"
rating: 2074
created: "2025-12-24T02:22:38+08:00"
updated: "2025-12-24T02:22:39+08:00"
upvotes: 2
comments: 0
---

# 3782. 交替删除操作后最后剩下的整数

> **[yiduobo的每日leetcode 3782.交替删除操作后最后剩下的整数](https://zhuanlan.zhihu.com/p/1986223716267480347) · 知乎 · 2025-12-24 · 赞同 2**
> 力扣：[3782. 交替删除操作后最后剩下的整数](https://leetcode.cn/problems/last-remaining-integer-after-alternating-deletion-operations/) · Hard · 灵茶山艾府：[从 O(log n) 到 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3782.交替删除操作后最后剩下的整数

<https://leetcode.cn/problems/last-remaining-integer-after-alternating-deletion-operations/description/>

题目给出一个整数n，其大小不超过10^15。

现在要求将1到n按从左到右的顺序排列好，然后交替执行以下两种操作，直到只剩下一个数为止：

- 从左侧开始，每隔一个数删除一个数
- 从右侧开始，每隔一个数删除一个数

例如n \= 8时，一开始是[1, 2, 3, 4, 5, 6, 7, 8]。第一次操作后，剩下[1, 3, 5, 7]；第二次操作后，剩下[3, 7]；第三次操作后，剩下[3]。

而当n \= 5时，一开始是[1, 2, 3, 4, 5]。第一操作后，剩下[1, 3, 5]；第二次操作后，剩下[1, 5]；第三次操作后，剩下[1]。

问对于给出的n，数组中最后剩下的是多少。

直观感觉上，本题应该是有O(1)的数学方法的，不过没有什么好的思路。

注意到每次操作剩余元素的规模都会缩减一半，因此直接模拟应该是可行的，问题就是应该如何表示剩下的元素是什么。由于题目中给出的两种操作都是隔一个删一个，而一开始的元素是1到n，这也就意味着无论何时，剩余的元素必然都是一个等差数列，而对于等差数列，只需维护其起始值a，公差d以及项数cnt就行了。

于是只需维护a、d以及cnt，初始值分别为1、1、n，然后模拟上面的操作，直到cnt等于1为止，此时对应的a即为最终答案。

对于上面两种操作，可以发现：

- 对于从左到右的操作，起始项a不变，公差d变为两倍，cnt则变为(cnt + 1) // 2
- 对于从右到左的操作，则需要根据cnt的奇偶性进行判断。当cnt为奇数时，起始项a不变，公差d变为两倍，cnt变为(cnt + 1) // 2；当cnt为偶数时，起始项会在此次操作中被移除掉，那么新的起始项就是原先数列中的第二项，即a + d，于是应该将a更新为a + d，另外公差d也是变为两倍，cnt同样是变为(cnt + 1) // 2

最后附上python代码：

```python
class Solution(object):
    def lastInteger(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        a = 1
        d = 1
        cnt = n
        while cnt > 1:
            d += d
            cnt = (cnt + 1) // 2
            if cnt == 1:
                break
            
            if cnt % 2 == 0:
                a += d
            d += d
            cnt = (cnt + 1) // 2
        
        return a
```
