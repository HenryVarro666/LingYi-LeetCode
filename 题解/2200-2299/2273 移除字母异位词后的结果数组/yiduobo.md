---
title: "2273. 移除字母异位词后的结果数组"
aliases: ["yiduobo的每日leetcode 2273.移除字母异位词后的结果数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550447458"
zhihu_id: "550447458"
zhihu_title: "yiduobo的每日leetcode 2273.移除字母异位词后的结果数组"
question_id: "2273"
question: "移除字母异位词后的结果数组"
problem_url: "https://leetcode.cn/problems/find-resultant-array-after-removing-anagrams/"
difficulty: "Easy"
rating: 1295
created: "2022-08-06T00:52:05+08:00"
updated: "2022-08-06T00:52:05+08:00"
upvotes: 0
comments: 0
---

# 2273. 移除字母异位词后的结果数组

> **[yiduobo的每日leetcode 2273.移除字母异位词后的结果数组](https://zhuanlan.zhihu.com/p/550447458) · 知乎 · 2022-08-06 · 赞同 0**
> 力扣：[2273. 移除字母异位词后的结果数组](https://leetcode.cn/problems/find-resultant-array-after-removing-anagrams/) · Easy · 灵茶山艾府：[原地做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2273.移除字母异位词后的结果数组

[力扣](https://leetcode.cn/problems/find-resultant-array-after-removing-anagrams/)

题目中关于字母异位词的判断方式是两个单词中包含的字母一样，那么可以统计单词中各个字母出现的次数形成dict，然后通过判断dict是否相同来判断两个单词是否为字母异位词。

接下来就只需要一趟遍历，使用last_word记录上一个单词，同时使用last_char_dict记录上一个单词每个字母出现的次数。接下来对于当前遍历到的单词，统计当前单词中每个字母出现的次数，得到now_char_dict。若last_char_dict与now_char_dict一样，那么就删去当前单词，否则就将last_word加入到答案中，然后将last_char_dict更新为now_char_dict，将last_word更新为当前单词。

全部遍历完成后，还需要将最后这一轮的last_word加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def removeAnagrams(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """

        def get_char_dict(word):
            char_dict = {}
            for char in word:
                char_dict[char] = char_dict.get(char, 0) + 1
            return char_dict
        
        last_char_dict = get_char_dict(words[0])
        last_word = words[0]
        res = []
        for index in range(1, len(words)):
            now_char_dict = get_char_dict(words[index])
            if last_char_dict != now_char_dict:
                res.append(last_word)
                last_char_dict = now_char_dict
                last_word = words[index]
        
        res.append(last_word)
        return res
```
