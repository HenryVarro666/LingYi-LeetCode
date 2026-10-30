CONFIG = dict(
    num=605, title='种花问题', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从左到右 · 能种就种',
    tags=['灵神题单', '难度分 1400'],
    code='''
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        flowerbed = [0] + flowerbed + [0]
        for i in range(1, len(flowerbed) - 1):
            if flowerbed[i - 1] == 0 and flowerbed[i] == 0 and flowerbed[i + 1] == 0:
                flowerbed[i] = 1  # 种花！
                n -= 1
        return n <= 0
''',
    call='Solution().canPlaceFlowers([1,0,0,0,0,0,1,0,0], 3)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"看第 `{S['i']}` 格：左 `{S['flowerbed'][S['i']-1]}`，中 `{S['flowerbed'][S['i']]}`，右 `{S['flowerbed'][S['i']+1]}`；还要种 ==`{S['n']}`== 朵" if 'i' in S and 0 < S['i'] < len(S['flowerbed']) - 1 else f"还要种 ==`{S['n']}`== 朵"), size=30),
        dict(type='array', var='flowerbed', pointers={'i': 'blue'}, label='flowerbed（两端各补一个 0；黄 = 正在检查的三格）', h=300,
             color=lambda S, i, v: ('yellow' if S['i'] - 1 <= i <= S['i'] + 1 else None) if 'i' in S else None),
    ],
    watch=[('i', 'i', 'blue'), ('n', 'n', 'green')],
    captions={
        'flowerbed = [0]': '两端各补一个 `0`，这样边界格也能统一判断：长度变为 `{len(flowerbed)}`',
        'for i in range': '看第 `i = {i}` 格',
        'if flowerbed[i - 1] == 0': lambda S, B, r: (f"左 `{S.flowerbed[S.i-1]}`、中 `{S.flowerbed[S.i]}`、右 `{S.flowerbed[S.i+1]}`：三格全是 0 → ==能种=="
                                                      if S.flowerbed[S.i-1] == 0 and S.flowerbed[S.i] == 0 and S.flowerbed[S.i+1] == 0
                                                      else f"左 `{S.flowerbed[S.i-1]}`、中 `{S.flowerbed[S.i]}`、右 `{S.flowerbed[S.i+1]}`：不是三个 0，不能种"),
        'flowerbed[i] = 1': '种花！第 `{i}` 格变成 `1`，它的右邻居下一步自然不满足三个 0',
        'n -= 1': '种下一朵，还差 `n` = =={n}==',
        'return n <= 0': lambda S, B, r: f"`n = {S.n} <= 0` → {'种够了' if S.n <= 0 else '没种够'}，返回 ==`{r}`==",
    },
    cards=dict(
        one_liner='从左到右扫，能种就立刻种',
        complexity='时间 `O(n)`，空间 `O(n)`（原地写法为 `O(1)`）',
        problem=['`flowerbed` 里 `1` 是已种花，`0` 是空地，花不能相邻',
                 '问能否再种下 `n` 朵花',
                 '示例：`[1,0,0,0,1]`，`n = 1` → `true`；`n = 2` → `false`'],
        quote='从左到右遍历数组，能种花就立刻种花。',
        quote_src='—— 灵茶山艾府题解',
        idea=['种在 `i` 的条件：`i-1`、`i`、`i+1` 三格都是 `0`',
              '尽早种、越靠左越好，给右边留下更多空地',
              '开头结尾各补一个 `0`，省去边界判断'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '种花后要真的把那格改成 `1`，下一格才会判不能种',
                 '最后是 `n <= 0`，种多了也算成功',
                 '另一写法：不建新数组，用 `while` 循环，种完 `i += 2` 直接跳过'],
    ),
)
