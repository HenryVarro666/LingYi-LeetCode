---
title: "30. 串联所有单词的子串"
aliases: ["yiduobo的每日leetcode 30.串联所有单词的子串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/面试经典-150-题/滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/118659881"
zhihu_id: "118659881"
zhihu_title: "yiduobo的每日leetcode 30.串联所有单词的子串"
question_id: "30"
question: "串联所有单词的子串"
problem_url: "https://leetcode.cn/problems/substring-with-concatenation-of-all-words/"
difficulty: "Hard"
created: "2020-03-27T22:33:09+08:00"
updated: "2020-03-27T22:33:09+08:00"
upvotes: 0
comments: 0
---

# 30. 串联所有单词的子串

> **[yiduobo的每日leetcode 30.串联所有单词的子串](https://zhuanlan.zhihu.com/p/118659881) · 知乎 · 2020-03-27 · 赞同 0**
> 力扣：[30. 串联所有单词的子串](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/) · Hard · 灵茶山艾府：[30 次定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

30.串联所有单词的字串<https://leetcode-cn.com/problems/substring-with-concatenation-of-all-words/>

拿到题目的第一想法是现在s中找到words中所有单词出现的位置，然后看看能否找到连续的位置。不过前面这步的复杂度是O(len(s)len(words))，后面这个dp可能可以做，但是想想就比较复杂，因此还是老老实实一个一个来比较。

设一共有k个单词，注意到这里每个词的长度都是一样的，设这个长度为word_len，那么对于位置p开头的串，比较的就是

s[p : p + word_len]

s[p + word_len : p + word_len \* 2]

...

s[p + word_len \* (k - 1) : p + word_len \* k]

这一共k个字符串是否能匹配上所有的单词。

对于位置p + word_len开始的串，则是

s[p + word_len : p + word_len \* 2]

s[p + word_len \* 2 : p \*+ word_len \* 3]

...

s[p + word_len \* k : p + word_len \* (k + 1)]

这一共k个字符串是否能匹配上所有的单词。

可以发现，二者相比，后面这种情况其实就是去掉了头部的那个串，加入了尾部的这个串，因此利用滑动窗口的思想，可以一次扫描解决掉所有模word_len等于p的情况。那么通过枚举每个p，然后进行扫描就能找出所有的答案。

具体的比较方法可以维护一个dict，表示当前有了哪些词。当新来一个词word的时候：

1、如果word不在words中，那么表示当前这一堆词都无法形成合法的答案，因此清空掉dict然后将p跳转到当前词的末尾。

2、如果word在words中，将其加入dict[word]加一。如果此时的dict[word]大于word在words中出现的次数，那么说明需要在前面的部分中去除掉一个word，但是不能拦腰斩断，必须从p开始去除。当然此时p开始的单词不一定就是word，那么也必须将其误杀掉，直到dict[word]等于word在words中出现的次数为止。如果此时dict中的单词数量等于单词的个数k，说明没有误杀掉单词，即找到了一种合法的情况，那么将p加入答案。

时间复杂度应该是O(len(s) \* word_len \* log(len(words)))，分别为

len(s)代表滑动窗口一次扫描的复杂度

word_len代表枚举所有p的复杂度

log(len(words)则是dict相关操作的复杂度

最后附上python代码：

```python
class Solution(object):
    def findSubstring(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: List[int]
        """

        if not s or not words:
            return []

        word_dict = {}
        for word in words:
            word_dict[word] = word_dict.get(word, 0) + 1

        word_len = len(words[0])
        s_len = len(s)
        max_start_pos = s_len - word_len * len(words)
        res = []

        for index in range(word_len):
            left = index
            right = index
            now_word_dict = {}
            word_cnt = 0
            while left <= max_start_pos and right + word_len <= s_len:
                now_word = s[right : right + word_len]
                right += word_len
                if now_word not in word_dict:
                    now_word_dict = {}
                    left = right
                    word_cnt = 0
                else:
                    word_cnt += 1
                    now_word_dict[now_word] = now_word_dict.get(now_word, 0) + 1
                    while now_word_dict[now_word] > word_dict[now_word]:
                        left_word = s[left : left + word_len]
                        now_word_dict[left_word] -= 1
                        left += word_len
                        word_cnt -= 1

                    if word_cnt == len(words):
                        res.append(left)
                
        return res
```
