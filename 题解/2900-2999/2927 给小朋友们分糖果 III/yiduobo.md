---
title: "2927. 给小朋友们分糖果III & 2928. 给小朋友们分糖果 I & 2929. 给小朋友们分糖果 II"
aliases: ["yiduobo的每日leetcode 2927.给小朋友们分糖果III & 2928/2929", "2927. 给小朋友们分糖果III", "2928. 给小朋友们分糖果 I", "2929. 给小朋友们分糖果 II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学", "leetcode/easy", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690272297"
zhihu_id: "690272297"
zhihu_title: "yiduobo的每日leetcode 2927.给小朋友们分糖果III & 2928/2929"
question_id: ["2927", "2928", "2929"]
question: ["给小朋友们分糖果 III", "给小朋友们分糖果 I", "给小朋友们分糖果 II"]
problem_url: ["https://leetcode.cn/problems/distribute-candies-among-children-iii/", "https://leetcode.cn/problems/distribute-candies-among-children-i/", "https://leetcode.cn/problems/distribute-candies-among-children-ii/"]
difficulty: ["Hard", "Easy", "Medium"]
created: "2024-04-02T02:36:51+08:00"
updated: "2024-04-02T02:36:51+08:00"
upvotes: 2
comments: 0
---

# 2927. 给小朋友们分糖果III & 2928. 给小朋友们分糖果 I & 2929. 给小朋友们分糖果 II

> **[yiduobo的每日leetcode 2927.给小朋友们分糖果III & 2928/2929](https://zhuanlan.zhihu.com/p/690272297) · 知乎 · 2024-04-02 · 赞同 2**
> 力扣：[2927. 给小朋友们分糖果 III](https://leetcode.cn/problems/distribute-candies-among-children-iii/) · Hard · 灵茶山艾府：[O(1) 容斥原理（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[2928. 给小朋友们分糖果 I](https://leetcode.cn/problems/distribute-candies-among-children-i/) · Easy · 灵茶山艾府：[O(1) 容斥原理（Python/Java/C++/C/Go/JS/Rust）](../2928%20给小朋友们分糖果%20I/灵茶山艾府.md)
> 力扣：[2929. 给小朋友们分糖果 II](https://leetcode.cn/problems/distribute-candies-among-children-ii/) · Medium · 灵茶山艾府：[O(1) 容斥原理（Python/Java/C++/C/Go/JS/Rust）](../2929%20给小朋友们分糖果%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2927.给小朋友们分糖果III & 2928/2929

[. - 力扣（LeetCode）](https://leetcode.cn/problems/distribute-candies-among-children-iii/description/)

[. - 力扣（LeetCode）](https://leetcode.cn/problems/distribute-candies-among-children-i/description/)

[. - 力扣（LeetCode）](https://leetcode.cn/problems/distribute-candies-among-children-ii/description/)

三个相同的题目，其中最前面的2927的数据规模反而是最大的，那么只要解决了2927，后面的直接照搬就行了。

题目要求将n颗糖果分给3个小朋友，每个小朋友拿到的糖果数不超过limit个，问有多少种方案。

由于题目只限定了3个小朋友，那么完全可以从1到3逐个推导。

1、首先是1个小朋友的情况。很明显，当n处于0到limit之间时，有唯一的一种分法，否则不存在可行的方案。

2、接下来对于2个小朋友的情况，可以明确的事当n大于limit \* 2时必然无解，因为至少有一个小朋友将分到超过limit颗糖果。另一方面，由于1个小朋友的情况中存在limit这个限制，因此在这里可以将n分为0 \<\= n \<\= limit以及limit \< n \<\= limit \* 2这两种情况进行讨论。

2-1）对于0 \<\= n \<\= limit的情况，这种情况下无论分给第一个小朋友多少糖果，剩下的都可以分给第二个小朋友，也就是说一共存在(0, n), (1, n - 1), (2, n - 2), ..., (n, 0)这一共n + 1种可行的方案。

2-2）对于limit \< n \<\= limit \* 2的情况，由于单个小朋友存在limit的限制，因此给第一个小朋友的糖果最少也要n - limit颗，而最多则依然是limit颗，因此在这里存在(n - limit, limit), (n - limit + 1, limit - 1), ..., (limit, n - limit)这一共limit \* 2 - n + 1种可行的方案。

3、最后是3个小朋友的情况。与上面的处理方法相同，将n按照limit的倍数进行分档。

3-1）首先n > limit \* 3的情况，显然是无解。

3-2）对于0 \<\= n \<\= limit的情况，假设分给第一个小朋友k颗，那么从2个小朋友相关的讨论可以得知，剩下的n - k颗分给两个小朋友一共有n - k + 1种可行的方案，也就是说当k \= 0时，有n + 1种方案，当k \= 1时，有n种方案，依次类推，当k \= n时，有一种方案。这是很明显的等差数列求和，总的方案数就是(n + 1) + n + (n - 1) + ... + 1 \= (n + 2) \* (n + 1) / 2种方案。

3-3）对于limit \< n \<\= limit \* 2的情况，同样是假设分了k颗糖果给第一个小朋友，那么在这里n - k既可能落在0到limit之间，也可能落在limit + 1到limit \* 2之间，对应了两个小朋友两种不同的情况。更具体的，在这里可以利用n - k \= limit计算出k的取值的临界点。

当分给第一个小朋友的糖果在0到n - (limit + 1)颗之间时，剩余的糖果数量n - k将满足limit \< n - k \<\= limit \* 2，对应的方案数就是limit \* 2 - (n - k) + 1。同样是等差数列求和问题，其中k的取值范围在0到n - (limit + 1)，因此等差数列的首项和末项就分别是limit \* 2 - n + 1以及limit，因此这里的总方案数就是(limit \* 3 - n + 1) \* (n - limit) / 2。

当分给第一个小朋友的糖果在n - limit到limit颗之间时，剩余的糖果数量n - k则是满足0 \< n - k \<\= limit，对应的方案数就是n - k + 1种。此时等差数列的首项为limit + 1，末项为n - limit + 1，因此这里的总方案数就是(n + 2) \* (limit \* 2 - n + 2) / 2。

上面两项之和就是limit \< n \<\= limit \* 2这种情况下的可行方案。

3-4）最后，对于limit \* 2 \< n \<\= limit \* 3的情况，第一个小朋友可以分的糖果只能是落在n - limit \* 2到limit之间，而剩下的糖果分给后面两个小朋友则对应到2-2中的情况，也就是此时n - k颗分给两个小朋友一共是limit \* 2 - (n - k) + 1种可行的方案。此时等差数列的首项为1，末项为limit \* 3 - n + 1，因此这里的总方案数就是(limit \* 3 - n + 2) \* (limit \* 3 - n + 1) / 2。

到了这里，分给3个小朋友的所有情况就已经讨论完毕了，根据对应情况计算答案即可。

最后附上python代码：

```python
class Solution(object):
    def distributeCandies(self, n, limit):
        """
        :type n: int
        :type limit: int
        :rtype: int
        """

        if n <= limit:
            return (1 + n + 1) * (n + 1) // 2
        elif limit < n <= limit * 2:
            left = (n + 2) * (limit * 2 - n + 1) // 2
            right = (limit * 3 - n + 1) * (n - limit) // 2
            return left + right
        elif limit * 2 < n <= limit * 3:
            return (limit * 3 - n + 2) * (limit * 3 - n + 1) // 2
        else:
            return 0
```
