CONFIG = dict(
    num=2266, title='统计打字方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 四个变量滚动',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1857'],
    code='''
class Solution(object):
    def countTexts(self, pressedKeys):

        mod = 10 ** 9 + 7
        a = b = c = d = 1
        for index in range(1, len(pressedKeys)):
            now = 0
            if pressedKeys[index] == pressedKeys[index - 1]:
                if index >= 2 and pressedKeys[index] == pressedKeys[index - 2]:
                    if index >= 3 and pressedKeys[index] == pressedKeys[index - 3] and (pressedKeys[index] == '7' or pressedKeys[index] == '9'):
                        now += a
                        if now >= mod:
                            now -= mod
                    
                    now += b
                    if now >= mod:
                        now -= mod
                
                now += c
                if now >= mod:
                    now -= mod
            
            now += d
            if now >= mod:
                now -= mod

            a, b, c, d = b, c, d, now
        
        return d
''',
    call='Solution().countTexts("22277")',
    expect=8,
    views=[
        dict(type='string', var='pressedKeys', pointers={'index': 'blue'}, h=240,
             window=('max(0, index - 3)', 'index'),
             label='pressedKeys（蓝框 = 往前看的最多 4 位）'),
        dict(type='array', var=lambda S: [S['a'], S['b'], S['c'], S['d']] if 'a' in S else [],
             label='滚动的 f 值：f[i-4]  f[i-3]  f[i-2]  f[i-1]', h=170,
             color=lambda S, i, v: 'green' if i == 3 else None),
        dict(type='text', size=30, fn=lambda S: (f"本位 `now` = =={S['now']}==（f[{S['index']}]）" if 'now' in S and 'index' in S else '')),
    ],
    watch=['index', 'now', ('a', 'a', 'cyan'), ('b', 'b', 'cyan'), ('c', 'c', 'cyan'), ('d', 'd', 'green')],
    captions={
        'a = b = c = d = 1': '`f[-1]`（空）和 `f[0]` 都是 1：四个变量先全设成 `1`，后面逐位往前滚',
        'now = 0': '算第 `{index}` 位的 `f[{index}]`，先从 0 开始累加',
        'if pressedKeys[index] == pressedKeys[index - 1]': lambda S, B, r: (f"第 {S.index} 位与前一位{'相同' if S.pressedKeys[S.index]==S.pressedKeys[S.index-1] else '不同'}：" + ('最后两个数字可合成一个字符，要加 `f[i-2]`（`c`）' if S.pressedKeys[S.index]==S.pressedKeys[S.index-1] else '只能单独解码，只加 `f[i-1]`')),
        'if index >= 2': lambda S, B, r: (lambda ok: f"往前第 3 位{'也相同' if ok else '不同'}" + ('：最后三个数字可合成，要加 `f[i-3]`（`b`）' if ok else '：到此为止'))(S.index >= 2 and S.pressedKeys[S.index] == S.pressedKeys[S.index - 2]),
        'if index >= 3': lambda S, B, r: (lambda ok: ("连续第 4 位相同且是 7/9 键 → 最后四个数字可合成，加 `f[i-4]`（`a`）" if ok else '第 4 位不满足（不相同或不是 7/9 键），不加 `f[i-4]`'))(S.index >= 3 and S.pressedKeys[S.index] == S.pressedKeys[S.index - 3] and S.pressedKeys[S.index] in '79'),
        'now += a': '加 `f[i-4]`：`now = {now}`',
        'now += b': '加 `f[i-3]`：`now = {now}`',
        'now += c': '加 `f[i-2]`：`now = {now}`',
        'now += d': '总是可以把本位单独解码，加 `f[i-1]`：`now = {now}`',
        'if now >= mod': '`now = {now}` 没超过 `mod`，不用减',
        'a, b, c, d = b, c, d, now': '四个变量整体往前滚一格：`d = f[{index}] = {d}`',
        'return d': '`d` 就是 `f[-1]` = 答案 `{d}`',
    },
    cards=dict(
        one_liner='f[i] = 往前最多 4 位能凑成一个字母的 f 之和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`pressedKeys` 是按键串，每个字母按对应键 `i` 次得到，求可能的文字信息种数',
                 '`7`、`9` 键有 4 个字母，其它键 3 个；结果对 `10^9+7` 取余',
                 '本视频：`"22277"` → `8`'],
        quote='直接将pressedKeys[i]解码成一个字符总是可行的，那么可以初始化f[i] = f[i - 1]；如果pressedKeys[i]与pressedKeys[i - 1]相同，那么将最后这两个数字解码成一个字符也是可以的，于是就有f[i] += f[i - 2]',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 是前 `i+1` 个按键的方案数，按“最后一个字母占几次按键”分类累加',
              '占 1、2、3 次要求末尾相同字符够多；占 4 次还要求是 `7` 或 `9`',
              '只依赖前 4 个状态 → 用 `a b c d` 四个变量滚动'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：==占 4 次只有 7、9 键==；条件是连续相同，不能漏判 `index >= 3`',
                 '用 `if now >= mod: now -= mod` 取模，比 `%` 少一次除法',
                 '对比灵神：灵神按相同字符分组做乘法；这里是逐位线性 DP',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
