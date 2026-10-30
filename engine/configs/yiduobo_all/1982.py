def _x(S, B, r):
    return (f"`x = now[0] − now[1] = {S.now[0]} − {S.now[1]} = {S.x}`：==最小的两个子集和之差==，"
            f"`|x|` 就是某个元素的绝对值")


def _pair(S, B, r):
    return f'`now[{S.index}] = {S.now[S.index]}` 还没配对：它是不含 x 的“较小”一方，要找 `{S.now[S.index]} − ({S.x}) = {S.now[S.index] - S.x}`'


CONFIG = dict(
    num=1982, title='从子集的和还原数组', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='按最值差两两分组 · 逐个还原',
    tags=['贪心', '数组'],
    code='''
class Solution(object):
    def recoverArray(self, n, sums):

        l = 1 << n
        now = sorted(sums)
        res = []

        for _ in range(n):
            x = now[0] - now[1]
            used = set()
            p = 0
            part1 = []
            part2 = []
            for index in range(l):
                if index in used:
                    continue
                
                part1.append(now[index])
                used.add(index)
                while p in used or now[p] != now[index] - x:
                    p += 1
                part2.append(now[p])
                used.add(p)
            
            if 0 in part1:
                res.append(-x)
                now = part1[:]
            else:
                res.append(x)
                now = part2[:]

            l //= 2
        
        return res
''',
    call='Solution().recoverArray(3, [-3, -1, 0, 1, 2, 3, 4, 6])',
    expect=[2, -3, 4],
    skip=['l = 1 << n', 'used = set()', 'p = 0', 'part1 = []', 'part2 = []', 'used.add', 'continue', 'p += 1', 'while p in used', 'for index in range(l)'],
    views=[
        dict(type='text', fn=lambda S: ('原数组 `[-3, 2, 4]` 的 8 个子集和，目标：还原出 3 个数（答案不唯一，这里得到 `[2, -3, 4]`）' if 'x' not in S else
                                        f"本轮 `x = {S['x']}`：把 `now` 按“差为 x”两两配对：一半含某个元素、一半不含")),
        dict(type='array', var='now', pointers={'index': 'blue', 'p': 'pink'}, h=190, label='now（当前子集和，已排序）',
             color=lambda S, i, v: 'purple' if 'used' in S and i in S['used'] else None),
        dict(type='array', var='part1', h=140, label='part1（每对较小的）'),
        dict(type='array', var='part2', h=140, label='part2（每对较大的）'),
        dict(type='array', var='res', h=140, label='res（已还原的元素）'),
    ],
    watch=[('l', 'l', 'cyan'), ('x', 'x', 'yellow'), ('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'now = sorted': '子集和排序：最小的两个数之差，就藏着一个元素的信息',
        'res = []': '`res` 收集还原出的元素，每轮还原一个',
        'for _ in range(n)': '还原一个元素就把子集和个数减半，共 `n = {n}` 轮；本轮有 `{l}` 个子集和',
        'x = now[0]': _x,
        'for index in range(l)': '`index = {index}`：从小到大扫描 `now`',
        'if index in used': lambda S, B, r: (f'扫描到 `index = {S.index}`：已被配成较大的 → 跳过' if S.index in S.used else f'扫描到 `index = {S.index}`：还没配对 → 它是这一对里较小的'),
        'part1.append': '`now[{index}] = {now[index]}` 放入 `part1`（每对里较小的）',
        'part2.append': '`p` 右移到 `now[{p}] = {now[p]}`，恰好等于 `{now[index]} − ({x})`：配对成功，放入 `part2`（每对里较大的）',
        'if 0 in part1': lambda S, B, r: ('`0` 在 `part1` 里：不含 x 的一半必含空集 0，所以 ==part1 才是不含 x 的== → 还原 `-x`' if 0 in S.part1
                                          else '`0` 不在 `part1`：说明 `part2` 才含 0，即 ==part2 是不含 x 的=='),
        'res.append(-x)': '含 0 的 `part1` 是不含该元素的一半，元素 = 较大 − 较小 = `-x = {-x}`：`res = {res}`',
        'now = part1[:]': '去掉 x 的影响，只剩 `part1`，递归处理：`now = {now}`',
        'res.append(x)': '含 0 的是 `part2`，较小一半含该元素，元素 = `x = {x}`：`res = {res}`',
        'now = part2[:]': '只剩 `part2`，递归处理：`now = {now}`',
        'l //= 2': '子集和个数减半：`l = {l}`',
        'return res': '3 轮完成，还原出 `{res}`',
    },
    cards=dict(
        one_liner='从最小的两个子集和入手：每轮差出一个元素，子集和减半',
        complexity='时间 `O(n·2^n)`，空间 `O(2^n)`',
        problem=['已知长为 `n` 的数组的全部 `2^n` 个子集和 `sums`（含空集 0，元素可正可负可为 0）',
                 '还原出任意一个满足的原数组',
                 '示例：`n=2, sums=[-3,-2,-1,0]` → `[1,-2]`；本视频 `n=3`，`sums=[-3,-1,0,1,2,3,4,6]`'],
        quote='最小值和次小值之差 x，将 sums 按差为 x 进行两两分组。……不受 x 影响的那一组中必然有 0。',
        quote_src='—— yiduobo 题解（摘要）',
        idea=['空集和为 0，所以一定有一半子集和不含 x，另一半恰好比它们大（或小）`x`',
              '最小与次小之差给出 `|x|`，把 `sums` 排序后按“差为 x”两两分组',
              '含 0 的那一组就是不含 x 的一组：在较小组则元素是 `-x`，否则是 `x`；再对这一组递归',
              '两组都含 0 时，任选一组仍可构造出合法答案（原文有证明）'],
        summary=['时间 `O(n·2^n)`，空间 `O(2^n)`',
                 '易错：配对时 `now[p] == now[index] − x`，x 可能是负数',
                 '易错：`0 in part1` 决定的是==符号==，不是取哪一半的位置',
                 '原文为 Python 2 写法，`l /= 2` 已改为 `l //= 2`（整数除法，否则 `range(l)` 报错）',
                 '本题答案不唯一：示例得到 `[2,-3,4]`，与原数组 `[-3,2,4]` 的子集和相同'],
    ),
)
