---
title: "1419. 数青蛙"
aliases: ["yiduobo的每日leetcode 1419.数青蛙"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/array", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/407473423"
zhihu_id: "407473423"
zhihu_title: "yiduobo的每日leetcode 1419.数青蛙"
question_id: "1419"
question: "数青蛙"
problem_url: "https://leetcode.cn/problems/minimum-number-of-frogs-croaking/"
difficulty: "Medium"
created: "2021-09-06T17:38:52+08:00"
updated: "2021-09-06T17:38:52+08:00"
upvotes: 0
comments: 0
---

# 1419. 数青蛙

> **[yiduobo的每日leetcode 1419.数青蛙](https://zhuanlan.zhihu.com/p/407473423) · 知乎 · 2021-09-06 · 赞同 0**
> 力扣：[1419. 数青蛙](https://leetcode.cn/problems/minimum-number-of-frogs-croaking/) · Medium · 灵茶山艾府：[别想太复杂，模拟题罢了！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1419.数青蛙

[力扣](https://leetcode-cn.com/problems/minimum-number-of-frogs-croaking/)

与括号匹配很类似的问题，如果这里只有两个字母，那么就是一个判断括号串是否合法的问题。这里也可以使用类似的方法。这里有五个字母，那么分别使用c、r、o、a、k表示对应字母出现的次数，并使用遍历now表示当前尚未闭合的“括号”数目。接下来一趟扫描，对于当前字符：

1、若当前字符为'c'，那么先将c加上1。同时这也意味着新起了一个“括号”，那么将now加上1，并使用当前的now来更新答案res

2、若当前字符为'r'，那么先将r加上1。就像括号匹配问题中，任意时刻右括号的数目都不能大于左括号的数目，这里就转化成了r不能大于c。若r大于c，那么直接返回-1

3、若当前字符为'o'，那么先将o加上1。同样地，o的数目不能大于c或者r的数目。由于任意时刻都有r \<\= c，那么此时只需要判断o和r的大小。若o大于r，那么直接返回-1

4、若当前字符为'a'，那么先将a加上1。与上面相同，此时只需要判断a与o的大小

5、若当前字符为'k'，那么先将k加上1。与上面相同，此时只需要判断k与a的大小。另外，k意味着一组“括号”的闭合，那么将now减去1

遍历完成后，若c、r、o、a、k的数目不一样，说明存在未闭合的括号，此时返回-1，否则返回答案res

最后附上python代码：

```python
class Solution(object):
    def minNumberOfFrogs(self, croakOfFrogs):
        """
        :type croakOfFrogs: str
        :rtype: int
        """

        c = r = o = a = k = 0
        now = 0
        res = 0
        for char in croakOfFrogs:
            if char == 'c':
                c += 1
                now += 1
                res = max(now, res)
            elif char == 'r':
                r += 1
                if r > c:
                    return -1
            elif char == 'o':
                o += 1
                if o > r:
                    return -1
            elif char == 'a':
                a += 1
                if a > o:
                    return -1
            elif char == 'k':
                k += 1
                if k > a:
                    return -1
                now -= 1
        
        if c == r == o == a == k:
            return res
            
        return -1
```
