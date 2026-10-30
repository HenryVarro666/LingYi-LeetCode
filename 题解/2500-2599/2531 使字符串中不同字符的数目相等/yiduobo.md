---
title: "2531. 使字符串总不同字符的数目相等"
aliases: ["yiduobo的每日leetcode 2531.使字符串总不同字符的数目相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637165329"
zhihu_id: "637165329"
zhihu_title: "yiduobo的每日leetcode 2531.使字符串总不同字符的数目相等"
question_id: "2531"
question: "使字符串中不同字符的数目相等"
problem_url: "https://leetcode.cn/problems/make-number-of-distinct-characters-equal/"
difficulty: "Medium"
created: "2023-06-15T00:13:16+08:00"
updated: "2023-06-15T00:13:16+08:00"
upvotes: 0
comments: 0
---

# 2531. 使字符串总不同字符的数目相等

> **[yiduobo的每日leetcode 2531.使字符串总不同字符的数目相等](https://zhuanlan.zhihu.com/p/637165329) · 知乎 · 2023-06-15 · 赞同 0**
> 力扣：[2531. 使字符串中不同字符的数目相等](https://leetcode.cn/problems/make-number-of-distinct-characters-equal/) · Medium · 灵茶山艾府：[枚举+简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2531.使字符串总不同字符的数目相等

[力扣](https://leetcode.cn/problems/make-number-of-distinct-characters-equal/)

题目中的字符串长度很长，因此不能直接枚举具体的交换位置。不过本题中的字符仅有小写字符构成，换言之单个字符串中最多出现26种字符，可以改为枚举交换了哪两种字符。

分别遍历两个字符串，使用两个哈希表cnt1和cnt2统计各种字符出现的次数，此时就可以通过cnt1和cnt2中出现次数大于0的字符串得到初始状态下不同的字符数目，分别记为tot1和tot2。

接下来分别枚举两个字符串中用来替换的字符i和j，在这里需要确保这两个字符在对应的字符串中出现过，也就是cnt1[i] > 0且cnt2[j] > 0，那么对于i和j：

1、若i和j相同，那么相当于没有进行交换。若tot1与tot2一开始就相同，那么交换i和j就是一种可行的方案，此时返回true。反之，交换i和j则不行，需要考虑其他方案。

2、若i和j不同，那么交换后第一个字符串中的i就减少了一个，同时j增加了一个，若此时出现了从有到无或者从无到有的变化，也就是cnt1[i]从1变成了0，或者cnt1[j]从0变成了1，那么就需要对应地更新tot1；同样的，对于tot2也需要进行相应的操作。若处理完后最新的tot1和tot2相同，那么当前的交换方案就是可行的，返回true。

在具体实现上，不需要真正修改cnt1和cnt2，只需判断对应的字符出现次数是否为1或0。

若遍历完了所有的交换方案依然没有找出可行的方案，那么就返回false。

最后附上python代码：

```python
class Solution(object):
    def isItPossible(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: bool
        """

        cnt1 = [0] * 26
        for char in word1:
            cnt1[ord(char) - 97] += 1
        
        cnt2 = [0] * 26
        for char in word2:
            cnt2[ord(char) - 97] += 1
        
        tot1 = tot2 = 0
        for i in range(26):
            if cnt1[i] > 0:
                tot1 += 1
            if cnt2[i] > 0:
                tot2 += 1
        
        for i in range(26):
            for j in range(26):
                if cnt1[i] == 0 or cnt2[j] == 0:
                    continue

                if i == j:
                    if tot1 == tot2:
                        return True
                    continue

                now1, now2 = tot1, tot2
                if cnt1[i] == 1:
                    now1 -= 1
                if cnt2[j] == 1:
                    now2 -= 1
                
                if cnt2[i] == 0:
                    now2 += 1
                if cnt1[j] == 0:
                    now1 += 1
                
                if now1 == now2:
                    return True

        return False
```
