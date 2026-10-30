---
title: "3154. 到达第K级台阶的方案数"
aliases: ["yiduobo的每日leetcode 3154.到达第K级台阶的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703956515"
zhihu_id: "703956515"
zhihu_title: "yiduobo的每日leetcode 3154.到达第K级台阶的方案数"
question_id: "3154"
question: "到达第 K 级台阶的方案数"
problem_url: "https://leetcode.cn/problems/find-number-of-ways-to-reach-the-k-th-stair/"
difficulty: "Hard"
rating: 2071
created: "2024-06-18T02:34:21+08:00"
updated: "2024-06-18T02:34:21+08:00"
upvotes: 0
comments: 0
---

# 3154. 到达第K级台阶的方案数

> **[yiduobo的每日leetcode 3154.到达第K级台阶的方案数](https://zhuanlan.zhihu.com/p/703956515) · 知乎 · 2024-06-18 · 赞同 0**
> 力扣：[3154. 到达第 K 级台阶的方案数](https://leetcode.cn/problems/find-number-of-ways-to-reach-the-k-th-stair/) · Hard · 灵茶山艾府：[两种方法：记忆化搜索/组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3154.到达第K级台阶的方案数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-number-of-ways-to-reach-the-k-th-stair/description/)

给出一个从0开始编号的无限长的台阶，另外有一个整数jump初始化为0，接下来每一轮选择下面两种操作之一：

1、若当前不处于第0阶，那么可以向下走一阶，即从当前的第i阶走到第i - 1阶。这个操作不能连续执行。

2、也可以向上走2^jump阶，然后将jump加上1，即从当前的第i阶走到第i + 2^jump阶，然后将jump加上1。这个操作的执行不受限制。

现在给出一个非负整数K，问从第1阶台阶开始，走到第K阶台阶的方案数。如果不存在可行的方案则返回-1。另外，可以先走到第k阶，然后继续向后走，再走回到第k阶。

---

首先观察题目中的两种操作，其中第一种操作只能往前走，第二种操作只能往后走，且第二种操作执行jump次后，走过的台阶数一共是2^0 + 2^1 + ... + 2^(jump - 1) \= 2^jump - 1。

不妨设第一种操作一共执行了d次，第二种操作一共执行了jump次，那么就有1 + 2^jump - 1 - d \= k。由于第一种操作不能连续执行，那么在极限情况下，如果将第一种操作穿插在第二种操作之间，最多可以执行jump + 1次第一种操作，即d \<\= jump + 1。注意到d的增长对答案的影响是线性的，而jump的增长则是指数级的，而d的大小又受到限制，因此在这里就需要jump尽量小，才能让d合法的概率最大。

于是在这里就应该取jump为最小的满足2^jump >\= k的整数，那么就有d \= 2^jump - k。若此时的d \<\= jump + 1，那么只需将这d次第二种操作穿插到jump次第一种操作之间就行了。对于这个问题，相当于jump + 1个空隙，从中选出d个用来放置第二种操作，那么一共就有C(jump + 1, d)种可行的方案。对于这个组合数，可以利用C(m, n) \= C(m - 1, n) + C(m - 1, n - 1)，通过动态规划进行求解。

---

需要特别注意的是，虽然d的次数受到限制，但是也可以尝试考虑，当2^jump - d \= k时，是否存在合法的d'满足当jump' \= jump + 1时，有2^jump' - d' \= k，即多执行一次第二种操作，然后使用大量的第一种操作来回填。如果存在合法的d'，那么就可以继续向后考虑是否可以再跳一次，即jump'' \= jump + 2时，是否存在2^jump'' - d'' \= k且d'' \<\= jump'' + 1。

在这里先考虑d'。

首先，由于2^jump - d \= k，且2^(jump + 1) - d' \= k，那么就有

d' \= 2^jump + d

另一方面，又有d' \<\= jump + 2，即jump + 2 >\= 2^jump + d

又由于d >\= 0，那么就有jump + 2 - 2^jump >\= 0

可以发现，此时只有当jump取0、1、2时这个式子才可能成立，另外由于需要同时满足d \<\= jump + 1、jump + 2 >\= 2^jump + d，因此d的取值也基本固定下来了。

接下来考虑d''。

同样的，有2^(jump + 2) - 2^jump + d \<\= jump + 3

又由于d >\= 0，那么就有jump + 3 - 2^(jump + 1) - 2^jump >\= 0，此时只有jump \= 0时式子才可能成立，而此时jump \= 0对应的jump'' \= 2实际上与jump \= 1时的jump' \= 1一致，因此没必要额外考虑了。

再往后，不存在更大的jump''' \= jump + 3满足jump + 4 - 2^(jump + 2) - 2^(jump + 1) - 2^jump >\= 0。

---

综合上面的结论，可以发现只需要考虑jump \= 0、1、2，且存在合法的jump'以及d'的几种特殊情况。

接下来就jump \= 0、1、2时进行分类讨论：

1、当jump \= 0时：

如果想要合法的d'存在，那么就有d \<\= jump + 1 \= 1，且d \<\= jump + 2 - 2^jump \= 1，即d \<\= 1。

因此d只能取0或者1，此时对应的k分别为1和0。

2、当jump \= 1时：

如果想要合法的d'存在，那么就有d \<\= jump + 1 \= 2，且d \<\= jump + 2 - 2^jump \= 1，即d \<\= 1。

因此d只能取0或者1，此时对应的k分别为2和1。

3、当jump \= 2时：

如果想要合法的d'存在，那么就有d \<\= jump + 1 \= 3，且d \<\= jump + 2 - 2^jump \= 0，即d \<\= 0。

因此d只能取0，此时对应的k为4。

换言之，只需对k等于0、1、2、4这四种情况进行特殊讨论，其他情况下jump唯一，按照上面组合数学的方法处理就行了。接下来对于这几种特殊情况：

1、当k \= 0时：

可以有jump \= 0，d \= 1，或者jump \= 1，d \= 2。

对于前者，只有"操作一"这一种方案。

对于后者，只有"操作一，操作二，操作一"这一种方案。

综合起来，一共是2种可行方案。

2、当k \= 1时：

可以有jump \= 0，d \= 0，或者jump \= 1，d \= 1，或者jump \= 2，d \= 3。

对于jump \= 0，d \= 0的情况，只有不执行任何操作这种方案。

对于jump \= 1，d \= 1的情况，可以先执行操作一，也可以先执行操作二，因此一共有两种方案。

对于jump \= 2，d \= 3的情况，只有"操作一，操作二，操作一，操作二，操作一"这一种方案。

综合起来，一共是4种可行方案。

3、当k \= 2时：

可以有jump \= 1，d \= 0，或者jump \= 2，d \= 2。

对于前者，只有"操作二"这一种方案。

对于后者，则一共有C(3, 2) \= 3种方案，分别是

"操作一，操作二，操作一，操作二"

"操作一，操作二，操作二，操作一"

"操作二，操作一，操作二，操作一"

综合起来，一共是4种可行方案。

4、当k \= 4时：

可以有jump \= 2，d \= 0，或者jump \= 3，d \= 4。

对于前者，只有"操作二"这一种方案。

对于后者，只有"操作一，操作二，操作一，操作二，操作一，操作二，操作一"这一种方案。

综合起来，一共是2种可行方案。

---

到了这里，就得到了完整的算法。

当k等于0、1、2、4其中之一时，直接返回对应的答案2、4、4、2。而对于其他的k，则需要先找出最小的满足2^jump >\= k的jump。对于jump的计算，一种简单的计算方法是计算k - 1的二进制表示的位数。

得到jump后，通过d \= 2^jump - k得到d，若d > jump + 1，那么答案为-1，否则答案为C(jump + 1, d)。

最后附上python代码：

```python
class Solution(object):
    def waysToReachStair(self, k):
        """
        :type k: int
        :rtype: int
        """

        if k == 0:
            return 2
        
        if k == 1:
            return 4
        
        if k == 2:
            return 4

        if k == 4:
            return 2
        
        jump = len(bin(k - 1)) - 2
        d = (1 << jump) - k

        if d > jump + 1:
            return 0

        c = [[0] * (d + 1) for _ in range(jump + 2)]
        for i in range(jump + 2):
            c[i][0] = 1
            for j in range(1, min(i, d) + 1):
                c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
        
        return c[jump + 1][d]
```
