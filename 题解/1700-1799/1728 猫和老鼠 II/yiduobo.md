---
title: "1728. 猫和老鼠II"
aliases: ["yiduobo的每日leetcode 1728.猫和老鼠II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/topological-sort", "leetcode/queue", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/十三-图-DP", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452465656"
zhihu_id: "452465656"
zhihu_title: "yiduobo的每日leetcode 1728.猫和老鼠II"
question_id: "1728"
question: "猫和老鼠 II"
problem_url: "https://leetcode.cn/problems/cat-and-mouse-ii/"
difficulty: "Hard"
rating: 2849
created: "2022-01-01T23:19:18+08:00"
updated: "2022-01-01T23:19:18+08:00"
upvotes: 7
comments: 0
---

# 1728. 猫和老鼠II

> **[yiduobo的每日leetcode 1728.猫和老鼠II](https://zhuanlan.zhihu.com/p/452465656) · 知乎 · 2022-01-01 · 赞同 7**
> 力扣：[1728. 猫和老鼠 II](https://leetcode.cn/problems/cat-and-mouse-ii/) · Hard · 灵茶山艾府：[逆向思维 + 拓扑序 DP，复用 913 题代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1728.猫和老鼠II

[力扣](https://leetcode-cn.com/problems/cat-and-mouse-ii/)

由于地图非常小，那么可以直接用五元组(mx, my, cx, cy, m_round)来表示所有的状态，其中mx和my为老鼠当前的坐标，cx和cy为猫当前的坐标，m_round表示当前行动的是猫还是老鼠。对于所有的状态，由于这里有步数的限制，那么最终一定是可以确定每个状态时必胜态还是必败态，那么现在的目标就是计算初始状态下老鼠先行动是否必胜，不妨将这个是否必胜即为win_state，初始化为空，表示还不知道当前状态对当前操作者而言是否必胜。

对于这种胜负态之间的转移，一般的做法是先确定出所有的终局状态，然后从这些状态往前倒推。在这里一共有三种，分别是老鼠吃到了食物，猫吃到了食物以及猫逮到了老鼠：

1、对于老鼠吃到了食物，必然是老鼠最后行动了一次然后到达了食物所在地，此时轮到猫行动，老鼠的坐标为食物的坐标，因此可以将所有满足猫不在食物的位置，且老鼠在食物的位置，现在轮到猫行动的状态全部置为false，反映到代码上就是state(fx, fy, x, y, 0).win_state \= false，其中x和y表示猫当前位置，取值范围是地图中所有合法且不是食物所在的位置。

2、对于猫吃到了食物，则与上面的情况相反，即猫行动了一次之后到达了食物所在地，此时轮到老鼠行动，因此可以将所有满足老鼠不在食物的位置，且猫在食物的位置，现在轮到老鼠行动的状态全部置为false，反映到代码上就是state(x, y, fx, fy, 1).win_state \= false，其中x和y为老鼠的位置，取值范围是地图中所有合法且不是食物所在的位置。

3、对于猫逮到了老鼠，很明显老鼠不会主动往身上撞，因此只能是猫在行动了一次之后逮到了老鼠，此时轮到老鼠行动。猫可能在任何不是食物所在地的位置逮到老鼠，因此需要将所有猫和老鼠在同一位置，且不是在食物的位置，现在轮到老鼠行动的状态全部置为false，反映到代码上就是state(x, y, x, y, 1).win_state \= false，其中x和y表示猫逮到老鼠的位置，取值范围是地图中所有合法且不是食物所在的位置。

得到了上述终局状态之后，就可以通过bfs开始向前倒推。由于这里最多只能操作1000轮，因此在bfs最终只能执行1000轮。对于当前处理的状态state：

1、若该状态是一个必败状态，那么对于所有没被处理过且可以到达该状态的前置状态pre_state而言，pre_state的操作方可以通过一次操作来到state，此时操作方交换。由于state对state的操作方是一个必败的状态，换言之pre_state对pre_state的操作方来说就是必胜的，因此可以置pre_state.win_state \= true。

2、若该状态是一个必胜状态，那么对于所有没被处理过且可以到达该状态的前置状态pre_state而言，就应该避免来到state。那么对于pre_state而言，若其可以到达的状态全都是必胜态，那么pre_state.win_state \= false。具体是实现上，可以使用类似拓扑排序的做法，使用一个变量out_d记录下当前状态可以到达多少个其他的状态。根据情况1的结论，若pre_state可以到达某个必败的state，那么就可以立即确定pre_state.win_state \= true，而如果pre_state可以到达某个必胜的state，此时则需要将out_d减去1。一旦out_d变成了0，说明pre_state可以到达的全是必胜态，那么此时就有pre_state.win_state \= false。

那么此时对于所有的状态而言，只有可以立即确定必胜以及被迫确定必败的状态可以最终确定下来，而对于其中某些可以互相转移，但又无法确定必胜的状态而言，相当于在拓扑排序中出现了环，而一旦当前操作者选择跳出环，那么就会输。但是由于存在步数的限制，因此对于环中的状态，也都是老鼠输。具体实现上则无需进行额外操作，因为环上的状态都不会进入到bfs队列当中，那么当bfs自然终止之后，还不能确定胜负的状态统统都是老鼠输。也就是说在bfs结束后，若初始态不是确定是老鼠赢，那么就是老鼠输。

对于上面使用到的pre_state以及out_d，则可以在bfs开始之前先进行预处理，枚举所有合法的状态state，然后模拟当前状态操作者来进行一次操作得到next_state，就可以将state作为next_state的pre_state记录下来，并将state的out_d加上1。需要特别注意，这里猫和老鼠可以选择挂机，不要忘记了这种状态。

最后附上python代码，由于部分地方比较繁琐，所以特意加上了注释方便解读：

```python
class Node(object):

    def __init__(self, mx, my, cx, cy, m_round):
        self.mx = mx
        self.my = my
        self.cx = cx
        self.cy = cy
        self.m_round = m_round
        self.out_d = 0
        self.g = set()
        self.win_state = None

class Solution(object):
    def canMouseWin(self, grid, catJump, mouseJump):
        """
        :type grid: List[str]
        :type catJump: int
        :type mouseJump: int
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '#':
                    continue
                if grid[i][j] == 'C':
                    cx = i
                    cy = j
                elif grid[i][j] == 'M':
                    mx = i
                    my = j
                elif grid[i][j] == 'F':
                    fx = i
                    fy = j
                
        cnt = 0
        node_dict = {}
        for x1 in range(m):
            for y1 in range(n):
                if grid[x1][y1] == '#': #必须是合法单元格
                    continue
                for x2 in range(m):
                    for y2 in range(n):
                        if grid[x2][y2] == '#':
                            continue
                        if x1 == fx and y1 == fy and x2 == fx and y2 == fy: #不会同时出现在食物所在的位置
                            continue

                        if x1 == fx and y1 == fy: #老鼠在上一次操作之后到达了食物，因此只需要记录轮到猫行动的这个状态
                            node_dict[(x1, y1, x2, y2, 0)] = Node(x1, y1, x2, y2, 0)
                        elif x2 == fx and y2 == fy: #猫在上一次操作之后到达了食物，因此只需要记录轮到老鼠行动的这个状态
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
                        elif x1 == x2 and y1 == y2: #猫在上一操作之后抓到了老鼠，因此只需要记录轮到老鼠行动的这个状态
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
                        else:
                            node_dict[(x1, y1, x2, y2, 0)] = Node(x1, y1, x2, y2, 0)
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        #预处理pre_state以及out_d
        for node in node_dict.values():
            if node.mx == fx and node.my == fy: #无需考察老鼠吃到食物的下一个状态
                continue
            if node.cx == fx and node.cy == fy: #无需考察猫吃到食物的下一个状态
                continue
            if node.mx == node.cx and node.my == node.cy: #无需考察猫逮到老鼠的下一个状态
                continue

            if node.m_round == 1:
                step_range = mouseJump
                nowx, nowy = node.mx, node.my
            else:
                step_range = catJump
                nowx, nowy = node.cx, node.cy
            
            for index in range(4):
                for l in range(1, step_range + 1):
                    x = dx[index] * l + nowx
                    y = dy[index] * l + nowy

                    if x < 0 or x == m or y < 0 or y == n or grid[x][y] == '#':
                        break
                    if node.m_round == 1:
                        if x == node.cx and y == node.cy: #当前是老鼠行动，老鼠不可能走到猫所在的位置
                            continue
                        next_node = node_dict[(x, y, node.cx, node.cy, 0)]
                    else:
                        next_node = node_dict[(node.mx, node.my, x, y, 1)]
                    
                    node.out_d += 1
                    next_node.g.add(node)

            node.out_d += 1

            node_dict[(node.mx, node.my, node.cx, node.cy, 1 - node.m_round)].g.add(node)
        
        q = []
        for node in node_dict.values():
            if (node.mx == fx and node.my == fy) or (node.cx == fx and node.cy == fy) or (node.mx == node.cx and node.my == node.cy): #三种终局状态均设置为必败
                node.win_state = False
                q.append(node)
        
        l = 0
        r = len(q)
        round = 0
        while l < r and round < 1000:
            round += 1
            for node in q[l : r]:
                if not node.win_state: #当前状态必败，那么上一个状态必胜
                    for pre_node in node.g:
                        if pre_node.win_state is None:
                            pre_node.win_state = True
                            q.append(pre_node)
                else:
                    for pre_node in node.g:
                        pre_node.out_d -= 1
                        if pre_node.out_d == 0: #所有可到达的状态都是必胜，那么必败
                            pre_node.win_state = False
                            q.append(pre_node)
            
            l, r = r, len(q)
        
        if node_dict[(mx, my, cx, cy, 1)].win_state:
            return True
        
        return False
```
