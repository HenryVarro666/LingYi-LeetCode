---
title: "3139. 使数组中所有元素相等的最小开销"
aliases: ["yiduobo的每日leetcode 3139.使数组中所有元素相等的最小开销"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/一-贪心策略", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702836721"
zhihu_id: "702836721"
zhihu_title: "yiduobo的每日leetcode 3139.使数组中所有元素相等的最小开销"
question_id: "3139"
question: "使数组中所有元素相等的最小开销"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-equalize-array/"
difficulty: "Hard"
rating: 2666
created: "2024-06-12T02:12:10+08:00"
updated: "2024-06-12T02:12:10+08:00"
upvotes: 0
comments: 0
---

# 3139. 使数组中所有元素相等的最小开销

> **[yiduobo的每日leetcode 3139.使数组中所有元素相等的最小开销](https://zhuanlan.zhihu.com/p/702836721) · 知乎 · 2024-06-12 · 赞同 0**
> 力扣：[3139. 使数组中所有元素相等的最小开销](https://leetcode.cn/problems/minimum-cost-to-equalize-array/) · Hard · 灵茶山艾府：[分类讨论，O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3139.使数组中所有元素相等的最小开销

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-equalize-array/description/)

题目给出一个数组nums和两个正整数cost1和cost2，每一轮都可以使用代价cost1让数组中的任意数加上1，或者使用代价cost2让数组中的任意两个下标不同的数分别加上1，问使得nums中所有元素都相等所需的最小代价。

首先考虑特殊情况。若cost1 \* 2 \<\= cost2，那么是就没有使用cost2的意义了，因为所有的cost2操作都可以使用两次cost1操作来替代，所需的代价只会更小。

不妨设数组中的最大值为ma，那么在这种情况下，使用cost1操作将所有元素都变成ma就是最优的处理方法。记tot_diff为将数组中所有元素变为ma所需的操作次数，那么最终答案就是tot_diff \* cost1。

---

接下来考虑cost1 \* 2 > cost2的情况。在这种情况下，就应该尽量采用cost2操作。更具体的来说，在这里每一轮都应该选择当前数组中最小的两个数执行cost2操作。但是在这里可能出现一种情况，就是数组中某个元素太小了，cost2操作不足以将其抬起来。

例如数组[1, 4, 4, 5]，此时如果以ma \= 5为目标，那么只能执行两次cost2操作，得到的结果为[3, 5, 5, 5]。这种情况只有在满足下面两个前提条件下才会出现：

1、数组中的最小值mi是落单的。

记freq为数组中每种元素出现的次数，那么当最小值mi出现多次，即freq[mi] \= k > 1时，那么

若k为偶数，那么就可以两两分组，采用cost2操作同步抬升；若k为奇数，那么就可以按照(1, 2)、(3, 4)、...、(k - 2, k - 1)、(k, 1)、(2, 3)、...、(k - 3, k - 2)、(k - 1, k)，通过k次cost2操作同步抬升。

需要注意的是，当k为奇数时，由于将按照2抬升，那么对于[4, 4, 4, 5]这种情况，也是无法将这些数变为5的。对于这种情况后面会进行讨论。

2、将数组中的最小值变为ma所需的操作次数大于将其他数变为ma所需的操作次数。

这一点则比较明显，就不展开了。

---

在这里就可以先排除掉cost2够用的情况。方便起见，记min_diff为将最小值mi变为ma所需的操作次数，other_diff为将其他元素变为ma所走的操作次数，那么就有other_diff \= tot_diff - min_diff。

那么当freq[mi] > 1，或者other_diff >\= min_diff时，就可以先执行足量的cost2操作，初始化答案

res \= tot_diff // 2 \* cost2

另外这里可能出现落单的某个数，例如上面的[4, 4, 4, 5]这种情况，执行一次cost2操作后还会有一个4，在这里记

sp \= tot_diff % 2

sp的处理留在后面再讨论。

---

而对于cost2不够用的情况，也一定要全靠cost1操作来填补。例如上面的[1, 4, 4, 5]，首先依然是变成[3, 5, 5, 5]，接下来，可以设置目标值为6，那么就可以通过3次cost2操作将数组变为[6, 6, 6, 6]。

更进一步的，对于这种情况，相当于通过n - 1次cost2操作，将mi变为mi + n - 1，将其他数都变为ma + 1，此时mi + n - 1距离ma + 1还差ma - mi - (n - 2)，相比之前的ma - mi相当于多了n - 2。也就是说，在这里通过n - 1次cost2操作，起到了n - 2次cost1操作的作用。

对于这种情况，即freq[mi] \= 1且other_diff \< min_diff时，若n > 2，且(n - 1) \* cost2 \< (n - 2) \* cost1，就可以采用n - 1次cost2来替代n - 2次cost1。

因此在这种情况下，可以先让其他元素与mi配对，执行一共other_diff次cost2操作，而对于剩下的(min_diff - other_diff)个mi，则可以采用上面的替代操作，一共可以执行(min_diff - other_diff) // (n - 2)次，代价为(min_diff - other_diff) // (n - 2) \* (n - 1) \* cost2，这种情况下就应该初始化答案

res \= (other_diff \* cost2 + (min_diff - other_diff) // (n - 2) \* (n - 1) \* cost2)

而用不完的mi同样记为sp后面讨论

sp \= (min_diff - other_diff) % (n - 2)

---

如果不满足以上两种情况，即cost2不够用，且用cost2去替代cost1也划不来，那么就只能用cost1去填充mi，那么此时就应该让其他元素与mi配对，同样是other_diff次cost2操作，而剩下的mi则都应该用cost1，因此答案

res \= other_diff \* cost2 + (min_diff - other_diff) \* cost1

另外此时不存在用不完的情况，因此可以置sp \= 0

---

最后，还需要讨论sp大于0时应该如何处理。在这里有一个前提是sp要么是tot_diff % 2得到的，即sp等于1，要么是(min_diff - other_diff) % (n - 2)得到的，即sp小于n - 2。

使用cost1直接填充是一个可行的方法，代价为sp \* cost1。

另一方面，当n > 2时，也可以考虑再次放大ma，使用cost2来填充。此时则需要对sp和n分奇偶进行讨论：

1、当sp同n奇偶时：

由于sp \< n - 2，那么就可以从除mi之外的n - 1个元素中，选出sp + 1个与mi配对，使的这些元素都变成mi + sp + 1，而剩下的n - (sp + 1) - 1个元素则可以两两配对，因此此时一共执行了(n + sp) // 2次cost2操作，代价为(n + sp) // 2 \* cost2。

2、当sp为偶数，n为奇数时：

这种情况下，依然可以采取情况1中的处理方法，先选出sp + 1个元素与mi配对，但是这样一来将会有一个落单的元素无法使用cost2。此时又有两种处理方法，即使用一次cost1来填充，或者再将目标值加1，执行一轮cost2。

对于这两种方案，前者执行了一共(n + sp) // 2次cost2操作以及一次cost1操作，代价为(n + sp) // 2 \* cost2 + cost1，后者则执行了(n + n + sp) // 2次cost2操作，代价为(n + n + sp) // 2 \* cost2。

3、当sp为奇数，n为偶数时：

此时由于n为偶数，因此sp + k \* n必然为奇数，即无论如何都会有一个落单的数，因此此时最多只需进行一轮尝试，即执行(n + sp) // 2次cost2操作以及一次cost1操作，代价为(n + sp) // 2 \* cost2 + cost1。

对于以上三种情况，分别计算代价，然后与全部采用cost1操作的代价进行对比，取较小值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minCostToEqualizeArray(self, nums, cost1, cost2):
        """
        :type nums: List[int]
        :type cost1: int
        :type cost2: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        freq = Counter(nums)
        n = len(nums)

        ma = max(freq.keys())
        mi = min(freq.keys())

        tot_diff = 0
        for v, f in freq.items():
            tot_diff += (ma - v) * f

        min_diff = (ma - mi) * freq[mi]
        other_diff = tot_diff - min_diff

        if cost1 + cost1 <= cost2:
            return tot_diff * cost1 % mod

        if freq[mi] > 1 or min_diff <= other_diff:
            res = tot_diff // 2 * cost2 % mod
            sp = tot_diff % 2
        elif n > 2 and (n - 1) * cost2 < (n - 2) * cost1:
            res = (other_diff * cost2 + (min_diff - other_diff) // (n - 2) * (n - 1) * cost2) % mod
            sp = (min_diff - other_diff) % (n - 2)
        else:
            res = ((min_diff - other_diff) * cost1 + other_diff * cost2) % mod
            sp = 0

        sp_cost = sp * cost1
        if sp > 0 and n > 2:
            if (sp + n) % 2 == 0:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2)
            elif sp % 2 == 0:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2 + cost1, (sp + n + n) // 2 * cost2)
            else:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2 + cost1)

        res = (res + sp_cost) % mod
        return res
```
