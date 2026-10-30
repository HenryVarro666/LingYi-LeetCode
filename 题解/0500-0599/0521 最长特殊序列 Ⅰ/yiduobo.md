---
title: "521. 最长特殊序列I & 522. 最长特殊序列II"
aliases: ["yiduobo的每日leetcode 521.最长特殊序列I && 522.最长特殊序列II", "521. 最长特殊序列I", "522. 最长特殊序列II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "leetcode/string", "题单/贪心算法", "题单/贪心算法/五-思维题", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261029224"
zhihu_id: "261029224"
zhihu_title: "yiduobo的每日leetcode 521.最长特殊序列I && 522.最长特殊序列II"
question_id: ["521", "522"]
question: ["最长特殊序列 Ⅰ", "最长特殊序列 II"]
problem_url: ["https://leetcode.cn/problems/longest-uncommon-subsequence-i/", "https://leetcode.cn/problems/longest-uncommon-subsequence-ii/"]
difficulty: ["Easy", "Medium"]
rating: ["1400", "1700"]
created: "2020-10-01T23:21:57+08:00"
updated: "2020-10-01T23:23:14+08:00"
upvotes: 0
comments: 0
---

# 521. 最长特殊序列I & 522. 最长特殊序列II

> **[yiduobo的每日leetcode 521.最长特殊序列I && 522.最长特殊序列II](https://zhuanlan.zhihu.com/p/261029224) · 知乎 · 2020-10-01 · 赞同 0**
> 力扣：[521. 最长特殊序列 Ⅰ](https://leetcode.cn/problems/longest-uncommon-subsequence-i/) · Easy · 灵茶山艾府：[分类讨论/脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[522. 最长特殊序列 II](https://leetcode.cn/problems/longest-uncommon-subsequence-ii/) · Medium · 灵茶山艾府：[枚举+判断子序列（Python/Java/C++/C/Go/JS/Rust）](../0522%20最长特殊序列%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

521.最长特殊序列I <https://leetcode-cn.com/problems/longest-uncommon-subsequence-i/>

522.最长特殊序列II <https://leetcode-cn.com/problems/longest-uncommon-subsequence-ii/>

根据题目的描述，对于两个字符串A和B，若A是B的子序列，那么A的任意子序列也一定是B的子序列，换言之，就是A的任意子序列必然不是特殊子序列。

对于521题来说：

1、若A和B长度相等，那么当A等于B时，A是B的子序列，B也是A的子序列，因此答案为-1。若A不等于B，那么选择A或者B都可以。

2、若A和B长度不相等，那么较长字符串显然不可能是较短字符串的子序列，因此答案就是较长的那一个字符串。

对于522题来说，则需要考虑每个字符串是否是其他字符串的子序列，因此可以将字符串先按长度从大到小进行排序，然后一趟扫描检测当前字符串是否是其他字符串的子序列，若不是，那么当前字符串就是最终答案。

检测子序列的方法可以使用贪心法，即从头开始扫描两个字符串，尽可能地进行匹配。

最后附上python代码:

521:

```python
class Solution(object):
    def findLUSlength(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: int
        """

        if a == b:
            return -1
        
        return max(len(a), len(b))
```

522:

```python
class Solution(object):
    def findLUSlength(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        strs = sorted(strs, key=lambda d:-len(d))
        for i in range(len(strs)):
            for j in range(len(strs)):
                if i == j:
                    continue
                pos = 0
                flag = True
                for char in strs[j]:
                    if strs[i][pos] == char:
                        pos += 1
                        if pos == len(strs[i]):
                            flag = False
                            break
                if not flag:
                    break
            
            if flag:
                return len(strs[i])
        
        return -1
```
