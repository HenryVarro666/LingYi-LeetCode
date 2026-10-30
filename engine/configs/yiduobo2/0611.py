def _live(S):
    return all(x in S for x in ('left', 'right', 'index')) and S['left'] < S['right'] < S['index']


def _color(S, idx, v):
    if 'index' not in S:
        return None
    if idx == S['index']:
        return 'orange'
    if S.get('_line') == 11 and _live(S) and S['left'] <= idx < S['right']:
        return 'green'  # (left, right) ... (right-1, right) 都可行
    return None


def _formula(S):
    if not _live(S):
        if 'index' in S:
            return f"长边 `l = nums[{S['index']}] = {S['nums'][S['index']]}`：在它左边找和 ==大于 l== 的数对"
        return '两条短边之和 ==大于== 长边，就是有效三角形'
    a, b, c = S['nums'][S['left']], S['nums'][S['right']], S['nums'][S['index']]
    rel = '>' if a + b > c else '≤'
    return f"`nums[left] + nums[right] = {a} + {b} = {a + b}` {rel} `{c}`" + (' → ==可行==' if a + b > c else ' → 不够长')


def _cmp(S, B, ret):
    a, b, c = S.nums[S.left], S.nums[S.right], S.nums[S.index]
    if a + b > c:
        return f'`{a} + {b} = {a + b} > {c}`：nums 单调递增，`left` 换成更大的数也一定可行'
    return f'`{a} + {b} = {a + b} ≤ {c}`：`nums[left] = {a}` 不够长，和 `nums[right]` 组不成三角形'


CONFIG = dict(
    num=611, title='有效三角形的个数', difficulty='Medium', category='双指针',
    author='yiduobo', technique='排序 · 从大到小枚举长边 · 两数之和式双指针',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def triangleNumber(self, nums):
        nums = sorted(nums)
        res = 0

        for index in range(len(nums) - 1, 1, -1):
            left = 0
            right = index - 1
            while left < right:
                if nums[left] + nums[right] > nums[index]:
                    res += right - left
                    right -= 1
                else:
                    left += 1

        return res
''',
    call='Solution().triangleNumber([3, 6, 2, 4, 2])',
    expect=4,
    views=[
        dict(type='text', h=70, size=28, fn=_formula),
        dict(type='array', var='nums', h=360, cell=130, label='nums（排序后；橙 = 当前长边，灰 = 已枚举过的长边）',
             pointers={'left if left < right else None': 'blue', 'right if left < right else None': 'pink', 'index': 'orange'},
             pointer_labels={'left if left < right else None': 'left', 'right if left < right else None': 'right', 'index': 'index'},
             color=_color, dim=lambda S, idx, v: 'index' in S and idx > S['index']),
    ],
    watch=[('index', 'index', 'orange'), ('长边', 'nums[index]', 'orange'), ('left', 'left', 'blue'),
           ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums = sorted(nums)': '先把所有边排序：之后才能利用==单调性==',
        'res = 0': '`res` 统计可行的三元组个数',
        'for index in range': lambda S, B, r: ('长边枚举完毕（至少要留两条短边）' if getattr(B, 'index', None) == S.index
                                               else f'==从大到小==枚举长边：`nums[{S.index}] = {S.nums[S.index]}`'),
        'left = 0': '在比长边小的数里找数对：`left` 从最左边开始',
        'right = index - 1': '`right` 从长边左边一个开始：`right = {right}`',
        'while left < right': lambda S, B, r: ('`left < right`，继续' if S.left < S.right
                                               else f'`left`、`right` 相遇：长边 `{S.nums[S.index]}` 处理完毕'),
        'if nums[left] + nums[right] > nums[index]': _cmp,
        'res += right - left': '`(left, right)` … `(right − 1, right)` 都可行 → 次长边选 `nums[{right}]` 共 `{right - left}` 组，`res = {res}`',
        'right -= 1': '选 `nums[{right + 1}]` 当次长边的情况处理完了 → `right` 左移到 {right}',
        'left += 1': '`nums[left]` 不够长 → `left` 右移到 {left}',
        'return res': '一共 `{ret}` 个有效三角形',
    },
    cards=dict(
        one_liner='排序后从大到小枚举长边，用两数之和的双指针找短边',
        complexity='时间 `O(n²)`，空间 `O(n)`（`sorted` 生成新数组）',
        problem=['给定非负整数数组 `nums`，返回能组成三角形三条边的三元组个数',
                 '示例：`[2,2,3,4]` → `3`（`2,3,4` 用两个不同的 2 各算一次）',
                 '本视频：`[3,6,2,4,2]` → `4`'],
        quote='若nums[left] + nums[right] > l，由于现在nums是单调递增的，因此现在(left, right)，(left + 1, right)，... (right - 1, right)都是可行的组合……一共有right - left组可行的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['有效三角形 = ==两条短边之和大于长边==；排序后从大到小枚举长边 `l`',
              '在 `l` 左边找和 `> l` 的数对，和「两数之和」一样用左右指针',
              '`> l`：次长边选 `nums[right]` 的 `right − left` 组全部可行，`right` 左移；否则 `left` 右移'],
        summary=['时间 `O(n²)`：枚举长边 `O(n)` × 双指针 `O(n)`',
                 '易错：一次加 `right − left` 组，而不是只加 1',
                 '`right` 从 `index − 1` 开始，长边本身不能再当短边',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神多了两个剪枝（最小两边已够大直接加组合数、最大两边不够就跳过）'],
    ),
)
