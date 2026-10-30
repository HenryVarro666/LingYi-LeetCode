---
title: "712. 两个字符串的最小ASCII删除和"
aliases: ["yiduobo的每日leetcode 712.两个字符串的最小ASCII删除和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/326856782"
zhihu_id: "326856782"
zhihu_title: "yiduobo的每日leetcode 712.两个字符串的最小ASCII删除和"
question_id: "712"
question: "两个字符串的最小ASCII删除和"
problem_url: "https://leetcode.cn/problems/minimum-ascii-delete-sum-for-two-strings/"
difficulty: "Medium"
created: "2020-12-02T22:07:52+08:00"
updated: "2020-12-02T22:07:52+08:00"
upvotes: 0
comments: 0
---

# 712. 两个字符串的最小ASCII删除和

> **[yiduobo的每日leetcode 712.两个字符串的最小ASCII删除和](https://zhuanlan.zhihu.com/p/326856782) · 知乎 · 2020-12-02 · 赞同 0**
> 力扣：[712. 两个字符串的最小ASCII删除和](https://leetcode.cn/problems/minimum-ascii-delete-sum-for-two-strings/) · Medium · 灵茶山艾府：[正难则反：计算最多保留的 ASCII 之和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

712.两个字符串的最小ASCII删除和

[力扣](https://leetcode-cn.com/problems/minimum-ascii-delete-sum-for-two-strings/)

另类的编辑距离问题，不过这里只有删除操作，且删除的代价不是1而是当前字符的ascii码。做法依然是动态规划，f[i][j]表示s1的前i个字符与s2的前j个字符匹配的最小代价是多少，那么对于f[i][j]：

1、若i和j都是0，此时两个串都为空，因此f[i][j] \= 0

2、若i为0且j不为0，此时必须删去s2中的字符，因此f[i][j] \= f[i][j - 1] + ord(s2[j - 1])。注意这里的下标，例如j\=3时表示的是s2中的前3个字符，也就是s2[0]、s2[1]以及s2[2]

3、若i不为0且j为0，与情况2类似，有f[i][j] \= f[i - 1][j] + ord(s1[i - 1])

4、若i和j都不为0，且s1[i - 1]等于s2[j - 1]，此时两个串的最后一个字符可以匹配无需删去，因此有f[i][j] \= f[i - 1][j - 1]

5、若i和j都不为0，且s1[i - 1]不等于s2[j - 1]，此时可以删去其中一个串的最后一个字符看如何操作代价较小，因此有f[i][j] \= min(f[i - 1][j] + ord(s1[i - 1]), f[i][j - 1] + ord(s2[j - 1]))

求解完成后，f[len(s1)][len(s2)]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumDeleteSum(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: int
        """

        n = len(s1)
        m = len(s2)

        nums1 = [ord(x) for x in s1]
        nums2 = [ord(x) for x in s2]

        f = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            f[i][0] = f[i - 1][0] + nums1[i - 1]
        for j in range(1, m + 1):
            f[0][j] = f[0][j - 1] + nums2[j - 1]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if nums1[i - 1] == nums2[j - 1]:
                    f[i][j] = f[i - 1][j - 1]
                else:
                    f[i][j] = min(f[i][j - 1] + nums2[j - 1], f[i - 1][j] + nums1[i - 1])
        return f[n][m]
```
