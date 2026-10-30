CONFIG = dict(
    num=370, title='区间加法', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def getModifiedArray(self, length, updates):

        f = [0] * length
        for x, y, inc in updates:
            f[x] += inc
            if y + 1 < length:
                f[y + 1] -= inc
        
        now = 0
        res = []
        for index in range(length):
            now += f[index]
            res.append(now)
        return res
''',
    call='Solution().getModifiedArray(5, [[1,3,2],[2,4,3],[0,2,-2]])',
    expect=[-2, 0, 3, 5, 3],
    views=[
        dict(type='text', fn=lambda S: f"当前操作：`[{S['x']}, {S['y']}]` 加 ==`{S['inc']}`==" if 'inc' in S and 'index' not in S else (f"累加到下标 `{S['index']}`：`now = {S['now']}`" if 'index' in S else ''), size=28),
        dict(type='array', var='f', label='差分数组 f（只改区间两端）', h=170, pointers={'x': 'blue', 'y+1': 'pink'},
             color=lambda S, i, v: 'yellow' if v != 0 else None),
        dict(type='array', var='res', label='res（f 的前缀和 = 最终数组）', h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'inc', 'now', 'index'],
    captions={
        'f = [0]': '`f[i]` 表示从下标 `i` 开始的==后缀==被统一加了多少，初始都是 0',
        'for x, y, inc': '取出一次操作：区间 `[{x}, {y}]`，每个数加 `{inc}`',
        'f[x] += inc': '区间起点 `{x}`：后缀从这里开始加 `{inc}` → `f[{x}] = {f[x]}`',
        'if y + 1 < length': lambda S, B, r: (f'`y + 1 = {S.y + 1} < {S.length}`：右端点后面还有数，需要在那里抵消' if S.y + 1 < S.length
                                              else f'`y + 1 = {S.y + 1}` 没有小于 `{S.length}`：区间直达末尾，不需要抵消'),
        'f[y + 1] -= inc': '`y + 1 = {y+1}` 处把 `{inc}` 减掉，后缀的加法到 `y` 就停 → `f[{y+1}] = {f[y+1]}`',
        'now = 0': '`now` 记录当前位置累计的增量',
        'for index in range': '第二遍：从左到右扫 `f`，下标 `{index}`',
        'now += f[index]': '`now += f[{index}]` → ==`{now}`==，这就是下标 `{index}` 的最终值',
        'res.append(now)': '把 `{now}` 放进答案',
        'return res': '全部累加完，返回 `{res}`',
    },
    cards=dict(
        one_liner='区间加改成两端打标记，最后一遍前缀和还原',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['长度为 `length` 的数组初始全 0，给若干操作 `[start, end, inc]`',
                 '每个操作把下标 `start..end` 的元素都加上 `inc`，返回最终数组',
                 '示例：`length=5`，`[[1,3,2],[2,4,3],[0,2,-2]]` → `[-2,0,3,5,3]`'],
        quote='非常标准的差分数组的问题，具体实现上与之前的253题类似，不过在这里每次加减的值应该是inc而不是1。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间 `[x, y]` 加 `inc` = 后缀 `[x, n)` 加 `inc` + 后缀 `[y+1, n)` 减 `inc`',
              '所以每次操作只改 `f[x]` 和 `f[y+1]` 两个位置，`O(1)`',
              '全部操作完，前缀和一遍就得到每个位置的最终值'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '易错：`y + 1` 可能等于 `length`，要先判断再减，否则越界',
                 '与第 253 题会议室 II 同一思路，只是增量由 1 换成 `inc`',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
