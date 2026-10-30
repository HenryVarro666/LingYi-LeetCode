---
title: "17. 电话号码的字母组合"
aliases: ["yiduobo的每日leetcode 17.电话号码的字母组合"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115104837"
zhihu_id: "115104837"
zhihu_title: "yiduobo的每日leetcode 17.电话号码的字母组合"
question_id: "17"
question: "电话号码的字母组合"
problem_url: "https://leetcode.cn/problems/letter-combinations-of-a-phone-number/"
difficulty: "Medium"
created: "2020-03-21T23:06:57+08:00"
updated: "2020-03-21T23:09:47+08:00"
upvotes: 0
comments: 0
---

# 17. 电话号码的字母组合

> **[yiduobo的每日leetcode 17.电话号码的字母组合](https://zhuanlan.zhihu.com/p/115104837) · 知乎 · 2020-03-21 · 赞同 0**
> 力扣：[17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/) · Medium · 灵茶山艾府：[【视频】回溯不会写？套路在此！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

17.电话号码的字母组合<https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number/>

比较基础的搜索回溯题，不过在python环境下利用生成式的方法可以很方便的求解，即按位枚举digits中的每一位，然后从上一位的解中生成这一位的解。

具体代码如下，其中res为按位迭代的解，char_list为数字对应的字母表：

```python
res = ['']
for k in digits:
    res = [i + j for i in res for j in char_list[int(k)]]
```

不过这里主要还是讲一个搜索回溯的思路，就是对于每一位，先选择一种可能的情况，然后继续做下一位。当后面位的情况都做完之后，再反过来重新选择一种可能的情况，接着再在做后面的位。

利用一个字符串记录中间的情况，同时记录当前的位数，当位数达到digits的位数时，表明已经生成了一种答案，记录下来然后尝试其他情况即可。

最后附上python代码：

```
class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """

        char_list = [[], 
                     [], 
                     ['a', 'b', 'c'], 
                     ['d', 'e', 'f'],
                     ['g', 'h', 'i'],
                     ['j', 'k', 'l'],
                     ['m', 'n', 'o'],
                     ['p', 'q', 'r', 's'],
                     ['t', 'u', 'v'],
                     ['w', 'x', 'y', 'z']]

        res = []
        self.search(digits, '', 0, char_list, res)
        return res

    def search(self, digits, now, level, char_list, res):
        if level == len(digits):
            if now:
                res.append(now)
            return

        for char in char_list[int(digits[level])]:
            self.search(digits, now + char, level + 1, char_list, res)
```
