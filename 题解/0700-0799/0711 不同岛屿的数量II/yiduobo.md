---
title: "711. 不同岛屿的数量II"
aliases: ["yiduobo的每日leetcode 711.不同岛屿的数量II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604693893"
zhihu_id: "604693893"
zhihu_title: "yiduobo的每日leetcode 711.不同岛屿的数量II"
question_id: "711"
question: "不同岛屿的数量II"
problem_url: "https://leetcode.cn/problems/number-of-distinct-islands-ii/"
created: "2023-02-09T03:17:42+08:00"
updated: "2023-02-09T03:17:42+08:00"
upvotes: 0
comments: 0
---

# 711. 不同岛屿的数量II

> **[yiduobo的每日leetcode 711.不同岛屿的数量II](https://zhuanlan.zhihu.com/p/604693893) · 知乎 · 2023-02-09 · 赞同 0**
> 力扣：[711. 不同岛屿的数量II](https://leetcode.cn/problems/number-of-distinct-islands-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

711.不同岛屿的数量II

[力扣](https://leetcode.cn/problems/number-of-distinct-islands-ii/)

之前694题的升级版，不过在这里由于加入了旋转和翻转操作，所以不能直接套用694题的做法，只能老老实实想办法哈希。

具体来说，同样是先通过bfs或者dfs找出所有的连通块，接下来对于每个连通块：

1、找出这个连通块中最小的横纵坐标，记为min_x以及min_y

2、遍历连通块中的所有位置，计算其到min_x和min_y的距离。这样一来就得到了一系列的相对坐标。如果两个连通块的相对坐标相同，那么说明这两个连通块相同。另外，在这个过程中顺便统计连通块中与min_x和min_y最远的距离，分别记为h和w。

3、将这些相对坐标做成哈希表的key。我在这里采用的是直接将坐标排序，然后转化成字符串。当然也可以设计更优美高效的哈希函数。

4、接下来处理旋转的情况。根据遍历的方式，(row, col)实际上可以认为是常规坐标系上，y的负半轴上的-row以及x正半轴上的col，如果顺时针旋转90度，那么原坐标系下x正半轴就变成了新坐标系下y的负半轴，而原坐标系下y的负半轴则变成了新坐标系下x的正半轴。换言之，在这里的变换就是从(row, col)变成了(col, -row)。

为了对其坐标，在这里需要将-row修正为非负整数，因此最终的变换坐标就是(col, h - row)

接下来，对(col, h - row)进行同样的90度旋转，得到(h - row, w - col)，就是(row, col)旋转180度得到的结果了

同样的，可以得到270度的结果(w - col, row)

这样一来，常规旋转的坐标变换公式就都有了。接下来只需遍历连通块中的所有位置，计算变换后的坐标，然后形成哈希表中的key，就可以得到旋转后的连通块的key了。

最后，还需要考虑翻转的情况。对于(row, col)这个位置而言，只需考虑按一条坐标轴向一个方向翻转即可，因为其他翻转的情况可以通过翻转后选择得到。在这里不妨按x轴翻转，那么得到的坐标就是(-row, col)。接下来，将其修正为非负数，就得到了(h - row, col)。

对(h - row, col)同样90度依次旋转3次，就得到了翻转后选择的所有坐标公式，按同样的方法计算出key就行了。

这样一来，就得到了所有8种情况的8个key，在这里取一个最小的加入到key的集合中即可。

全部连通块处理完毕后，key的集合的大小即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def numDistinctIslands2(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        vis = set()
        parts_set = set()

        def encode(q):
            min_x, min_y = q[0]
            for x, y in q[1:]:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
            
            t = []
            h = w = 0
            for x, y in q:
                t.append([x - min_x, y - min_y])
                h = max(h, x - min_x)
                w = max(w, y - min_y)
            
            key = '|'.join([str(x) + ',' + str(y) for x, y in sorted(t)])

            tmp = [[y, h - x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[h - x, w - y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[w - y, x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[h - x, y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[y, x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[x, w - y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[w - y, h - x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            return key

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (i, j) not in vis:
                    vis.add((i, j))
                    q = [[i, j]]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if 0 <= x < m and 0 <= y < n and grid[x][y] == 1 and (x, y) not in vis:
                                q.append([x, y])
                                vis.add((x, y))
                                tail += 1
                    
                    key = encode(q)
                    parts_set.add(key)
        
        return len(parts_set)
```
