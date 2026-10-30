CONFIG = dict(
    num=1799, title='N次操作后的最大分数和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状态压缩 DP · 类 BFS 按步转移',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maxScore(self, nums):

        m = len(nums)
        q = [0]
        f = [0] * (1 << m)
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for i in range(m - 1):
                    if now & (1 << i) == 0:
                        for j in range(i + 1, m):
                            if now & (1 << j) == 0:
                                next = now | (1 << i) | (1 << j)
                                if f[next] == 0:
                                    q.append(next)

                                x, y = nums[i], nums[j]
                                while x:
                                    x, y = y % x, x
                                f[next] = max(f[next], f[now] + y * step)

            l, r = r, len(q)

        return f[-1]
''',
    call='Solution().maxScore([3, 4, 6, 8])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = i，粉 = j）', cell=70, h=170,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='array', var='f', label='f[state]（state 第 k 位 = 1 表示 nums[k] 已用）', cell=56, h=210,
             pointers={'now': 'cyan', 'next': 'yellow'},
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='q', label='q：分层队列（亮 = 当前层 l..r）', cell=56, h=190,
             pointers={'l': 'blue', 'r': 'pink'},
             dim=lambda S, i, v: not (S.get('l', 0) <= i < S.get('r', 0))),
        dict(type='text', fn=lambda S: (f"这一轮 `step = {S['step']}`：每次再选两个数，得分 `gcd × {S['step']}`" if 'step' in S else '')),
    ],
    watch=['step', 'now', 'i', 'j', 'next', ('f[next]', "f[next] if 'next' in dir() else 0", 'green')],
    skip=['while x:', 'x, y = y % x, x', 'for j in range', 'q.append', 'l = 0', 'r = 1', 'step = 0', 'm = len'],
    captions={
        'q = [0]': '`q = [0]`：从什么都没选的状态 `0` 出发；`l, r, step` 记录当前层的范围和步数',
        'f = [0]': '`f` 有 `2^m = {len(f)}` 个状态，初值全 0',
        'step += 1': '进入第 `{step}` 层：这一层的状态里已选 `{2*step-2}` 个数，再选两个 → 第 `{step}` 次操作',
        'for now in': '取出本层状态 `now = {now}`（二进制 `{now:0{m}b}`）',
        'for i in range(m - 1)': '枚举还没用的第一个数 `i`（要给 `j` 留位置，所以到 `m-1`）',
        'if now & (1 << i)': '`now` 的第 `{i}` 位是 `{now >> i & 1}`：{"==没用过==，可以选" if now >> i & 1 == 0 else "已用，跳过"}',
        'if now & (1 << j)': '`now` 的第 `{j}` 位是 `{now >> j & 1}`：{"==没用过==，和 i 配成一对" if now >> j & 1 == 0 else "已用，跳过"}',
        'next = now': '选了 `nums[{i}]={nums[i]}` 和 `nums[{j}]={nums[j]}`，新状态 `next = {next}`（二进制 `{next:0{m}b}`）',
        'if f[next] == 0': '`f[next] == 0` → 这个状态==第一次出现==，`next` 入队，留给下一层转移',
        'q.append': '`next = {next}` 入队，下一层再处理',
        'x, y = nums[i], nums[j]': '辗转相除求 `gcd({nums[i]}, {nums[j]})`，结果最后落在 `y`',
        'f[next] = max': '得分 = `f[now]` + gcd × step = `{B.f[now]} + {y} × {step}`，取最大 → `f[{next}]` = =={f[next]}==',
        'l, r = r, len(q)': '本层处理完：下一层就是 `q[{r}:{len(q)}]`（刚入队的新状态），步数 +1',
        'while l < r': '`l < r` 时队列里还有未处理的一层',
        'return f[-1]': '全部 `{m}` 个数都用完的状态是 `f[-1]`，最大总分 =={ret}==',
    },
    max_steps=46,
    cards=dict(
        one_liner='f[state] 记录已选数字集合的最大得分，按步数分层转移',
        complexity='时间 `O(2^m · m^2 · log)`，空间 `O(2^m)`',
        problem=['给你长为 `2n` 的正整数数组 `nums`，做 `n` 次操作',
                 '第 `i` 次（从 1 起）取两个数 `x, y`，得分 `i × gcd(x, y)`，取走后不再使用',
                 '求最大总分；本视频示例：`[3,4,6,8]`'],
        quote='没有想出什么特别好的算法，只能老老实实用状态压缩动态规划来做。令f[state]表示选择了数组下标压缩后为state的数字可以得到的最大分数和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 的每一位表示某个数是否用过，`f[state]` 是用完这些数的最大分数',
              '`state` 里有 `2k` 个数，说明刚做完第 `k` 步 → 这一步得分乘 `step`',
              '`next` 一定比 `now` 大，所以用类似 BFS 的队列一层一层转移'],
        summary=['时间约 `O(2^m · m^2 · log U)`，空间 `O(2^m)`，m 最大 14',
                 '`f[next] == 0` 用来判断 next 是否第一次出现，只入队一次',
                 'gcd 用辗转相除手写：`x, y = y % x, x`，循环结束 `y` 即 gcd',
                 '答案是 `f[-1]`，即全部数字都用完的状态',
                 '原文为 Python 2 风格写法，Python 3 下可直接运行，未改动'],
    ),
)
