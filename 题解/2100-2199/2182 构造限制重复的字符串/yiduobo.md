---
title: "2182. 构造限制重复的字符串"
aliases: ["yiduobo的每日leetcode 2182.构造限制重复的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string", "题单/贪心算法", "题单/贪心算法/三-字符串贪心", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536087362"
zhihu_id: "536087362"
zhihu_title: "yiduobo的每日leetcode 2182.构造限制重复的字符串"
question_id: "2182"
question: "构造限制重复的字符串"
problem_url: "https://leetcode.cn/problems/construct-string-with-repeat-limit/"
difficulty: "Medium"
rating: 1680
created: "2022-07-01T01:09:28+08:00"
updated: "2022-07-01T01:09:28+08:00"
upvotes: 0
comments: 0
---

# 2182. 构造限制重复的字符串

> **[yiduobo的每日leetcode 2182.构造限制重复的字符串](https://zhuanlan.zhihu.com/p/536087362) · 知乎 · 2022-07-01 · 赞同 0**
> 力扣：[2182. 构造限制重复的字符串](https://leetcode.cn/problems/construct-string-with-repeat-limit/) · Medium · 灵茶山艾府：[简洁写法：从大到小贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2182.构造限制重复的字符串

[力扣](https://leetcode.cn/problems/construct-string-with-repeat-limit/)

题目要求构造的字符串字典序最大，虽然存在重复的限制，但是同时并不需要用完所有的字符，因此只需在重复限制内尽量将字典序较大的字符排到前面就行了。

在这里可以先统计每种字符串的出现次数，然后找出剩余字符中字典序最大的，作为主力字符，在这里使用now来表示。同时还需要找出字典序第二大的，作为间隔字符，在这里使用next来表示。

接下来按照repeatLimit个now、1个next、再repeatLimit个now、再1个next的顺序来构造答案，直到now或者next用完。

若用完的是now，那么对于剩下的字符而言，当前的next字典序是最大的，因此新的now就是当前的next，而新的next则需要从next在字母表中的上一个字符往前找。

若用完的是next，那么now不需要变动，只需寻找新的next即可。

重复上面的过程，直到所有字符用完或者找不到新的next。

最后附上python代码：

```python
class Solution(object):
    def repeatLimitedString(self, s, repeatLimit):
        """
        :type s: str
        :type repeatLimit: int
        :rtype: str
        """
        
        cnt_list = [0] * 26
        for char in s:
            cnt_list[ord(char) - 97] += 1
        
        now = 25
        while cnt_list[now] == 0:
            now -= 1
        
        next = now - 1
        while next >= 0 and cnt_list[next] == 0:
            next -= 1

        res = ''
        while now >= 0:
            if cnt_list[now] > repeatLimit:
                res += chr(now + 97) * repeatLimit
                cnt_list[now] -= repeatLimit
                if next < 0:
                    break
                res += chr(next + 97)
                cnt_list[next] -= 1
                while next >= 0 and cnt_list[next] == 0:
                    next -= 1
            else:
                res += chr(now + 97) * cnt_list[now]
                cnt_list[now] = 0
                now = next
                next -= 1
                while next >= 0 and cnt_list[next] == 0:
                    next -= 1
        
        return res
```
