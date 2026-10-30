NUMS = [1, 3, 1, 2, 2, 3]


def _rr(S):
    # right 是开区间，窗口最后一个元素在 right − 1
    if 'right' not in S or 'res' not in S:
        return None
    return S['right'] - 1


def _color(S, i, v):
    if 'res' in S and S.get('_line') == 17 and i >= S['right'] - 1:
        return 'green'
    return None


def _top(S):
    if 'res' not in S:
        return '先用集合求出不同数字的个数 distinct'
    l, r, n = S['left'], S['right'], len(S['nums'])
    if S.get('_line') == 17:
        return f"左边界 {l}：右端点取 `{r - 1}..{n - 1}` 都合法 → =={n - r + 1}== 个"
    return f"窗口 `nums[{l}:{r}]` = `{S['nums'][l:r]}`，{len(S['cnt'])} / {S['distinct']} 种"


CONFIG = dict(
    num=2799, title='统计完全子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左边界 · 最小右边界单调右移',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def countCompleteSubarrays(self, nums):

        distinct = len(set(nums))
        cnt = {}
        left = 0
        right = 0
        res = 0
        while left < len(nums):
            while right < len(nums) and len(cnt) < distinct:
                cnt[nums[right]] = cnt.get(nums[right], 0) + 1
                right += 1

            if len(cnt) < distinct:
                break

            res += len(nums) - right + 1
            cnt[nums[left]] -= 1
            if cnt[nums[left]] == 0:
                cnt.pop(nums[left])
            left += 1
        
        return res
''',
    call=f'Solution().countCompleteSubarrays({NUMS})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, right−1]，绿 = 合法右端点）',
             pointers={'left': 'blue', _rr: 'pink'}, pointer_labels={_rr: 'right−1'}, window=('left', _rr),
             color=_color, cell=110, h=280),
        dict(type='map', var='cnt', label='cnt（窗口内每个数字的次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('distinct', 'distinct', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    skip=['left = 0', 'right = 0'],
    captions={
        'distinct = len(set(nums))': '用集合求出不同数字有 `distinct = {distinct}` 种',
        'cnt = {}': '`cnt` 统计窗口内每种数字的次数',
        'res = 0': '`left`、`right = 0`，`right` 指向窗口==下一个==位置',
        'while left < len(nums)': lambda S, B, r: ('`left < n`，继续' if S.left < len(S.nums) else '`left` 到末尾，结束'),
        'while right < len(nums)': lambda S, B, r: (f'窗口只有 {len(S.cnt)} 种 < {S.distinct} → 右边界扩展' if S.right < len(S.nums) and len(S.cnt) < S.distinct
                                                    else (f'窗口已有 {S.distinct} 种 → 找到最小右边界 `right − 1 = {S.right - 1}`' if len(S.cnt) == S.distinct
                                                          else '右边界到头了')),
        'cnt[nums[right]] = cnt.get': '`{nums[right]}` 进入窗口：`cnt[{nums[right]}]` → {cnt[nums[right]]}',
        'right += 1': '`right` → {right}',
        'if len(cnt) < distinct': lambda S, B, r: ('凑不齐：以后的左边界更凑不齐 → 结束' if len(S.cnt) < S.distinct else '种类齐了，可以计数'),
        'break': '跳出循环',
        'res += len(nums)': '右端点在 `{right - 1}..{len(nums) - 1}` 都合法：`{len(nums)} − {right} + 1` 个 → `res` = =={res}==',
        'cnt[nums[left]] -= 1': '左边界 `{nums[left]}` 移出窗口：`cnt[{nums[left]}]` → {cnt[nums[left]]}',
        'if cnt[nums[left]] == 0': lambda S, B, r: (f'{S.nums[S.left]} 没了，种类减少' if S.cnt[S.nums[S.left]] == 0 else f'窗口里还有 {S.nums[S.left]}，种类不变 → 右边界不用动'),
        'cnt.pop(nums[left])': '删掉 `{nums[left]}` → 只剩 {len(cnt)} 种',
        'left += 1': '左边界右移 → `left = {left}`',
        'return res': '一共 =={ret}== 个完全子数组',
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举左边界，最小右边界只会右移：每次加 n − right + 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['==完全子数组==：不同元素个数 = 整个 `nums` 的不同元素个数',
                 '求完全子数组的个数',
                 '示例：`[1,3,1,2,2]` → `4`；`[5,5,5,5]` → `10`',
                 f'本视频：`{NUMS}` → `7`'],
        quote='当窗口的左边界left向右移动时，其对应的最小右边界right必然大于等于之前轮次的最小右边界，这样一来就可以在均摊O(1)的时间内找出所有当前left对应的right。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用集合求出种类数 k，问题变成“含 k 种数字的子数组个数”',
              '对每个左边界，扩展右边界直到种类凑齐',
              '最小右边界之后的右端点==都合法==，一次全部计入'],
        summary=['时间 `O(n)`：left、right 都只右移',
                 '代码里 right 是==开区间==，最小右端点是 `right − 1`，所以是 `n − right + 1`',
                 '凑不齐时直接 `break`：左边界再右移只会更少',
                 '对比灵神：灵神枚举右端点 `ans += left`；这里枚举左端点',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
