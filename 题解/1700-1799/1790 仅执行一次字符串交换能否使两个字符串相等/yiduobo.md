---
title: "1790. 仅执行一次字符串交换能否使两个字符串相等"
aliases: ["yiduobo的每日leetcode 1790.仅执行一次字符串交换能否使两个字符串相等"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463268707"
zhihu_id: "463268707"
zhihu_title: "yiduobo的每日leetcode 1790.仅执行一次字符串交换能否使两个字符串相等"
question_id: "1790"
question: "仅执行一次字符串交换能否使两个字符串相等"
problem_url: "https://leetcode.cn/problems/check-if-one-string-swap-can-make-strings-equal/"
created: "2022-01-30T23:36:55+08:00"
updated: "2022-01-30T23:36:55+08:00"
upvotes: 0
comments: 0
---

# 1790. 仅执行一次字符串交换能否使两个字符串相等

> **[yiduobo的每日leetcode 1790.仅执行一次字符串交换能否使两个字符串相等](https://zhuanlan.zhihu.com/p/463268707) · 知乎 · 2022-01-30 · 赞同 0**
> 力扣：[1790. 仅执行一次字符串交换能否使两个字符串相等](https://leetcode.cn/problems/check-if-one-string-swap-can-make-strings-equal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1790.仅执行一次字符串交换能否使两个字符串相等

[力扣](https://leetcode-cn.com/problems/check-if-one-string-swap-can-make-strings-equal/)

题目要求最多交换一次字符，那么只有当两个字符串完全相同，或者两个字符串中有两处字符恰好错位了，才能在一次交换之内使得两个字符串相等。

于是可以一趟扫描，统计当前不同字符的数目cnt。当出现一处不相等的字符时：

1、若之前没有出现过不同的字符，那么将cnt加1，并使用一个变量p记录这一处字符

2、若之前出现过一个不同的字符，其位置为p，那么就可以对比p和index这两处的字符是否恰好错位。若不是恰好错位，那么返回false

3、若之前已经出现过两处不同的字符，那么返回false

若能成功遍历完整个字符串，则还需要判断cnt是否等于0或者2，因为cnt为1时表示两个字符串中有一处字符不同，但没有办法通过交换使得两个字符串相同

最后附上python代码：

```python
class Solution(object):
    def areAlmostEqual(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        n = len(s1)
        cnt = 0
        p = None
        for index in range(n):
            if s1[index] != s2[index]:
                if cnt == 0:
                    p = index
                elif cnt == 1:
                    if s1[p] != s2[index] or s2[p] != s1[index]:
                        return False
                else:
                    return False
                
                cnt += 1
        
        return cnt % 2 == 0
```
