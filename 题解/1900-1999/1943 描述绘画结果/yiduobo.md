---
title: "1943. 描述绘画结果"
aliases: ["yiduobo的每日leetcode 1943.描述绘画结果"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/sweep-line", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/489873575"
zhihu_id: "489873575"
zhihu_title: "yiduobo的每日leetcode 1943.描述绘画结果"
question_id: "1943"
question: "描述绘画结果"
problem_url: "https://leetcode.cn/problems/describe-the-painting/"
difficulty: "Medium"
rating: 1969
created: "2022-03-29T22:19:14+08:00"
updated: "2022-03-29T22:19:14+08:00"
upvotes: 0
comments: 0
---

# 1943. 描述绘画结果

> **[yiduobo的每日leetcode 1943.描述绘画结果](https://zhuanlan.zhihu.com/p/489873575) · 知乎 · 2022-03-29 · 赞同 0**
> 力扣：[1943. 描述绘画结果](https://leetcode.cn/problems/describe-the-painting/) · Medium · 灵茶山艾府：[事件扫描线](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1943.描述绘画结果

[力扣](https://leetcode-cn.com/problems/describe-the-painting/)

经典的差分数组问题，将每个线段视作起点和终点加入差分数组中。对于起点start，在差分数组中start的位置加上color；对于终点end，则在end的位置减去color。

一般情况下，需要从0开始枚举线段上的每一个点，并使用差分数组来更新当前点的颜色。对于本题，则可以只枚举线段的起点和终点，因为是有线段的起点和终点会影响到最终的结果。

因此在具体实现上，不需要使用差分数组来保存这些点，而是直接将这些点在数轴上的下标和对应的颜色保存起来，然后从小到大排序，接下来一趟遍历。在遍历的过程中，还需要几个变量now、last以及start，分别表示当前颜色now，上一个线段的颜色last以及上一个线段的起点start。

对于当前遍历到的点p，首先可能存在若干个点在数轴上的位置与p在数轴上的位置相同，因此需要先向后合并同一位置的点。具体来说就是对于p和p + 1在数轴上的位置是否相同，若相同，那么就需要额外将p + 1的颜色也更新到now中，然后将p向后移动到p + 1。重复此过程直到p到达末尾或者p和p + 1在数轴上的位置不同。除此之外，还需要将p的颜色也更新到now中。

根据按照题目样例3的意思，即使最终颜色相同，但如果是由不同线段混合带来的，那也视为不同的线段。由于题目中线段的颜色都大于0，也就是说只要遇到了线段的起点和终点，上一条线段就必然结束了。于是此时只需要满足last > 0，那么就说明从start到p在数轴上的位置这一段是一条有颜色的线段，需要将其加入到答案中，其颜色就是last，并更新last为now，start为p在数轴上的位置。

全部遍历完成后，不要忘记将最后这一条线段也加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def splitPainting(self, segments):
        """
        :type segments: List[List[int]]
        :rtype: List[List[int]]
        """

        points = []
        for start, end, color in segments:
            points.append([start, color])
            points.append([end, -color])
        
        points = sorted(points, key=lambda d:d[0])

        now = 0
        last = 0
        start = None
        p = 0
        res = []
        while p < len(points):
            while p + 1 < len(points) and points[p][0] == points[p + 1][0]:
                now += points[p][1]
                p += 1
            
            now += points[p][1]
            if start is not None and last > 0:
                res.append([start, points[p][0], last])
            last = now
            start = points[p][0]
            
            p += 1
        
        if start < points[p - 1][0] and last > 0:
            res.append([start, points[p - 1][0], last])
        return res
```
