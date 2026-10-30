---
title: "2268. 最少按键次数"
aliases: ["yiduobo的每日leetcode 2268.最少按键次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629017937"
zhihu_id: "629017937"
zhihu_title: "yiduobo的每日leetcode 2268.最少按键次数"
question_id: "2268"
question: "最少按键次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-keypresses/"
created: "2023-05-13T00:49:17+08:00"
updated: "2023-05-13T00:49:17+08:00"
upvotes: 1
comments: 0
---

# 2268. 最少按键次数

> **[yiduobo的每日leetcode 2268.最少按键次数](https://zhuanlan.zhihu.com/p/629017937) · 知乎 · 2023-05-13 · 赞同 1**
> 力扣：[2268. 最少按键次数](https://leetcode.cn/problems/minimum-number-of-keypresses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2268.最少按键次数

[力扣](https://leetcode.cn/problems/minimum-number-of-keypresses/)

对于s中的字符，出现频率越高就越应该将其放在数字的第一位，若第一位用完了就应该放在第二位，最后才是第三位，于是可以一趟遍历，统计每种字符出现的次数，然后将这些字符按次数从大到小进行排序。

对于排在1到9位的，可以将这些字符安排在第一位，这些字符需要其频次对应的按键次数；对于排在10到18位的，则可以将这些字符安排在第二位，这些字符需要其频次乘以2的按键次数；而对于最后这一部分，则只能安排在第三位，需要的按键次数就是频次乘以3。将这些次数累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumKeypresses(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        
        for index, freq in enumerate(sorted(cnt.values(), reverse=True)):
            if index < 9:
                res += freq
            elif index < 18:
                res += freq * 2
            else:
                res += freq * 3
        
        return res
```
