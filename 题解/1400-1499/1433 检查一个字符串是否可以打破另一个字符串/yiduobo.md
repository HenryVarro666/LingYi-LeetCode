---
title: "1433. 检查一个字符串是否可以打破另一个字符串"
aliases: ["yiduobo的每日leetcode 1433.检查一个字符串是否可以打破另一个字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409168536"
zhihu_id: "409168536"
zhihu_title: "yiduobo的每日leetcode 1433.检查一个字符串是否可以打破另一个字符串"
question_id: "1433"
question: "检查一个字符串是否可以打破另一个字符串"
problem_url: "https://leetcode.cn/problems/check-if-a-string-can-break-another-string/"
created: "2021-09-10T22:54:00+08:00"
updated: "2021-09-10T22:54:00+08:00"
upvotes: 0
comments: 0
---

# 1433. 检查一个字符串是否可以打破另一个字符串

> **[yiduobo的每日leetcode 1433.检查一个字符串是否可以打破另一个字符串](https://zhuanlan.zhihu.com/p/409168536) · 知乎 · 2021-09-10 · 赞同 0**
> 力扣：[1433. 检查一个字符串是否可以打破另一个字符串](https://leetcode.cn/problems/check-if-a-string-can-break-another-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1433.检查一个字符串是否可以打破另一个字符串

[力扣](https://leetcode-cn.com/problems/check-if-a-string-can-break-another-string/)

题目中的打破要求字符串中的每一位都满足特定的大小关系，因此在这里我们需要使用强强对话而不是田忌赛马的策略，于是我们可以先对两个字符串中的字符进行排序，然后逐位进行对比。具体实现时我采用的是类似桶排的做法，统计每个字符出现的次数，然后从z开始向a遍历，对比当前字符在两个串中出现的次数。

最后附上pythond代码：

```python
class Solution(object):
    def checkIfCanBreak(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        cnt1 = [0] * 26
        for char in s1:
            cnt1[ord(char) - 97] += 1

        cnt2 = [0] * 26
        for char in s2:
            cnt2[ord(char) - 97] += 1
        
        flag = 0
        for index in range(25, -1, -1):
            if cnt1[index] == cnt2[index]:
                continue
            elif cnt1[index] > cnt2[index]:
                if flag == 2:
                    return False

                flag = 1
                cnt1[index - 1] += cnt1[index] - cnt2[index]
            else:
                if flag == 1:
                    return False
                
                flag = 2
                cnt2[index - 1] += cnt2[index] - cnt1[index]
        
        return True
```
