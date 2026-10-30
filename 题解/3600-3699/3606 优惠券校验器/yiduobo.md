---
title: "3606. 优惠券校验器"
aliases: ["yiduobo的每日leetcode 3606.优惠券校验器"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sorting", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942369824501118322"
zhihu_id: "1942369824501118322"
zhihu_title: "yiduobo的每日leetcode 3606.优惠券校验器"
question_id: "3606"
question: "优惠券校验器"
problem_url: "https://leetcode.cn/problems/coupon-code-validator/"
difficulty: "Easy"
created: "2025-08-22T23:53:55+08:00"
updated: "2025-08-22T23:53:56+08:00"
upvotes: 1
comments: 0
---

# 3606. 优惠券校验器

> **[yiduobo的每日leetcode 3606.优惠券校验器](https://zhuanlan.zhihu.com/p/1942369824501118322) · 知乎 · 2025-08-22 · 赞同 1**
> 力扣：[3606. 优惠券校验器](https://leetcode.cn/problems/coupon-code-validator/) · Easy · 灵茶山艾府：[分组 + 排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3606.优惠券校验器

[3606. 优惠券校验器 - 力扣（LeetCode）](https://leetcode.cn/problems/coupon-code-validator/description/)

题目给出三个长度为n的数组，分别描述n个优惠券的属性：code、businessLine和isActive。其中第index个优惠券具有以下属性：

code[index]：一个字符串，表示优惠券的标识符

businessLine[index]：一个字符串，表示优惠券所属的业务类别

isActive[index]：一个布尔值，表示优惠券是否当前有效

当以下所有条件都满足时，优惠券被认为是可用的：

1、code[index]不为空，且仅有大小写字母、数字以及下划线组成

2、businessLine[index]必须是以下四个类别之一："electronics"，"grocery"，"pharmacy"，"restaurant"

3、isActive[index]为true

要求返回所有可用优惠券的标识符组成的数组，按照一下规则排序：

先按照businessLine的顺序排序："electronics"，"grocery"，"pharmacy"，"restaurant"

若相同，再按照标识符的字典序排序

题目要求先筛选出可用的优惠券，然后按照指定的规则排序。那么就可以先一趟遍历，分别按照三条规则检测每张优惠券是否可用，并将可用优惠券的下标储存起来。接下来需要对其进行排序，注意到题目中businessLine的顺序刚好是按照字典序排好的，因此可以直接一businessLine为第一关键字，code为第二关键字，对可用优惠券的下标进行排序，然后将排序后的下标对应的code返回即可。

最后附上python代码：

```python
class Solution(object):
    def validateCoupons(self, code, businessLine, isActive):
        """
        :type code: List[str]
        :type businessLine: List[str]
        :type isActive: List[bool]
        :rtype: List[str]
        """
        
        def check_code(code):
            if not code:
                return False

            for c in code:
                if not (c == '_' or 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9'):
                    return False
            
            return True
        
        business_set = set(['electronics', 'grocery', 'pharmacy', 'restaurant'])
        def check_business(business):
            return business in business_set

        def check_active(is_active):
            return is_active

        active_index = []
        for index in range(len(code)):
            if check_code(code[index]) and check_business(businessLine[index]) and check_active(isActive[index]):
                active_index.append(index)

        active_index.sort(key=lambda d:(businessLine[d], code[d]))
        return [code[index] for index in active_index]
```
