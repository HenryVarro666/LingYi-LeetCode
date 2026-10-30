CONFIG = dict(
    num=2530, title='执行 K 次操作后的最大分数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最大堆模拟 + 原地堆化',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1386'],
    code='''
class Solution:
    def maxKelements(self, nums: List[int], k: int) -> int:
        heapify_max(nums)  # 原地堆化
        ans = 0
        for _ in range(k):
            ans += heapreplace_max(nums, (nums[0] + 2) // 3)
        return ans
''',
    setup='heapify_max = heapq._heapify_max\nheapreplace_max = heapq._heapreplace_max',
    call='Solution().maxKelements([1,10,3,3,3], 3)',
    expect=17,
    views=[
        dict(type='heap', var='nums', label='nums（原地堆化后的最大堆，堆顶 = 当前最大值）', top_color='yellow', h=160),
        dict(type='text', fn=lambda S: f'得分 `ans` = ==`{S["ans"]}`==' if 'ans' in S else '', size=28, h=60),
    ],
    watch=[('堆顶', 'nums[0]', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'heapify_max': '原地堆化：`nums` 变成最大堆，堆顶 ==`{nums[0]}`== 是当前最大值',
        'ans = 0': '得分从 0 开始',
        'for _ in': lambda S, B, ret: (f'`k` 次操作都做完了，循环结束' if (S.get('_') is not None and S.get('_') == B.get('_')) else f'第 {S["_"] + 1} 次操作'),
        'ans += heapreplace_max': lambda S, B, ret: (f'取走堆顶 ==`{S.ans - B.ans}`== 加进得分，同时把它换成 `({S.ans - B.ans}+2)//3` = `{(S.ans - B.ans + 2) // 3}`（向上取整）并下沉：`ans` = `{B.ans} + {S.ans - B.ans}` = =={S.ans}=='),
        'return ans': '`k` 次做完，最大得分 = ==`{ret}`==',
    },
    max_steps=60,
    cards=dict(
        one_liner='每次拿最大的数加分，再把它变成三分之一（向上取整）',
        complexity='时间 `O(n + k log n)`，空间 `O(1)`',
        problem=['每次选一个 `nums[i]`：分数加 `nums[i]`，再把它换成 `ceil(nums[i]/3)`',
                 '恰好操作 `k` 次，求最大分数',
                 '本视频：`nums=[1,10,3,3,3], k=3` → ==17=='],
        quote='用一个最大堆模拟。循环 k 次，每次循环把堆顶加入答案，然后把堆顶 top 更新为 ceil(top/3) = floor((top+2)/3)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：每次加分当然选==最大的数==；选完它会变小，下一次最大值可能换人',
              '“取最大值 + 改这个值”正好是堆顶替换：`heapreplace_max`',
              '向上取整 `ceil(x/3)` 写成 `(x+2)//3`'],
        summary=['时间 `O(n + k log n)`：原地堆化 `O(n)`，每次替换堆顶 `O(log n)`；空间 `O(1)`',
                 '`heapify_max` / `heapreplace_max` 是 Python 3.14 新增的；本视频用 heapq 内部同名实现代替',
                 '`heapreplace_max` 返回的是替换前的旧堆顶，直接加到 `ans`',
                 '易错：向上取整别写成 `x//3`；同类题：1962. 移除石子使总数最小'],
    ),
)
