CONFIG = dict(
    num=2875, title='无限数组的最短子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='三段拆分 · 中间整除 + 两倍数组滑窗',
    tags=['滑动窗口与双指针', '难度分 1914'],
    code='''
class Solution(object):
    def minSizeSubarray(self, nums, target):

        s = sum(nums)
        n = len(nums)
        res = target // s * n
        target %= s
        if target == 0:
            return res

        left = 0
        right = 0
        now = 0
        need_fill = None
        while right < n + n:
            while right < n + n and now < target:
                now += nums[right % n]
                right += 1

            if now < target:
                break

            while now > target:
                now -= nums[left % n]
                left += 1

            if now == target:
                if need_fill is None or need_fill > right - left:
                    need_fill = right - left
                now -= nums[left % n]
                left += 1

        if need_fill is None:
            return -1

        return need_fill + res
''',
    call='Solution().minSizeSubarray([1,2,1,3,1], 20)',
    expect=12,
    views=[
        dict(type='array', var=lambda S: S['nums'] * 2, label='nums + nums（框 = 窗口 [left, right)）', cell=84, h=250,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', lambda S: S['right'] - 1),
             dim=lambda S, i, v: 'right' in S and 'left' in S and not (S['left'] <= i < S['right'])),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"中间部分 `res` = ==`{S['res']}`== 个元素；两端要凑的和 target = ==`{S['target']}`==" if 'res' in S and 'target' in S and 's' in S else '')),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 now = ==`{S['now']}`==，目标 target = `{S['target']}`" if 'now' in S and 'right' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('now', 'now', 'cyan'), ('target', 'target', 'yellow'), ('res', 'res', 'purple'), ('need_fill', 'need_fill', 'green')],
    captions={
        's = sum': '整组的和 `s = {s}`',
        'res = target': '中间的完整 `nums` 有 `target // s = {target // s}` 组 → 贡献 `res = {res}` 个元素',
        'target %= s': '两端只需凑 `target % s = {target}`，滑窗的目标缩小成它',
        'if target == 0': lambda S, B, r: ('`target == 0`：正好是整组，直接返回 `res`' if S.target == 0 else f'`target = {S.target}` 不为 0：还要找两端的窗口'),
        'need_fill = None': '`need_fill` 记录两端最短窗口，`None` 表示还没找到',
        'while right < n + n:': lambda S, B, r: (f'`right = {S.right} < {2 * S.n}`：两倍数组还没扫完' if S.right < 2 * S.n else f'`right = {S.right}` 到头了：结束'),
        'while right < n + n and now < target': lambda S, B, r: (f'`now = {S.now} < target = {S.target}`：窗口和不够，右边界继续扩' if S.now < S.target and S.right < 2 * S.n else f'`now = {S.now}`：不用再扩了'),
        'now += nums': '`nums[{right % n}] = {nums[right % n]}` 进窗口：`now = {now}`',
        'if now < target': lambda S, B, r: (f'`now = {S.now} < target`：右边到头了还不够，后面不可能再有解 → 跳出' if S.now < S.target else f'`now = {S.now} >= target`：和够了，可以收左边界'),
        'while now > target': lambda S, B, r: (f'`now = {S.now} > target = {S.target}`：窗口和超了，缩左边界' if S.now > S.target else f'`now = {S.now} <= target`：不用缩了'),
        'now -= nums[left': '`nums[{left % n}] = {nums[left % n]}` 被移出窗口：`now = {now}`',
        'right += 1': '`right` → {right}（窗口是左闭右开 `[left, right)`）',
        'left += 1': '`left` → {left}',
        'if now == target': lambda S, B, r: (f'`now == target = {S.target}`：窗口和恰好等于目标，窗口长度 `{S.right - S.left}`' if S.now == S.target else f'`now = {S.now} != target`：这一轮没有合法窗口'),
        'if need_fill is None or': lambda S, B, r: ((f'还没有记录（None）：直接记下长度 `{S.right - S.left}`' if S.need_fill is None else f'已有 `{S.need_fill}` > 当前 `{S.right - S.left}`：更短，更新') if S.need_fill is None or S.need_fill > S.right - S.left else f'已有 `{S.need_fill}` <= `{S.right - S.left}`：不更新'),
        'need_fill = right - left': '`need_fill = {right - left}`',
        'break': '跳出循环',
        'if need_fill is None': lambda S, B, r: ('一直没找到窗口 → 返回 -1' if S.need_fill is None else f'找到了窗口，`need_fill = {S.need_fill}`'),
        'return need_fill + res': '`need_fill + res` = `{need_fill} + {res}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='整除先把中间的整组算掉，两端的和在两倍数组里滑窗',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 无限重复拼接，找和等于 `target` 的最短子数组长度，没有返回 -1',
                 '示例：`nums=[1,1,1,2,3], target=4` → `2`',
                 '本视频：`[1,2,1,3,1], target=20` → `12`'],
        quote='这个子数组可以拆分成三个部分，分别是左侧的某个nums的后缀，中部的若干个完整的nums，以及右侧的某个nums的前缀',
        quote_src='—— yiduobo 题解原文',
        idea=['中间部分：`target` 整除 `sum(nums)` 得到整组数，乘 `n` 就是它的长度',
              '左右两段：在重复一次的数组里，找和等于 `target % sum` 的最短子数组',
              '先扩右边界直到和够，再缩左边界到不超；相等就更新答案，并把左边界再右移一步继续找'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`target % s == 0` 时直接返回中间部分 `res`',
                 '右边界到头仍 `now < target` 要 `break`，否则会死循环',
                 '原文为 Python 2 写法，`res = target / s * n` 的整数除法已改为 `//`',
                 '对比灵神：灵神 `right` 为闭区间且边扫边缩；这里 `right` 是开区间，分「扩」「缩」两段写'],
    ),
)
