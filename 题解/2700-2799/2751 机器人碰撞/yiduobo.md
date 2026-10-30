---
title: "2751. 机器人碰撞"
aliases: ["yiduobo的每日leetcode 2751.机器人碰撞"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654321803"
zhihu_id: "654321803"
zhihu_title: "yiduobo的每日leetcode 2751.机器人碰撞"
question_id: "2751"
question: "机器人碰撞"
problem_url: "https://leetcode.cn/problems/robot-collisions/"
difficulty: "Hard"
rating: 2092
created: "2023-09-05T03:42:11+08:00"
updated: "2023-09-05T03:42:11+08:00"
upvotes: 0
comments: 0
---

# 2751. 机器人碰撞

> **[yiduobo的每日leetcode 2751.机器人碰撞](https://zhuanlan.zhihu.com/p/654321803) · 知乎 · 2023-09-05 · 赞同 0**
> 力扣：[2751. 机器人碰撞](https://leetcode.cn/problems/robot-collisions/) · Hard · 灵茶山艾府：[用栈维护机器人（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2751.机器人碰撞

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/robot-collisions/)

与之前有一题行星碰撞很像，但是记不清楚题号了。

处理方法也是一样，从左向右遍历，使用栈维护当前还在向右移动的机器人。

对于当前遍历到的机器人，若其朝右移动，那么就将其加入到栈中；若其向左移动且此时的栈非空，那么其将与栈顶的机器人发生碰撞。对于碰撞机器人则可能出现三种情况：

1、向左走的机器人血量比向右走的机器人血量高：

此时需要将栈顶机器人弹出，同时将这个机器人的血量更新为0，即栈顶机器人被摧毁了。接下来将向左走的机器人血量减去1，然后继续检测栈顶机器人，直到栈为空或者来到了情况2或者情况3

2、向左走的机器人血量与向右走的机器人血量相同：

此时二者将同归于尽，此时就应该弹出栈顶机器人，然后将这两个机器人的血量都置为0

3、向左走的机器人血量比向右走的机器人血量低：

此时向左走的机器人将被摧毁，因此需要将其血量置为0，然后将栈顶机器人的血量减去1即可

遍历完成后，将血量依然大于0的机器人加入到答案中返回即可。

最后附上python代码：

```python
class Solution(object):
    def survivedRobotsHealths(self, positions, healths, directions):
        """
        :type positions: List[int]
        :type healths: List[int]
        :type directions: str
        :rtype: List[int]
        """

        stack = []
        for index, p in sorted(enumerate(positions), key=lambda d:d[1]):
            if directions[index] == 'R':
                stack.append(index)
            else:
                v = healths[index]
                while stack and healths[stack[-1]] < v:
                    v -= 1
                    healths[stack[-1]] = 0
                    stack.pop()
                
                if stack:
                    if healths[stack[-1]] == v:
                        healths[stack[-1]] = 0
                        stack.pop()
                    else:
                        healths[stack[-1]] -= 1
                    v = 0

                healths[index] = v
        
        res = []
        for v in healths:
            if v > 0:
                res.append(v)
        
        return res
```
