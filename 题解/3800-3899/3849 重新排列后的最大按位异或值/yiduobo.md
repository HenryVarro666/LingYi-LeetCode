---
title: "3849. 重新排列后的最大按位异或值"
aliases: ["yiduobo的每日leetcode 3849.重新排列后的最大按位异或值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011494033567016595"
zhihu_id: "2011494033567016595"
zhihu_title: "yiduobo的每日leetcode 3849.重新排列后的最大按位异或值"
question_id: "3849"
question: "重新排列后的最大按位异或值"
problem_url: "https://leetcode.cn/problems/maximum-bitwise-xor-after-rearrangement/"
difficulty: "Medium"
rating: 1556
created: "2026-03-03T23:58:53+08:00"
updated: "2026-03-03T23:58:53+08:00"
upvotes: 0
comments: 0
---

# 3849. 重新排列后的最大按位异或值

> **[yiduobo的每日leetcode 3849.重新排列后的最大按位异或值](https://zhuanlan.zhihu.com/p/2011494033567016595) · 知乎 · 2026-03-03 · 赞同 0**
> 力扣：[3849. 重新排列后的最大按位异或值](https://leetcode.cn/problems/maximum-bitwise-xor-after-rearrangement/) · Medium · 灵茶山艾府：[从左到右贪心，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3849.重新排列后的最大按位异或值

<https://leetcode.cn/problems/maximum-bitwise-xor-after-rearrangement/description/>

题目给出两个长度均为n的二进制字符串s和t。

现在可以按任意顺序重新排列t中的字符，但s需要保持不变。

要求返回一个长度为n的二进制字符串，表示将s与重新排列后的t进行按位异或所能得到的最大值。

为了使得结果尽量大，就应该尽量让高位上为1，也就是说应该尽量让t在高位上的数字与s在高位上的数字不同。于是可以先对t进行一趟遍历，统计其中0和1的数目。接下来对s进行一趟遍历，对于当前的s[index]，若还有未使用的s[index] ^ 1，那么就将其填充到t这一位上，而答案的这一位就为1，否则只能将s[index]填充到t这一位上，而答案的这一位就为0。

最后附上python代码：

```python
class Solution(object):
    def maximumXor(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        
        cnt = [0] * 2
        for c in t:
            cnt[int(c)] += 1
        
        res = []
        for c in s:
            c = int(c)
            target = int(c) ^ 1
            if cnt[target] > 0:
                cnt[target] -= 1
                res.append('1')
            else:
                cnt[c] -= 1
                res.append('0')
        
        return ''.join(res)
```
