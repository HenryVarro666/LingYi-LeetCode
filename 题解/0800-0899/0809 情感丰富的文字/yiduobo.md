---
title: "809. 情感丰富的文字"
aliases: ["yiduobo的每日leetcode 809.情感丰富的文字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343564101"
zhihu_id: "343564101"
zhihu_title: "yiduobo的每日leetcode 809.情感丰富的文字"
question_id: "809"
question: "情感丰富的文字"
problem_url: "https://leetcode.cn/problems/expressive-words/"
created: "2021-01-11T21:59:43+08:00"
updated: "2021-01-11T21:59:43+08:00"
upvotes: 0
comments: 0
---

# 809. 情感丰富的文字

> **[yiduobo的每日leetcode 809.情感丰富的文字](https://zhuanlan.zhihu.com/p/343564101) · 知乎 · 2021-01-11 · 赞同 0**
> 力扣：[809. 情感丰富的文字](https://leetcode.cn/problems/expressive-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

809.情感丰富的文字

[力扣](https://leetcode-cn.com/problems/expressive-words/)

对于S而言，其中连续出现，且出现次数大于等于3次的字符我们可以认为是本来就是这样，或者是扩展得来的，于是可以从头到尾进行一趟扫描，统计各个字符连续出现的次数，并将这类连续出现的字符缩成一个字符。

接下来对于每个word，进行同样的操作，那么缩短后得到的字符串必须与s缩短后得到的字符串完全一致，且出现次数要么一致，要么比s中对应出现的次数要少，且s中出现的次数大于等于3次。只要不满足其中任意条件，就说明word无法扩展到S。

例如样例中的S，缩短后变为helo，连续出现次数分别为[1, 3, 2, 3]

对于各个word，则有

hello -> helo，连续出现次数为[1,1,2,1]

hi -> hi，连续出现次数为[1,1]

helo -> helo，连续出现次数为[1,1,1,1]

那么对于各个word而言：

hello是满足条件的

hi不能匹配上S缩短后形成的helo因此

helo则因为l的数量少于S中对应位上l的数量，且这个数量也小于3因此不行

因此最终就只要hello满足条件，答案为1

最后附上python代码：

```python
class Solution(object):
    def expressiveWords(self, S, words):
        """
        :type S: str
        :type words: List[str]
        :rtype: int
        """

        cnt_list = []
        now = ''
        cnt = 0
        for char in S + ' ':
            if char == now:
                cnt += 1
            else:
                if cnt > 0:
                    cnt_list.append([now, cnt])
                now = char
                cnt = 1

        res = 0
        for word in words:
            now = ''
            cnt = 0
            pos = 0
            flag = True
            for char in word + ' ':
                if char == now:
                    cnt += 1
                else:
                    if cnt > 0:
                        if pos == len(cnt_list):
                            flag = False
                            break
                        if cnt_list[pos][0] != now:
                            flag = False
                            break
                        if cnt_list[pos][1] < cnt or (cnt_list[pos][1] < 3 and cnt_list[pos][1] > cnt):
                            flag = False
                            break
                        pos += 1
                    now = char
                    cnt = 1
            
            if flag and pos == len(cnt_list):
                res += 1
        
        return res
```
