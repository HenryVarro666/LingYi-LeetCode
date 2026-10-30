---
title: "3494. 酿造药水需要的最少总时间"
aliases: ["yiduobo的每日leetcode 3494.酿造药水需要的最少总时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/math", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/数学算法", "题单/贪心算法", "题单/动态规划/十一-优化-DP", "题单/数学算法/三-概率期望", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899510872914792938"
zhihu_id: "1899510872914792938"
zhihu_title: "yiduobo的每日leetcode 3494.酿造药水需要的最少总时间"
question_id: "3494"
question: "酿造药水需要的最少总时间"
problem_url: "https://leetcode.cn/problems/find-the-minimum-amount-of-time-to-brew-potions/"
difficulty: "Medium"
rating: 2042
created: "2025-04-27T23:15:34+08:00"
updated: "2025-04-27T23:15:34+08:00"
upvotes: 0
comments: 0
---

# 3494. 酿造药水需要的最少总时间

> **[yiduobo的每日leetcode 3494.酿造药水需要的最少总时间](https://zhuanlan.zhihu.com/p/1899510872914792938) · 知乎 · 2025-04-27 · 赞同 0**
> 力扣：[3494. 酿造药水需要的最少总时间](https://leetcode.cn/problems/find-the-minimum-amount-of-time-to-brew-potions/) · Medium · 灵茶山艾府：[四种方法：正反两次扫描 / 递推 / record / 凸包+二分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3494.酿造药水需要的最少总时间

[3494. 酿造药水需要的最少总时间 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-minimum-amount-of-time-to-brew-potions/description/)

题目给出两个长度分别为n和m的整数数组skill以及mana，表示有n个巫师，需要按顺序酿造m个药水。每个药水的法力值为mana[j]，且每个药水必须依次通过所有巫师处理才能完成酿造。第i个巫师在第j个药水上处理的时间为skill[i] \* mana[j]。

另外，由于酿造过程非常精细，需要保证药水在当前巫师加工完成后立马传递给下一位巫师并开始处理，也就是说时间必须保持同步，确保每个巫师在药水到达时里面开始工作。

问酿造所有药水所需的最短时间。

按照题目的描述，可以简单概括成人可以等药水，但是药水不能等人。

第一瓶药水的制作是很简单的，从时间点0开始，每个巫师按顺序进行加工就行了。而对于后续的药水，则比较复杂。对于某个巫师，其可以开始加工的时间取决于前一名巫师加工当前药水完工的时间、自己加工上一瓶药水完工的时间，以及后续所有巫师加工上一瓶药水完工的时间。需要特别注意的是，在这里不能单单考虑后一名巫师加工上一瓶药水完工的时间，因为如果卡着下一名巫师加工上一瓶药水完工的时间将当前药水交给下一名巫师，可能出现下一名巫师加工完成后下下名巫师还没有完成上一轮的加工。也就是说，在这里应该从最后这名巫师的完工时间开始向前倒推。

具体来说，对于第一瓶药水，只需一趟遍历，计算出每名巫师完工的时间。接下来对于后续的药水，都可以先通过一趟正序遍历，根据每名巫师上一轮完工的时间以及前一名巫师在当前这一轮完工的时间计算每名巫师处理当前这瓶药水的最早完工时间。接下来，最后这名巫师处理当前药水的完工时间就是计算出来的这个最早完工时间，接下来从倒数第二名巫师开始向前倒推，对于当前巫师，其完工时间就只能是下一名巫师完工时间减去下一名巫师处理当前药水所需的时间。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, skill, mana):
        """
        :type skill: List[int]
        :type mana: List[int]
        :rtype: int
        """
        
        n = len(skill)
        f = [skill[0] * mana[0]]
        for index in range(1, n):
            f.append(f[-1] + skill[index] * mana[0])
        
        for ma in mana[1:]:
            t = f[0] + skill[0] * ma
            for index in range(1, n):
                t = max(t, f[index]) + skill[index] * ma
            
            f[-1] = t
            for index in range(n - 2, -1, -1):
                f[index] = f[index + 1] - skill[index + 1] * ma
        
        return f[-1]
```
