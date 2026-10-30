---
title: "3076. 数组中的最短非公共子字符串"
aliases: ["yiduobo的每日leetcode 3076.数组中的最短非公共子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bao-li", "题单/字符串", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697992111"
zhihu_id: "697992111"
zhihu_title: "yiduobo的每日leetcode 3076.数组中的最短非公共子字符串"
question_id: "3076"
question: "数组中的最短非公共子字符串"
problem_url: "https://leetcode.cn/problems/shortest-uncommon-substring-in-an-array/"
difficulty: "Medium"
created: "2024-05-15T22:21:57+08:00"
updated: "2024-05-15T22:21:57+08:00"
upvotes: 0
comments: 0
---

# 3076. 数组中的最短非公共子字符串

> **[yiduobo的每日leetcode 3076.数组中的最短非公共子字符串](https://zhuanlan.zhihu.com/p/697992111) · 知乎 · 2024-05-15 · 赞同 0**
> 力扣：[3076. 数组中的最短非公共子字符串](https://leetcode.cn/problems/shortest-uncommon-substring-in-an-array/) · Medium · 灵茶山艾府：[暴力，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3076.数组中的最短非公共子字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-uncommon-substring-in-an-array/description/)

题目的数据规模很小，直接暴力法是完全够用的。

逐个枚举字符串s，然后从1到len(s)枚举最短子串的长度length，接下来枚举s中所有长度为length的子串，并检测该子串是否在其他字符串中出现过。如果一次都没有出现过，那么就用这个字符串更新s对应的答案。

最后附上python代码：

```python
class Solution(object):
    def shortestSubstrings(self, arr):
        """
        :type arr: List[str]
        :rtype: List[str]
        """

        n = len(arr)
        res = [""] * n
        for i in range(n):
            s = arr[i]
            for length in range(1, len(s) + 1):
                for start in range(len(s)):
                    end = start + length
                    if end > len(s):
                        break
                    sub_s = s[start : end]
                
                    flag = True
                    for j in range(n):
                        if i == j:
                            continue
                        if arr[j].find(sub_s) != -1:
                            flag = False
                            break
                    
                    if flag and (res[i] == "" or res[i] > sub_s):
                        res[i] = sub_s
                
                if res[i] != "":
                    break

        return res
```
