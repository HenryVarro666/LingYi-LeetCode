def _formula(S):
    if 'right' not in S or 'ans' not in S:
        return '面积 = ==较短的侧边 × 底边=='
    l, r, h = S['left'], S['right'], S['height']
    if l >= r:
        return '无法再往内推进，结束'
    h1 = min(h[l], h[r])
    return f"`h1 = min({h[l]}, {h[r]}) = {h1}`，底边 `l = {r - l}`，面积 `h1 × l` = =={h1 * (r - l)}=="


def _short(S, B, ret):
    hl, hr = S.height[S.left], S.height[S.right]
    if hl < hr:
        return f'左边 `{hl}` 是较短的侧边（h1），右边 `{hr}` 较长'
    return f'右边 `{hr}` 不比左边 `{hl}` 长 → 右边当作较短的侧边'


def _ans(S, B, ret):
    l, r, h = S.left, S.right, S.height
    area = (r - l) * min(h[l], h[r])
    tail = '（更新！）' if S.ans != B.ans else ''
    return f'当前面积 `{r - l} × min({h[l]}, {h[r]}) = {area}`，`ans = max({B.ans}, {area}) = {S.ans}`{tail}'


CONFIG = dict(
    num=11, title='盛最多水的容器', difficulty='Medium', category='双指针',
    author='yiduobo', technique='左右往内推进较短的侧边',
    code='''
class Solution(object):
    def maxArea(self, height):
        left = 0
        right = len(height) - 1
        ans = 0
        while left < right:
            ans = max(ans, (right - left) * min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return ans
''',
    call='Solution().maxArea([1,8,6,2,5,4,8,3,7])',
    expect=49,
    views=[
        dict(type='text', fn=_formula),
        dict(type='bars', var='height', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=500,
             color=lambda S, i, v: (('cyan' if i == S['left'] else 'orange' if i == S['right'] else None)
                                    if 'right' in S and S['left'] < S['right'] else None),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'left = 0': '从最左边开始：底边最长的组合是最左 + 最右',
        'right = len': '`right = {right}`：最右边那根',
        'ans = 0': '`ans` 记录最大面积',
        'ans = max(': _ans,
        'if height[left] < height[right]': _short,
        'left += 1': '若推进较长的右边：底边变短，高度仍不超过 `h1` → 必定更差；所以==推进较短的左边==，`left` → {left}',
        'right -= 1': lambda S, B, r: (f'推进较长的一边只会更差 → ==推进较短的右边==，`right` → {S.right}'
                                       if S.right == len(S.height) - 2 else f'推进较短的右边：`right` → {S.right}'),
        'return ans': '无法再推进，返回 `ans = {ans}`',
    },
    cards=dict(
        one_liner='从最宽的底边出发，每次往内推进较短的侧边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`height[i]` 是第 `i` 根竖线的高度，选两根线和 x 轴组成容器，求最多能装多少水',
                 '水量 = ==较短的侧边 × 底边==',
                 '示例：`[1,8,6,2,5,4,8,3,7]` → `49`'],
        quote='因此当其中某一边较短时，==如果往内移动另一边，结果必定是越来越差的==，说明往内推进时需要先推进较短的那条侧边。',
        quote_src='—— yiduobo 题解原文',
        idea=['设两条侧边 `h1 ≤ h2`，底边为 `l`，面积 `h1 × l`',
              '把较长的 `h2` 往内移到 `h2"`，新底边 `l" < l`',
              '`h2" < h1`：宽高都变小；`h2" ≥ h1`：面积 `h1 × l" < h1 × l` —— 都更差'],
        summary=['时间 `O(n)`：每次推进一条边，最多 `n − 1` 次',
                 '只推进较短边：被跳过的组合都不可能更优',
                 '两边一样高时走 `else`，推进右边也没问题',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（`ans = 0 ` 行尾空格照录）'],
    ),
)
