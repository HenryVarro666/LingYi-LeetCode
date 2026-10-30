---
title: "3412. 计算字符串的镜像分数"
aliases: ["yiduobo的每日leetcode 3412.计算字符串的镜像分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32085715094"
zhihu_id: "32085715094"
zhihu_title: "yiduobo的每日leetcode 3412.计算字符串的镜像分数"
question_id: "3412"
question: "计算字符串的镜像分数"
problem_url: "https://leetcode.cn/problems/find-mirror-score-of-a-string/"
difficulty: "Medium"
rating: 1578
created: "2025-03-22T22:07:22+08:00"
updated: "2025-03-22T22:07:22+08:00"
upvotes: 0
comments: 0
---

# 3412. 计算字符串的镜像分数

> **[yiduobo的每日leetcode 3412.计算字符串的镜像分数](https://zhuanlan.zhihu.com/p/32085715094) · 知乎 · 2025-03-22 · 赞同 0**
> 力扣：[3412. 计算字符串的镜像分数](https://leetcode.cn/problems/find-mirror-score-of-a-string/) · Medium · 灵茶山艾府：[26 个栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3412.计算字符串的镜像分数

[3412. 计算字符串的镜像分数 - 力扣（LeetCode）](https://leetcode.cn/problems/find-mirror-score-of-a-string/description/)

题目给出一个字符串s，另外定义字母的镜像为其在反转字母表之后对应位置上的字符，例如'a'的镜像是'z'，而'y'的镜像是'b'。

一开始，s中所有的字符都是未标记的，且初始分数为0。接下来需要从左到右遍历字符串，对于当前遍历到的下标i，尝试找到i左侧最近的未被标记的下标j，要求s[j]是s[i]的镜像。若存在这样的j，就将i和j进行标记，并将i - j累加到得分中；若不存在这样的j，则跳过下标i继续向后处理。

问最终的得分是多少。

题目实际上是要求找出当前字符的镜像字符上一次出现且未被标记过的下标，那么在这里就可以对每个字符都是用一个栈来储存其未被标记的下标位置，使用栈的理由是为了方便获取最近一次的下标。

接下来就只需按照题目要求进行一趟遍历，对于当前遍历到的字符char，先计算其镜像字符mirror。若mirror对应的栈中还有未被标记的下标，那么栈顶的下标就是要找的上一次出现且未被标记过的下标，将其从栈中弹出，并使用当前下标与栈顶下标之差更新答案；若mirror对应的栈为空，说明不存在合法的下标，此时需要将当前下标加入char对应的栈中以供后续的匹配使用。

另外对于mirror的计算，我在这里采用的是ascii码之和的方式进行计算的，因为一组镜像字符的ascii码之和恰好是219。

最后附上python代码：

```python
class Solution(object):
    def calculateScore(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        unmarked = {}
        for asc in range(92, 123):
            char = chr(asc)
            unmarked[char] = []
        
        res = 0
        for index, char in enumerate(s):
            mirror = chr(219 - ord(char))
            if unmarked[mirror]:
                res += index - unmarked[mirror].pop()
            else:
                unmarked[char].append(index)

        return res
```
