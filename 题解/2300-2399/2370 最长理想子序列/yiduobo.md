---
title: "2370. 最长理想子序列"
aliases: ["yiduobo的每日leetcode 2370.最长理想子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563390380"
zhihu_id: "563390380"
zhihu_title: "yiduobo的每日leetcode 2370.最长理想子序列"
question_id: "2370"
question: "最长理想子序列"
problem_url: "https://leetcode.cn/problems/longest-ideal-subsequence/"
difficulty: "Medium"
rating: 1835
created: "2022-09-11T16:17:37+08:00"
updated: "2022-09-11T16:17:37+08:00"
upvotes: 0
comments: 0
---

# 2370. 最长理想子序列

> **[yiduobo的每日leetcode 2370.最长理想子序列](https://zhuanlan.zhihu.com/p/563390380) · 知乎 · 2022-09-11 · 赞同 0**
> 力扣：[2370. 最长理想子序列](https://leetcode.cn/problems/longest-ideal-subsequence/) · Medium · 灵茶山艾府：[子序列 DP + 枚举字符 + 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2370.最长理想子序列

[力扣](https://leetcode.cn/problems/longest-ideal-subsequence/)

动态规划的题目。

题目要找的是最长子序列而不是子串，因此在这里可以使用相对离散的状态表示，我在这里使用的是f[i]表示以第i小的字符结尾的最长理想子序列的长度，也就是f[0]表示以'a'结尾的最长子序列的长度，f[1]表示以'b'结尾的最长子序列的长度，依次类推。f中的元素都初始化为0。

接下来一趟遍历，对于当前字符char，首先根据char的ascii码计算出char是第几小的字符，记为order。

然后根据题目给出的k和计算出的order，得到char上一个字符的合法取值范围[left, right]。

最后遍历[left, right]，对于当前遍历到的last_order，当前字符可以接在以第last_order小结尾的子序列的后面，因此就有f[order] \= max(f[last_order]) + 1

全部计算完成后，f中的最大值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def longestIdealString(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        f = [0] * 26

        for char in s:
            order = ord(char) - 97
            left = max(0, order - k)
            right = min(25, order + k)
            ma = 0
            for last_order in range(left, right + 1):
                ma = max(ma, f[last_order])
            
            f[order] = ma + 1
        
        return max(f)
```
