CONFIG = dict(
    num=3066, title='超过阈值的最少操作数 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆模拟 + 直接改堆顶',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1400'],
    code='''
class Solution:
    def minOperations(self, h: List[int], k: int) -> int:
        heapify(h)
        ans = 0
        while h[0] < k:
            x = heappop(h)
            heapreplace(h, h[0] + x * 2)
            ans += 1
        return ans
''',
    call='Solution().minOperations([2,11,10,1,3], 10)',
    expect=2,
    views=[
        dict(type='heap', var='h', label='h（最小堆，堆顶 = 当前最小值）', top_color='yellow', h=160),
        dict(type='text', fn=lambda S: f'堆顶 `{S["h"][0]}` {"<" if S["h"][0] < S["k"] else ">="} `k = {S["k"]}`' if S.get('h') and S['_line'] in (5, 7) else '', size=28, h=60),
    ],
    watch=[('x', 'x', 'pink'), ('堆顶', 'h[0]', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'heapify(h)': '堆化：堆顶 ==`{h[0]}`== 是最小的数',
        'ans = 0': '操作次数从 0 开始',
        'while h[0] < k': lambda S, B, ret: (f'最小值 `{S["h"][0]}` < `{S.k}`，还有数不够大，继续操作' if S['h'][0] < S.k else f'最小值 `{S["h"][0]}` >= `{S.k}`，==所有数都 >= k==，结束'),
        'x = heappop(h)': '弹出最小的数 `x` = ==`{x}`==；次小的数 `{h[0]}` 现在在堆顶',
        'heapreplace': '新数 = `min*2 + max` = `{x}*2 + {B.h[0]}` = ==`{x * 2 + B.h[0]}`==；直接替换堆顶（次小的数 `{B.h[0]}` 被弹出）并下沉',
        'ans += 1': '做完一次操作：`ans` = ==`{ans}`==',
        'return ans': '最小值已经 >= `k`，共操作 ==`{ret}`== 次',
    },
    max_steps=60,
    cards=dict(
        one_liner='每次合并最小的两个数，用最小堆模拟',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次选最小的两个数 `x ≤ y`，删掉并加入 `x*2 + y`',
                 '求让所有数都 `>= k` 的最少操作次数',
                 '本视频：`nums=[2,11,10,1,3], k=10` → ==2=='],
        quote='每次选择最小的两个数操作，这可以用最小堆模拟。如果最小值 ≥ k，那么所有数都 ≥ k。所以循环直到堆顶 ≥ k 为止。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题目规定了每次操作的对象：==最小的两个数==，所以只需要一直取最小值',
              '堆顶 `>= k` 就说明所有数都够大，这是循环的终止条件',
              '弹出 `x` 后，堆顶就是次小数 `y`：用 `heapreplace` 把它直接换成 `y + 2x`，省一次弹出再压入'],
        summary=['时间 `O(n log n)`：每次循环堆里少一个数，最多 `n` 轮，每轮 `O(log n)`',
                 '空间：把输入当堆原地操作，额外空间 `O(1)`',
                 '题目保证有解，所以不会出现堆里只剩一个且小于 `k` 的情况',
                 '易错：新数是 `min*2 + max`，弹出的第一个数才是 `min`',
                 '同类题：2233. K 次增加后的最大乘积'],
    ),
)
