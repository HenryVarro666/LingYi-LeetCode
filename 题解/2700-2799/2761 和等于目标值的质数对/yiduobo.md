---
title: "2761. 和等于目标值的质数对"
aliases: ["yiduobo的每日leetcode 2761.和等于目标值的质数对"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654540312"
zhihu_id: "654540312"
zhihu_title: "yiduobo的每日leetcode 2761.和等于目标值的质数对"
question_id: "2761"
question: "和等于目标值的质数对"
problem_url: "https://leetcode.cn/problems/prime-pairs-with-target-sum/"
difficulty: "Medium"
rating: 1505
created: "2023-09-06T03:30:52+08:00"
updated: "2023-09-06T03:30:52+08:00"
upvotes: 0
comments: 0
---

# 2761. 和等于目标值的质数对

> **[yiduobo的每日leetcode 2761.和等于目标值的质数对](https://zhuanlan.zhihu.com/p/654540312) · 知乎 · 2023-09-06 · 赞同 0**
> 力扣：[2761. 和等于目标值的质数对](https://leetcode.cn/problems/prime-pairs-with-target-sum/) · Medium · 灵茶山艾府：[预处理质数+枚举+特判奇数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2761.和等于目标值的质数对

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/prime-pairs-with-target-sum/description/)

最直观的做法自然是暴力枚举x，然后检测x和n - x是否都是质数。这个做法的时间复杂度为O(n \* sqrt(n))，本题的数据规模比较大，需要进行优化。

更好的处理方法是先通过筛法找出1到n之间的所有质数，简单来说就是使用一个数组来标记当前下标是否为质数，接下来从2到sqrt(n)进行遍历，对于当前遍历到的数p，若其没有被标记为合数，那么就将p的所有大于一的倍数都标记为合数。这个过程中，枚举单个p的计算次数为n / p。由于期间只需要对所有不超过sqrt(n)的质数p进行倍数标记，因此总的计算次数必然小于n / 1 + n / 2 + n / 3 + ... + n / n。

上面这个式子是一个发散的级数，但是其存在极限，数值等于n \* (ln(n) + C)，这里的C是一个很小的常数，一般称作欧拉常数。因此在计算时间复杂度时，上面做法的时间复杂度可以认为是O(n \* logn)。具体的证明可以参考欧拉常数的说明，这里就不展开了。

得到n之内的质数表之后，再暴力枚举x并检测x和n - x是否都是质数，这个过程就是O(n)的，总的时间复杂度就优化到了O(n \* logn)。

另外需要注意x和y相等的情况，需要特殊处理保证不重不漏。

最后附上python代码：

```python
class Solution(object):
    def findPrimePairs(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """

        f = [True] * (n + 1)
        f[0] = f[1] = False
        p = 2
        while p * p <= n:
            if f[p]:
                for x in range(p + p, n + 1, p):
                    f[x] = False
            
            p += 1
        
        res = []
        for x in range(2, (n + 1) / 2):
            y = n - x
            if f[x] and f[y]:
                res.append([x, y])
        
        if n % 2 == 0 and f[n / 2]:
            res.append([n / 2, n / 2])
        return res
```
