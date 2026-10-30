---
title: "864. 获取所有钥匙的最短路径"
aliases: ["yiduobo的每日leetcode 864.获取所有钥匙的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349827083"
zhihu_id: "349827083"
zhihu_title: "yiduobo的每日leetcode 864.获取所有钥匙的最短路径"
question_id: "864"
question: "获取所有钥匙的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-to-get-all-keys/"
created: "2021-02-09T22:03:16+08:00"
updated: "2021-02-09T22:03:16+08:00"
upvotes: 0
comments: 0
---

# 864. 获取所有钥匙的最短路径

> **[yiduobo的每日leetcode 864.获取所有钥匙的最短路径](https://zhuanlan.zhihu.com/p/349827083) · 知乎 · 2021-02-09 · 赞同 0**
> 力扣：[864. 获取所有钥匙的最短路径](https://leetcode.cn/problems/shortest-path-to-get-all-keys/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

864.获取所有钥匙的最短路径

[力扣](https://leetcode-cn.com/problems/shortest-path-to-get-all-keys/)

由于钥匙最多只有6把，因此可以使用状态压缩，即2^k来表示是否获取到第k把钥匙。配合当前坐标，就可以表示现在处于迷宫的哪个位置，手中有哪几把钥匙了。

按照上面的状态表示方法，从起点开始执行bfs的方法，向四周进行扩展：

1、若扩展到了门，那么需要检测当前状态是否包含了门对应的钥匙。只有能开门才能将扩展到的节点加入到bfs队列中。

2、若扩展到了钥匙，那么将钥匙加入到当前状态。

3、若扩展了其他普通节点，那么无需进行特殊操作。

当然，既然是使用了bfs，那么无论是碰到上面哪种情况，都需要判断对应的状态是否已经被访问过，只有没有访问过的状态才能加入到bfs队列中。

在bfs过程中，若某一时刻集齐了所有的钥匙，那么当前bfs的轮次就是最终答案，否则无解，返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def shortestPathAllKeys(self, grid):
        """
        :type grid: List[str]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        max_key = 'a'
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    start_x = i
                    start_y = j
                elif grid[i][j] != '#' and grid[i][j] != '.':
                    if grid[i][j] > max_key:
                        max_key = grid[i][j]
        
        key_num = ord(max_key) - 96
        used = [[[False] * (1 << key_num) for _ in range(n)] for _ in range(m)]
        used[start_x][start_y][0] = True
        q = [[start_x, start_y, 0]]
        l = 0
        r = 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        step = 0
        while l < r:
            step += 1
            for nowx, nowy, now_state in q[l:r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] != '#':
                        if grid[x][y] == '.' or grid[x][y] == '@':
                            if not used[x][y][now_state]:
                                q.append([x, y, now_state])
                                used[x][y][now_state] = True
                        elif grid[x][y] >= 'a' and grid[x][y] <= max_key:
                            state = now_state | (1 << (ord(grid[x][y]) - 97))
                            if state == (1 << key_num) - 1:
                                return step
                            if not used[x][y][state]:
                                q.append([x, y, state])
                                used[x][y][state] = True
                        elif (now_state & (1 << (ord(grid[x][y]) - 65))) and not used[x][y][now_state]:
                                q.append([x, y, now_state])
                                used[x][y][now_state] = True

            l, r = r, len(q)
        
        return -1
```
