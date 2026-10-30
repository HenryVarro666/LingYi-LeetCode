---
title: "159. 至多包含两个不同字符的最长子串"
aliases: ["yiduobo的每日leetcode 159.至多包含两个不同字符的最长子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590826920"
zhihu_id: "590826920"
zhihu_title: "yiduobo的每日leetcode 159.至多包含两个不同字符的最长子串"
question_id: "159"
question: "至多包含两个不同字符的最长子串"
problem_url: "https://leetcode.cn/problems/longest-substring-with-at-most-two-distinct-characters/"
created: "2022-12-10T17:42:27+08:00"
updated: "2022-12-10T17:42:27+08:00"
upvotes: 1
comments: 0
---

# 159. 至多包含两个不同字符的最长子串

> **[yiduobo的每日leetcode 159.至多包含两个不同字符的最长子串](https://zhuanlan.zhihu.com/p/590826920) · 知乎 · 2022-12-10 · 赞同 1**
> 力扣：[159. 至多包含两个不同字符的最长子串](https://leetcode.cn/problems/longest-substring-with-at-most-two-distinct-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

159.至多包含两个不同字符的最长子串

[力扣](https://leetcode.cn/problems/longest-substring-with-at-most-two-distinct-characters/)

经典的变长滑动窗口问题，使用一个哈希表cnt_dict记录当前窗口中每种字符出现的次数。

接下来每一轮，窗口右边界都向右移动一位，同时使用右边界对应的字符更新cnt_dict。若此时的cnt_dict中包含了超过三种字符，那么就不断将窗口左边界向右移动，直到cnt_dict中包含的字符数量小于等于2为止。确定好窗口左右边界之后，就可以使用窗口长度来更新答案了。

最后附上python代码：

```python
class Solution(object):
    def lengthOfLongestSubstringTwoDistinct(self, s):
        """
        :type s: str
        :rtype: int
        """

        char_cnt = {s[0] : 1}
        res = 1
        left = right = 0
        while right + 1 < len(s):
            right += 1
            char_cnt[s[right]] = char_cnt.get(s[right], 0) + 1
            while len(char_cnt) > 2:
                char_cnt[s[left]] -= 1
                if char_cnt[s[left]] == 0:
                    char_cnt.pop(s[left])
                left += 1
            
            res = max(res, right - left + 1)
        
        return res
```
