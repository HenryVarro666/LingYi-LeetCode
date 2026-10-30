---
title: "3609. 到达目标点的最小移动次数"
aliases: ["yiduobo的每日leetcode 3609.到达目标点的最小移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942686048019814154"
zhihu_id: "1942686048019814154"
zhihu_title: "yiduobo的每日leetcode 3609.到达目标点的最小移动次数"
question_id: "3609"
question: "到达目标点的最小移动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-reach-target-in-grid/"
difficulty: "Hard"
rating: 2419
created: "2025-08-23T20:48:19+08:00"
updated: "2025-08-23T20:48:19+08:00"
upvotes: 1
comments: 0
---

# 3609. 到达目标点的最小移动次数

> **[yiduobo的每日leetcode 3609.到达目标点的最小移动次数](https://zhuanlan.zhihu.com/p/1942686048019814154) · 知乎 · 2025-08-23 · 赞同 1**
> 力扣：[3609. 到达目标点的最小移动次数](https://leetcode.cn/problems/minimum-moves-to-reach-target-in-grid/) · Hard · 灵茶山艾府：[逆向思维 + 分类讨论，严格证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3609.到达目标点的最小移动次数

[3609. 到达目标点的最小移动次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-reach-target-in-grid/description/)

题目给出四个整数sx、sy、tx、ty，表示在一个无限大的二维网格上有两个点(sx, sy)和(tx, ty)。

现在要求以(sx, sy)为起点，移动到(tx, ty)。每次移动，可以从(x, y)移动到(x + m, y)或者(x, y + m)，其中m为x和y中的较大值。问到达(tx, ty)所需的最小移动次数，若无法到达，则返回-1。

直接从(sx, sy)开始计算后续的行动可能性非常多，在这里不妨看看能否从(tx, ty)倒推回去。

观察题目给出的移动操作，可以发现，对于当前的位置(x, y)，若x和y不同，设其中较大值为ma，较小值为mi，那么首先可以明确的是，上一轮必然是某个数加上了m，得到了ma，那么m要么是ma的一半，要么就是mi。由于m必须取上一轮的(x, y)中的较大值，因此在这里可以对于mi是否超过了ma的一半。若超过了，那么m就是mi，而ma上一轮就是ma - mi，反之，m就是ma的一半，那么ma上一轮就是ma / 2，这种情况下需要判断ma是否为偶数，若不是，则直接返回-1。

基于上面的结论，就可以从(tx, ty)向前倒推，直到tx和ty相等，或者tx小于sx或者ty小于sy为止。若此时(sx, sy)和(tx, ty)相等，那么直接返回倒推的步数即可，而如果tx小于sx或ty小于sy，则直接返回-1，否则还需要考察相等的(sx, sy)如何倒推得到(tx, ty)。

由于tx和ty相等，那么上一轮要么是(0, ty)，要么是(tx, 0)。更进一步的，由于其中有一个元素为0了，那么另一个非0元素必然经过了若干轮翻倍操作，于是可以先根据sx为0或者sy为0，来确定tx或者ty上一轮为0，然后对于另一个元素，不断除以2直到其小于等于对应的sy或者sx为止。若最终二者不相等，或者过程中遇到了奇数，那么直接返回-1，否则将一开始倒推的次数，加上除以2的操作次数，再加上1即为最终答案。这里最后的1表示的是从(0, ty)或者(tx, 0)变为(tx, ty)所需的这一次操作。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, sx, sy, tx, ty):
        """
        :type sx: int
        :type sy: int
        :type tx: int
        :type ty: int
        :rtype: int
        """
        
        res = 0
        while tx >= sx and ty >= sy and (tx != sx or ty != sy):
            if tx == ty:
                res += 1
                if sx == 0:
                    while ty > sy:
                        res += 1
                        if ty % 2 != 0:
                            return -1
                        ty //= 2

                    if ty != sy:
                        return -1

                elif sy == 0:
                    while tx > sx:
                        res += 1
                        if tx % 2 != 0:
                            return -1
                        tx //= 2

                    if tx != sx:
                        return -1
                else:
                    return -1
            
                return res
            
            elif tx > ty:
                if ty * 2 < tx:
                    if tx % 2 != 0:
                        return -1
                    tx //= 2
                else:
                    tx -= ty
                
                res += 1
            
            else:
                if tx * 2 < ty:
                    if ty % 2 != 0:
                        return -1
                    ty //= 2
                else:
                    ty -= tx
                
                res += 1
        
        if tx == sx and ty == sy:
            return res
        return -1
```
