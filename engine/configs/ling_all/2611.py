CONFIG = dict(
    num=2611, title='老鼠和奶酪', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='先全给老鼠 2，再撤销 k 块（差值排序）',
    tags=['灵神题单', '难度分 1663'],
    code='''
class Solution:
    def miceAndCheese(self, r1: List[int], r2: List[int], k: int) -> int:
        a = sorted(zip(r1, r2), key=lambda p: p[1] - p[0])
        return sum(x for x, _ in a[:k]) + sum(y for _, y in a[k:])
''',
    call='Solution().miceAndCheese([5,2,7,1,6,3], [3,6,4,4,1,5], 3)',
    expect=33,
    views=[
        dict(type='array', var='r1', h=150, label='r1（老鼠 1 的得分）', color=lambda S, i, v: 'blue'),
        dict(type='array', var='r2', h=150, label='r2（老鼠 2 的得分）', color=lambda S, i, v: 'pink'),
        dict(type='text', h=90, fn=lambda S: ('各块奶酪 `r1 − r2`：' + '、'.join(str(x - y) for x, y in zip(S['r1'], S['r2'])) + '（改给老鼠 1 的收益）') if 'r1' in S else ''),
        dict(type='text', h=170, fn=lambda S: ('排好序的 `a`（每项 `(r1, r2)`，收益 `r1−r2` 从大到小）：' + ' '.join(('==(%d,%d)==' if i < S['k'] else '`(%d,%d)`') % p + ('[%+d]' % (p[0] - p[1])) for i, p in enumerate(S['a'])) + '　前 `k` 个（强调）给老鼠 1') if 'a' in S else ''),
    ],
    watch=[('k', 'k', 'green')],
    captions={
        'a = sorted': '按 `p[1]-p[0]` 升序 = 按收益 `r1−r2` ==降序==：收益最大的排最前，`a` 如上',
        'return sum': '前 `k={k}` 块给老鼠 1：取 `x` 之和 `{sum(x for x, _ in a[:k])}`；其余给老鼠 2：取 `y` 之和 `{sum(y for _, y in a[k:])}` → =={ret}==',
    },
    max_steps=40,
    cards=dict(
        one_liner='先全给老鼠 2，再撤销 k 块给老鼠 1：选 r1−r2 最大的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两只老鼠分 `n` 块奶酪，第 `i` 块给老鼠 1 得 `reward1[i]`，给老鼠 2 得 `reward2[i]`',
                 '老鼠 1 ==恰好吃 `k` 块==，求最大总得分',
                 '本视频：`[5,2,7,1,6,3]`、`[3,6,4,4,1,5]`、`k=3` → `33`'],
        quote='先把奶酪全部给第二只老鼠，然后「撤销」其中的一块奶酪，给第一只老鼠。如何选择可以使得分最大？',
        quote_src='—— 灵茶山艾府题解',
        idea=['先从 `k=1` 想：撤销第 `i` 块，得分增加 `r1[i] − r2[i]`，选最大的',
              '推广到 `k>1`：按 `r1[i] − r2[i]` 从大到小排，取前 `k` 个',
              '代码里按 `p[1]-p[0]` 升序，前 `k` 个取 `x`，其余取 `y`'],
        after=[dict(heading='用示例走一遍', lines=['收益 `r1−r2` 依次是 `2, −4, 3, −3, 5, −2`', '从大到小：`5, 3, 2, −2, −3, −4`，取前 3 个给老鼠 1', '总分 = `sum(r2)` + 前 3 大收益 = `23 + 10` = ==33==']),],
        summary=['时间 `O(n log n)`；快速选择可优化到 `O(n)`',
                 '老鼠 1 必须==恰好== `k` 块，即使差值为负也要选满',
                 '另一种写法：`r1[i] -= r2[i]` 后原地降序排序，答案 `sum(r2) + sum(r1[:k])`',
                 '同类题：1029. 两地调度'],
    ),
)
