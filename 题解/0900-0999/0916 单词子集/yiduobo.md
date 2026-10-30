---
title: "916. 单词子集"
aliases: ["yiduobo的每日leetcode 916.单词子集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355266658"
zhihu_id: "355266658"
zhihu_title: "yiduobo的每日leetcode 916.单词子集"
question_id: "916"
question: "单词子集"
problem_url: "https://leetcode.cn/problems/word-subsets/"
created: "2021-03-07T16:09:24+08:00"
updated: "2021-03-07T16:09:24+08:00"
upvotes: 0
comments: 0
---

# 916. 单词子集

> **[yiduobo的每日leetcode 916.单词子集](https://zhuanlan.zhihu.com/p/355266658) · 知乎 · 2021-03-07 · 赞同 0**
> 力扣：[916. 单词子集](https://leetcode.cn/problems/word-subsets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

916.单词子集

[力扣](https://leetcode-cn.com/problems/word-subsets/)

对于B中的某个单词b，若其包含的每个字母出现的次数都小于等于A中某个单词a中对应字母的出现次数，那么就说b是a的子集。

现在要求B中所有单词都是a的子集，那么就意味着每个字符在B中各个单词出现次数中的最大值依然是小于等于a中对应字母的出现次数的，因此可以先统计每个字母在B中各个单词中出现次数的最大值，然后再逐个遍历A中的单词进行判断。

最后附上python代码：

```python
class Solution(object):
    def wordSubsets(self, A, B):
        """
        :type A: List[str]
        :type B: List[str]
        :rtype: List[str]
        """

        char_dict = {}
        for word in B:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            for char in tmp_dict:
                char_dict[char] = max(char_dict.get(char, 0), tmp_dict[char])
        
        res = []
        for word in A:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            flag = True
            for char in char_dict:
                if tmp_dict.get(char, 0) < char_dict[char]:
                    flag = False
                    break
            
            if flag:
                res.append(word)
        
        return res
```
