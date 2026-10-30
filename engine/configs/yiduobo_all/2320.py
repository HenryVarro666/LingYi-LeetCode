CONFIG = dict(
    num=2320, title='统计放置房子的方式数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='一侧 DP · 滚动变量',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1608'],
    code='''
class Solution(object):
    def countHousePlacements(self, n):

        if n == 1:
            return 4
        elif n == 2:
            return 9
        else:
            a, b = 2, 3
            mod = 10 ** 9 + 7
            for index in range(2, n):
                a, b = b, (a + b) % mod

            return b * b % mod
''',
    call='Solution().countHousePlacements(6)',
    expect=441,
    views=[
        dict(type='array', var=lambda S: [S['a'], S['b']] if 'a' in S else [], h=190,
             label='滚动变量：a（前一项）、b（当前项，绿）',
             color=lambda S, i, v: 'green' if i == 1 else None),
        dict(type='text', size=30, fn=lambda S: (f"一侧放法 `f[{S['index'] + 1}]` = =={S['b']}==" if 'index' in S and 'b' in S else
                                                  (f"一侧放法 `b` = =={S['b']}==，两侧相乘 `b × b`" if 'b' in S else ''))),
    ],
    watch=['n', 'index', ('a', 'a', 'cyan'), ('b', 'b', 'green')],
    captions={
        'if n == 1': '`n = {n}`：不是 1，不走特判',
        'elif n == 2': '`n = {n}`：不是 2，也不走特判',
        'a, b = 2, 3': '起点：一侧 1 个地块有 `2` 种（放/不放），2 个地块有 `3` 种（空空、放空、空放）→ `a = f[1] = 2, b = f[2] = 3`',
        'for index': lambda S, B, r: ('`range(2, n)` 走完，循环结束' if B.get('index') == S.index else f'从第 3 个地块开始递推，`index = {S.index}`'),
        'a, b = b, (a + b)': '`f[i] = f[i-1] + f[i-2]`：第 i 块不放沿用 `f[i-1]`，放则第 i-1 块空沿用 `f[i-2]` → `b = {b}`',
        'return b * b': '两侧互不影响，总数 = 一侧 × 一侧 = `{b} × {b}` = {ret}',
    },
    cards=dict(
        one_liner='马路两侧互不影响：一侧方案数 k，答案 k × k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['马路两侧各 `n` 个地块，每块最多放一所房子',
                 '同一侧不能相邻；两侧互不影响',
                 '示例：`n = 1` → `4`，`n = 2` → `9`；本视频 `n = 6` → `441`'],
        quote='马路两侧的房子是互不影响的，不妨设其中一侧的放置方案数有k种，那么总的放置方案数就是k * k。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `i` 个位置不放：沿用 `f[i-1]` 的任意方案',
              '第 `i` 个位置放：`i-1` 必须空，沿用 `f[i-2]`',
              '`f[i] = f[i-1] + f[i-2]`，只依赖前两项 → 两个变量滚动'],
        summary=['时间 `O(n)`，空间 `O(1)`；原文还提到可用矩阵乘法优化到 `O(log n)`',
                 '易错点：==n = 1、2 要单独返回 4、9==，因为循环从 `range(2, n)` 开始',
                 '起点是 `a, b = 2, 3`（`f[1]`、`f[2]`），不是 1、2',
                 '对比灵神：灵神预处理全表后查表；这里每次现算',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
