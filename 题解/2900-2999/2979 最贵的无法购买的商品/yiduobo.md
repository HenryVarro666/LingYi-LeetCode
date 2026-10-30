---
title: "2979. 最贵的无法购买的商品"
aliases: ["yiduobo的每日leetcode 2979.最贵的无法购买的商品"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692230589"
zhihu_id: "692230589"
zhihu_title: "yiduobo的每日leetcode 2979.最贵的无法购买的商品"
question_id: "2979"
question: "最贵的无法购买的商品"
problem_url: "https://leetcode.cn/problems/most-expensive-item-that-can-not-be-bought/"
created: "2024-04-13T03:40:50+08:00"
updated: "2024-04-13T03:40:50+08:00"
upvotes: 1
comments: 0
---

# 2979. 最贵的无法购买的商品

> **[yiduobo的每日leetcode 2979.最贵的无法购买的商品](https://zhuanlan.zhihu.com/p/692230589) · 知乎 · 2024-04-13 · 赞同 1**
> 力扣：[2979. 最贵的无法购买的商品](https://leetcode.cn/problems/most-expensive-item-that-can-not-be-bought/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2979.最贵的无法购买的商品

[. - 力扣（LeetCode）](https://leetcode.cn/problems/most-expensive-item-that-can-not-be-bought/description/)

为了方便描述，在这里设x为primeOne，y为primeTwo，那么问题就是要求找出一个最大的v，使得ax + by \= v没有a和b同时非负的解。

这里的v就等于xy - x - y，下面给出一种比较简单的证明方法。

首先证明v + x一定是y的倍数。

根据假设，v + x可以被写成cx + dy的形式，且此时的c和d都非负。即

cd + dy \= v + x

若此时的c大于1，式子就可以写成

(c - 1) \* x + x + dy \= v + x

于是就有

(c - 1) \* x + dy \= v

这里的c - 1和d都非负，与上面不存在a和b同时非负的解这一假设产生了矛盾，因此在这里c只能等于0，也就是说dy \= v + x。

接下来，上面式子中的d一定满足d \< x，因为若d >\= x，就可以令t \= d - x，就有

dy \= (t + x) \* y \= ty + xy \= v + x

移项后就是

(y - 1)x + ty \= v

在这里又出现了一组同时非负的解(y - 1, t)，与最开始的假设矛盾，因此在这里d一定小于x。

由于d \< x，那么其最大可能的取值就是x - 1，也就是v的最大可能取值不会超过v \= (x - 1) \* y - x \= xy - x - y。另一方面，如果反过来假设cx \= v + y，得到的结论同样是v不超过xy - x - y，因此可以猜测是否这就是最终答案。那么接下来的问题就是如何证明对于ax + by \= v，当v \= xy - x - y时确实找不到一组同时非负的解。

对于v \= xy - x - y，不妨设存在一组同时非负的整数(a, b)满足ax + by \= v，即

ax + by \= xy - x - y

接下来从同余的角度来看这个问题，将带y的项合并到一起，就有

(a + 1) \* x \= (x - b - 1) \* y

由于a非负，因此等号两侧不可能为0，也就是说等号两侧都是y的倍数。由于x和y互质，那么就有a + 1 \= ky，也就是a \= ky - 1。其中的k必须为正，才能保证a非负。

将其带入回上面的式子，就有

kxy \= xy - (b + 1) \* y

移项后有

(k - 1)xy \= -(b + 1) \* y

其中等号左侧非负，右侧则必然是负数，说明不可能相等，也就是说确实不存在同时非负的(a, b)。

到了这里，先是证明的了最终答案v一定不超过xy - x - y，又证明了xy - x - y确实是无法构成的，因此xy - x - y就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def mostExpensiveItem(self, primeOne, primeTwo):
        """
        :type primeOne: int
        :type primeTwo: int
        :rtype: int
        """

        return primeOne * primeTwo - primeOne - primeTwo
```
