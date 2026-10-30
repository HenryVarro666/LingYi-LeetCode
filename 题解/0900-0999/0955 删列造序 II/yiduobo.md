---
title: "955. 删列造序II"
aliases: ["yiduobo的每日leetcode 955.删列造序II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360239728"
zhihu_id: "360239728"
zhihu_title: "yiduobo的每日leetcode 955.删列造序II"
question_id: "955"
question: "删列造序 II"
problem_url: "https://leetcode.cn/problems/delete-columns-to-make-sorted-ii/"
difficulty: "Medium"
rating: 1876
created: "2021-03-27T00:08:51+08:00"
updated: "2021-03-27T00:08:51+08:00"
upvotes: 0
comments: 0
---

# 955. 删列造序II

> **[yiduobo的每日leetcode 955.删列造序II](https://zhuanlan.zhihu.com/p/360239728) · 知乎 · 2021-03-27 · 赞同 0**
> 力扣：[955. 删列造序 II](https://leetcode.cn/problems/delete-columns-to-make-sorted-ii/) · Medium · 灵茶山艾府：[从左到右贪心 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

955.删列造序II

[力扣](https://leetcode-cn.com/problems/delete-columns-to-make-sorted-ii/)

朴素的算法是很容易想到的。从左向右枚举每一列i，然后从头开始枚举每一行j，那么对于第j行，此时的字符串为第j行，第0到i - 1列中剩下的列中的字符，加上strs[j][i]形成的字符串。同理，对于第j + 1行，则是第j + 1行，第0到i - 1列中剩下的列中的字符，加上strs[j + 1][i]形成的字符串。对比这两个字符串的大小，若第j行的字符大于第j + 1行的字符串，那么说明第i列需要删除。若遍历完每一行都没有出现大于的情况，那么说明第i列应当保留。

上面这个做法的时间复杂度是O(n \* l \* l)的，其中n为字符串的数目，l为字符串的长度。这个时间复杂度是比较高的。

对于j和j + 1这两个字符串而言，不妨设其第0到i - 1位完全一致，那么若此时第i为保留，同时有strs[j][i] \< strs[j + 1][I]，那么无论第i列之后是什么样，第j行的字符串必然是小于第j + 1行的字符串的，也就是说对于第j行和第j + 1行的大小情况，我们都无需再考察后续的列了。

于是我们可以使用一个数组small来记录当前这个确定的大小情况，当某一时刻small[j]为true时，说明之后的列我们无需考察第j行以及第j + 1行了。而当small[j]为false时，对于第j行以及第j + 1行而言，之前剩下的列必然是完全一致的。

证明也很简单，若之前处理完的某一列k满足strs[j][k] !\= strs[j + 1][k]，且此时small[j]为false，那么若strs[j][k] > strs[j + 1][k]，那么第k列应当删去，不会剩下；若strs[j][k] \< strs[j + 1][k]，那么此时small[j]应当为true，产生了矛盾。

这就意味着我们每次只需要判断small[j]为true，或者strs[j][i] \<\= strs[j + 1][i]就可以确定第j行以及第j + 1行在前i列的大小情况。

在每处理完一列之后，若该列保留，那么就需要一趟遍历更新small数组。

这样一来，就得到了一种时间复杂度为O(n \* l)的做法。

最后附上python代码：

```python
class Solution(object):
    def minDeletionSize(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        n = len(strs)
        l = len(strs[0])
        small = [False] * (n - 1)
        
        res = 0
        for i in range(l):
            flag = False
            for j in range(n - 1):
                if small[j]:
                    continue
                if strs[j][i] > strs[j + 1][i]:
                    flag = True
                    break
            
            if flag:
                res += 1
            else:
                for j in range(n - 1):
                    if strs[j][i] < strs[j + 1][i]:
                        small[j] = True
        
        return res
```
