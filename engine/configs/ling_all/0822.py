CONFIG = dict(
    num=822, title='翻转卡片游戏', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='哈希集合 · 排除正反相同的数',
    code='''
class Solution:
    def flipgame(self, fronts: List[int], backs: List[int]) -> int:
        forbidden = {x for x, y in zip(fronts, backs) if x == y}
        return min((x for x in fronts + backs if x not in forbidden), default=0)
''',
    call='Solution().flipgame([1,2,4,4,7], [1,3,4,1,3])',
    expect=2,
    views=[
        dict(type='array', var='fronts', h=150, label='fronts（正面）',
             color=lambda S, i, v: 'red' if 'forbidden' in S and S['backs'][i] == v else None),
        dict(type='array', var='backs', h=150, label='backs（背面）',
             color=lambda S, i, v: 'red' if 'forbidden' in S and S['fronts'][i] == v else None),
        dict(type='set', var='forbidden', h=130, label='forbidden（正反相同，不可能当答案）'),
        dict(type='text', fn=lambda S: '红色 = 这张卡两面一样；其余数字都能翻到背面当答案' if 'forbidden' in S else '', size=28, h=60),
    ],
    watch=[('forbidden', 'forbidden', 'red')],
    captions={
        'forbidden = ': '正反两面相同的卡：这个数无论怎么翻，正面都有它 → 不可能是答案。`forbidden = {forbidden}`',
        'return min': lambda S, B, r: f'在 `fronts + backs` 里找不在 `forbidden` 的最小值 → ==`{r}`==（都被排除则返回默认值 0）',
    },
    cards=dict(
        after=[dict(heading='为什么两面相同才排除', lines=[
            '示例：`fronts=[1,2,4,4,7]`，`backs=[1,3,4,1,3]`',
            '第 0、2 张两面相同 → `1`、`4` 进入 `forbidden`',
            '其余候选 `2,3,7,1,3`（还有被排除的 1、4）中最小可用的是 `2`',
            '`[1]`、`[1]`：唯一的数被排除 → 返回 `0`']),
               dict(heading='代码写法', lines=[
            '第一行：集合推导式 + `zip` 找出两面相同的数',
            '第二行：生成器遍历 `fronts + backs`，过滤后取 `min`',
            '`default=0` 兜住「全部被排除」']),],
        one_liner='两面相同的数一定不行，其余数里取最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 张卡片，正面 `fronts[i]`，背面 `backs[i]`，可任意翻转',
                 '选一张卡，若它背面的数 `x` 与所有卡的正面都不同，`x` 就是想要的数',
                 '求最小的想要的数，没有则返回 `0`；示例：`[1,2,4,4,7]`、`[1,3,4,1,3]` → `2`'],
        quote='只要有数字满足 fronts[i]=backs[i]，那么 fronts[i] 绝对不可能是答案，否则 fronts[i] 或者 backs[i] 作为背面的数字可以满足要求，取最小值作为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正反相同的数：翻哪面它都在正面，必须排除，存入哈希集合 `forbidden`',
              '其他数字不会同时在同一张卡的两面，可以单独翻到背面',
              '在所有正反面数字里取不在集合中的最小值，没有就 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：要同时看 `fronts` 和 `backs`，答案可能来自任一面',
                 '`min(..., default=0)` 处理全部被排除的情况（如 `[1]`、`[1]`）',
                 '两张不同的卡上有相同数字没关系，只有「同一张卡两面相同」才排除'],
    ),
)
