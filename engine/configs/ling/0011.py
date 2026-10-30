CONFIG = dict(
    num=11, title='盛最多水的容器', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='相向双指针',
    code='''
class Solution:
    def maxArea(self, height: List[int]) -> int:
        ans = left = 0
        right = len(height) - 1
        while left < right:
            area = (right - left) * min(height[left], height[right])
            ans = max(ans, area)
            if height[left] < height[right]:
                # height[left] 与右边的任意垂线都无法组成一个比 ans 更大的面积
                left += 1
            else:
                # height[right] 与左边的任意垂线都无法组成一个比 ans 更大的面积
                right -= 1
        return ans
''',
    call='Solution().maxArea([1,8,6,2,5,4,8,3,7])',
    expect=49,
    views=[
        dict(type='text', fn=lambda S: f"当前两根线：`({S['right']} − {S['left']}) × min({S['height'][S['left']]}, {S['height'][S['right']]})` = =={(S['right']-S['left'])*min(S['height'][S['left']], S['height'][S['right']])}==" if 'right' in S and S['left'] < S['right'] else ('两指针相遇，结束' if 'right' in S else '')),
        dict(type='bars', var='height', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=470,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'area', ('ans', 'ans', 'green')],
    captions={
        'right = len': '`right = len(height) - 1 = {right}`：==注意是 len - 1==，否则越界',
        'area = (': '当前容器：宽 `{right - left}` × 高 `min({height[left]}, {height[right]})` = =={area}==',
        'ans = max': '`ans = max({B.ans}, {area}) = {ans}`' ,
        'left += 1': '左边更矮：它和右边任何线都组不出更大面积 → 扔掉，`left` 右移到 {left}',
        'right -= 1': '右边不更高：它和左边任何线都组不出更大面积 → 扔掉，`right` 左移到 {right}',
    },
    cards=dict(
        one_liner='每次扔掉较矮的那根线，它已经不可能组成更大的容器',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`height[i]` 是第 `i` 根竖线的高度，选两根线和 x 轴组成容器，求最多能装多少水',
                 '水量 = ==较矮的高度 × 两线距离==：`min(height[l], height[r]) * (r - l)`',
                 '示例：`[1,8,6,2,5,4,8,3,7]` → `49`'],
        quote='当 `height[left] < height[right]`：==height[left] 与右边的任意垂线都无法组成一个比 ans 更大的面积==，所以 `left += 1`。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['以矮线为一端的其他容器：==宽度更小==，高度 ==不超过矮线== → 面积只会更小',
              '每比较一次就安全删掉一根线，最多删 `n-1` 次'],
        summary=['`right = len(height) - 1`，不是 `len(height)`',
                 '==先用 area 更新 ans，再按高度移动较矮一端==；不要用 `area > ans` 决定移动哪边',
                 '相等时移动哪边都行'],
    ),
)
