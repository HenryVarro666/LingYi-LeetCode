---
title: "1707. 与数组中元素的最大异或值"
aliases: ["yiduobo的每日leetcode 1707.与数组中元素的最大异或值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449610412"
zhihu_id: "449610412"
zhihu_title: "yiduobo的每日leetcode 1707.与数组中元素的最大异或值"
question_id: "1707"
question: "与数组中元素的最大异或值"
problem_url: "https://leetcode.cn/problems/maximum-xor-with-an-element-from-array/"
created: "2021-12-24T23:57:12+08:00"
updated: "2021-12-24T23:57:12+08:00"
upvotes: 0
comments: 0
---

# 1707. 与数组中元素的最大异或值

> **[yiduobo的每日leetcode 1707.与数组中元素的最大异或值](https://zhuanlan.zhihu.com/p/449610412) · 知乎 · 2021-12-24 · 赞同 0**
> 力扣：[1707. 与数组中元素的最大异或值](https://leetcode.cn/problems/maximum-xor-with-an-element-from-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1707.与数组中元素的最大异或值

[力扣](https://leetcode-cn.com/problems/maximum-xor-with-an-element-from-array/)

首先，关于异或操作，通常是按位来进行运算。由于数组nums中的所有数以及询问中的所有x都小于等于10^9，那么首先可以将这些水转化为30位的2进制来方便进行异或运算。这里取30位的原因是2^31 \= 2147483648，那么2^30应该大于10^9，所以选30是比较合适的。

接下俩考虑异或运算的性质，只有当计算的双方该位不同时才为1，否则为0。换言之，对于一个x，如果从高位向低位进行扫描的话，应该尽量选择nums中当前位与x不同的数。

例如样例中的[0, 1, 2, 3, 4]，写成二进制表示分别是

0 0 0

0 0 1

0 1 0

0 1 1

1 0 0

方便起见这里只写了最后三位

接下来对于询问中的5，其二进制表示为101，那么从高位开始向低位扫描：

1、首先是最高位的1，此时应该选择最高位为0的数，那么4就被排除了，剩下0, 1, 2, 3

2、接下来是次高位的0，此时应该选择次高位为1的数，那么0和1就被排除了，剩下2, 3

3、最后考察最低位的1，此时应该选择最低位为0的数，那么3就被排除了，剩下2

所以最终答案就是5^2 \= 7

当然，上面这个例子是比较理想的情况，在扫描过程中不存在期望中的数也是有可能的，例如上面样例中如果没有3，仅由0, 1, 2, 4构成nums，那么对于x \= 5而言，在考察最后一步最低位的1时就只能被迫选择3

对于上面的选择过程，每次都遍历每个数字进行选择显然是不行的，复杂度太高了。注意到这里每一位上仅有0和1两种情况，且每次都是从高位向低位进行扫描的，因此在这里可以使用trie树来储存nums的二进制表示，那么对于每个x而言，就可以从trie树的根节点开始向下走，每次尽量选择与x当前位上的数相反的那条边往下走，并同步更新答案。

上面讨论的是没有nums[j] \<\= m的情况，如果有这个限制条件，在这里有两种思路。

第一种做法自然是利用离线。先将询问按照m从小到大进行排序，然后对于当前的m[index]，将nums中所有大于m[index - 1]且小于等于m[index]的值加入到trie树当中，然后计算当前x[index]在trie树中可以获得的最大异或结果即可。当然，在保证m有序的前提下，还需要保证nums也是有序的，这样才好操作大于m[index - 1]且小于等于m[index]的数。

第二种做法则是为trie树中的每个节点额外添加一个值v，表示这颗trie树中储存的nums中的最小值。那么对于trie树中的某个节点node而言，若node.v > m，那么说明node里面储存的所有数必然都大于m，因此node后面的值就没有继续往下计算的必要了。

具体实现上，可以在每次将nums中的数加入到trie树当中时顺便更新其二进制表示经过的节点，那么最终根节点的v就是nums中的最小值。对于一个询问(x, m)，若m \< root.v，说明nums中的所有数都大于m，因此可以直接返回-1，否则说明nums中至少存在一个数小于等于m，那么可以按照上面的方法从root开始向下走，至少是会存在一个可行解的。

最后附上python代码：

```python
class Node(object):
    def __init__(self, v):
        self.v = v
        self.left = self.right = None

class Solution(object):
    def maximizeXor(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        root = Node(10 ** 9 + 1)
        for num in nums:
            tmp = num
            binary = []
            while True:
                binary.append(tmp % 2)
                tmp /= 2
                if not tmp:
                    break
            
            now = root
            p = 29
            while p >= len(binary):
                if now.left is None:
                    node = Node(num)
                    now.left = node
                
                now.v = min(now.v, num)
                now = now.left
                p -= 1

            while p >= 0:
                if binary[p] == 0:
                    if now.left is None:
                        node = Node(num)
                        now.left = node
                    
                    now.v = min(now.v, num)
                    now = now.left
                else:
                    if now.right is None:
                        node = Node(num)
                        now.right = node
                    
                    now.v = min(now.v, num)
                    now = now.right
        
                p -= 1

        res = []
        for x, m in queries:
            if root.v > m:
                res.append(-1)
                continue

            tmp = x
            binary = []
            while True:
                binary.append(tmp % 2)
                tmp /= 2
                if not tmp:
                    break

            now = root
            res.append(0)
            p = 29
            while p >= len(binary):
                if now.right and now.right.v <= m:
                    now = now.right
                    res[-1] += res[-1] + 1
                else:
                    now = now.left
                    res[-1] += res[-1]
                
                p -= 1
            
            while p >= 0:
                if binary[p] == 0:
                    if now.right and now.right.v <= m:
                        now = now.right
                        res[-1] += res[-1] + 1
                    else:
                        now = now.left
                        res[-1] += res[-1]
                else:
                    if now.left and now.left.v <= m:
                        now = now.left
                        res[-1] += res[-1] + 1
                    else:
                        now = now.right
                        res[-1] += res[-1]
                
                p -= 1
        
        return res
```
