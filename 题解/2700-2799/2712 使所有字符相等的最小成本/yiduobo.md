---
title: "2712. 使所有字符相等的最小成本"
aliases: ["yiduobo的每日leetcode 2712.使所有字符相等的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651241072"
zhihu_id: "651241072"
zhihu_title: "yiduobo的每日leetcode 2712.使所有字符相等的最小成本"
question_id: "2712"
question: "使所有字符相等的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-make-all-characters-equal/"
difficulty: "Medium"
rating: 1791
created: "2023-08-21T02:43:36+08:00"
updated: "2023-08-21T02:43:36+08:00"
upvotes: 0
comments: 0
---

# 2712. 使所有字符相等的最小成本

> **[yiduobo的每日leetcode 2712.使所有字符相等的最小成本](https://zhuanlan.zhihu.com/p/651241072) · 知乎 · 2023-08-21 · 赞同 0**
> 力扣：[2712. 使所有字符相等的最小成本](https://leetcode.cn/problems/minimum-cost-to-make-all-characters-equal/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2712.使所有字符相等的最小成本

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-cost-to-make-all-characters-equal/)

题目给出一个仅由0和1构成的字符串，每次可以将其中的某个前缀或者后缀进行翻转，代价为翻转的长度，问最终将这个字符串变为全0或者全1所需的最小代价。

首先可以明确的是，所有对前缀翻转的区间与所有对后缀翻转的区间是不可能重叠的，因为对于重叠的区间，翻转两次相当于没有翻转，相当于浪费了两倍重叠长度的代价。

有了这个结论，就可以先计算出仅通过前缀翻转将字符串的所有前缀变为全0或者全1的最小代价left，其中left[i][0]表示将s[0 : i + 1]这一段前缀变为0的最小代价，而left[i][1]则表示将这一段前缀变为1的最小代价。同样的，也可以计算出仅通过后缀翻转将字符串的所有后缀变为全0或者全1的最小代价right。

接下来对于某个分割点cut_pos，这个分割点会将字符串分成前缀和后缀两个部分，而这种分割方案的最小代价就是left[cut_pos][0] + right[cut_pos + 1][0]与left[cut_pos][1] + right[cut_pos + 1][1]中的较小值。于是只需枚举所有可行的cut_pos，找出其中的最小代价就行了。

到了这里，还有一个问题需要解决的就是如何计算left和right。由于left和right的计算是完全对称的，因此在这里以left的计算进行说明，right的计算只需要对称操作就行了。

首先考虑边界情况。当s[0]为0时，left[0][0] \= 0，left[0][1] \= 1，反之left[0][0] \= 1，left[0][1] \= 0。简化的写法就是left[0][0] \= int(s[0])，left[0][1] \= 1 - int(s[0])。

接下来对于i > 0的情况：

1、当s[i] \= 0时：

1-1）对于left[i][0]，此时无需对s[i]进行任何操作，因此就有left[i][0] \= left[i - 1][0]

1-2）对于left[i][1]，此时需要先将s[i]左侧的所有值都变为0，然后将s[0: i + 1]这一段进行翻转，而将s[i]左侧所有值变为0的最小代价为left[i - 1][0]，因此这里就有left[i][0] \= left[i - 1][0] + i + 1

2、当s[i] \= 1时：

2-1）对于left[i][0]，此时与情况1-2类似，需要先将s[i]左侧的所有值都变为1，然后将s[0: i + 1]这一段进行翻转，因此这里就有left[i][0] \= left[i - 1][0] + i + 1

2-2）对于left[i][1]，此时无需对s[i]进行任何操作，因此就有left[i][1] \= left[i - 1][1]

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        left = [[int(s[0]), 1 - int(s[0])]]
        for index in range(1, len(s)):
            char = s[index]
            if char == '0':
                left.append([left[-1][0], left[-1][0] + index + 1])
            else:
                left.append([left[-1][1] + index + 1, left[-1][1]])
        
        right = [[int(s[-1]), 1 - int(s[-1])]]
        for index in range(len(s) - 2, -1, -1):
            char = s[index]
            if char == '0':
                right.append([right[-1][0], right[-1][0] + len(s) - index])
            else:
                right.append([right[-1][1] + len(s) - index, right[-1][1]])
        right.reverse()
        
        res = min(min(left[-1]), min(right[0]))
        for cut_pos in range(len(s) - 1):
            res = min(res, left[cut_pos][0] + right[cut_pos + 1][0], left[cut_pos][1] + right[cut_pos + 1][1])
        
        return res
```
