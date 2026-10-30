---
title: "2131. 连接两字母单词得到的最长回文串"
aliases: ["yiduobo的每日leetcode 2131.连接两字母单词得到的最长回文串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527233147"
zhihu_id: "527233147"
zhihu_title: "yiduobo的每日leetcode 2131.连接两字母单词得到的最长回文串"
question_id: "2131"
question: "连接两字母单词得到的最长回文串"
problem_url: "https://leetcode.cn/problems/longest-palindrome-by-concatenating-two-letter-words/"
difficulty: "Medium"
rating: 1557
created: "2022-06-11T00:49:14+08:00"
updated: "2022-06-11T00:49:14+08:00"
upvotes: 0
comments: 0
---

# 2131. 连接两字母单词得到的最长回文串

> **[yiduobo的每日leetcode 2131.连接两字母单词得到的最长回文串](https://zhuanlan.zhihu.com/p/527233147) · 知乎 · 2022-06-11 · 赞同 0**
> 力扣：[2131. 连接两字母单词得到的最长回文串](https://leetcode.cn/problems/longest-palindrome-by-concatenating-two-letter-words/) · Medium · 灵茶山艾府：[构造题：贪心 + 分类讨论（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2131.连接两字母单词得到的最长回文串

[力扣](https://leetcode.cn/problems/longest-palindrome-by-concatenating-two-letter-words/)

首先可以明确的，对于每个两字母单词，只有唯一的两字母单词，也就是其两个字符调换过的反向单词能与之配对。而对于所有配对的词组，可以将二者分别添加在答案的两侧，这样的话答案的回文性质不会产生变化，同时长度增加了4，因此应当尽可能多地找出配对。对于寻找配对的问题，在这里可以使用哈希表统计每种两字母单词出现的次数。对于当前处理的两字母单词，利用哈希表判断其未使用的反向单词还有多少个。若大于0，则将其减去1，并形成一组配对，将答案加上4，否则将当前单词自身加入到哈希表中。

另外，在找完所有可能的配对之后，如果还有两个字母相同的两字母单词没有被使用过，那么可以将其放在回文串的中心位置，此时应该将答案再加上2。

最后附上python代码：

```python
class Solution(object):
    def longestPalindrome(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        def get_num(first, second):
            return (ord(first) - 97) * 26 + ord(second) - 97

        mid_cnt = 0
        res = 0
        num_dict = {}
        for word in words:
            if word[0] == word[1]:
                mid_flag = True
            else:
                mid_flag = False

            reverse_num = get_num(word[1], word[0])
            if num_dict.get(reverse_num, 0) > 0:
                res += 4
                num_dict[reverse_num] -= 1
                if mid_flag:
                    mid_cnt -= 1
            else:
                num = get_num(word[0], word[1])
                num_dict[num] = num_dict.get(num, 0) + 1
                if mid_flag:
                    mid_cnt += 1
        
        if mid_cnt > 0:
            res += 2
        
        return res
```
