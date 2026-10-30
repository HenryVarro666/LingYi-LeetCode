CONFIG = dict(
    num=3767, title='选择 K 个任务的最大总分数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='先全选 a，再撤销改选 b', tags=['灵神题单', '难度分 1704'],
    code='''
class Solution:
    def maxPoints(self, a: List[int], b: List[int], k: int) -> int:
        d = sorted((y - x for x, y in zip(a, b) if y > x), reverse=True)
        return sum(a) + sum(d[:len(a) - k])
''',
    call='Solution().maxPoints([5,2,10,4,7,3], [10,3,8,9,1,6], 3)',
    expect=44,
    views=[
        dict(type='array', var='a', label='a（技巧 1 得分）', h=170,
             color=lambda S, i, v: 'green' if 'd' in S and S['b'][i] > v else None),
        dict(type='array', var='b', label='b（技巧 2 得分）', h=170,
             color=lambda S, i, v: 'orange' if 'd' in S and v > S['a'][i] else None),
        dict(type='array', var=lambda S: S['d'] if 'd' in S else [], label='d = b[i] − a[i]，只留 > 0 并从大到小', h=190,
             color=lambda S, i, v: 'green' if i < len(S['a']) - S['k'] else None),
        dict(type='text', fn=lambda S: (f"先全选 a：`sum(a)` = =={sum(S['a'])}==；最多撤销 `n−k` = `{len(S['a'])-S['k']}` 个，取最大的 d" if 'd' in S else '先看 a、b：每个位置 b 比 a 大多少？')),
    ],
    watch=['k', ('n-k', 'len(a) - k', 'cyan'), ('d', 'd if "d" in dir() else None', 'green')],
    captions={
        'd = sorted': '全选 a 后，撤销 `a[i]` 改选 `b[i]` 增加 `b[i]−a[i]`；==只留 > 0 的==，从大到小排：`d = {d}`',
        'return sum': '`sum(a)` = {sum(a)}，再加 d 的前 `n−k = {len(a)-k}` 个 `{d[:len(a)-k]}` = =={ret}==（d 不够就全加）',
    },
    cards=dict(
        one_liner='先全选 a，再把最划算的 n−k 个改选 b',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`a`、`b` 是同一批任务用技巧 1 / 2 的得分，至少 `k` 个任务必须用技巧 1，其余随意',
                 '求最大总分',
                 '示例：`a=[10,20,30], b=[5,15,25], k=2` → `60`'],
        quote='我们可以先选择所有 a[i]，然后再从中撤销至多 n-k 个，改成选择 b 中的元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个数组一起想很乱：==先全选 a==，保证 k 个条件自动满足',
              '撤销 `a[i]` 改选 `b[i]`，分数增加 `d[i] = b[i] − a[i]`',
              '撤销至多 `n−k` 个：只取 ==d > 0 的最大的 n−k 个=='],
        summary=['时间 `O(n log n)`，瓶颈在排序；快速选择可到 `O(n)`',
                 '易错：`d[i] <= 0` 的不要选，所以生成式里加 `if y > x`',
                 '易错：撤销个数是 `n-k`，且不超过 `len(d)`，切片 `d[:n-k]` 自动处理',
                 '同类题：2611. 老鼠和奶酪'],
        after=[dict(heading='为什么能这样撤销', lines=['全选 `a` 后，已经满足「至少 k 个用技巧 1」', '最多撤销 `n-k` 个，所以 ==至多 n-k 个改选 b==', '收益 `d[i]` 互相独立，所以直接取最大的几个', '`d[i] <= 0` 的撤销只会亏，丢掉']),
               dict(heading='另一种写法', lines=['题解还给了 C++ 快速选择：不用排序，`O(n)` 找第 `n-k` 大', '思路相同，只是把「排序取前 n-k」换成「划分」'])],
    ),
)
