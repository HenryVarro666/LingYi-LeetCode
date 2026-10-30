---
title: "1781. 所有子字符串美丽值之和"
aliases: ["yiduobo的每日leetcode 1781.所有子字符串美丽值之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462564256"
zhihu_id: "462564256"
zhihu_title: "yiduobo的每日leetcode 1781.所有子字符串美丽值之和"
question_id: "1781"
question: "所有子字符串美丽值之和"
problem_url: "https://leetcode.cn/problems/sum-of-beauty-of-all-substrings/"
created: "2022-01-27T22:46:21+08:00"
updated: "2022-01-27T22:46:22+08:00"
upvotes: 0
comments: 0
---

# 1781. 所有子字符串美丽值之和

> **[yiduobo的每日leetcode 1781.所有子字符串美丽值之和](https://zhuanlan.zhihu.com/p/462564256) · 知乎 · 2022-01-27 · 赞同 0**
> 力扣：[1781. 所有子字符串美丽值之和](https://leetcode.cn/problems/sum-of-beauty-of-all-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1781.所有子字符串美丽值之和

[力扣](https://leetcode-cn.com/problems/sum-of-beauty-of-all-substrings/)

没有什么好的思路，好在是字符串的规模不大，因此可以直接枚举所有的子字符串，然后计算字符串中各个字符的数量从而得出该字符串的美丽值。

具体计算美丽值时，可以对每个字符维护一个前缀和，然后利用前缀和计算区间中该字符的数量。即[l, r]这一段中某个字符的数量等于[0, r]中该字符的数量减去[0, l - 1]中该字符的数量。

最后附上python代码：

```python
class Solution(object):
    def beautySum(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt_list = [{}]
        for char in s:
            cnt_list.append(cnt_list[-1].copy())
            cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1

        n = len(s)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                ma = 0
                mi = j - i + 1
                for index in range(26):
                    char = chr(index + 97)
                    cnt = cnt_list[j + 1].get(char, 0) - cnt_list[i].get(char, 0)
                    ma = max(ma, cnt)
                    if cnt > 0:
                        mi = min(mi, cnt)
                
                res += ma - mi
        
        return res
```
