CONFIG = dict(
    num=1981, title='最小化目标值与所选元素的差', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分组背包 · 布尔 DP 倒序压缩（Go 原文转写）',
    tags=['动态规划', '难度分 2010'],
    code='''
class Solution:
    def minimizeTheDifference(self, mat: List[List[int]], target: int) -> int:
        dp = [False] * (min(len(mat) * 70, target * 2) + 1) # 需要枚举的重量不会超过 target*2
        dp[0] = True
        minSum, maxSum = 0, 0
        for row in mat:
            mi, mx = row[0], row[0]
            for v in row[1:]:
                if v > mx:
                    mx = v
                elif v < mi:
                    mi = v
            minSum += mi # 求 minSum 是为了防止 target 过小导致 dp 没有记录到
            maxSum = min(maxSum + mx, target * 2) # 前 i 组的最大重量，优化枚举时 j 的初始值
            for j in range(maxSum, -1, -1):
                dp[j] = False
                for v in row:
                    if v <= j and dp[j - v]:
                        dp[j] = True
                        break
        ans = abs(minSum - target)
        for i, ok in enumerate(dp):
            if ok:
                ans = min(ans, abs(i - target))
        return ans
''',
    call='Solution().minimizeTheDifference([[1,2],[3,4]], 5)',
    expect=0,
    skip=['mi, mx = ', 'for v in row[1:]', 'if v > mx', 'mx = v', 'elif v < mi', 'mi = v', 'dp = [False]', 'minSum, maxSum = 0, 0', 'dp[j] = False',
          'for v in row:', 'dp[j] = True', 'break', 'for j in range', 'for i, ok', 'if ok'],
    max_steps=70,
    views=[
        dict(type='table', var='mat', label='mat：每行是一组，每组恰好选一个', h=170, cell=62),
        dict(type='array', var=lambda S: [1 if b else 0 for b in S['dp']], label='dp[j]：前几组能否凑出和恰好为 j（1 = 能，绿）',
             h=210, cell=60, pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if v else None,
             dim=lambda S, i, v: 'maxSum' in S and i > S['maxSum']),
        dict(type='text', fn=lambda S: (f"`minSum = {S['minSum']}`（每行最小值之和），`maxSum = {S['maxSum']}`（本组最多能到的重量，封顶 `target×2`）" if 'maxSum' in S else ''), size=22, h=60),
    ],
    watch=['minSum', 'maxSum', 'j', ('target', 'target', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'dp = [False]': '`dp` 只开到 `{len(dp)-1}`：重量超过 `target×2` 没必要考虑',
        'dp[0] = True': '没选任何组，和为 0 能凑出',
        'for row in mat': lambda S, B, r: (f'处理这一组（一行）`{S.row}`：恰好选一个' if S.row != B.get('row') else '所有行都处理完'),
        'minSum += mi': '这一组最小值 `{mi}`，`minSum` → {minSum}（防止 target 太小，dp 里记不到）',
        'maxSum = min': '前面各组最大值之和（封顶 `target×2 = {target*2}`）→ `maxSum` = {maxSum}，只需枚举 `j ≤ {maxSum}`',
        'if v <= j': lambda S, B, r: (f'`j = {S.j}`，试选 `v = {S.v}`：' + (f'`dp[{S.j} − {S.v}]` = {S.dp[S.j - S.v]}' if S.v <= S.j else f'`v > j`，放不下')),
        'dp[j] = True': '选 `{v}` 后和为 `{j}`：前面组能凑出 `{j - v}` → `dp[{j}]` = ==True==',
        'ans = abs(minSum': '先取 `|minSum − target| = {ans}` 当候选',
        'ans = min(ans': '`ans = min({B.ans}, |{i} − {target}|)` = =={ans}==',
        'return ans': '最小绝对差 = =={ret}==',
    },
    cards=dict(
        one_liner='每行当一组，选一个，布尔背包倒序刷；上限只要 target×2',
        complexity='时间 `O(m·target·n)`，空间 `O(target)`',
        problem=['矩阵每行选一个数，使总和与 `target` 的绝对差最小',
                 '`m,n ≤ 70`，`target ≤ 800`',
                 '示例：`[[1,2],[3,4]]`，`target=5` → `0`（1+4 或 2+3）'],
        quote='把每一行看成一组，物品的体积就是元素值，这样就转化成了一个分组背包的模型。……注意背包大小至多是 target·2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dp[j]` = 前 `i` 组每组恰好选一个，能否凑出重量 `j`',
              '倒序枚举 `j`，用本组每个 `v` 看 `dp[j−v]` 是否为真，压缩掉第一维',
              '重量封顶 `target×2`；`minSum` 防止 target 太小时漏掉“全选最小”的情况'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(m·target·n)`，空间 `O(target)`',
                 '易错：`dp[j]` 必须先置 `False` 再重算，因为每组恰好选一个',
                 '易错：`j` 倒序，保证 `dp[j-v]` 还是上一组的值',
                 '同类题：分组背包（每组恰好选一个）'],
    ),
)
