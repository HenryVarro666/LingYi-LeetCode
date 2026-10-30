---
title: "555. 分割连接字符串"
aliases: ["yiduobo的每日leetcode 555.分割连接字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601145505"
zhihu_id: "601145505"
zhihu_title: "yiduobo的每日leetcode 555.分割连接字符串"
question_id: "555"
question: "分割连接字符串"
problem_url: "https://leetcode.cn/problems/split-concatenated-strings/"
created: "2023-01-27T02:25:34+08:00"
updated: "2023-01-27T02:25:34+08:00"
upvotes: 0
comments: 0
---

# 555. 分割连接字符串

> **[yiduobo的每日leetcode 555.分割连接字符串](https://zhuanlan.zhihu.com/p/601145505) · 知乎 · 2023-01-27 · 赞同 0**
> 力扣：[555. 分割连接字符串](https://leetcode.cn/problems/split-concatenated-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

555.分割连接字符串

[力扣](https://leetcode.cn/problems/split-concatenated-strings/)

看上去感觉题目应该存在某种优美的算法，不过没有想出来，好在题目的数据规模不大，可以支撑O(nm)的时间复杂度，其中n为单词的数量，m为所有单词中字符的总数。

最终答案一定是某个子串或者其反转从某个位置cus_pos截断，取后缀的部分，然后按顺序拼接其他单词或者反转后的单词，最后再拼接剩截断单词前缀的部分。

对于这三种拼接材料而言，可以很明确的是如果不对单词进行切分，那么只需考察反转后与原串的字典序大小，并将较大的那一种用来填充最终答案，因此在这里就可以先将所有单词的预处理工作做好，这样一来拼接的时间复杂度就是标准的O(m)。

对于被切分的单词，暂时没有什么比较好的想法，那么就只能枚举这个单词的所有后缀以及配对的前缀，以及反转后单词的所有后缀以及配对的前缀，然后根据上面三部分连接的方法拼接出可能的常规字符串，并更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def splitLoopedString(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """

        n = len(strs)
        best_strs = strs[:]
        for index, s in enumerate(strs):
            left, right = 0, len(s) - 1
            while left < right:
                if s[left] != s[right]:
                    if s[left] < s[right]:
                        best_strs[index] = s[::-1]
                    break
                left += 1
                right -= 1

        res = None
        for index, s in enumerate(strs):
            best_other = ''.join(best_strs[index + 1:]) + ''.join(best_strs[:index])
            for start_pos in range(len(s)):
                f = s[start_pos:]
                f += best_other
                f += s[:start_pos]
                g = s[::-1][start_pos:]
                g += best_other
                g += s[::-1][:start_pos]

                if res is None or res < f:
                    res = f
                if res is None or res < g:
                    res = g
        
        return res
```
