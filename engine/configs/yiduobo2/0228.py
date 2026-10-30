NUMS = [0, 2, 3, 4, 6, 8, 9]


def _idx(S):
    """for num in nums[1:] 没有下标：值互不相同且有序，用 nums.index 找回位置"""
    if 'num' in S and S['num'] in NUMS:
        return NUMS.index(S['num'])
    return None


def _color(S, i, v):
    if 'left' not in S or 'now' not in S:
        return None
    if S['left'] <= v <= S['now']:
        return 'cyan'  # 当前区间
    if v < S['left']:
        return 'green'  # 已经输出
    k = _idx(S)
    if k is not None and i == k:
        return 'orange'
    return None


def _text(S):
    if 'left' not in S or 'now' not in S:
        return ''
    l, n = S['left'], S['now']
    cur = f'"{l}"' if l == n else f'"{l}->{n}"'
    return f"当前区间 `[left, now] = [{l}, {n}]`，输出时写成 `{cur}`"


def _cap_if(S, B, ret):
    num, now = S.num, B.now
    if num == now + 1:
        return f'`num = {num} == now + 1 = {now + 1}`：==连上了== → 区间右边界加一'
    return f'`num = {num} ≠ now + 1 = {now + 1}`：==断开了== → 先输出当前区间 `[{B.left}, {now}]`'


def _cap_single(S, B, ret):
    if B.now == B.left:
        return f'`now == left = {B.left}`：==只有一个数==的区间'
    return f'`left = {B.left} ≠ now = {B.now}`：区间里有多个数'


CONFIG = dict(
    num=228, title='汇总区间', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='一趟扫描：连上就扩右边界，断开就输出',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def summaryRanges(self, nums):
        if not nums:
            return []

        left = now = nums[0]
        res = []
        for num in nums[1:]:
            if num == now + 1:
                now += 1
            else:
                if now == left:
                    res.append(str(left))
                else:
                    res.append("%d->%d" % (left, now))
                now = left = num

        if now == left:
            return res + [str(left)]
        else:
            return res + ["%d->%d" % (left, now)]
''',
    call=f'Solution().summaryRanges({NUMS})',
    expect=['0', '2->4', '6', '8->9'],
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='array', var='nums', label='nums（青 = 当前区间 [left, now]，绿 = 已输出，橙 = 当前 num）', cell=96, h=200,
             pointers={_idx: 'orange'}, pointer_labels={_idx: 'num'}, color=_color),
        dict(type='array', var='res', label='res（已经输出的区间）', cell=150, h=170),
    ],
    watch=[('left', 'left', 'cyan'), ('now', 'now', 'cyan'), ('num', 'num', 'orange'), 'res'],
    captions={
        'if not nums': '先处理空数组：`nums` 非空，继续',
        'left = now = nums[0]': '当前区间从第一个数开始：`left = now = {left}`',
        'res = []': '`res` 存放汇总好的区间字符串',
        'for num in nums[1:]': lambda S, B, ret: (f'从第二个数开始扫描：`num = {S.num}`' if 'num' not in B
                                                   else f'下一个数 `num = {S.num}`' if S.get('num') != B.get('num')
                                                   else '扫描结束，但==最后一个区间还没输出=='),
        'if num == now + 1': _cap_if,
        'now += 1': '`now` → {now}，区间变成 `[{left}, {now}]`',
        12: _cap_single,
        'res.append(str(left))': '单个数直接写成 `"{left}"`',
        'res.append("%d->%d"': '多个数写成 `"{left}->{now}"`',
        'now = left = num': '从 `num` 开一个新区间：`left = now = {now}`',
        18: _cap_single,
        'return res + [str(left)]': '补上最后一个区间 `"{left}"`，返回 `{ret}`',
        'return res + ["%d->%d"': '补上最后一个区间 `"{left}->{now}"`，返回 `{ret}`',
    },
    cards=dict(
        one_liner='一趟扫描：连续就把右边界加一，断开就输出当前区间',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['`nums` 是==有序且无重复==的整数数组，用最少的区间覆盖所有数',
                 '区间 `[a,b]` 写成 `"a->b"`，`a == b` 时写成 `"a"`',
                 '示例：`[0,1,2,4,5,7]` → `["0->2","4->5","7"]`',
                 '本视频：`[0,2,3,4,6,8,9]` → `["0","2->4","6","8->9"]`'],
        quote='从左往右一趟扫描，若当前的数字等于上一个数字，那么将区间的右边界加一，否则输出当前区间即可。==需要注意只有一个数的区间==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`[left, now]` 是正在延伸的区间；`num == now + 1` 说明和上一个数连续',
              '断开时输出 `[left, now]`，再从 `num` 开新区间',
              '`left == now` 时只有一个数，格式不同'],
        summary=['时间 `O(n)`，空间 `O(1)`（`nums[1:]` 切片另占 `O(n)`）',
                 '易错：==循环结束后还要补上最后一个区间==',
                 '易错：单个数输出 `"7"` 而不是 `"7->7"`',
                 '空数组要特判，否则 `nums[0]` 越界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
