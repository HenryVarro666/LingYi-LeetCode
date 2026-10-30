---
title: "2000. 反转单词前缀"
aliases: ["yiduobo的每日leetcode 2000.反转单词前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/simulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/502138448"
zhihu_id: "502138448"
zhihu_title: "yiduobo的每日leetcode 2000.反转单词前缀"
question_id: "2000"
question: "反转单词前缀"
problem_url: "https://leetcode.cn/problems/reverse-prefix-of-word/"
difficulty: "Easy"
rating: 1199
created: "2022-04-21T00:21:04+08:00"
updated: "2022-04-21T00:21:04+08:00"
upvotes: 0
comments: 0
---

# 2000. 反转单词前缀

> **[yiduobo的每日leetcode 2000.反转单词前缀](https://zhuanlan.zhihu.com/p/502138448) · 知乎 · 2022-04-21 · 赞同 0**
> 力扣：[2000. 反转单词前缀](https://leetcode.cn/problems/reverse-prefix-of-word/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2000.反转单词前缀

[力扣](https://leetcode-cn.com/problems/reverse-prefix-of-word/)

比较基础的题目，直接按照题意来操作就好了。一趟扫描，将当前遍历到的字符记录在一个list中，直到当前遍历到的字符等于ch或者到达word的末尾为止。

若中途退出，那么就将list反转后转化为字符串，拼接上剩下没遍历过的word后返回。若遍历完了整个word，那么就直接返回word。

最后附上python代码：

```python
class Solution(object):
    def reversePrefix(self, word, ch):
        """
        :type word: str
        :type ch: str
        :rtype: str
        """

        p = None
        res = []
        for index in range(len(word)):
            res.append(word[index])
            if word[index] == ch:
                p = index
                break
        
        if p is None:
            return word
        else:
            res.reverse()
            return ''.join(res) + word[p + 1:]
```
