---
title: "2825. 循环增长使字符串子序列等于另一个字符串"
aliases: ["yiduobo的每日leetcode 2825.循环增长使字符串子序列等于另一个字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659004932"
zhihu_id: "659004932"
zhihu_title: "yiduobo的每日leetcode 2825.循环增长使字符串子序列等于另一个字符串"
question_id: "2825"
question: "循环增长使字符串子序列等于另一个字符串"
problem_url: "https://leetcode.cn/problems/make-string-a-subsequence-using-cyclic-increments/"
difficulty: "Medium"
rating: 1415
created: "2023-09-29T01:27:09+08:00"
updated: "2023-09-29T01:27:09+08:00"
upvotes: 1
comments: 0
---

# 2825. 循环增长使字符串子序列等于另一个字符串

> **[yiduobo的每日leetcode 2825.循环增长使字符串子序列等于另一个字符串](https://zhuanlan.zhihu.com/p/659004932) · 知乎 · 2023-09-29 · 赞同 1**
> 力扣：[2825. 循环增长使字符串子序列等于另一个字符串](https://leetcode.cn/problems/make-string-a-subsequence-using-cyclic-increments/) · Medium · 灵茶山艾府：[双指针](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2825.循环增长使字符串子序列等于另一个字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/make-string-a-subsequence-using-cyclic-increments/description/)

如果不考虑循环增长操作，常规的字符串子序列匹配应该遵从贪心的思路，也就是能匹配就尽量匹配，理由的话也很直观，就是待匹配的剩余字符越少，匹配成功率越高，而剩余的原字符串越长，匹配成功率越高，综合这两点，对于可以匹配的位置尽量匹配就是最优的选择了。

对于本体，在多出了循环增长操作之后，这个贪心的思路是不受影响的，因此在这里就可以遍历str1，尽量通过直接相等或者循环增长一位后相等来按顺序匹配str2中的字符，检测是否能完整匹配str2。

最后附上python代码：

```python
class Solution(object):
    def canMakeSubsequence(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: bool
        """

        p = 0
        for char in str1:
            if char == str2[p] or chr((ord(char) - 97 + 1) % 26 + 97) == str2[p]:
                p += 1
                if p == len(str2):
                    return True
        
        return False
```
