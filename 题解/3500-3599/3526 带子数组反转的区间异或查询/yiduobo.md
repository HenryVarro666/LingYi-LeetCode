---
title: "3526. 范围异或查询与子数组反转"
aliases: ["yiduobo的每日leetcode 3526.范围异或查询与子数组反转"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "题单/常用数据结构", "题单/常用数据结构/九-伸展树-Splay-树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904672413330937852"
zhihu_id: "1904672413330937852"
zhihu_title: "yiduobo的每日leetcode 3526.范围异或查询与子数组反转"
question_id: "3526"
question: "带子数组反转的区间异或查询"
problem_url: "https://leetcode.cn/problems/range-xor-queries-with-subarray-reversals/"
difficulty: "Hard"
created: "2025-05-11T22:51:33+08:00"
updated: "2025-05-11T22:51:33+08:00"
upvotes: 0
comments: 0
---

# 3526. 范围异或查询与子数组反转

> **[yiduobo的每日leetcode 3526.范围异或查询与子数组反转](https://zhuanlan.zhihu.com/p/1904672413330937852) · 知乎 · 2025-05-11 · 赞同 0**
> 力扣：[3526. 带子数组反转的区间异或查询](https://leetcode.cn/problems/range-xor-queries-with-subarray-reversals/) · Hard · 灵茶山艾府：[Splay 模板](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3526.范围异或查询与子数组反转

[3526. 范围异或查询与子数组反转 - 力扣（LeetCode）](https://leetcode.cn/problems/range-xor-queries-with-subarray-reversals/description/)

题目给出一个长度为n的整数数组nums以及一个长度为q的二维整数数组queries，两个数组的长度都可达10^5。对于queries，其中的每个查询可能为：

1、更新操作，queries[i] \= [1, index, value]。要求将nums[index]修改为value

2、范围异或查询，queries[i] \= [2, left, right]。要求计算子数组nums[left: right + 1]之间所有元素的按位异或值

3、反转子数组，queries[i] \= [3, left, right]。原地反转子数组nums[left: right + 1]

现在要求按照顺序执行所有的查询，并返回所有异或查询的结果构成的数组。

有一种出题人无题可出了的感觉，所以随便找个高级数据结构放下来。本题如果不考虑第三种操作，就是很常规的单点查询区间求值问题，使用线段树就可以处理。但是有了第三种操作，事情就变得复杂了。

为了处理区间问题，我在这里使用的是splay。splay是一种平衡二叉树，其特点是每次操作是都要将操作的节点向上旋转至根节点，而旋转的方式与常规平衡树的旋转也略有不同。

对于需要旋转的节点，若其旋转一次就可以到达目标位置，那么就执行常规的旋转操作，否则的话就一次执行两步旋转：若其与其父亲节点、祖父节点形成的是斜链，也就是说该节点是父亲节点的左孩子，父亲节点又是祖父节点的左孩子，或者该节点是父亲节点的右孩子，父亲节点又是祖父节点的右孩子，那么就先旋转父亲节点，在旋转该节点；反之，若其与其父亲节点、祖父节点形成的是折链，那么就连续旋转该节点两次。

在splay中处理区间问题，则只需将区间两侧的节点向上旋转，例如现在需要对区间[x, y]进行，那么首先需要在树中找到第x - 1小的节点p，以及第y + 1小的节点q，接下来先将p旋转到根节点，然后将q旋转到p的右孩子，那么此时q的左子树中的节点就是区间[x, y]之间的所有节点。

对于本题中的三种操作：

1、其中修改元素值只需找到树中第index小的节点，修改其元素值，然后旋转到根节点处即可

2、对于另外两种区间操作，则可以按照上面描述的做法，将对应的p和q旋转到根部。区间中所有元素的异或值就是q的左子树中所有节点的异或值，因此在这里对于每个节点，需要额外维护子树中所有节点的异或值，记为xor。那么对于某个节点now，其对应的now.xor就应该等于now.val ^ now.left.xor ^ now.right.xor，也就是其自身的值与左右子树的异或值再计算异或。在初始化splay以及进行旋转时，都需要更新这个xor

3、对于区间翻转则比较复杂，因为不能真的去翻转整颗子树，这样时间复杂度就太高了。在这里依然可以使用懒更新的思路，对于q的左子树，只需标记其根节点q.left为需要翻转，因此在这里还需要对每个节点额外添加一个是否需要翻转的标记reversed。由于每种操作都需要自顶向下根据排名去寻找节点，那么在这个过程中如果碰到了reversed为true的节点，就应该交换该节点的左右孩子，然后将其左右孩子的reversed各自取反。

在具体实现上，为了防止查询区间左侧或右侧没有节点的情况，可以新增0号节点以及n + 1号节点，另外在向上旋转至树根时，可以新增n + 2号节点作为固定的根节点，旋转至根节点改为旋转至n + 2号节点的左孩子，方便选择操作的实现，不需要判断祖先节点是否为空。

最后附上python代码，其中第一份是按照类成员的方式写的，但是会超时。第二份使用数组实现，并且做了一些常数优化，例如在建树时尽量让其平衡，同时在两步旋转时直接按旋转后的节点关系设置旋转后的形态，而不是老老实实旋转两次：

```
class Node():
    def __init__(self, index, val, fa=None):
        self.index = index
        self.val = val
        self.fa = fa
        self.left = None
        self.right = None
        self.xor = val
        self.size = 1
        self.reversed = False
        
class Splay():
    def __init__(self, nums):
        n = len(nums)

        pre = Node(0, 0)
        for index in range(1, n + 3):
            if 1 <= index <= n:
                node = Node(index, nums[index - 1])
            else:
                node = Node(index, 0)

            pre.fa = node
            node.left = pre
            node.size = pre.size + 1
            node.xor = node.val ^ pre.xor
            pre = node

        self.root = pre
    
    def update_reverse(self, p):
        if p.reversed:
            p.left, p.right = p.right, p.left
            if p.left:
                p.left.reversed = not p.left.reversed
            if p.right:
                p.right.reversed = not p.right.reversed
            p.reversed = False

    def find(self, k):
        now = self.root
        while True:
            self.update_reverse(now)
            if now.left:
                left_size = now.left.size
            else:
                left_size = 0
            
            if left_size + 1 == k:
                break
            elif left_size >= k:
                now = now.left
            else:
                k -= left_size + 1
                now = now.right

        return now

    def left_rotate(self, p):
        fa = p.fa
        grand_fa = fa.fa

        if fa == grand_fa.left:
            grand_fa.left = p
        else:
            grand_fa.right = p
        p.fa = grand_fa

        if p.left:
            p.left.fa = fa
        fa.right = p.left
        
        fa.fa = p
        p.left = fa

    def right_rotate(self, p):
        fa = p.fa
        grand_fa = fa.fa
        if fa == grand_fa.left:
            grand_fa.left = p
        else:
            grand_fa.right = p
        p.fa = grand_fa

        if p.right:
            p.right.fa = fa
        fa.left = p.right
        
        fa.fa = p
        p.right = fa

    def update_xor_size(self, p):
        p.xor = p.val
        p.size = 1
        if p.left:
            p.xor ^= p.left.xor
            p.size += p.left.size
        if p.right:
            p.xor ^= p.right.xor
            p.size += p.right.size

    def splay_to_target(self, p, target):
        while p.fa != target:
            fa = p.fa
            grand_fa = fa.fa

            if grand_fa == target:
                if p == fa.left:
                    self.right_rotate(p)
                else:
                    self.left_rotate(p)

                self.update_xor_size(fa)
            else:
                if fa == grand_fa.left and p == fa.left:
                    self.right_rotate(fa)
                    self.right_rotate(p)
                elif fa == grand_fa.left and p == fa.right:
                    self.left_rotate(p)
                    self.right_rotate(p)
                elif fa == grand_fa.right and p == fa.left:
                    self.right_rotate(p)
                    self.left_rotate(p)
                elif fa == grand_fa.right and p == fa.right:
                    self.left_rotate(fa)
                    self.left_rotate(p)

                self.update_xor_size(grand_fa)
                self.update_xor_size(fa)
    
        self.update_xor_size(p)

    def print_nodes(self):
        print('-------------------------')
        q = deque()
        q.append(self.root)
        while q:
            now = q.popleft()
            left_id, right_id, fa_id = None, None, None
            if now.left:
                left_id = now.left.index
                q.append(now.left)
            if now.right:
                right_id = now.right.index
                q.append(now.right)
            if now.fa:
                fa_id = now.fa.index
            
            print now.index, now.val, now.xor, now.size, left_id, right_id, fa_id

    def update_value(self, index, value):
        p = self.find(index + 2)
        p.val = value
        self.splay_to_target(p, self.root)
    
    def query(self, left, right):
        p = self.find(left + 1)
        q = self.find(right + 3)
        self.splay_to_target(p, self.root)
        self.splay_to_target(q, p)
        if q.left:
            return q.left.xor
        return 0

    def reverse(self, left, right):
        p = self.find(left + 1)
        q = self.find(right + 3)
        self.splay_to_target(p, self.root)
        self.splay_to_target(q, p)
        if q.left:
            q.left.reversed = not q.left.reversed

class Solution(object):
    def getResults(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        splay = Splay(nums)
        res = []
        for q in queries:
            if q[0] == 1:
                splay.update_value(q[1], q[2])
            elif q[0] == 2:
                res.append(splay.query(q[1], q[2]))
            else:
                splay.reverse(q[1], q[2])
                
        return res
```

```python
class Solution(object):
    def getResults(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(nums)
        fa = [n + 2] * (n + 3)
        childs = [[n + 2] * 2 for _ in range(n + 3)]
        val = [0] * (n + 3)
        xor = [0] * (n + 3)
        size = [0] * (n + 3)
        reverse = [0] * (n + 3)

        def build(left, right):
            mid = (left + right) >> 1
            if 1 <= mid <= n:
                val[mid] = nums[mid - 1]
                xor[mid] = val[mid]
            size[mid] = 1
            
            if left < mid:
                childs[mid][0] = build(left, mid - 1)
                fa[childs[mid][0]] = mid
                size[mid] += size[childs[mid][0]]
                xor[mid] ^= xor[childs[mid][0]]
            
            if mid < right:
                childs[mid][1] = build(mid + 1, right)
                fa[childs[mid][1]] = mid
                size[mid] += size[childs[mid][1]]
                xor[mid] ^= xor[childs[mid][1]]
            
            return mid
            
        def find(k):
            now = childs[n + 2][0]
            while True:
                if reverse[now]:
                    childs[now].reverse()
                    reverse[childs[now][0]] ^= 1
                    reverse[childs[now][1]] ^= 1
                    reverse[now] = 0
            
                left_size = size[childs[now][0]] + 1
                if left_size == k:
                    return now
                if left_size > k:
                    now = childs[now][0]
                else:
                    k -= left_size
                    now = childs[now][1]
            
            return now

        def update_value(now):
            xor[now] = val[now]
            size[now] = 1
            for index in range(2):
                xor[now] ^= xor[childs[now][index]]
                size[now] += size[childs[now][index]]

        def splay(now, target):
            while fa[now] != target:
                f = fa[now]
                gf = fa[f]
                if now == childs[f][0]:
                    side = 0
                else:
                    side = 1

                if gf == target:
                    if f == childs[gf][0]:
                        childs[gf][0] = now
                    else:
                        childs[gf][1] = now
                    fa[now] = gf

                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]

                    fa[b] = f
                    childs[f][side] = b

                    fa[f] = now
                    childs[now][side ^ 1] = f

                    size[f] = 1 + size[b] + size[c]
                    xor[f] = val[f] ^ xor[b] ^ xor[c]

                    break

                if (childs[gf][0] == f and childs[f][0] == now) or (childs[gf][1] == f and childs[f][1] == now):
                    ggf = fa[gf]
                    if gf == childs[ggf][0]:
                        childs[ggf][0] = now
                    else:
                        childs[ggf][1] = now
                    fa[now] = ggf

                    a = childs[now][side]
                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]
                    d = childs[gf][side ^ 1]

                    fa[c] = gf
                    childs[gf][side] = c
                    size[gf] = 1 + size[c] + size[d]
                    xor[gf] = val[gf] ^ xor[c] ^ xor[d]

                    fa[b] = f
                    fa[gf] = f
                    childs[f][side] = b
                    childs[f][side ^ 1] = gf
                    size[f] = 1 + size[b] + size[gf]
                    xor[f] = val[f] ^ xor[b] ^ xor[gf]

                    fa[f] = now
                    childs[now][side ^ 1] = f
                
                else:
                    ggf = fa[gf]
                    if gf == childs[ggf][0]:
                        childs[ggf][0] = now
                    else:
                        childs[ggf][1] = now
                    fa[now] = ggf

                    a = childs[now][side]
                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]
                    d = childs[gf][side]

                    fa[a] = gf
                    childs[gf][side ^ 1] = a
                    size[gf] = 1 + size[a] + size[d]
                    xor[gf] = val[gf] ^ xor[a] ^ xor[d]

                    fa[b] = f
                    childs[f][side] = b
                    size[f] = 1 + size[b] + size[c]
                    xor[f] = val[f] ^ xor[b] ^ xor[c]

                    fa[f] = now
                    fa[gf] = now
                    childs[now][side] = gf
                    childs[now][side ^ 1] = f

            update_value(now)
                
        childs[-1][0] = build(0, n + 1)
        fa[childs[-1][0]] = n + 2

        res = []
        for q in queries:
            if q[0] == 1:
                now = find(q[1] + 2)
                val[now] = q[2]
                splay(now, n + 2)
            else:
                x = find(q[1] + 1)
                y = find(q[2] + 3)
                splay(x, n + 2)
                splay(y, x)
                
                if q[0] == 2:
                    if childs[y][0]:
                        res.append(xor[childs[y][0]])
                    else:
                        res.append(0)
                else:
                    if childs[y][0]:
                        reverse[childs[y][0]] ^= 1

        return res
```
