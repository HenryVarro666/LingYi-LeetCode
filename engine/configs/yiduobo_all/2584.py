def _sets(S):
    L = S.get('prime_set_list')
    if L is None:
        return ''
    return '各位置的质因子集合：' + '  '.join(f"`[{i}]` {{{','.join(str(p) for p in sorted(s))}}}" for i, s in enumerate(L))


CONFIG = dict(
    num=2584, title='分割数组使乘积互质', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='质因子最后出现位置 · 前缀取最大',
    tags=['灵神题单', '难度分 2159'],
    setup='''
f = [None] * 1000001
x = 2
while x <= 1000:
    if f[x] is None:
        f[x] = x
        for y in range(x + x, 1000001, x):
            f[y] = x
    x += 1
''',
    code='''
class Solution(object):
    def findValidSplit(self, nums):

        n = len(nums)
        prime_set_list = [set() for _ in range(n)]
        last = {}
        for index in range(n - 1, -1, -1):
            now = nums[index]
            while f[now] is not None:
                prime_set_list[index].add(f[now])
                if f[now] not in last:
                    last[f[now]] = index
                now //= f[now]
            if now != 1:
                prime_set_list[index].add(now)
                if now not in last:
                    last[now] = index
        
        res = 0
        for index in range(n - 1):
            for p in prime_set_list[index]:
                res = max(res, last[p])
            
            if res == index:
                return res
        
        return -1
''',
    call='Solution().findValidSplit([4, 7, 8, 15, 3, 5])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = index）', pointers={'index': 'blue'}, cell=100, h=190,
             color=lambda S, i, v: ('green' if 'res' in S and i <= S['index'] else None)),
        dict(type='map', var='last', label='last：质因子 → 最后出现的下标', fmt=lambda k, v: f'{k}: {v}', h=130, font=30),
        dict(type='text', h=110, size=26, fn=_sets),
        dict(type='text', h=70, size=30, fn=lambda S: (f"前缀的质因子最远出现在 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=['index', 'now', 'p', ('res', 'res', 'green')],
    captions={
        'n = len': '先倒着扫一遍，记下每个质因子==最后出现==的位置',
        'prime_set_list = ': '`prime_set_list[i]`：第 `i` 个数的所有质因子',
        'last = {}': '`last[p]`：质因子 `p` 最后一次出现的下标',
        'for index in range(n - 1, -1, -1)': lambda S, B, r: f'倒序处理 `index = {S.index}`：第一次见到的 `p` 就是它的==最后位置==',
        'prime_set_list[index].add(f[now])': lambda S, B, r: (
            f"`f[now]` 给出质因子 `{(S.prime_set_list[S.index] - B.prime_set_list[S.index]).pop()}`，加入 `prime_set_list[{S.index}]`"
            if S.prime_set_list[S.index] != B.prime_set_list[S.index] else '这个质因子已在集合里，不用重复加'),
        'last[f[now]] = index': lambda S, B, r: (
            f"倒着扫，`{[k for k in S.last if k not in B.last][0]}` 第一次出现 → 这里就是它==最后==的位置：`last[{[k for k in S.last if k not in B.last][0]}] = {S.index}`"),
        'now //= f[now]': '除掉这个质因子：`now` → {now}（原文 `/` 已改 `//`）',
        'if now != 1': lambda S, B, r: (f'剩下 `{S.now}` 是大于 1000 的质数 → 也要记录' if S.now != 1 else '`now = 1`：分解完毕'),
        'prime_set_list[index].add(now)': '大质因子 `{now}` 加入 `prime_set_list[{index}]`',
        'if now not in last': lambda S, B, r: (f'`{S.now}` 之前没见过：记最后位置' if S.now not in S.last else f'`{S.now}` 已有更靠后的记录'),
        'last[now] = index': '`last[{now}] = {index}`',
        'res = 0': '`res`：前缀 `nums[:index+1]` 所有质因子最后出现位置的最大值',
        'for index in range(n - 1)': '正序枚举切点 `index`（最后一个位置不能切）',
        'for p in prime_set_list[index]': '取 `nums[{index}]` 的质因子 `{p}`',
        'res = max(res, last[p])': '`res = max({B.res}, last[{p}]) = {res}`：`{p}` 最后出现在 `{last[p]}`，前缀必须延伸到那里',
        'if res == index': lambda S, B, r: (f'`res = {S.res} == index`：前缀的质因子都不会出现在右边 → ==可以切==' if S.res == S.index
                                           else f'`res = {S.res} > index = {S.index}`：还有质因子出现在右边，继续'),
        'return res': '切点 =={res}==',
        'return -1': '走完都没有 `res == index`：==无法分割==',
    },
    cards=dict(
        one_liner='前缀里每个质因子的最后出现位置，不能越过切点',
        complexity='筛法 `O(U log log U)`，查询 `O(n log U)`',
        problem=['在下标 `i` 切开，前缀乘积与后缀乘积要==互质==',
                 '返回最小的有效切点 `i`，没有就返回 `-1`',
                 '示例：`[4,7,8,15,3,5]` → `2`；`[4,7,15,8,3,5]` → `-1`'],
        quote='要求前缀中所有数的质因子都不是剩余的数的约数，也就是说这些质因数最后出现的位置都不超过前缀的右边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['互质问题 → 分解质因数，转成质因子位置问题',
              '倒序扫一遍，用哈希表 `last` 记下每个质因子最后出现的位置',
              '正序扫前缀：`res` 取前缀质因子最后位置的最大值，`res == index` 就能切'],
        summary=['时间 `O(U log log U + n log U)`，空间 `O(U + n)`',
                 '筛法 `f[]` 预处理在配置的 setup 中执行（不逐行演示），`f[x]` 存 1000 以内最大的质因子',
                 '原文为 Python 2 写法，`now /= f[now]` 已改为 `now //= f[now]`',
                 '与灵神对比：灵神用「首次出现 + 区间右端点」像跳跃游戏；这里用「最后出现」的位置取前缀最大值'],
    ),
    skip=['if f[now] not in last', 'now = nums[index]', 'while f[now] is not None'],
    max_steps=120,
)
