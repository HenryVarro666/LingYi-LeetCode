---
title: "14. 最长公共前缀"
aliases: ["yiduobo的每日leetcode 14.最长公共前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/bian-li", "题单/面试经典-150-题", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114551819"
zhihu_id: "114551819"
zhihu_title: "yiduobo的每日leetcode 14.最长公共前缀"
question_id: "14"
question: "最长公共前缀"
problem_url: "https://leetcode.cn/problems/longest-common-prefix/"
difficulty: "Easy"
created: "2020-03-19T21:53:09+08:00"
updated: "2020-03-19T21:53:09+08:00"
upvotes: 0
comments: 0
---

# 14. 最长公共前缀

> **[yiduobo的每日leetcode 14.最长公共前缀](https://zhuanlan.zhihu.com/p/114551819) · 知乎 · 2020-03-19 · 赞同 0**
> 力扣：[14. 最长公共前缀](https://leetcode.cn/problems/longest-common-prefix/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

14.最长公共前缀<https://leetcode-cn.com/problems/longest-common-prefix/>

直接按位枚举每一个字符，然后判断其他串中的这个字符是否相同，相同则累加到答案中，否则直接返回即可。

最终时间复杂度为O(nk)，n为字符串的数目，k为答案，且k不超过最短的字符串的长度。

最后附上python代码：

```python
class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        pos = 0
        res = ''

        if not strs:
            return res

        len_list = [len(x) for x in strs]
        for pos in range(min(len_list)):
            now = strs[0][pos]
            for string in strs[1:]:
                if string[pos] != now:
                    return res
            res += now

        return res
```
