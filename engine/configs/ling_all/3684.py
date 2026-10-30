CONFIG = dict(
    num=3684, title='至多 K 个不同元素的最大和', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='去重 + nlargest',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def maxKDistinct(self, nums: list[int], k: int) -> list[int]:
        return nlargest(k, set(nums))
''',
    setup='from heapq import nlargest',
    call='Solution().maxKDistinct([84,93,100,77,93], 3)',
    expect=[100, 93, 84],
    views=[
        dict(type='text', size=34, fn=lambda S: f"去重后的集合：`{sorted(set(S['nums']), reverse=True)}`（从大到小）" if 'nums' in S else ''),
        dict(type='array', var='nums', h=260, label='nums（有重复的 93）',
             color=lambda S, i, v: 'yellow' if S['nums'].count(v) > 1 else None),
        dict(type='text', size=34, fn=lambda S: f"取最大的 `k = {S['k']}` 个：=={sorted(set(S['nums']), reverse=True)[:S['k']]}==" if 'nums' in S else ''),
    ],
    watch=['k', ('去重大小', 'len(set(nums))', 'cyan')],
    captions={
        'return nlargest': '`set(nums)` 去重得到 `{sorted(set(nums), reverse=True)}`，`nlargest({k}, ...)` 取最大的 {k} 个（从大到小）→ =={ret}==，和为 `{sum(ret)}`',
    },
    cards=dict(
        after=[dict(heading='另一种写法', lines=['`a = sorted(set(nums), reverse=True)`：去重 + 降序排序',
                                              '`return a[:k]`：切片取前 `k` 个',
                                              '`k` 比 `a` 的长度大也没关系，切片不会越界',
                                              '瓶颈是排序，`O(n log n)`；`nlargest` 用堆，`O(n log k)`'])],
        one_liner='先去重，再取最大的 k 个：数越大和越大',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['选至多 `k` 个互不相同的数，使和最大，按从大到小返回',
                 '示例：`[84,93,100,77,93], k=3` → `[100,93,84]`',
                 '两个 `93` 只能选一个'],
        quote='题意：选出最大的 min(k,n) 个不同的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数全是正数，选得越多和越大 → 能选满 `k` 个就选满',
              '互不相同 → 先用 `set` 去重',
              '再取最大的 `k` 个：`nlargest(k, set(nums))`，结果已是严格递减'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '不同数不足 `k` 个时，`nlargest` 自动返回全部，不用特判',
                 '写法二：`sorted(set(nums), reverse=True)[:k]`（去重+排序再切片）',
                 '这里的 `nlargest` 来自 `heapq`，已在 setup 里 import'],
    ),
)
