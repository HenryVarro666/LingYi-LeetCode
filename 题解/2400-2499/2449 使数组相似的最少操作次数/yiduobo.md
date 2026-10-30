---
title: "2449. 使数组相似的最少操作次数"
aliases: ["yiduobo的每日leetcode 2449.使数组相似的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585130340"
zhihu_id: "585130340"
zhihu_title: "yiduobo的每日leetcode 2449.使数组相似的最少操作次数"
question_id: "2449"
question: "使数组相似的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-arrays-similar/"
difficulty: "Hard"
rating: 2076
created: "2022-11-20T18:08:01+08:00"
updated: "2022-11-20T18:08:01+08:00"
upvotes: 0
comments: 0
---

# 2449. 使数组相似的最少操作次数

> **[yiduobo的每日leetcode 2449.使数组相似的最少操作次数](https://zhuanlan.zhihu.com/p/585130340) · 知乎 · 2022-11-20 · 赞同 0**
> 力扣：[2449. 使数组相似的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-arrays-similar/) · Hard · 灵茶山艾府：[按奇偶性分类贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2449.使数组相似的最少操作次数

[力扣](https://leetcode.cn/problems/minimum-number-of-operations-to-make-arrays-similar/)

观察对nums的操作可以发现，无论怎样操作，nums中每一位的奇偶性是不变的，这也就意味着在可以需要分开来考虑，将nums中的奇数变为target中的奇数，nums中的偶数变为target中的偶数。

接下来需要确定操作的方案。不妨设有四个数nums[i]、nums[j]、target[i]、target[j]，这四个数奇偶性相同，且nums[i] \< nums[j]、target[i] \< target[j]，那么此时有两种操作方案，分别是让nums[i]变为target[i]、nums[j]变为target[j]以及让nums[j]变为target[i]、nums[i]变为target[j]。

在这里需要分情况进行讨论，但是相对复杂。可以将这四个数视为数轴上的四个点，而数的变化视为上面的线段。可以发现，当区间\[nums\[i\], nums\[j\]\]与\[target\[i\], target\[j\]\]相交时，后面这种方案产生的两条线段将出现相交的情况，而前面这种方案没有；反过来，当区间\[nums\[i\], nums\[j\]\]与\[target\[i\], target\[j\]\]不相交时，两种方案的线段都将出现相交的情况，但是相交的长度相等。综合起来，就说明后面这种方案存在不必要的操作。根据这个结论，在进行操作时就应该按照nums和target数值大小的顺序一一对应着进行操作。

到了这里，就有了一种算法。将nums和target分奇偶，从小到大进行排序，然后一趟遍历。需要注意的是，每次加2减2都是同步执行的，因此只需要计算加或者减的操作次数就行了。也就是说只有在当前的nums[index] > target[index]时，才需要计算将当前nums[index]变为target[index]所需的操作次数并累加到答案。

最后附上python代码：

```python
class Solution(object):
    def makeSimilar(self, nums, target):
        """
        :type nums: List[int]
        :type target: List[int]
        :rtype: int
        """

        nums.sort(key=lambda d:(d % 2, d))
        target.sort(key=lambda d:(d % 2, d))

        n = len(nums)
        res = 0
        for index in range(n):
            if nums[index] > target[index]:
                res += (nums[index] - target[index]) / 2
        
        return res
```
