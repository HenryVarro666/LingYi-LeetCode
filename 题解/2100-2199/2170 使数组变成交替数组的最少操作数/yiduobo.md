---
title: "2170. 使数组变成交替数组的最少操作数"
aliases: ["yiduobo的每日leetcode 2170.使数组变成交替数组的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/533842283"
zhihu_id: "533842283"
zhihu_title: "yiduobo的每日leetcode 2170.使数组变成交替数组的最少操作数"
question_id: "2170"
question: "使数组变成交替数组的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-the-array-alternating/"
difficulty: "Medium"
rating: 1663
created: "2022-06-26T00:37:10+08:00"
updated: "2022-06-26T00:37:10+08:00"
upvotes: 1
comments: 0
---

# 2170. 使数组变成交替数组的最少操作数

> **[yiduobo的每日leetcode 2170.使数组变成交替数组的最少操作数](https://zhuanlan.zhihu.com/p/533842283) · 知乎 · 2022-06-26 · 赞同 1**
> 力扣：[2170. 使数组变成交替数组的最少操作数](https://leetcode.cn/problems/minimum-operations-to-make-the-array-alternating/) · Medium · 灵茶山艾府：[贪心 + 分类讨论](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2170.使数组变成交替数组的最少操作数

[力扣](https://leetcode.cn/problems/minimum-operations-to-make-the-array-alternating/)

首先是边界情况。当数组中仅有一个数时，无需进行操作，此时的答案为0。

接下来考虑数组长度大于等于2的情况。题目要求将数组奇数位上的数变为同一个，偶数位上的数也变为同一个，且奇数位上的数和偶数位上的数不能相同。为了使得操作次数最少，那么就应该分别选择奇数位以及偶数位上出现次数最多的数作为变换的目标。

那么可以先将数组中的所有数按照奇数位和偶数位分开，统计每个数出现的次数并按这个次数从大到小进行排序。

在这里定义odd_info和even_info为排序后的结果数组，其中odd_info[index][0]和odd_info[index][1]分别表示奇数位上出现次数排名第index的数，以及其对应的出现次数。类似的，even表示的是偶数位上的情况。

得到odd_info以及even_info后，若odd_info[0][0]与even_info[0][0]不同，那么就可以按照上面的结论进行操作，将偶数位上的数全部变为even_info[0][0]，将奇数位上的数全部变为odd_info[0][0]，那么此时的答案就是数组长度n减去odd_info[0][1]再减去even_info[0][1]。

但是，若odd_info[0][0]与even_info[0][0]相同，那么就不能使用上面的方案了，在这里需要分下面四种情况进行讨论。方便起见，记odd_cnt为奇数位的数目，even_cnt为偶数位的数目。

1、奇数位上所有数都相同，且偶数位上所有数都相同：

此时相当于整个数组都是同一种数，那么就应该将奇数位上的数变为另一种数，此时的答案就是odd_cnt。

在这里选择对奇数位进行变换而不是偶数位的原因是，当数组长度为奇数时，even_cnt \= odd_cnt + 1，而当数组长度为偶数时，even_cnt \= odd_cnt，因此选择变换奇数位总是最优的

2、奇数位上所有数都相同，偶数位上至少有两种不同的数：

此时有两种选择。

第一种是奇数位保持不变，将偶数位替换成出现even_info[1][0]。这种方案需要的替换次数为even_cnt减去even_info[1][1]

第二种则是将偶数位替换成偶数位上出现最多的数，将奇数位上的所有数替换成另一个数。这种方案的替换次数为n - even_info[0][1]

由于在这里even_info[0][1] > 0，那么第二种方案的操作次数必然大于等于第一种方案的操作，因此此时应该选择第一种方案，答案为even_cnt - even_info[1][1]

3、偶数位上的所有数都相同，奇数位上至少有两种不同的数：

与情况2完全对称，此时的答案为odd_cnt - odd_info[1][1]

4、奇数位和偶数位上都至少有两种不同的数：

此时也是两种选择。

第一种是将奇数位变为odd_info[0][0]，将偶数位变为even_info[1][0]。此时需要的操作次数为n - odd_info[0][1] - even_info[1][1]

第二种是将奇数位变为odd_info[1][0]，将偶数位变为even_info[0][0]。此时需要的操作次数为n - odd_info[1][1] - even_info[0][1]

最终答案就是这两种方案中操作次数的较小值

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        if n == 1:
            return 0

        odd = {}
        even = {}
        for index, num in enumerate(nums):
            if index % 2 == 0:
                even[num] = even.get(num, 0) + 1
            else:
                odd[num] = odd.get(num, 0) + 1
        
        odd_info = sorted(odd.items(), key=lambda d:d[1], reverse=True)
        even_info = sorted(even.items(), key=lambda d:d[1], reverse=True)
        odd_cnt = n / 2
        even_cnt = (n + 1) / 2

        if odd_info[0][0] != even_info[0][0]:
            return n - odd_info[0][1] - even_info[0][1]
        elif len(odd_info) == 1:
            if len(even_info) == 1:
                return odd_cnt
            else:
                return even_cnt - even_info[1][1]
        elif len(even_info) == 1:
            return odd_cnt - odd_info[1][1]
        else:
            return min(n - odd_info[0][1] - even_info[1][1], n - odd_info[1][1] - even_info[0][1])
```
