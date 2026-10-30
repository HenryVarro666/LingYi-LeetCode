---
title: "2337. 移动片段得到字符串"
aliases: ["yiduobo的每日leetcode 2337.移动片段得到字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/559660747"
zhihu_id: "559660747"
zhihu_title: "yiduobo的每日leetcode 2337.移动片段得到字符串"
question_id: "2337"
question: "移动片段得到字符串"
problem_url: "https://leetcode.cn/problems/move-pieces-to-obtain-a-string/"
difficulty: "Medium"
rating: 1693
created: "2022-08-31T01:27:43+08:00"
updated: "2022-08-31T01:27:43+08:00"
upvotes: 0
comments: 0
---

# 2337. 移动片段得到字符串

> **[yiduobo的每日leetcode 2337.移动片段得到字符串](https://zhuanlan.zhihu.com/p/559660747) · 知乎 · 2022-08-31 · 赞同 0**
> 力扣：[2337. 移动片段得到字符串](https://leetcode.cn/problems/move-pieces-to-obtain-a-string/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2337.移动片段得到字符串

[力扣](https://leetcode.cn/problems/move-pieces-to-obtain-a-string/)

根据题目的描述，L和R是不能相互交换位置的，那么如果抛开start和target中的下划线不看，两个字符串中L和R形成的子序列必须是完全一致的。于是可以使用两个遍历p1和p2分别从start和target的开头向后扫，找到第一个不是下划线的字符，此时有几种可能的情况需要分别讨论：

1、p1和p2中有一方并没有找到不是下划线的字符。说明start和target中由L和R构成的子序列必然是不一致的，直接返回false

2、start[p1]与target[p2]不一致。同理，也是直接返回false

3、start[p1]和target[p2]都是字符'L'，且p1 \< p2。由于start中的'L'只能向右移动，因此start[p1]这个'L'是无法移动到p2这个位置上的，因此直接返回false

4、start[p1]和target[p2]都是字符'R'，且p1 > p2。同理，也是直接返回false

如果全部字符遍历完毕也没有出现上面几种情况，那么就返回true

最后附上python代码：

```python
class Solution(object):
    def canChange(self, start, target):
        """
        :type start: str
        :type target: str
        :rtype: bool
        """

        p1 = p2 = 0
        while p1 < len(start) or p2 < len(target):
            while p1 < len(start) and start[p1] == '_':
                p1 += 1
            
            while p2 < len(target) and target[p2] == '_':
                p2 += 1

            if p1 < len(start):
                if p2 < len(target):
                    if start[p1] != target[p2]:
                        return False
                    
                    if start[p1] == 'L':
                        if p1 < p2:
                            return False
                    elif p1 > p2:
                        return False
                
                else:
                    return False
            
            elif p2 != len(target):
                return False
        
            p1 += 1
            p2 += 1

        return True
```
