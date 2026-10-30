---
title: "2116. 判断一个括号字符串是否有效"
aliases: ["yiduobo的每日leetcode 2116.判断一个括号字符串是否有效"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524302298"
zhihu_id: "524302298"
zhihu_title: "yiduobo的每日leetcode 2116.判断一个括号字符串是否有效"
question_id: "2116"
question: "判断一个括号字符串是否有效"
problem_url: "https://leetcode.cn/problems/check-if-a-parentheses-string-can-be-valid/"
difficulty: "Medium"
rating: 2038
created: "2022-06-04T22:36:18+08:00"
updated: "2022-06-04T22:36:18+08:00"
upvotes: 1
comments: 0
---

# 2116. 判断一个括号字符串是否有效

> **[yiduobo的每日leetcode 2116.判断一个括号字符串是否有效](https://zhuanlan.zhihu.com/p/524302298) · 知乎 · 2022-06-04 · 赞同 1**
> 力扣：[2116. 判断一个括号字符串是否有效](https://leetcode.cn/problems/check-if-a-parentheses-string-can-be-valid/) · Medium · 灵茶山艾府：[一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2116.判断一个括号字符串是否有效

[力扣](https://leetcode.cn/problems/check-if-a-parentheses-string-can-be-valid/)

对于常规的判断括号字符串的问题，经典的做法是从左向右一趟遍历，使用一个变量cnt记录当前落单的左括号的数目。若当前的括号为左括号，那么将cnt加上1，否则将cnt减去1。在这个过程中若cnt小于0，说明存在超量的右括号无法匹配。另外，在遍历完成后若cnt还大于0，则说明有超量的左括号无法匹配。

对于本题，由于可以灵活变换括号，那么对于超量右括号的问题，可以尝试将当前右括号以及之前的部分可变的右括号变为左括号来暂时缓解左括号紧缺的问题。这样一来，只需在从左向右遍历的过程中使用另一个变量change_able，记录当前可变右括号的数目，当出现左括号不足的情况时，选择将之前的某个可变右括号变为左括号即可。

这样一来可以尽最大可能保证右括号不超量，但是依然可能产生多余的左括号。最理想的情况是在过程中就完成了左括号到右括号的转化，但是在这里并不好确定转化的时机。

不妨从另一个角度来考虑。

如果从右向左遍历，那么上面算法中左右括号的地位就互换了。那么如果在从右向左遍历时，又出现了右括号多余的情况，就说明有部分括号无需适配前面或者后面的括号，是可以灵活变化的，此时只需从中间向两侧成对安排这些多出来括号成对匹配就能使得最终整个括号串都匹配了。

最后附上python代码：

```python
class Solution(object):
    def canBeValid(self, s, locked):
        """
        :type s: str
        :type locked: str
        :rtype: bool
        """

        n = len(s)
        if n % 2 == 1:
            return False

        cnt = 0
        change_able = 0
        for index in range(n):
            if s[index] == '(':
                cnt += 1
            else:
                if locked[index] == '0':
                    change_able += 1
                if cnt == 0:
                    if change_able > 0:
                        change_able -= 1
                        cnt = 1
                    else:
                        return False
                else:
                    cnt -= 1

        cnt = 0
        change_able = 0
        for index in range(n - 1, -1, -1):
            if s[index] == ')':
                cnt += 1
            else:
                if locked[index] == '0':
                    change_able += 1
                if cnt == 0:
                    if change_able > 0:
                        change_able -= 1
                        cnt = 1
                    else:
                        return False
                else:
                    cnt -= 1
                
        return True
```
