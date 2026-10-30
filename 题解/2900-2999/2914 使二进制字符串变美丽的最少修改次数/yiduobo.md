---
title: "2914. 使二进制字符串变美丽的最少修改次数"
aliases: ["yiduobo的每日leetcode 2914.使二进制字符串变美丽的最少修改次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664611108"
zhihu_id: "664611108"
zhihu_title: "yiduobo的每日leetcode 2914.使二进制字符串变美丽的最少修改次数"
question_id: "2914"
question: "使二进制字符串变美丽的最少修改次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-changes-to-make-binary-string-beautiful/"
difficulty: "Medium"
rating: 1480
created: "2023-11-02T02:11:40+08:00"
updated: "2023-11-02T02:11:40+08:00"
upvotes: 0
comments: 0
---

# 2914. 使二进制字符串变美丽的最少修改次数

> **[yiduobo的每日leetcode 2914.使二进制字符串变美丽的最少修改次数](https://zhuanlan.zhihu.com/p/664611108) · 知乎 · 2023-11-02 · 赞同 0**
> 力扣：[2914. 使二进制字符串变美丽的最少修改次数](https://leetcode.cn/problems/minimum-number-of-changes-to-make-binary-string-beautiful/) · Medium · 灵茶山艾府：[[灵茶山艾府题解/solutions/2914 使二进制字符串变美丽的最少修改次数 · 统计 s-i- != s-i+1-（Python-Java-C++-Go）|统计 s[i] != s[i+1]（Python/Java/C++/Go）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2914.使二进制字符串变美丽的最少修改次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-number-of-changes-to-make-binary-string-beautiful/)

首先可以明确的是，构造一个较长的美丽子串显然是比构造若干个长度为2的美丽子串更容易的，因此最终字符串应该划分成若干个长度为2的子串，然后逐个计算将其变为美丽子串需要的操作数。于是只需按步长为2遍历整个字符串，比较当前字符与下一个字符是否相同并更新答案。

最后附上python代码：

```python
class Solution(object):
    def minChanges(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        for index in range(0, len(s), 2):
            if s[index] != s[index + 1]:
                res += 1
        
        return res
```
