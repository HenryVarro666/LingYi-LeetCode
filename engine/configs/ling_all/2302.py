CONFIG = dict(
    num=2302, title='统计得分小于 K 的子数组数目', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑窗 · 越短越合法',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1808'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        ans = s = left = 0
        for right, x in enumerate(nums):
            s += x
            while s * (right - left + 1) >= k:
                s -= nums[left]
                left += 1
            ans += right - left + 1
        return ans
''',
    call='Solution().countSubarrays([2,1,4,3,5], 10)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, right]）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), cell=100, h=240,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"窗口分数 = `{S['s']}` × `{S['right']-S['left']+1}` = =={S['s']*(S['right']-S['left']+1)}==，k = {S['k']}"
                           if 'right' in S and 's' in S else '窗口为空：s = 0，left = 0')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = left': '`ans`（答案）、`s`（窗口和）、`left`（窗口左端点）都从 0 开始',
        's += x': '`nums[{right}] = {x}` 进入窗口，窗口和 `s` = =={s}==',
        'while s *': lambda S, B, r: (f'分数 `{S.s} × {S.right - S.left + 1} = {S.s * (S.right - S.left + 1)}` ≥ `{S.k}` → ==窗口太大==，要缩小'
                                      if S.s * (S.right - S.left + 1) >= S.k
                                      else f'分数 `{S.s} × {S.right - S.left + 1} = {S.s * (S.right - S.left + 1)}` < `{S.k}` → 窗口合法，停止缩小'),
        's -= nums[left]': '移出左端点 `nums[{left}] = {nums[left]}`：`s` 变为 {s}',
        'left += 1': '`left` → {left}。元素全为正，缩短窗口分数一定变小',
        'ans += right': '右端点固定为 {right} 时，左端点可取 `{left}..{right}`，共 `{right} - {left} + 1` = =={right - left + 1}== 个合法子数组；`ans` = {ans}',
        'return ans': '统计完毕，一共 `{ans}` 个',
    },
    cards=dict(
        one_liner='枚举右端点，窗口越短分数越低：缩到合法后一次数 right-left+1 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['分数 = 子数组元素和 × 长度。数正整数数组 `nums` 中，分数 ==严格小于 k== 的非空子数组个数',
                 '示例：`nums=[2,1,4,3,5]`，`k=10` → `6`'],
        quote='本题元素均为正数，所以子数组越长，分数越高；子数组越短，分数越低。这意味着只要某个子数组的分数小于 k，在该子数组内的更短的子数组，分数也小于 k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有单调性才能用滑窗：元素为正 → 窗口越长分数越大',
              '枚举右端点 `right`，分数 `>= k` 就不断移出左端点',
              '合法后，以 `right` 结尾的合法子数组恰好有 `right-left+1` 个，之前的右端点已统计过，不重复'],
        summary=['时间 `O(n)`：`left` 只增不减，内层循环总共执行不超过 n 次',
                 '分数是 `s * 长度`，注意是 `>= k` 才缩窗（严格小于才合法）',
                 '`s * (right-left+1)` 可达 10^10 以上，Python 不怕溢出，其他语言要用 64 位',
                 '思考题：改成平均数 `< k` 时不再有这个单调性，需另想办法'],
    ),
)
