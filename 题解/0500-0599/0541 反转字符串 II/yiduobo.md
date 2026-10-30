---
title: "541. 反转字符串"
aliases: ["yiduobo的每日leetcode 541.反转字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261213963"
zhihu_id: "261213963"
zhihu_title: "yiduobo的每日leetcode 541.反转字符串"
question_id: "541"
question: "反转字符串 II"
problem_url: "https://leetcode.cn/problems/reverse-string-ii/"
difficulty: "Easy"
created: "2020-10-08T15:09:37+08:00"
updated: "2020-10-08T15:09:37+08:00"
upvotes: 0
comments: 0
---

# 541. 反转字符串

> **[yiduobo的每日leetcode 541.反转字符串](https://zhuanlan.zhihu.com/p/261213963) · 知乎 · 2020-10-08 · 赞同 0**
> 力扣：[541. 反转字符串 II](https://leetcode.cn/problems/reverse-string-ii/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

541.反转字符串<https://leetcode-cn.com/problems/reverse-string-ii/>

比较基础的题目，一趟扫描，使用一个cnt累积当前字符数量，累积到k位进行翻转，然后累积到2k位将cnt归零。需要注意的是，当扫描完成，cnt大于0且cnt小于k，说明最后的这cnt个字符也需要进行翻转。

我在这里先将字符串变为字符list，然后翻转的时候通过对称交换实现。

最后附上python代码：

```python
class Solution(object):
    def reverseStr(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        s_list = list(s)

        cnt = 0
        for index in range(len(s_list)):
            cnt += 1
            if cnt == k:
                start_pos = index - k + 1
                for pos in range(k / 2):
                    s_list[start_pos + pos], s_list[index - pos] = s_list[index - pos], s_list[start_pos + pos]
            elif cnt == k * 2:
                cnt = 0

        if cnt > 0 and cnt < k:
            start_pos = index - cnt + 1
            for pos in range(cnt / 2):
                s_list[start_pos + pos], s_list[index - pos] = s_list[index - pos], s_list[start_pos + pos]

        return ''.join(s_list)
```
