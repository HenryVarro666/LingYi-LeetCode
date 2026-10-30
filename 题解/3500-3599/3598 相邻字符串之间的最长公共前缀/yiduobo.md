---
title: "3598. 相邻字符串之间的最长公共前缀"
aliases: ["yiduobo的每日leetcode 3598.相邻字符串之间的最长公共前缀"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940928080068739344"
zhihu_id: "1940928080068739344"
zhihu_title: "yiduobo的每日leetcode 3598.相邻字符串之间的最长公共前缀"
question_id: "3598"
question: "相邻字符串之间的最长公共前缀"
problem_url: "https://leetcode.cn/problems/longest-common-prefix-between-adjacent-strings-after-removals/"
difficulty: "Medium"
rating: 1655
created: "2025-08-19T00:40:05+08:00"
updated: "2025-08-19T00:40:05+08:00"
upvotes: 1
comments: 0
---

# 3598. 相邻字符串之间的最长公共前缀

> **[yiduobo的每日leetcode 3598.相邻字符串之间的最长公共前缀](https://zhuanlan.zhihu.com/p/1940928080068739344) · 知乎 · 2025-08-19 · 赞同 1**
> 力扣：[3598. 相邻字符串之间的最长公共前缀](https://leetcode.cn/problems/longest-common-prefix-between-adjacent-strings-after-removals/) · Medium · 灵茶山艾府：[三种方法：前后缀分解 / 维护前三大 LCP / 维护前二大 LCP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3598.相邻字符串之间的最长公共前缀

[3598. 相邻字符串之间的最长公共前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-common-prefix-between-adjacent-strings-after-removals/description/)

给出一个字符串数组words，对于从0到words.length - 1之间的下标index，要求执行以下步骤：

1、从words中移除下标index处的元素

2、计算修改后数组中所有相邻对之间的最长公共前缀的长度

返回一个数组answer，其中answer[index]是移除下标index后相邻对之间最长公共前缀的长度。若不存在相邻对或者不存在公共前缀，answer[index]则为0。

对于下标index的字符串，如果将其删除，原来处于index - 1以及index + 1的字符串将变得相邻，但是对其他的字符串不会产生任何影响。也就是说，将下标index的字符串删除，将使得index与index - 1以及index与index +1这两组公共前缀消失，但是会新增index - 1与index + 1的公共前缀。于是在这里可以先一趟遍历，对于每个下标index，计算words[index]与words[index - 1]的最长公共前缀，记为f[index]，同时计算words[index]与words[index - 2]的最长公共前缀，记为g[index]。

接下来，从f中选出最大的三个值first、second、third，在这里选出三个值的理由是一次删除操作中可能会同时移除掉first和second，因此还需要保留一个thrid。接下来只需一趟遍历，对于当前移除掉的字符串words[index]：

1、若f[index]以及f[index + 1]中的较大值等于first，且这二者中的较小值等于second：

此时说明first和second都被这次操作移除掉了，此时应该对比的就是其他相邻字符串的最长公共前缀长度，即third，与words[index + 1]与words[index - 1]的最长公共前缀长度，也就是g[index + 1]。此时的答案就是third与g[index + 1]的较大值

2、若f[index]以及f[index + 1]中的较大值等于first，且这二者中的较小值不等于second：

此时其他相邻字符串的最长公共前缀长度就是second，与g[index + 1]对比后取较大值即可

3、若f[index]以及f[index + 1]中的较大值不等于first：

此时first依然是其他相邻字符串的最长公共前缀长度，与g[index + 1]对比后取较大值即可

最后附上python代码：

```python
class Solution(object):
    def longestCommonPrefix(self, words):
        """
        :type words: List[str]
        :rtype: List[int]
        """
        
        n = len(words)
        if n == 1:
            return [0]

        f = [0] * n
        g = [0] * n

        def get_length(w1, w2):
            for index in range(min(len(w1), len(w2))):
                if w1[index] != w2[index]:
                    return index
            
            return min(len(w1), len(w2))

        for index in range(1, n):
            f[index] = get_length(words[index - 1], words[index])

            if index > 1:
                g[index] = get_length(words[index - 2], words[index])
        
        first, second, third = 0, 0, 0
        for index in range(1, n):
            if f[index] > first:
                first, second, third = f[index], first, second
            elif f[index] > second:
                second, third = f[index], second
            elif f[index] > third:
                third = f[index]

        res = []
        for index in range(n):
            if index == 0:
                if f[index + 1] == first:
                    res.append(second)
                else:
                    res.append(first)
            
            elif index == n - 1:
                if f[index] == first:
                    res.append(second)
                else:
                    res.append(first)
            
            else:
                if max(f[index], f[index + 1]) == first:
                    if min(f[index], f[index + 1]) == second:
                        res.append(max(third, g[index + 1]))
                    else:
                        res.append(max(second, g[index + 1]))
                else:
                    res.append(max(first, g[index + 1]))
        
        return res
```
