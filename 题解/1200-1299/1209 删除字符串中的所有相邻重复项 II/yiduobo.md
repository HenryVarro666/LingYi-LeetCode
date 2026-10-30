---
title: "1209. 删除字符串中的所有相邻重复项II"
aliases: ["yiduobo的每日leetcode 1209.删除字符串中的所有相邻重复项II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382318632"
zhihu_id: "382318632"
zhihu_title: "yiduobo的每日leetcode 1209.删除字符串中的所有相邻重复项II"
question_id: "1209"
question: "删除字符串中的所有相邻重复项 II"
problem_url: "https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string-ii/"
difficulty: "Medium"
rating: 1542
created: "2021-06-20T13:00:18+08:00"
updated: "2021-06-20T13:00:18+08:00"
upvotes: 0
comments: 0
---

# 1209. 删除字符串中的所有相邻重复项II

> **[yiduobo的每日leetcode 1209.删除字符串中的所有相邻重复项II](https://zhuanlan.zhihu.com/p/382318632) · 知乎 · 2021-06-20 · 赞同 0**
> 力扣：[1209. 删除字符串中的所有相邻重复项 II](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string-ii/) · Medium · 灵茶山艾府：[邻项消除问题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1209.删除字符串中的所有相邻重复项II

[力扣](https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string-ii/)

当某个字符与之前的k - 1个字符相同，形成了连续的k个重复字符时需要将其删去，那么当我们继续向后看时，则需要用到更之前的字符，于是需要想办法将这些字符以及出现的次数储存起来，同时每次我们使用的都是最靠后的字符，因此一个自然的想法就是使用栈来储存每个剩下的字符以及出现的次数。

于是现在的做法就是一趟扫描，对于当前字符：

1、若当前字符与栈顶字符一致，且该字符在栈中已出现k - 1次，那么此时就出现了一个长度为k个连续重复字符，那么要将该字符弹出栈中

2、若当前字符与栈顶字符一致，且该字符在栈中出现未到k - 1次，那么此时应该将该字符出现的次数加上1

3、若当前字符与栈顶字符不同，那么此时应该直接将该字符加入到栈顶，同时置出现的次数为1

扫描完成后，栈中剩余的字符就是最终答案。另外在拼凑最终答案时需要注意不要忘记字符出现的次数。

最后附上python代码：

```python
class Solution(object):
    def removeDuplicates(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        stack = []
        for char in s:
            if stack and stack[-1][0] == char:
                if stack[-1][1] == k - 1:
                    stack.pop()
                else:
                    stack[-1][1] += 1
            else:
                stack.append([char, 1])

        return ''.join([x[0] * x[1] for x in stack])
```
