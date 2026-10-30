---
title: "170. 两数之和III-数据结构设计"
aliases: ["yiduobo的每日leetcode 170.两数之和III-数据结构设计"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591357757"
zhihu_id: "591357757"
zhihu_title: "yiduobo的每日leetcode 170.两数之和III-数据结构设计"
question_id: "170"
question: "两数之和III-数据结构设计"
problem_url: "https://leetcode.cn/problems/two-sum-iii-data-structure-design/"
created: "2022-12-13T00:26:36+08:00"
updated: "2022-12-13T00:26:36+08:00"
upvotes: 0
comments: 0
---

# 170. 两数之和III-数据结构设计

> **[yiduobo的每日leetcode 170.两数之和III-数据结构设计](https://zhuanlan.zhihu.com/p/591357757) · 知乎 · 2022-12-13 · 赞同 0**
> 力扣：[170. 两数之和III-数据结构设计](https://leetcode.cn/problems/two-sum-iii-data-structure-design/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

170.两数之和III-数据结构设计

[力扣](https://leetcode.cn/problems/two-sum-iii-data-structure-design/)

题目是在线的模式，因此只能在每一次add时预处理出所有可能的两数之和，或者在每次find到来时通过遍历寻找是否存在两个数之和等于value。

不妨设询问的次数为q，那么上面这两种做法，前者的时间复杂度为O((n - q)^2)，而后者则为O((n - q) \* q)。对于本题的数据规模而言，必须选择后者才行。

现在确认了通过遍历寻找的做法，那么同样有两种寻找的方法，分别是利用有序性的双指针以及哈希表。如果想要维护有序性，就必须使用比较麻烦的数据结构来保证有序，因此在这里使用哈希表是更方便的做法。

对于插入操作，直接将其加入到哈希表中即可。对于查询操作，则需要遍历哈希表中的所有数number，判断value - number是否也存在于哈希表中。需要特别注意的是，当number \= value - number时，也就是想要通过两个number之和构成value时，需要判断number出现的次数是否大于等于两次，而不能只判断其是否出现在哈希表中。

最后附上python代码：

```python
class TwoSum(object):

    def __init__(self):
        self.cnt_dict = {}

    def add(self, number):
        """
        :type number: int
        :rtype: None
        """
        self.cnt_dict[number] = self.cnt_dict.get(number, 0) + 1

    def find(self, value):
        """
        :type value: int
        :rtype: bool
        """
        for number in self.cnt_dict:
            target = value - number
            if number == target:
                if self.cnt_dict[number] >= 2:
                    return True
                else:
                    continue
            elif target in self.cnt_dict:
                return True
        
        return False

# Your TwoSum object will be instantiated and called as such:
# obj = TwoSum()
# obj.add(number)
# param_2 = obj.find(value)
```
