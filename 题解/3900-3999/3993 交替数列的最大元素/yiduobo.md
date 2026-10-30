---
title: "3993. 交替数列的最大元素"
aliases: ["yiduobo的每日leetcode 3993.交替数列的最大元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2062641650665525872"
zhihu_id: "2062641650665525872"
zhihu_title: "yiduobo的每日leetcode 3993.交替数列的最大元素"
question_id: "3993"
question: "交替数列的最大元素"
problem_url: "https://leetcode.cn/problems/maximum-value-of-an-alternating-sequence/"
difficulty: "Medium"
created: "2026-07-20T21:07:44+08:00"
updated: "2026-07-20T21:07:59+08:00"
upvotes: 1
comments: 0
---

# 3993. 交替数列的最大元素

> **[yiduobo的每日leetcode 3993.交替数列的最大元素](https://zhuanlan.zhihu.com/p/2062641650665525872) · 知乎 · 2026-07-20 · 赞同 1**
> 力扣：[3993. 交替数列的最大元素](https://leetcode.cn/problems/maximum-value-of-an-alternating-sequence/) · Medium · 灵茶山艾府：[贪心，O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3993.交替数列的最大元素

<https://leetcode.cn/problems/maximum-value-of-an-alternating-sequence/description/>

题目给出三个整数n、s以及m。

若一个长度为n的整数序列seq满足以下条件，则认为它是有效的：

- seq以s开头
- 序列是交替的，即
   - seq[0] > seq[1] \< seq[2] > ...，或者
   - seq[0] \< seq[1] > seq[2] \< ...
- 对于其中每个相邻元素对，有|seq[index] - seq[index - 1]| \<\= m

长度为1的序列被认为是有效的。

问所有有效序列中可能出现的最大元素是多少。

题目要求找出可能出现的最大元素，那么在这里就应该按照

s -> s + m -> s + m - 1 -> s + m - 1 + m -> ...

这样构造，也就是尽量多做加m，而减法则只减去1。

那么对于一个长度为n的序列，去掉最左侧的s，后续剩下的n - 1项按两项分组则一定是分成(n - 1) // 2组(此处的//表示整除)。

若n - 1为奇数，那么最后还会多出一次加m的操作，这次操作的结果就是答案，同时前面刚好执行了(n - 1) // 2次加m然后减1的操作。还原到n，由于n是偶数，因此n // 2比(n - 1) // 2要多出1，也就是说这里执行加m减1的操作次数就是n // 2 - 1，对应的答案为s + (n // 2 - 1) \* (m - 1) + m。

若n - 1为偶数，最后这次减1操作会使得元素变小，在这里无需考虑，也就是说倒数第二次的加m操作就是答案，执行加m然后减1的操作次数则为(n - 1) // 2 - 1。还原到n，由于n为奇数，因此n // 2和(n - 1) // 2相同，此时的答案同样是s + (n // 2 - 1) \* (m - 1) + m。

需要特别注意的是，上面的算法默认考虑了至少有一个加m的操作，因此对于n \= 1的情况需要特殊处理，此时的答案应该就是s。

最后附上python代码：

```python
class Solution(object):
    def maximumValue(self, n, s, m):
        """
        :type n: int
        :type s: int
        :type m: int
        :rtype: int
        """
        
        if n == 1:
            return s
        return s + (m - 1) * (n // 2 - 1) + m
```
