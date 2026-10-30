---
title: "LCP 27. 黑盒光线反射"
aliases: ["yiduobo的每日leetcode LCP27.黑盒光线反射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573780665"
zhihu_id: "573780665"
zhihu_title: "yiduobo的每日leetcode LCP27.黑盒光线反射"
question_id: "LCP 27"
question: "黑盒光线反射"
created: "2022-10-15T08:33:29+08:00"
updated: "2022-10-15T08:33:29+08:00"
upvotes: 0
comments: 0
---

# LCP 27. 黑盒光线反射

> **[yiduobo的每日leetcode LCP27.黑盒光线反射](https://zhuanlan.zhihu.com/p/573780665) · 知乎 · 2022-10-15 · 赞同 0**
> 力扣：LCP 27. 黑盒光线反射

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP27.黑盒光线反射

[力扣](https://leetcode.cn/problems/IQvJ9i/)

非常复杂的题目，本身的难度并不是很大，但是有一些细节需要想清楚。

首先来分析这个黑盒中的光路的形式。可以发现，题目中的黑盒，四个角对光的反射是特殊的，因为从角反射出来的光线，direction并没有产生变化，而从边反射的光线direction是取反的。

在这里如果将盒子中的每个点视为图中的点，光路视为图中的边，那么图中一共有n + n + m + m个点，其中四个角上的点0、m、m + n以及m + n + m的度为1，其他点的度都为2。

从图的角度出发就可以断定，最终的图中一定是两条单链以及若干个环，这两条单链的顶点分别是黑盒的四个角，而不在单链上的点则构成了环。黑盒中的光，就会沿着某个方向，在单链上来回行进，或者在环上延顺时针或者逆时针方向绕圈。

根据这个结论，就可以先将这个图中的所有单链和环找出来。

为了适配光的行进方向，在这里可以将环按顺时针和逆时针拆成两份，同时将单链也按从某个端点到另一个端点的方向拆成两份。具体实现上，可以将direction为-1时光路上的节点设置为原始节点编号乘以2，将direction为1时光路上的节点设置为原始节点编号乘以2之后加1。

以图中的两个样例来说明：

对于样例一中2 \* 3的黑盒，存在一条单链0 - 6 - 4 - 2 - 8，那么可以拆分成两条光路，分别是

0 -> 6 -> 4 -> 2 -> 8以及反过来的8 -> 2 -> 4 -> 6 -> 0

接下来将光路上的节点根据光的方向进行编码，就有

0 -> 13 -> 8 -> 5 -> 17，以及17 -> 4 -> 9 -> 12 ->0

上面两条编码的光路，每个节点值除以2就是原始黑盒中的节点，而模2则是当前光路经过该节点时的方向

对于样例二中3 \* 3的黑盒，存在一个环1 - 5 - 7 - 11- 1，那么可以按照顺时针和逆时针形成光路，分别是

1 -> 5 -> 7 -> 11 -> 1以及反过来的1 -> 11 -> 7 -> 5 -> 1

同样是将光路上的节点按照光的方向进行编码，就有

2 -> 11 -> 14 -> 23 -> 2以及反过来的3 -> 22 -> 15 -> 10 -> 3

同样的，上面两条光路也满足除以2和模2的性质

这样做的好处是老板每次会规定光入射的角度，那么在这里如果提前将所有光路都预处理出来，那么在老板询问时就可以通过计算入射节点和方向的编码，通过哈希表找到其所在的光路了。

---

接下来的问题是对于一条光路，如何找到这条光路上最近的被打开的节点是什么。

在这里同样需要分链和环进行讨论。

对于一条单链而言，光最终会射入四个角落之一，如果在这个过程中没有打开的节点，那么光就是原路返回，从入射节点反射出去。

对于一条单链的光路path而言，如果从path[k]开始入射，实际上问的就是path[k + 1]到path[-1]之间下标最小的被打开过的节点是什么。

这是一个单点更新，区间查询的问题，可以通过线段树来解决。

使用线段树维护所有的光路。线段树记录两个值f和l_max，其中f表示的是区间中被打开的节点数量，而l_max则表示区间中被打开的最左侧节点的下标。那么当打开某个节点是，自顶向下递归更新f，对于当前的f[now]：

1、f[now] \= f[now \* 2 + 1] + f[now \* 2 + 2]，表示f[now]管辖区间中打开节点的数目等于其管辖的左右子区间中打开节点数目之和

2、对于l_max[now]，若f[now \* 2 + 1]大于0，说明左侧子区间中存在打开的节点，那么当前区间中被打开的最左侧节点必然位于左侧子区间中，于是有l_max[now] \= l_max[now \* 2 +1]。反过来若f[now \* 2 + 1]等于0，且f[now \* 2 + 2]大于0，说明只有右侧子区间中存在被打开的节点，于是有l_max[now] \= l_max[now \* 2 + 2]。最后，若两个条件都不满足，说明当前区间中的节点都是关闭的，此时应该置l_max[now]为空

另一方面，对于查询操作，其表现形式就应该是在区间[left, right]中查找pos右侧第一个打开的节点，那么：

1、若当前pos就等于left，说明当前区间对应的l_max[now]就是要找的答案

2、否则若pos位于左侧子区间，那么应该先递归求解左侧子区间[left, mid]，若得到的结果不为空，那么直接返回，否则答案就是右侧子区间对应的l_max，即l_max[now \* 2 + 2]

3、最后，若pos位于右侧子区间，那么直接递归求解右侧子区间[mid + 1, right]，并返回找到的答案

有了线段树的帮助，在遇到单链的光路path时，就可以在O(logn)的时间找出对应的答案了。当老板首次打开和关闭某个节点时，都需要更新线段树，需要注意的是，每个节点都会影响两条光路，所以需要更新两颗线段树。

---

上面所说的是对于单链的处理方法，接下来还需要考虑环的处理方法。

对于一个环形的光路path，如果从path[k]出发，那么其行进的路径就是

path[k] -> path[k + 1] -> ... -> path[-1] -> path[0] -> path[1] -> ... -> path[k - 1] -> path[k]

可以发现，在这里需要检查除path[k]之外光路上所有的节点是否被打开，在这里有两种处理方法。

第一种处理方法是先往后找再往前找，往后找直接沿用上面单链的做法，而往前找同样是使用线段树，不过还需要维护一个r_max用来储存下标最大的被打开的节点。

另一种处理方法则是将光路原封不动复制一份贴在后面，将

path[0] -> path[1] -> ... -> path[-1]

变成

path[0] -> path[1] -> ... ->path[-1] -> path[0] ->path[1] -> ... -> path[-1]

对于这种形式下的光路，path[k]再遇到下一个path[k]之前中间会按顺序检测需要检测的所有节点。那么在这里则可以原样照搬上面单链的处理方法。不过需要注意的是，在这种情况下，在首次打开和关闭path[k]时，线段树中的path[k]以及复制后的path[len(path) + k]都需要进行更新。再考虑到顺逆时针，每次操作就需要更新四个节点的值。

最后附上python代码：

```python
class BlackBox(object):

    def __init__(self, n, m):
        """
        :type n: int
        :type m: int
        """
        
        #coord_list记录的是盒子上各个点的下标到矩形二维下标的映射
        coord_list = []
        for index in range(m):
            coord_list.append([0, index])
        for index in range(n):
            coord_list.append([index, m])
        for index in range(m, 0, -1):
            coord_list.append([n, index])
        for index in range(n, 0, -1):
            coord_list.append([index, 0])

        #coord_map是coord_list的逆向映射
        coord_map = {}
        for index, coord in enumerate(coord_list):
            coord_map[(coord[0], coord[1])] = index
        
        #path和belong分别记录每条光路，以及每个编码后的节点位于哪条光路的第几个节点
        self.path = []
        self.belong = {}

        #get_path的作用是从编码后的节点now开始寻找光路
        def get_path(now):
            self.path.append([now])
            self.belong[now] = [len(self.path) - 1, 0]
            while True:
                direct = now % 2
                now /= 2
                x, y = coord_list[now]
                if x == 0:
                    if direct == 0:
                        #当x和direct都等于0时，表示从盒子上边往右下方向前进
                        #通过二维坐标计算最多可前进的距离dis
                        dis = min(m - y, n)
                        #dx和dy表示原始坐标x和y更新的方向
                        dx, dy = 1, 1
                    else:
                        #direct为1表示从盒子上边往左下方向前进
                        dis = min(y, n)
                        dx, dy = 1, -1
                elif y == m:
                    if direct == 0:
                        #右边往左上
                        dis = min(x, m)
                        dx, dy = -1, -1
                    else:
                        #右边往左下
                        dis = min(n - x, m)
                        dx, dy = 1, -1
                elif x == n:
                    if direct == 0:
                        #下边往左上
                        dis = min(y, n)
                        dx, dy = -1, -1
                    else:
                        #下边往右上
                        dis = min(m - y, n)
                        dx, dy = -1, 1
                else:
                    if direct == 0:
                        #左边往右下
                        dis = min(n - x, m)
                        dx, dy = 1, 1
                    else:
                        #左边往右上
                        dis = min(x, m)
                        dx, dy = -1, 1

                #计算下一个节点的坐标，然后得到其在盒子上对应的节点
                x += dis * dx
                y += dis * dy
                next = coord_map[(x, y)]
                if next == 0 or next == m or next == m + n or next == m + m + n:
                    #如果来到了一个角落上的节点，说明这是一条走到头的单链光路，更新后直接退出
                    if next == m or next == m + m + n:
                        next += next + 1
                    else:
                        next += next
                    self.path[-1].append(next)
                    break
                
                #否则对下一个节点进行编码
                elif direct == 0:
                    next += next + 1
                else:
                    next += next
                
                #若下一个编码后节点被访问过，说明这是一条走完了一遍的环形光路，直接退出
                if next in self.belong:
                    break
                #否则更新belong和path，然后继续往下走
                self.belong[next] = [len(self.path) - 1, len(self.path[-1])]
                self.path[-1].append(next)
                now = next
        
        #首先计算从四个角出发的单链光路
        get_path(0)
        get_path(m + m + 1)
        get_path(m + n + m + n)
        get_path(m + n + m + m + n + m + 1)
        #接下来计算环形光路
        for index in range((m + n) * 4):
            if index in (1, m + m, m + n + m + n + 1, m + n + m + m + n + m):
                continue
            if index not in self.belong:
                get_path(index)
        p1 = self.belong[0][0]
        p2 = self.belong[m + m + 1][0]
        p3 = self.belong[m + n + m + n][0]
        p4 = self.belong[m + n + m + m + n + m + 1][0]
        #corner_path记录单链光路在path数组中的下标
        self.corner_path = set([p1, p2, p3, p4])

        self.f = []
        self.l_max = []
        for index, p in enumerate(self.path):
            if index in self.corner_path:
                #初始化线段树需要的空间
                self.f.append([0] * (len(p) * 4))
                self.l_max.append([None] * (len(p) * 4))
            else:
                #环形光路需要双倍
                self.f.append([0] * (len(p) * 8))
                self.l_max.append([None] * (len(p) * 8))

        #open_index记录当前盒子上有哪些节点被打开了
        self.open_index = set()

    def insert(self, p, pos, delta):
        def put(now, left, right, pos, delta, f, l_max):
            f[now] += delta
            if left == right:
                if f[now] > 0:
                    l_max[now] = pos
                else:
                    l_max[now] = None
                return
            
            mid = (left + right) >> 1
            if pos <= mid:
                put(now + now + 1, left, mid, pos, delta, f, l_max)
            else:
                put(now + now + 2, mid + 1, right, pos, delta, f, l_max)
            
            if f[now + now + 1] > 0:
                l_max[now] = l_max[now + now + 1]
            elif f[now + now + 2] > 0:
                l_max[now] = l_max[now + now + 2]
            else:
                l_max[now] = None

        #单链光路只需要更新其在path中的位置
        if p in self.corner_path:
            left, right = 0, len(self.path[p]) - 1
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])
        #环形光路需要更新原始位置和复制后位置两个地方
        else:
            left, right = 0, len(self.path[p]) * 2 - 1
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])
            pos += len(self.path[p])
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])

    def query(self, p, pos):
        if p in self.corner_path:
            left, right = 0, len(self.path[p]) - 1
        else:
            left, right = 0, len(self.path[p]) * 2 - 1
        
        def get(now, left, right, pos, f, l_max):
            if left == pos:
                return l_max[now]
            
            mid = (left + right) >> 1
            if pos <= mid:
                res = get(now + now + 1, left, mid, pos, f, l_max)
                if res is None:
                    return l_max[now + now + 2]
                else:
                    return res
            else:
                return get(now + now + 2, mid + 1, right, pos, f, l_max)

        index = get(0, left, right, pos + 1, self.f[p], self.l_max[p])

        #index为空说明后续行进路线上没有被打开的节点，此时光线会原路返回
        if index is None:
            return pos
        #如果是某个复制后的节点被打开，需要将其下标还原成原数组中的下标
        elif index >= len(self.path[p]):
            return index - len(self.path[p])
        else:
            return index

    def open(self, index, direction):
        """
        :type index: int
        :type direction: int
        :rtype: int
        """
        #尚未打开则打开节点，并更新线段树
        if index not in self.open_index:
            #遍历光路的方向
            for direct in range(2):
                index_with_direct = index + index + direct
                if index_with_direct in self.belong:
                    p, pos = self.belong[index_with_direct]
                    self.insert(p, pos, 1)
                    #单链的两侧是角落节点，但角落节点只有一种表示法，所以需要借助另一侧的角落节点完成两条光路上的更新
                    if p in self.corner_path and pos == 0:
                        p, _ = self.belong[self.path[p][-1]]
                        pos = len(self.path[p]) - 1
                        self.insert(p, pos, 1)

            self.open_index.add(index)

        if direction == 1:
            index += index + 1
        else:
            index += index
        p, pos = self.belong[index]

        return self.path[p][self.query(p, pos)] / 2

    def close(self, index):
        """
        :type index: int
        :rtype: None
        """
        #关闭节点，更新线段数
        for direct in range(2):
            index_with_direct = index + index + direct
            if index_with_direct in self.belong:
                p, pos = self.belong[index_with_direct]
                self.insert(p, pos, -1)
                #单链节点两侧更新
                if p in self.corner_path and pos == 0:
                    p, _ = self.belong[self.path[p][-1]]
                    pos = len(self.path[p]) - 1
                    self.insert(p, pos, -1)
        self.open_index.remove(index)

# Your BlackBox object will be instantiated and called as such:
# obj = BlackBox(n, m)
# param_1 = obj.open(index,direction)
# obj.close(index)
```
