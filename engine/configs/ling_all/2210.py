CONFIG = dict(
    num=2210, title='统计数组中峰和谷的数量', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一次遍历 · 连续相同段去重',
    tags=[],
    code='''
class Solution:
    def countHillValley(self, nums: List[int]) -> int:
        ans = 0
        pre = nums[0]  # 上个连续相同段的元素
        for i in range(1, len(nums) - 1):
            cur = nums[i]  # 当前连续相同段的元素
            nxt = nums[i + 1]  # 下个连续相同段的元素
            if cur == nxt:  # 同一段
                continue
            # 注意 pre 可能等于 cur，比如 [1,1,2] 中 pre = cur = 1，nxt = 2
            if pre != cur and (pre < cur) == (cur > nxt):
                ans += 1
            pre = cur
        return ans
''',
    call='Solution().countHillValley([2,4,1,1,6,5,5,7])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=170, pointers={'i': 'blue'},
             color=lambda S, i, v: ('yellow' if i == S['i'] else None) if 'i' in S else None),
        dict(type='text', h=70, fn=lambda S: (f"pre=`{S['pre']}`  cur=`{S['cur']}`  nxt=`{S['nxt']}`" if 'cur' in S and 'nxt' in S else '')),
    ],
    watch=['i', ('pre', 'pre', 'cyan'), 'cur', 'nxt', ('ans', 'ans', 'green')],
    captions={
        'pre = nums[0]': '`pre` 是上一个连续相同段的元素，初始为 `nums[0]`',
        'cur = nums[i]': '`cur = {cur}`：当前段的元素',
        'nxt = nums[i + 1]': '`nxt = {nxt}`：下一个元素',
        'if cur == nxt': '`cur == nxt`（{cur} vs {nxt}）→ {"同一段，跳过，等这一段最后一个再判断（pre 不动）" if cur == nxt else "不同，当前段到头了"}',
        'if pre != cur and': '`pre = {pre}`，`cur = {cur}`，`nxt = {nxt}`：{"pre != cur 且 两边方向相同的比较结果一致" if (pre != cur and (pre < cur) == (cur > nxt)) else "不是峰也不是谷"}',
        'ans += 1': '`{pre}, {cur}, {nxt}` 构成峰或谷：`ans` → =={ans}==',
        'pre = cur': '这一段结束，`pre` 更新为 `{pre}`',
        'return ans': '一共 `{ans}` 个峰和谷',
    },
    cards=dict(
        one_liner='连续相同元素当一个，再看它比两侧都高或都低',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出数组中峰和谷的个数：最近的不相等邻居都更小是峰，都更大是谷',
                 '连续相等的下标属于同一个峰或谷，两侧必须都有不相等邻居',
                 '示例：`[2,4,1,1,6,5]` → `3`；本视频用 `[2,4,1,1,6,5,5,7]` → `4`'],
        quote='连续相同元素只需保留一个（去重），避免重复统计。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pre` 记上一段的值，`cur` 是当前段，`nxt` 是下一段',
              '`cur == nxt` 就跳过：同一段只在最后一个元素判断',
              '`(pre < cur) == (cur > nxt)`：同为真是峰，同为假是谷'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`[1,1,2]` 里 `pre == cur`，必须先判 `pre != cur`',
                 '首尾元素没有两侧，循环只跑 `1 ~ n-2`',
                 '另一种写法：用 `pairwise` 做状态机，记上一个非 `=` 的方向，方向反转就 +1'],
    ),
)
