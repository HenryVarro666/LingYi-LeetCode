---
title: "733. 图像渲染"
aliases: ["yiduobo的每日leetcode 733.图像渲染"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336274923"
zhihu_id: "336274923"
zhihu_title: "yiduobo的每日leetcode 733.图像渲染"
question_id: "733"
question: "图像渲染"
problem_url: "https://leetcode.cn/problems/flood-fill/"
created: "2020-12-11T23:16:43+08:00"
updated: "2020-12-11T23:16:43+08:00"
upvotes: 0
comments: 0
---

# 733. 图像渲染

> **[yiduobo的每日leetcode 733.图像渲染](https://zhuanlan.zhihu.com/p/336274923) · 知乎 · 2020-12-11 · 赞同 0**
> 力扣：[733. 图像渲染](https://leetcode.cn/problems/flood-fill/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

733.图像渲染

[力扣](https://leetcode-cn.com/problems/flood-fill/)

记(sr, sc)的原始颜色为orginal_color，然后从(sr, sc)开始进行bfs，每次将与当前节点相邻，且颜色等于original_color的节点加入bfs的队列中，然后将当前节点的颜色改为目标颜色即可。bfs完成后的image就是最终结果。

最后附上python代码：

```python
class Solution(object):
    def floodFill(self, image, sr, sc, newColor):
        """
        :type image: List[List[int]]
        :type sr: int
        :type sc: int
        :type newColor: int
        :rtype: List[List[int]]
        """

        original_color = image[sr][sc]
        if original_color == newColor:
            return image

        image[sr][sc] = newColor
        q = [[sr, sc]]
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        m = len(image)
        n = len(image[0])
        while l < r:
            now_x, now_y = q[l]
            l += 1
            for index in range(4):
                x = now_x + dx[index]
                y = now_y + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and image[x][y] == original_color:
                    image[x][y] = newColor
                    q.append([x, y])
                    r += 1

        return image
```
