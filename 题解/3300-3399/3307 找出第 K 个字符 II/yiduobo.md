---
title: "3307. 找出第K个字符II"
aliases: ["yiduobo的每日leetcode 3307.找出第K个字符II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/位运算", "题单/贪心算法", "题单/链表-二叉树与回溯/五-其他递归/分治", "题单/位运算/九-其他", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1266241017"
zhihu_id: "1266241017"
zhihu_title: "yiduobo的每日leetcode 3307.找出第K个字符II"
question_id: "3307"
question: "找出第 K 个字符 II"
problem_url: "https://leetcode.cn/problems/find-the-k-th-character-in-string-game-ii/"
difficulty: "Hard"
rating: 2232
created: "2024-10-16T00:07:43+08:00"
updated: "2024-10-16T00:07:43+08:00"
upvotes: 1
comments: 0
---

# 3307. 找出第K个字符II

> **[yiduobo的每日leetcode 3307.找出第K个字符II](https://zhuanlan.zhihu.com/p/1266241017) · 知乎 · 2024-10-16 · 赞同 1**
> 力扣：[3307. 找出第 K 个字符 II](https://leetcode.cn/problems/find-the-k-th-character-in-string-game-ii/) · Hard · 灵茶山艾府：[两种做法：递归 / 迭代（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3307.找出第K个字符II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-k-th-character-in-string-game-ii/)

题目给出一个字符串word，初始状态下word \= 'a'。另外给出一个由0和1组成的整数数组operations，其中operations[i]表示第i轮操作的类型。

接下来每一轮:

若operations[i] \= 0，则需要将word复制一份然后拼接在word自己的后面

若operations[i] \= 1，则需要让word中的每个字符都将生成字母表中的下一个字符，z将生成a，并将所有生成的字符按顺序拼接在word的后面

问执行所有操作后，word中的第k个字符是什么。题目保证执行完所有操作后一定具有第k个字符。

之前3304题的加强版，不仅多出了原地复制的操作，而且k的规模也来到了10^14，因此之前直接模拟的做法就行不通了。

注意到每轮操作并不会影响到原始的word，也就是说一旦生成了第k个字符，后续的operations就没有用了，那么在这里就可以先想办法找到是执行完哪个operation后字符串的长度大于等于k。

由于每轮操作字符串的长度都将倍增，因此在这里可以模拟字符串长度length的增长，从1开始倍增直到length大于等于k，期间的轮次就是操作执行的数量。

不妨设在执行了operations[p]之后length大于等于k，令half \= length // 2，那么：

1、当k > half时，说明第k个字符是通过operations[p]这次操作复制出来的。

若operations[p]等于0，那么第k个字符应该与第k - half个字符相同。反之若operations[p]等于1，则说明第k个字符应该是第k - half个字符的下一个字符。

这种情况下，问题就变成了在进行operations[0]到operations[p - 1]这些操作之后，字符串中的第k - half个字符是什么。

2、当k \<\= half时，说明第k个字符并没有收到operations[p]的影响。

这种情况下，问题就是变成了在进行operations[0]到operations[p - 1]这些操作之后，字符串中的第k个字符是什么。

这样一来，就相当于消除掉了operations[p]的影响，只需按照上面的过程从后往前，逐个消除opearations[p]到operations[0]的影响，在这个过程中使用一个变量delta记录在进行了多少次复制下一个字符的操作，那么当还原到最初的'a'时，就可以通过寻找'a'后的第delta个字符来确定最终答案了。

最后附上python代码：

```python
class Solution(object):
    def kthCharacter(self, k, operations):
        """
        :type k: int
        :type operations: List[int]
        :rtype: str
        """

        length = 1
        p = 0
        while length < k:
            length += length
            p += 1
        
        p -= 1
        delta = 0
        half = length >> 1

        for index in range(p, -1, -1):
            if k > half:
                k -= half
                delta += operations[index]
            half >>= 1

        return chr(97 + delta % 26)
```
