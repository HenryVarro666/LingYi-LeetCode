---
title: "2423. 删除字符使频率相同"
aliases: ["yiduobo的每日leetcode 2423.删除字符使频率相同"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/581680872"
zhihu_id: "581680872"
zhihu_title: "yiduobo的每日leetcode 2423.删除字符使频率相同"
question_id: "2423"
question: "删除字符使频率相同"
problem_url: "https://leetcode.cn/problems/remove-letter-to-equalize-frequency/"
difficulty: "Easy"
created: "2022-11-09T00:59:48+08:00"
updated: "2022-11-09T00:59:48+08:00"
upvotes: 0
comments: 0
---

# 2423. 删除字符使频率相同

> **[yiduobo的每日leetcode 2423.删除字符使频率相同](https://zhuanlan.zhihu.com/p/581680872) · 知乎 · 2022-11-09 · 赞同 0**
> 力扣：[2423. 删除字符使频率相同](https://leetcode.cn/problems/remove-letter-to-equalize-frequency/) · Easy · 灵茶山艾府：[两种方法：暴力/分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2423.删除字符使频率相同

[力扣](https://leetcode.cn/problems/remove-letter-to-equalize-frequency/)

最简单的做法自然是枚举所有种类的字符，如果其出现在word中，那么就删除其中一个，然后统计word中剩下字符出现的次数并检测频率是否相同。

我在这里采用的是统计每个字符出现的次数cnt，以及cnt.values()中每种次数出现的次数cnt_of_cnt，然后根据这两种次数来进行判断。

首先，所有字符出现的次数要么是同一种，要么集中在两种，也就是说len(cnt_of_cnt)应该为1或者2。

当len(cnt_of_cnt) \= 1时，说明原始的word中每种字符出现的次数都相同。如果在删除其中某个字符后要求每种字符出现的次数还是相同，那么说明要么每种字符刚好只出现了一次，要么总共就只有一种字符。这两种情况分别对应到min(cnt_of_cnt.keys()) \= 1以及min(cnt_of_cnt.values()) \= 1。

当len(cnt_of_cnt) \= 2时，则要求cnt_of_cnt.values()中至少有一个1，也就是不合群的cnt只能有一个，否则无论怎么删除都会有不合群的cnt存在。接下来讨论这个1出现在什么地方。

当key较大的那一个对应的value为1时，说明某种字符char出现了max(cnt_of_cnt.keys())次，其他字符都出现了min(cnt_of_cnt.keys())次。此时如果删除掉一个char，那么其出现次数就变成了max(cnt_of_cnt.keys()) - 1次，此时就需要满足max(cnt_of_cnt.keys()) - 1 \= min(cnt_of_cnt.keys())。

当key较小的那一个对应的value为1时，则说明其对应的那种字符只能出现1次，再删除后不再产生影响，因此需要满足min(cnt_of_cnt.keys()) \= 1，且cnt_of_cnt[1] \= 1。

最后附上python代码：

```python
class Solution(object):
    def equalFrequency(self, word):
        """
        :type word: str
        :rtype: bool
        """

        cnt_dict = {}
        for char in word:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        cnt_of_cnt = {}
        for cnt in cnt_dict.values():
            cnt_of_cnt[cnt] = cnt_of_cnt.get(cnt, 0) + 1

        if len(cnt_of_cnt) == 1:
            return min(cnt_of_cnt.values()) == 1 or min(cnt_of_cnt.keys()) == 1
        
        if len(cnt_of_cnt) == 2:
            if cnt_of_cnt[max(cnt_of_cnt.keys())] == 1 and min(cnt_of_cnt.keys()) == max(cnt_of_cnt.keys()) - 1:
                return True
            if min(cnt_of_cnt.keys()) == 1 and cnt_of_cnt[1] == 1:
                return True
        
        return False
```
