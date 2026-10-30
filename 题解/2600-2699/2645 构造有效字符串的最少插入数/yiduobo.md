---
title: "2645. 构造有效字符串的最少插入数"
aliases: ["yiduobo的每日leetcode 2645.构造有效字符串的最少插入数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646932945"
zhihu_id: "646932945"
zhihu_title: "yiduobo的每日leetcode 2645.构造有效字符串的最少插入数"
question_id: "2645"
question: "构造有效字符串的最少插入数"
problem_url: "https://leetcode.cn/problems/minimum-additions-to-make-valid-string/"
difficulty: "Medium"
created: "2023-07-31T03:24:02+08:00"
updated: "2023-07-31T03:24:02+08:00"
upvotes: 1
comments: 0
---

# 2645. 构造有效字符串的最少插入数

> **[yiduobo的每日leetcode 2645.构造有效字符串的最少插入数](https://zhuanlan.zhihu.com/p/646932945) · 知乎 · 2023-07-31 · 赞同 1**
> 力扣：[2645. 构造有效字符串的最少插入数](https://leetcode.cn/problems/minimum-additions-to-make-valid-string/) · Medium · 灵茶山艾府：[两种方法：考虑相邻字母/abc个数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2645.构造有效字符串的最少插入数

[力扣](https://leetcode.cn/problems/minimum-additions-to-make-valid-string/)

由于题目中只有三种字符，因此完全可以将所有情况都列举出来，分情况进行讨论。

不妨设目前处理到了字符串中的下标位置p，那么对于word[p]：

1、若word[p]为字符a：

首先，若p是word的最后一个字符，或者word[p]的下一个字符word[p + 1]也是a，这种情况下必须补充后面的bc，因此此时需要将答案加上2，然后将p向后移动一位

接下来，若word[p + 1]为b，那么最理想的情况就是word[p + 2]为c，这种情况下就不需要额外的插入操作，只需将p向后移动三位即可；反过来，则需要额外补充一个c，此时就应该将答案加上1，然后将p向后移动两位

最后，若word[p + 1]为c，那么此时就需要在a和c的中间插入一个b，此时应该将答案加上1，然后将p向后移动两位

2、若word[p]为字符b：

首先这个b的左侧必须要补充一个字符a，接下来则可以对其右侧的字符进行讨论

若p是word的最后一个字符，或者word[p + 1]不是c，那么b的右侧就还需要补充一个c，这种情况下就应该将答案加上2，然后将p向后移动一位；反过来则只需将答案加上1，然后将p向后移动两位

3、若word[p]为字符c：

此时只能选择在c的左侧补充ab，因此需要将答案加上2，然后将p向后移动一位

最后附上python代码：

```python
class Solution(object):
    def addMinimum(self, word):
        """
        :type word: str
        :rtype: int
        """

        p = 0
        res = 0
        while p < len(word):
            if word[p] == 'a':
                if p + 1 == len(word) or word[p + 1] == 'a':
                    res += 2
                    p += 1
                elif word[p + 1] == 'b':
                    if p + 2 == len(word) or word[p + 2] != 'c':
                        res += 1
                        p += 2
                    else:
                        p += 3
                elif word[p + 1] == 'c':
                    p += 2
                    res += 1
            
            elif word[p] == 'b':
                if p + 1 == len(word) or word[p + 1] != 'c':
                    res += 2
                    p += 1
                else:
                    res += 1
                    p += 2
            
            elif word[p] == 'c':
                res += 2
                p += 1
        
        return res
```
