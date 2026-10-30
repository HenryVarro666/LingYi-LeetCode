def _cur(S):
    return S.get('_inner', {}).get('x', -1) if '_inner' in S else -1


CONFIG = dict(
    num=1298, title='你能从盒子里获得的最大糖果数', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='DFS · 盒子与钥匙',
    tags=['灵神题单·图论算法', '难度分 1825'],
    code='''
class Solution:
    def maxCandies(self, status: List[int], candies: List[int], keys: List[List[int]], containedBoxes: List[List[int]], initialBoxes: List[int]) -> int:
        ans = 0
        has_key = status  # 把开着的盒子当作有钥匙
        has_box = [False] * len(status)
        for x in initialBoxes:
            has_box[x] = True

        def dfs(x: int) -> None:
            nonlocal ans
            ans += candies[x]
            has_box[x] = False  # 避免找到钥匙后重新访问开着的盒子

            # 找到钥匙，打开盒子（说明我们先找到盒子，然后找到钥匙）
            for y in keys[x]:
                has_key[y] = True
                if has_box[y]:
                    dfs(y)

            # 找到盒子，使用钥匙（说明我们先找到钥匙，然后找到盒子）
            for y in containedBoxes[x]:
                has_box[y] = True
                if has_key[y]:
                    dfs(y)

        for x in initialBoxes:
            if has_key[x] and has_box[x]:  # 注意 dfs 中会修改 has_box
                dfs(x)
        return ans
''',
    call='Solution().maxCandies([1,0,1,0], [7,5,4,100], [[],[],[1],[]], [[1,2],[3],[],[]], [0])',
    expect=16,
    views=[
        dict(type='array', var='candies', label='candies（糖果；蓝=当前盒子 x）', cell=100, h=175,
             color=lambda S, i, v: 'blue' if i == S.get('x') else None),
        dict(type='array', var='has_key', label='has_key（1=有钥匙）', cell=100, h=175,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='has_box', label='has_box（True=手里有盒子）', cell=100, h=175,
             color=lambda S, i, v: 'yellow' if v else None),
        dict(type='calls', h=130),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green'), 'y'],
    captions={
        'ans = 0': '`ans` 累计拿到的糖果',
        'has_key = status': '把开着的盒子当作有钥匙：`has_key = {has_key}`，打开条件统一成「有盒子 + 有钥匙」',
        'has_box = [False]': '`has_box` 记录手里有哪些盒子，一开始都没有',
        'has_box[x] = True': '初始盒子 `{x}` 放进手里：`has_box[{x}] = True`',
        'ans += candies[x]': '打开盒子 `{x}`，拿走 `{candies[x]}` 颗糖：`ans` = =={ans}==',
        'has_box[x] = False': '盒子 `{x}` 处理完了，标记「没有」：==避免之后找到钥匙又重复访问==',
        'has_key[y] = True': '拿到盒子 `{y}` 的钥匙：`has_key[{y}] = True`',
        'has_box[y] = True': '拿到盒子 `{y}`：`has_box[{y}] = True`',
        'if has_box[y]': lambda S, B, r: (f'钥匙 `{S.y}` 到手，盒子 `{S.y}` 之前就拿到了 → ==可以打开，递归== `dfs({S.y})`' if S.has_box[S.y]
                                          else f'盒子 `{S.y}` 还没拿到 → 先记下钥匙，等盒子出现时再开'),
        'if has_key[y]': lambda S, B, r: (f'盒子 `{S.y}` 到手，钥匙之前就有 → ==可以打开，递归== `dfs({S.y})`' if S.has_key[S.y]
                                          else f'盒子 `{S.y}` 到手但没有钥匙 → 先留着，等钥匙出现时再开'),
        'dfs(y)': '进入盒子 `{y}`',
        'if has_key[x] and has_box[x]': lambda S, B, r: ('初始盒子 `%s`：有盒子且有钥匙 → 开始 DFS' % S.x if S.has_key[S.x] and S.has_box[S.x]
                                                         else '初始盒子 `%s`：已被前面的 DFS 处理过，或没有钥匙 → 跳过' % S.x),
        'return ans': '所有能开的盒子都开完，共 `{ans}` 颗糖',
    },
    cards=dict(
        one_liner='「找到盒子」和「找到钥匙」必有先后，后到的那个触发 DFS',
        complexity='时间 `O(n+L)`，空间 `O(n)`',
        problem=['每个盒子有 `status`（开/关）、糖果、钥匙、内含盒子',
                 '拿到开着的盒子就能取糖果、钥匙和里面的盒子，求最多糖果数',
                 '示例：初始盒子 `[0]` → 糖果 `7+4+5 = 16`'],
        quote='把 status[i]=1 当作我们有第 i 个盒子的钥匙。……找到钥匙，打开盒子（说明我们先找到盒子，然后找到钥匙）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`has_key` 表示有没有钥匙，`has_box` 表示有没有盒子，两者都满足才 DFS',
              '拿到钥匙时检查盒子在不在手里；拿到盒子时检查钥匙在不在手里',
              '这样无论谁先到都不会漏，开完立刻把 `has_box` 清掉防重复'],
        summary=['时间 `O(n+L)`，空间 `O(n)`，`L` 是所有钥匙数组长度之和',
                 '易错：DFS 中可能打开后面的初始盒子，所以外层循环要再判一次 `has_box[x]`',
                 '`has_key = status` 是直接改了入参，这里是题解的写法',
                 '同样的思路也可以用 BFS 队列实现'],
    ),
)
