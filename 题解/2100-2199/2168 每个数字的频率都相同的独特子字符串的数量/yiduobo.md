---
title: "2168. 每个数字的频率都相同的独特子字符串的数量"
aliases: ["yiduobo的每日leetcode 2168.每个数字的频率都相同的独特子字符串的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627123613"
zhihu_id: "627123613"
zhihu_title: "yiduobo的每日leetcode 2168.每个数字的频率都相同的独特子字符串的数量"
question_id: "2168"
question: "每个数字的频率都相同的独特子字符串的数量"
problem_url: "https://leetcode.cn/problems/unique-substrings-with-equal-digit-frequency/"
created: "2023-05-06T01:47:06+08:00"
updated: "2023-05-06T01:47:06+08:00"
upvotes: 0
comments: 0
---

# 2168. 每个数字的频率都相同的独特子字符串的数量

> **[yiduobo的每日leetcode 2168.每个数字的频率都相同的独特子字符串的数量](https://zhuanlan.zhihu.com/p/627123613) · 知乎 · 2023-05-06 · 赞同 0**
> 力扣：[2168. 每个数字的频率都相同的独特子字符串的数量](https://leetcode.cn/problems/unique-substrings-with-equal-digit-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2168.每个数字的频率都相同的独特子字符串的数量

[力扣](https://leetcode.cn/problems/unique-substrings-with-equal-digit-frequency/)

题目的数据规模不大，那么完全一趟遍历，枚举所有可能的左边界left。对于当前的left，从nums[left]开始向后遍历，同时使用一个哈希表记录每种数字出现的次数。若某一时刻cnt中每种数字出现的频率一致，那么当前字符串就是一个候选字符串。

另一方面，对于字符串的去重，可以直接使用哈希表来去重，当然也可以利用trie树来进行，我在这里采用的是trie树。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self):
        self.childs = [None] * 10

class Solution(object):
    def equalDigitFrequency(self, s):
        """
        :type s: str
        :rtype: int
        """

        root = TreeNode()
        n = len(s)
        res = 0

        def check(cnt):
            target = None
            for v in cnt:
                if v != 0:
                    if target is None:
                        target = v
                    elif target != v:
                        return False

            return True

        num_list = [int(x) for x in list(s)]
        for left in range(n):
            cnt = [0] * 10
            check_flag = False
            now = root

            for digit in num_list[left:]:
                if now.childs[digit] is None:
                    now.childs[digit] = TreeNode()
                    check_flag = True
                
                now = now.childs[digit]
                cnt[digit] += 1

                if check_flag and check(cnt):
                    res += 1
        
        return res
```
