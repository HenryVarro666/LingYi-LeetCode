CONFIG = dict(
    num=1848, title='到目标元素的最小距离', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='从左到右遍历 · 维护最小值', tags=[],
    code='''
class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        ans = inf
        for i, x in enumerate(nums):
            if x == target:
                ans = min(ans, abs(i - start))
        return ans
''',
    call='Solution().getMinDistance([1,5,3,4,2,5,5], 5, 4)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: f"`target = {S['target']}`，`start = {S['start']}`；每遇到 target 就算 `|i − start|`", size=30),
        dict(type='array', var='nums', pointers={'i': 'blue', 'start': 'pink'}, h=260,
             color=lambda S, i, v: 'green' if v == S['target'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('start', 'start', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans` 记录最小距离，先设为无穷大',
        'if x == target': lambda S, B, r: (f'`nums[{S.i}] = {S.x}` 等于 target `{S.target}` → 要算距离' if S.x == S.target
                                           else f'`nums[{S.i}] = {S.x}` 不等于 target `{S.target}` → 跳过'),
        'ans = min': '距离 `|{i} − {start}|` = {abs(i - start)}，`ans = min({B.ans}, {abs(i - start)})` = =={ans}==',
        'return ans': '题目保证 target 一定存在，`ans` 已被更新过：返回 =={ans}==',
    },
    cards=dict(
        one_liner='遇到 target 就用 |i − start| 更新最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `nums` 中找一个等于 `target` 的下标 `i`，使 `abs(i - start)` 最小',
                 '返回这个最小距离，保证 target 存在',
                 '示例：`nums=[1,2,3,4,5], target=5, start=3` → `1`'],
        quote='如果 nums[i] = target，用 |i - start| 更新答案的最小值。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['从左到右扫一遍，==每个== 等于 target 的位置都是候选',
              '候选的代价是 `|i - start|`，取最小的那个',
              '`ans` 初始为 `inf`，因为保证 target 存在，最终一定会被更新'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '别忘了 `abs`：target 可能在 start 左边，也可能在右边',
                 '写法二：一行 `min(... for ... if x == target)`；方法二：从 start 往两侧找，第一个命中的 k 就是答案',
                 '思考题：多组 (target, start) 询问时，可对每个值预存下标列表，再二分'],
    ),
)
