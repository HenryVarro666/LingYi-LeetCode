---
title: "353. 贪吃蛇"
aliases: ["yiduobo的每日leetcode 353.贪吃蛇"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597361460"
zhihu_id: "597361460"
zhihu_title: "yiduobo的每日leetcode 353.贪吃蛇"
question_id: "353"
question: "贪吃蛇"
problem_url: "https://leetcode.cn/problems/design-snake-game/"
created: "2023-01-07T21:01:18+08:00"
updated: "2023-01-07T21:01:18+08:00"
upvotes: 0
comments: 0
---

# 353. 贪吃蛇

> **[yiduobo的每日leetcode 353.贪吃蛇](https://zhuanlan.zhihu.com/p/597361460) · 知乎 · 2023-01-07 · 赞同 0**
> 力扣：[353. 贪吃蛇](https://leetcode.cn/problems/design-snake-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

353.贪吃蛇

[力扣](https://leetcode.cn/problems/design-snake-game/)

观察蛇的行动，在没有撞墙、撞自己或者吃到食物的情况下，常规的行动都是蛇尾离开所在单元格，然后蛇头来到新的单元格，恰好是符合队列先进先出的概念的，因此可以尝试使用一个队列来维护蛇现在占据的单元格。

接下来的行动，则可以通过队尾，也就是蛇头所在的单元格，配合当前的指令以及食物列表来判断将会发生什么，具体来说：

1、蛇头撞墙：

即蛇头的下一个目标单元格超出了地图边缘，此时直接返回-1

2、蛇头吃到食物：

由于题目保证食物只会出现在可到达的空地上，那么如果蛇头的下一个目标单元格是食物，就一定不会触发撞墙或者撞自己。观察题目中关于蛇吃到食物的描述，可以发现，这种情况下蛇尾并没有离开所在单元格，但是蛇头来到了食物所在的单元格，因此在这里就只需将新的蛇头位置，也就是食物所在的位置加入到队列中，而蛇尾则不应该从队列中移除。

在这里有一个小问题是如何判断下一个食物的位置。注意到题目需要返回的是每一步操作后的得分，因此需要使用一个变量来储存这个得分。又由于当前得分的数量就是已经吃到的食物的数量，因此下一个食物在食物数组中的下标恰好就是当前的得分，所以可以直接使用当前得分来得知是否还有下一个食物，以及下一个食物的位置。

这种情况下应该更新得分数，然后返回得分数。

3、蛇头撞到自己：

这种情况下，在蛇尾离开所在单元格，也就是蛇尾从队列中移除后，若新的蛇头所在的位置以及被蛇占据，那么就出发了撞到自己的操作。这种情况下应该直接返回-1。

在这里为了方便判断，可以额外使用一个哈希表储存当前队列中有哪些单元格，也就是蛇占据了哪些单元格。随着队列的变化同步维护这个哈希表，就可以高效判断蛇是否会撞到自己了。

需要特别注意的是，必须先操作蛇尾离开，再判断蛇头是否会撞到自己。

4、正常行走：

与情况3类似，此时将蛇尾从队列中移除然后将新蛇头加入到队列中即可。

这种情况下应该返回得分数。

在具体实现上，如果使用的语言不支持取队列尾，那么就需要使用双向队列或者自己手动模拟队列了。

最后附上python代码：

```python
class SnakeGame(object):

    def __init__(self, width, height, food):
        """
        :type width: int
        :type height: int
        :type food: List[List[int]]
        """
        self.w = width
        self.h = height
        self.score = 0
        self.food = food[:]
        self.used = set()
        self.used.add(0)
        self.snake = [[0, 0]]
        self.left = 0
        self.right = 1
        self.dx = {'L': 0, 'R': 0, 'U': -1, 'D': 1}
        self.dy = {'L': -1, 'R': 1, 'U': 0, 'D': 0}

    def move(self, direction):
        """
        :type direction: str
        :rtype: int
        """
        head_x, head_y = self.snake[-1]
        head_x += self.dx[direction]
        head_y += self.dy[direction]
        if head_x < 0 or head_y < 0 or head_x == self.h or head_y == self.w:
            return -1
        
        if self.score < len(self.food) and self.food[self.score][0] == head_x and self.food[self.score][1] == head_y:
            self.score += 1
            self.snake.append([head_x, head_y])
            self.right += 1
            self.used.add(head_x * self.w + head_y)
        else:
            tail_x, tail_y = self.snake[self.left]
            self.left += 1
            self.used.remove(tail_x * self.w + tail_y)
            if head_x * self.w + head_y in self.used:
                return -1
            self.snake.append([head_x, head_y])
            self.right += 1
            self.used.add(head_x * self.w + head_y)

        return self.score

# Your SnakeGame object will be instantiated and called as such:
# obj = SnakeGame(width, height, food)
# param_1 = obj.move(direction)
```
