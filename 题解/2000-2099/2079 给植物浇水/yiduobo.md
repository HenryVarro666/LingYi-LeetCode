---
title: "2079. 给植物浇水"
aliases: ["yiduobo的每日leetcode 2079.给植物浇水"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/517497442"
zhihu_id: "517497442"
zhihu_title: "yiduobo的每日leetcode 2079.给植物浇水"
question_id: "2079"
question: "给植物浇水"
problem_url: "https://leetcode.cn/problems/watering-plants/"
difficulty: "Medium"
created: "2022-05-20T16:48:18+08:00"
updated: "2022-05-20T16:48:18+08:00"
upvotes: 0
comments: 0
---

# 2079. 给植物浇水

> **[yiduobo的每日leetcode 2079.给植物浇水](https://zhuanlan.zhihu.com/p/517497442) · 知乎 · 2022-05-20 · 赞同 0**
> 力扣：[2079. 给植物浇水](https://leetcode.cn/problems/watering-plants/) · Medium · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2079.给植物浇水

[力扣](https://leetcode.cn/problems/watering-plants/)

题目给出了明确的浇水规则，可以发现，每一轮从河边走到花园的下标取决于当前的水量可以满足哪些植物，于是可以枚举每一株植物。对于当前的植物plants[index]，如果当前剩余的水量不能满足该植物，那么这一轮浇水的路径就是从河边走到plants[index - 1]，然后再返回河边打水，一共走了index + index的路程，使用这个值更新答案即可。

对于上面这种计算方式，最后一次浇水的路径是必然不会被记录的，因此在遍历完成后还需要将答案额外加上n，表示最后这一轮浇水的路程。

最后附上python代码：

```python
class Solution(object):
    def wateringPlants(self, plants, capacity):
        """
        :type plants: List[int]
        :type capacity: int
        :rtype: int
        """

        now = 0
        res = 0
        for index in range(len(plants)):
            if now + plants[index] > capacity:
                res += index + index
                now = 0
            
            now += plants[index]
        
        res += len(plants)
        return res
```
