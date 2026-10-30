ANS = [2, 2, 2, 1, 1, 2, 0]


def _txt(S):
    if 'x' not in S:
        return '每个颜色组大小 = `x + 1`；`left[x]` = 该回答组里还能再容纳几只'
    x = S['x']
    return f"回答 `{x}` 的兔子属于大小 `{x + 1}` 的颜色组；`left[{x}] = {S['left'].get(x, 0)}` 个空位；目前至少 ==`{S['ans']}`== 只"


CONFIG = dict(
    num=781, title='森林中的兔子', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贪心 · 一次遍历维护空位',
    tags=['灵神题单', '贪心与思维', '难度分 1453'],
    code='''
class Solution:
    def numRabbits(self, answers: List[int]) -> int:
        ans = 0
        left = defaultdict(int)
        for x in answers:
            if left[x] == 0:
                ans += x + 1  # 找到了一个大小为 x+1 的颜色组
                left[x] = x  # 允许其他 x 只兔子也回答 x
            else:
                left[x] -= 1
        return ans
''',
    call=f'Solution().numRabbits({ANS})',
    expect=9,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='answers', color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None, h=200),
        dict(type='map', var='left', fmt=lambda k, v: f'回答 {k}：还能容纳 {v} 只', h=300),
    ],
    watch=['x', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计森林里兔子的最少数量',
        'left = defaultdict': '`left[x]`：回答 `x` 的颜色组里还剩几个空位，默认 0',
        'for x in answers': lambda S, B, r: ('全部兔子都处理完了，退出循环' if 'x' in B and B.x == S.x and S.x == S.answers[-1]
                                              else f'下一只兔子回答 `{S.x}`'),
        'if left[x] == 0': lambda S, B, r: (
            f'`left[{S.x}] = 0`：没有空位了 → ==这只兔子属于一个新颜色组==' if S.left[S.x] == 0
            else f'`left[{S.x}] = {S.left[S.x]}`：还有空位 → 它可以并入已有的颜色组'),
        'ans += x + 1': '新组一共 `{x} + 1 = {x + 1}` 只，一次性算进答案：`ans` → {ans}',
        'left[x] = x': '组里除了这只，还有 `{x}` 只可以也回答 `{x}`：`left[{x}] = {left[x]}`',
        'left[x] -= 1': '占掉一个空位，不增加兔子总数：`left[{x}]` → {left[x]}',
        'return ans': '最少 `{ans}` 只兔子',
    },
    cards=dict(
        one_liner='回答 x 的兔子 ==凑满 x+1 只一组==，不够就再开新组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每只被问到的兔子说出「还有几只和我同色」',
                 '给出所有回答 `answers`，求森林中兔子最少有多少只',
                 '示例：`[1,1,2]` → `5`；本视频用 `[2,2,2,1,1,2,0]` → `9`'],
        quote='如果有 c 只兔子都回答了 x，那么每只兔子都在大小为 x+1 的颜色组中，最少有 ⌈c/(x+1)⌉ 个颜色组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回答 x 的兔子，所在颜色组恰好有 `x+1` 只',
              '尽量让回答相同的兔子凑进同一组，组数最少，总数最少',
              '写法二：遇到 x 时，没有空位就开新组并记 x 个空位，有空位就占一个'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '开新组时一次加上整组的 `x+1`，包含了没被问到的兔子',
                 '写法一用 `Counter` 统计，每个 x 加 `ceil(c/(x+1))*(x+1)`',
                 '易错：回答 0 的兔子每只都是独立一组，加 1'],
    ),
)
