---
title: "1624. 两个相同字符之间的最长子字符串"
aliases: ["yiduobo的每日leetcode 1624.两个相同字符之间的最长子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/436477566"
zhihu_id: "436477566"
zhihu_title: "yiduobo的每日leetcode 1624.两个相同字符之间的最长子字符串"
question_id: "1624"
question: "两个相同字符之间的最长子字符串"
problem_url: "https://leetcode.cn/problems/largest-substring-between-two-equal-characters/"
created: "2021-11-22T23:24:34+08:00"
updated: "2021-11-22T23:24:34+08:00"
upvotes: 0
comments: 0
---

# 1624. 两个相同字符之间的最长子字符串

> **[yiduobo的每日leetcode 1624.两个相同字符之间的最长子字符串](https://zhuanlan.zhihu.com/p/436477566) · 知乎 · 2021-11-22 · 赞同 0**
> 力扣：[1624. 两个相同字符之间的最长子字符串](https://leetcode.cn/problems/largest-substring-between-two-equal-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1624.两个相同字符之间的最长子字符串

[力扣](https://leetcode-cn.com/problems/largest-substring-between-two-equal-characters/)

比较基础的题目。直接一趟扫描，记录每个字符首次出现的位置，并使用当前位置与该字符首次出现位置之间的差来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxLengthBetweenEqualCharacters(self, s):
        """
        :type s: str
        :rtype: int
        """

        last_pos = {}
        res = -1
        for index, char in enumerate(s):
            if char not in last_pos:
                last_pos[char] = index
            else:
                dis = index - last_pos[char] - 1
                res = max(dis, res)
        
        return res
```
