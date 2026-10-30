---
title: "432. 全O(1)的数据结构"
aliases: ["yiduobo的每日leetcode 432.全O(1)的数据结构"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/196788507"
zhihu_id: "196788507"
zhihu_title: "yiduobo的每日leetcode 432.全O(1)的数据结构"
question_id: "432"
question: "全O(1)的数据结构"
problem_url: "https://leetcode.cn/problems/all-oone-data-structure/"
created: "2020-08-24T23:08:24+08:00"
updated: "2020-08-24T23:08:24+08:00"
upvotes: 0
comments: 0
---

# 432. 全O(1)的数据结构

> **[yiduobo的每日leetcode 432.全O(1)的数据结构](https://zhuanlan.zhihu.com/p/196788507) · 知乎 · 2020-08-24 · 赞同 0**
> 力扣：[432. 全O(1)的数据结构](https://leetcode.cn/problems/all-oone-data-structure/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

432.全O(1)的数据结构<https://leetcode-cn.com/problems/all-oone-data-structure/>

比较复杂度数据结构题。

首先，对于inc和dec操作，自然的想法就是使用哈希表来维护每个key的weight，哈希表操作的复杂度是O(1)的。

接下来，对于max和min操作，有两种思路。

第一种是维护当前数据结构中所有的weight以及weight出现的次数，然后在这个inc和dec时维护max_weight和min_weight。不过这里有一个致命的缺陷就是，若当前的min_weight为1，且只出现了一次，而恰好对应的key遇到dec操作时，这里的1就变成了0从数据结构中清理掉了，而此时要想找到新的min_weight则需要一趟扫描的时间，这就与O(1)时间复杂度的要求不符合了。

例如当前数据结构中，a出现5次，b出现4次，c出现1次，此时要求dec(c)。那么在c被移除后，需要重新寻找min_weight的值。由于哈希表的key并不是有序的，因此需要重新遍历哈希表中的key才能知道此时的min_weight是多少。

第二种想法则是每次遇到inc和dec操作，使用某种有序的结构维护所有key的顺序，然后max_weight和min_weight就可以通过这个有序结构的两侧来获得。注意到这里weight的变化幅度只有1，这意味着相邻的操作，于是很自然就会联想到链表。那么此时的做法就是，维护一个双向链表，初始为两个端点maxBound以及minBound，分别为左右边界。这个链表则是从左到右按weight从大到小的顺序链接住所有的key。若某个key的weight已经出现在链表中时，则将这个key链接到该weight对应节点的下方。

例如a出现5次，b出现5次，c出现4次，d出现4次，e出现3次，f出现1次，g出现1次，那么最终这个链表就是这样的：

maxBound \<-> a \<-> c \<-> e \<-> f \<-> minBound

^ ^ ^

| | |

v v v

b d g

除此之外，还需要维护key_dict和head_dict，其中key_dict[key]表示key对应的具体节点，而head_dict[weight]表示在水平方向的链表中，weight对应的节点是哪一个，例如上面的head_dict[5]就等于节点a，而head_dict[4]则是节点c。

那么此时，对于题目要求的操作而言：

1、max和min操作：可以通过maxBound.right以及minBound.left直接找到对应的答案。

2、inc操作，且key此时未出现在链表中：

此时若存在head_dict[1]，那么key对应的节点node就应该链接在head_dict[1]的后面，对应到上图中就是g节点的下方。在这里可以先通过head_dict[1].up定位到g，然后将g.next以及head_dict[1].up都指向node，同时将node.next指向head_dict[1]，node.up指向g来完成。

此时若不存在head_dict[1]，那么直接将key对应的节点node插入到minBound的左侧即可，同时需要将head_dict[1]设为node。

3、inc操作，key已经出现在链表中：

此时先通过key_dict找到key对应节点node，然后通过head_dict[node.val]找到key所在竖直链表的顶端节点head。

若node不是head，那么直接将node从竖向链表中移除。

若node恰好就是head，那么首先需要判断head.down是否还是head。

1)如果是，说明此时head这一条竖向链表中就只有head这一个节点，因此此时只需要将head.left与head.right链接，相当于将head从中移除。此时还需要从head_dict中pop掉head.val。

2)如果不是，说明head这一条竖向链表中还有别的点，那么需要将head.down推上head的位置，让head.left以及head.right链接到head.down，同时将head从竖向链表中移除。

到了这里就已经将node从原先的weight\=node.val这一支竖向链表中移除了，接下来还需要再将node插入到weight\=node.val + 1这一支竖向链表中。

在这里可以利用移除node过程中，head.left以及head.right来帮助判断。

若head.left.val等于node.val + 1，那么说明head.left正好就是node要插入的竖向链表的头部，于是直接将node链接在head.left的下方即可。

若head.left.val不等于node.val + 1，说明此时链表中不存在weight等于node.val + 1的节点，这里判断的依据是head.val \= node.val，且head.left.val > node.val + 1，而head与head.left直接相连，因此不存在val等于node.val + 1的节点。那么此时就需要将node作为node.val + 1的头部节点插入到水平方向的链表中。此时插入的位置，左侧节点显然就是head.left，而其右侧节点则可能是head.right或者head，这取决于在将node移除后head对应的竖向链表中是否还存在节点。在这里可以判断head.right.left是否等于head.left，如果等于，说明此时head对应的竖向链表中已经没有节点了，这才使得head.right的左侧就直接是head.left，于是此时node.right就应该是head.right，否则node.right应该是新的head，即head.right.left。

4、dec操作：

dec操作需要key已经出现在链表中，其操作过程与情况2类似，同样也是将key从weight\=node.val的竖向链表中移除，然后再将key插入到weight\=node.val-1的竖向链表中去。需要注意的是，当node.val\=1时，就不再需要执行插入操作了。

删除具体操作与情况2完全相同，不过对于插入操作而言各个left与right应该是完全相反的。理由是inc操作中，node.val+1是插入在原始head的左侧，而这里的dec操作，node.val-1则应该是插入到原始head的右侧。

到了这里，就可以在O(1)的时间复杂度内完成题目要求的各项操作了。

最后附上python代码：

```python
class ListNode(object):

    def __init__(self, key, val=1):
        self.left = self.right = self.up = self.down = None
        self.key = key
        self.val = val

class AllOne(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.key_dict = {}
        self.head_dict = {}
        self.maxBound = ListNode("", -1)
        self.minBound = ListNode("", -1)
        self.maxBound.right = self.minBound
        self.minBound.left = self.maxBound

    def inc(self, key):
        """
        Inserts a new key <Key> with value 1. Or increments an existing key by 1.
        :type key: str
        :rtype: None
        """

        if key not in self.key_dict:
            node = ListNode(key)
            self.key_dict[key] = node
            tmp = self.minBound.left
            if 1 not in self.head_dict:
                self.head_dict[1] = node
                tmp.right = node
                node.left = tmp
                node.right = self.minBound
                self.minBound.left = node
                node.up = node.down = node
            else:
                tmp.up.down = node
                node.up = tmp.up
                tmp.up = node
                node.down = tmp
        else:
            node = self.key_dict[key]
            head = self.head_dict[node.val]
            left = head.left
            right = head.right
            if head == node:
                if head.down == head:
                    self.head_dict.pop(node.val)
                    left.right = right
                    right.left = left
                else:
                    self.head_dict[node.val] = head.down
                    head.up.down = head.down
                    head.down.up = head.up
                    left.right = head.down
                    right.left = head.down
                    head.down.left = left
                    head.down.right = right
            else:
                node.up.down = node.down
                node.down.up = node.up

            node.val += 1

            if left.val == node.val:
                left.up.down = node
                node.up = left.up
                left.up = node
                node.down = left
                node.left = node.right = None
            else:
                left.right = node
                node.left = left
                if right.left == left:
                    right.left = node
                    node.right = right
                else:
                    right.left.left = node
                    node.right = right.left
                node.up = node.down = node
                self.head_dict[node.val] = node

    def dec(self, key):
        """
        Decrements an existing key by 1. If Key's value is 1, remove it from the data structure.
        :type key: str
        :rtype: None
        """
        if key not in self.key_dict:
            return

        node = self.key_dict[key]
        head = self.head_dict[node.val]
        left = head.left
        right = head.right
        if node == head:
            if head.down == head:
                self.head_dict.pop(node.val)
                left.right = right
                right.left = left
            else:
                self.head_dict[node.val] = head.down
                head.up.down = head.down
                head.down.up = head.up
                left.right = head.down
                right.left = head.down
                head.down.left = left
                head.down.right = right
        else:
            node.up.down = node.down
            node.down.up = node.up
        
        node.val -= 1
        if node.val == 0:
            self.key_dict.pop(key)
            return
        if right.val == node.val:
            right.up.down = node
            node.up = right.up
            right.up = node
            node.down = right
            node.left = node.right = None
        else:
            right.left = node
            node.right = right
            if left.right == right:
                left.right = node
                node.left = left
            else:
                left.right.right = node
                node.left = left.right
            node.up = node.down = node
            self.head_dict[node.val] = node

    def getMaxKey(self):
        """
        Returns one of the keys with maximal value.
        :rtype: str
        """
        return self.maxBound.right.key

    def getMinKey(self):
        """
        Returns one of the keys with Minimal value.
        :rtype: str
        """
        return self.minBound.left.key

# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()
```
