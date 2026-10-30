---
title: "3245. 交替组III"
aliases: ["yiduobo的每日leetcode 3245.交替组III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721367341"
zhihu_id: "721367341"
zhihu_title: "yiduobo的每日leetcode 3245.交替组III"
question_id: "3245"
question: "交替组 III"
problem_url: "https://leetcode.cn/problems/alternating-groups-iii/"
difficulty: "Hard"
rating: 3112
created: "2024-09-22T02:35:09+08:00"
updated: "2024-09-22T02:35:09+08:00"
upvotes: 2
comments: 0
---

# 3245. 交替组III

> **[yiduobo的每日leetcode 3245.交替组III](https://zhuanlan.zhihu.com/p/721367341) · 知乎 · 2024-09-22 · 赞同 2**
> 力扣：[3245. 交替组 III](https://leetcode.cn/problems/alternating-groups-iii/) · Hard · 灵茶山艾府：[从易到难，一步步推导（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3245.交替组III

[. - 力扣（LeetCode）](https://leetcode.cn/problems/alternating-groups-iii/description/)

之前3208题的超级加强版，数据规模增大的前提下，还把单次询问变成了多次询问，处理方法也完全不同了。

先回顾一下题意。

给出一个整数数组colors，表示一个由红色和蓝色瓷砖组成的环，其中第i块瓷砖的颜色为colors[i]，若colors[i]为0表示这是一块红色的瓷砖，若为1则表示这是一块蓝色的瓷砖。如果环中有连续若干块瓷砖的颜色是交替颜色，即这一组瓷砖中，除了第一块和最后一块瓷砖外，其他的瓷砖与左右相邻瓷砖的颜色都不同，那么就称这一组瓷砖为一个交替组。

接下来给出若干组询问queries，包含两种类型。若queries\[i\] \= \[1, size\[i\]\]，需要计算当前的环中有多少个大小为size\[i\]的交替组；若queries\[i\] \= \[2, index\[i\], color\[i\]\]，那么就需要将colors\[index\[i\]\]修改称color\[i\]。

---

题目需要实现的东西比较复杂，不妨先从简单的状况开始考虑。

首先考虑如何处理非环状态下的静态查询。由于是多组查询，那么每次查询的时间复杂度必须是O(1)或者O(logn)的，因此每次都用滑动窗口来计算的做法可以直接排除掉。

另一种想法就是先把每种不同长度的交替组的数量先计算好，然后每次询问时只需查询就行了。具体来说，对于一段长度为m的交替组，其中可以提取出m个长度为1的交替组，m - 1个长度为2的交替组（这里补充一下，题目规定了需要求解的交替组的长度必须大于等于3，但是这里依然考虑长度为1和2的交替组并不会影响后续的计算），m - 2个长度为3的交替组，...，m - k + 1个长度为k的交替组，以此类推。

若需要查询有多个长度为k的交替组，不妨设当前的环按尽量长的原则划分成了若干个子段，那么其中长度小于k的子段可以直接忽略，而对于长度大于等于k的子段，则可以设这些子段的长度分别为m[0]、m[1]、...、m[t]，那么其中m[i]这一段可以提供m[i] - k + 1个长度为k的交替组，综合起来一共就可以提供

(m[0] - k + 1) + (m[1] - k + 1) + ... + (m[t] - k + 1) \= (m[0] + m[1] + ... + m[t]) - (k - 1) \* (t + 1)

可以发现，在这里只需要知道所有长度大于等于k的的子段的长度之和以及这些子段的数量，就可以高效计算出当前有多少个长度为k的交替组。而对于数组中大于等于k的数的和以及数量这个问题，是非常适合适用树状数组求解的。于是只需先对colors进行一趟遍历，按尽量长的标准将colors分割成若干个子段，将每个子段的长度加入到树状数组中即可。

---

接下来需要考虑的就是在环上进行分割的具体实现。

本题中给出的是一个环，对于环上的问题主要是首尾这一段的处理比较麻烦。一种场景的处理方法是将colors复制一份后接在后面，这样一来就有变成线性的问题的，不过对于本题而言，感觉还是要不停地判断可行的起点是否越界，并没有发挥出这种处理方法的优势。

注意到本题中的瓷砖是一定都会被记录下来的，因此我在这里选择的是标记法。具体来说，就是标记每一块与其上一块瓷砖同色的瓷砖，其中下标0的瓷砖的上一块为下标n - 1的瓷砖。这样一来，从某一块被标记的瓷砖开始，到下一块被标记的瓷砖的前一块瓷砖结束，这就是一个尽量长的分割的子段，其长度就是两侧被标记瓷砖下标之差。

例如样例2中，下标为1和5的瓷砖将被标记，那么从1到5的前一块瓷砖，也就是1到4的这一段是第一个子段，其长度为5 - 1 \= 4；从5到1的前一块瓷砖，也就是5到0的这一段是第二个字段，其长度为1 + 6 - 5 \= 2，这里加上6是因为跨过了0点。

这样一来，只需要一趟遍历进行标记，然后利用上一次标记的下标与当前标记的下标之差，就可以计算出上一个分割的子段的长度是多少了。

需要特别注意的是，这种标记法有两种特殊情况。第一种是没有任何瓷砖被标记，此时从任意瓷砖开始都可以得到长度为k的交替组，因此无论询问的k是多少，对应的答案都为n，而不能使用之前讨论的非环状态下的方法来计算。第二种情况则是仅有一块瓷砖被标记，此时可以认为是仅存在一个长度为n的子段，当然也可以认为这块被标记的瓷砖的下一块被标记瓷砖也是它自己，这样一来得到的结论不变。

---

接下来需要考虑的则是如何进行修改。

首先如果修改后的颜色与修改前的颜色相同，那么可以直接跳过。

接下来讨论需要修改的情况。不妨设当前修改颜色的瓷砖下标为y，那么其前一块瓷砖的下标x \= (y - 1 + n) % n，而下一块瓷砖的下标z \= (y + 1) % n。此时可以发现，根据x、y、z本身的色号可以判断出y或者z是否需要被标记，因此在这里就需要找到y左侧最近的被标记瓷砖，已经z右侧最近的被标记瓷砖。在这里先记这两块瓷砖的下标分别为pre和nxt，具体的计算方法后面再讨论。需要注意的是，这里的pre和nxt有可能为空，此时对应的是整个环内不存在任何被标记瓷砖，否则的话一定可以找到pre和nxt。

接下来就x、y、z的颜色进行讨论：

1、当colors[x] \= colors[y] \= colors[z]时：

在修改之前，y和z都是被标记的瓷砖，而在修改后，y和z都不再是被标记的瓷砖。接下来又有两种情况：

1-1）若此时的nxt等于y，即z的下一块被标记瓷砖就是y，说明z到y的前一块瓷砖，也就是z到x形成了一个子段，其长度为n - 1，另外y自身形成的长度为1的孤立子段。在修改后，整个环中将不再存在被标记的瓷砖，也就是说此时变成了之前的讨论的整个环内不存在任何被标记瓷砖的特殊情况。这种情况下，修改后将使得长度为n - 1的子段数量以及长度为1的子段数量都将减少1个，需要修改树状数组。另外将形成特殊的整环，关于特殊整环的判断也在后面再讨论。

1-2）若此时的nxt不等于y，那么在修改之前，存在pre到y的前一块瓷砖，孤立的y，以及z到nxt的前一块瓷砖这三个子段，对应的长度分别为(y + n - pre) % n、1、以及(nxt + n - z) % n，这里的加n模n的写法是为了避免跨过0点的情况。在修改后，这两段将被合并为一段，子段的起点为pre，终点为nxt的前一块瓷砖，而这个子段的长度为(nxt + n - 1 - pre) % n + 1，这里的先加n - 1，模n后再加1的写法是为了避免跨过0点以及pre和nxt重合的情况。同样的，此时需要根据这些子段的长度修改树状数组。

2、当colors[x] \= colors[y]，但colors[y] !\= colors[z]时：

在修改之前，y是被标记的瓷砖，而在修改后，y不再是被标记的瓷砖，但是z将变为被标记的瓷砖。接下来同样有两种情况：

2-1）若此时的nxt等于y，即z的下一块被标记瓷砖就是y。需要注意的时，此时z并不是被标记瓷砖，也就是说这里是从y开始，到y的前一块瓷砖形成了一个子段，即y是唯一一块被标记瓷砖。而在修改后，z将变为唯一一块被标记瓷砖，相当于把盘子转了一下，但是对交替组的数量不会产生任何影响，因此可以直接跳过这种情况。

2-2）若此时的nxt不等于y，那么在修改之前，存在pre到y的前一块瓷砖，以及y到nxt的前一块瓷砖这两个子段，对应的长度分别为(y + n - pre) % n、以及(nxt + n - y) % n。在修改后，前面这一段的终点向后移动到了z的前一块瓷砖，而后一段的起点也向后移动到了z，对应的长度则分别为(z + n - pre) % n、以及(nxt + n - z) % n，修改树状数组中对应的长度即可。

3、当colors[x] !\= colors[y]，但colors[y] \= colors[z]时：

在修改之前，z是被标记的瓷砖，而在修改后，y将变为被标记的瓷砖，而z不再是被标记的瓷砖。此时依然是两种情况：

3-1）若此时的nxt等于z，这种情况与2-1）类似，即z的下一块标记瓷砖就是z。此时从z开始，到z的前一块瓷砖形成了一个字段，即z是唯一一块被标记瓷砖。而在修改后，y将变成唯一一块被标记瓷砖，因此同样可以直接跳过这种情况。

3-2）若此时的nxt不等于z，那么在修改之前，存在pre到z的前一块瓷砖，以及z到nxt的前一块瓷砖这两个子段，对应的长度分别为(z + n - pre) % n、以及(nxt + n - z) % n。在修改后，前面这一段的终点向前移动到了y的前一块瓷砖，而后一段的起点也向前移动到了y，对应的长度则分别为(y + n - pre) % n、以及(nxt + n - y) % n，修改树状数组中对应的长度即可。

4、当colors[x] !\= colors[y]，且colors[y] !\= colors[z]时：

在修改之前，y和z都不是被标记的瓷砖，而在修改后，y和z都将变成被标记的瓷砖。此时依然是两种情况：

4-1）若在修改前是特殊的整环，那么在修改后将形成z到y的前一块瓷砖的一个子段，以及孤立的y，也就是形成一个长度为n - 1以及长度为1的子段，修改树状数组中对应的长度即可。

4-2）若在修改前不是特殊的正环，那么在修改前这是从pre到nxt前一块瓷砖形成的一个字段，其长度为(nxt + n - 1 - pre) % n + 1，而在修改后，将从中断开，形成从pre到y的前一块瓷砖、孤立的y、以及z到nxt的前一块瓷砖这三段，对应的长度分别为(y + n - pre) % n、1、以及(nxt + n - z) % n，修改树状数组中对应的长度即可。

---

到了这里，还有一个问题需要解决：如何高效的求解每块被标记瓷砖的前一块被标记瓷砖pre以及后一块被标记瓷砖nxt。对于这个问题，王道做法自然是用平衡二叉树维护被标记瓷砖的下标，对于pre和nxt的求解直接在树中查询就行了。

我在这里采用的是线段树，使用两个数组left和right分别表示区间中最左侧被标记瓷砖的下标以及最右侧被标记瓷砖的下标。那么对于某个区间[start, end]，若start \= end，说明这是单点，可以直接根据对应的colors的状态进行判断；若start \< end，此时可以考察其左半区间[start, mid]对应的left，若左半区间的left非空，那么该区间对应的left就是左半区间的left，否则就是右半区间对应的left，对于right的求解则是完全对称。

对于每次修改操作，就是标准的线段树中的单点修改。

可以发现，若没有任何瓷砖被标记，那么树中所有的left和right都为空，也就是说可以通过根节点对应的left是否为空来判断当前是否为特殊的整环。

最后是对于pre以及nxt的查询的具体处理方法。

首先是查询y的左侧最近的被标记瓷砖。若y > 0，那么就应该先查询0到y - 1之间最右侧的被标记瓷砖，若找不到，那么就应该经过零点回到环的尾部，此时对应的就是整个环中最右侧的被标记瓷砖。

接下来是查询z的右侧最近的被标记瓷砖。若z + 1 \< n，那么就应该先查询z + 1到n - 1之间最左侧的被标记瓷砖，若找不到，那么就应该经过n - 1来到环的头部，此时对应的就是整个环中最左侧的被标记瓷砖。

---

到了这里，就得到了完整的算法。

首先初始化线段树和树状数组，接下来先对colors进行一趟遍历，对其中的瓷砖进行标记，在标记瓷砖的同时一边通过被标记瓷砖的下标更新线段树，一边通过标记点之间的距离计算子段的长度更新树状数组。在这里需要留意如果有任意瓷砖被标记，那么在遍历完成后需要记得将最右侧的标记瓷砖到最左侧的标记瓷砖之间这一段的长度加入到树状数组中。

接下来遍历queries，对于查询操作，若此时环处于特殊状态，即根节点对应的left为空，那么此次查询对应的答案就为n，否则就通过树状数组计算对应的答案。对于修改操作，若修改前后颜色相同，则直接跳过，否则根据上面的讨论先计算x、y、z以及对应的pre和nxt，然后根据x、y、z的颜色对应到4种情况中的一种，计算修改前后的子段长度变化并更新树状数组，最后更新线段树中对应的点以及颜色数组即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfAlternatingGroups(self, colors, queries):
        """
        :type colors: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(colors)
        f = [0] * (n + 1)
        g = [0] * (n + 1)

        left = [None] * (n * 4)
        right = [None] * (n * 4)

        def add(v, sign):
            delta = v * sign
            v = n - v + 1
            while v <= n:
                f[v] += delta
                g[v] += sign
                v += v & -v
        
        def get(v):
            s = 0
            cnt = 0
            delta = v - 1
            v = n - v + 1
            while v > 0:
                s += f[v]
                cnt += g[v]
                v -= v & -v

            return s - delta * cnt

        def update(now, start, end, index):
            if start == end:
                if left[now] is None:
                    left[now] = index
                    right[now] = index
                else:
                    left[now] = None
                    right[now] = None
            else:
                mid = (start + end) // 2
                if index <= mid:
                    update(now + now + 1, start, mid, index)
                else:
                    update(now + now + 2, mid + 1, end, index)
                
                if left[now + now + 1] is None:
                    left[now] = left[now + now + 2]
                else:
                    left[now] = left[now + now + 1]
                
                if right[now + now + 2] is None:
                    right[now] = right[now + now + 1]
                else:
                    right[now] = right[now + now + 2]

        def find(now, start, end, ts, te, arr, left_flag):
            if start == ts and end == te:
                return arr[now]
            
            mid = (start + end) // 2
            if te <= mid:
                return find(now + now + 1, start, mid, ts, te, arr, left_flag)
            elif ts > mid:
                return find(now + now + 2, mid + 1, end, ts, te, arr, left_flag)
            else:
                if left_flag:
                    v = find(now + now + 1, start, mid, ts, mid, arr, left_flag)
                else:
                    v = find(now + now + 2, mid + 1, end, mid + 1, te, arr, left_flag)
                
                if v is not None:
                    return v

                if left_flag:
                    return find(now + now + 2, mid + 1, end, mid + 1, te, arr, left_flag)
                else:
                    return find(now + now + 1, start, mid, ts, mid, arr, left_flag)

        pre = None
        for index in range(n):
            if colors[index] == colors[(index - 1 + n) % n]:
                if pre is not None:
                    length = index - pre
                    add(length, 1)

                pre = index
                update(0, 0, n - 1, index)
        
        if left[0] is not None:
            add(left[0] + n - right[0], 1)
        
        res = []
        for q in queries:
            if q[0] == 1:
                if left[0] is None:
                    res.append(n)
                else:
                    res.append(get(q[1]))
            else:
                if colors[q[1]] == q[2]:
                    continue
                
                x = (q[1] - 1 + n) % n
                y = q[1]
                z = (q[1] + 1) % n

                pre = None
                if y > 0:
                    pre = find(0, 0, n - 1, 0, y - 1, right, False)
                if pre is None:
                    pre = right[0]

                nxt = None
                if z + 1 < n:
                    nxt = find(0, 0, n - 1, z + 1, n - 1, left, True)
                if nxt is None:
                    nxt = left[0]

                if colors[x] == colors[y] and colors[y] == colors[z]:
                    if nxt == y:
                        add(n - 1, -1)
                        add(1, -1)
                    else:
                        add((y + n - pre) % n, -1)
                        add(1, -1)
                        add((nxt + n - z) % n, -1)
                        add((nxt + n - 1 - pre) % n + 1 , 1)
                elif colors[x] == colors[y]:
                    if nxt == y:
                        pass
                    else:
                        add((y + n - pre) % n, -1)
                        add((nxt + n - y) % n, -1)
                        add((z + n - pre) % n, 1)
                        add((nxt + n - z) % n, 1)
                elif colors[y] == colors[z]:
                    if nxt == z:
                        pass
                    else:
                        add((z + n - pre) % n, -1)
                        add((nxt + n - z) % n, -1)
                        add((y + n - pre) % n, 1)
                        add((nxt + n - y) % n, 1)
                else:
                    if left[0] is None:
                        add(n - 1, 1)
                        add(1, 1)
                    else:
                        add((nxt + n - 1 - pre) % n + 1, -1)
                        add((y + n - pre) % n, 1)
                        add(1, 1)
                        add((nxt + n - z) % n, 1)

                update(0, 0, n - 1, y)
                update(0, 0, n - 1, z)
                colors[q[1]] = q[2]

        return res
```
