PALETTE = ['cyan', 'purple', 'orange', 'green']


def _color(S, i, v):
    parts = S.get('parts', [])
    ln = S.get('_line', 0)
    if 17 <= ln <= 22 and 'x2' in S and 'y2' in S:
        if S['x1'] <= i <= S['y1']:
            return 'cyan'
        if S['x2'] <= i <= S['y2']:
            return 'orange'
        return None
    for k, (a, b) in enumerate(parts):
        if a <= i <= b:
            return PALETTE[k % len(PALETTE)]
    return None


def _top(S):
    ln = S.get('_line', 0)
    parts = S.get('parts')
    if parts is None:
        return '先把数组切成尽可能长的非递减段，再看相邻两段能不能靠一次修改连起来'
    if ln < 17 or ln > 22:
        return f'已切出的段（闭区间）：`{parts}`'
    return f'段：`{parts}`；现在看相邻两段 `[{S.get("x1")}, {S.get("y1")}]` 和 `[{S.get("x2", "?")}, {S.get("y2", "?")}]`'


CONFIG = dict(
    num=3738, title='替换至多一个元素后最长非递减子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='切段 · 相邻两段能否一次修改连接',
    tags=['分组循环', '状态机 DP', '难度分 1811'],
    code='''
class Solution(object):
    def longestSubarray(self, nums):

        parts = []
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] >= nums[q - 1]:
                q += 1
            parts.append([p, q - 1])
            p = q
        
        if len(parts) == 1:
            return len(nums)
    
        x1, y1 = parts[0]
        res = y1 - x1 + 2
        for x2, y2 in parts[1:]:
            res = max(res, y2 - x2 + 2)
            if (y1 > x1 and nums[y1 - 1] <= nums[x2]) or (x2 < y2 and nums[x2 + 1] >= nums[y1]):
                res = max(res, y2 - x1 + 1)
            x1, y1 = x2, y2

        return res
''',
    call='Solution().longestSubarray([1,2,5,3,4,2,6])',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='nums', label='nums（同色 = 同一段非递减子数组）', cell=96, h=330,
             pointers={'p if _line < 16 else None': 'blue', 'q if _line < 16 else None': 'pink'},
             pointer_labels={'p if _line < 16 else None': 'p', 'q if _line < 16 else None': 'q'},
             color=_color),
        dict(type='text', fn=lambda S: (f"`res = {S['res']}`" if 'res' in S else ''), size=26, h=50),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'parts = []': '`parts`：每一段尽可能长的非递减子数组，记成闭区间 `[起点, 终点]`',
        'p = 0': '`p`：当前这一段的起点',
        'while p < len(nums)': lambda S, B, r: (f'`p = {S.p} < {len(S.nums)}`，还有新的一段要切' if S.p < len(S.nums) else f'`p = {S.p}`：切完了，共 `{len(S.parts)}` 段'),
        'q = p + 1': '`q` 从 `p + 1` 开始往右扩',
        'while q < len(nums) and': lambda S, B, r: ((f'`nums[{S.q}] = {S.nums[S.q]} ≥ nums[{S.q - 1}] = {S.nums[S.q - 1]}` → 还是非递减，继续扩')
                                                    if S.q < len(S.nums) and S.nums[S.q] >= S.nums[S.q - 1]
                                                    else (f'`nums[{S.q}] = {S.nums[S.q]} < nums[{S.q - 1}] = {S.nums[S.q - 1]}` → 断开' if S.q < len(S.nums) else '到数组末尾了')),
        'q += 1': '`q` → {q}',
        'parts.append': '这一段是 `[{p}, {q - 1}]`：`parts = {parts}`',
        'p = q': '下一段从 `q = {q}` 开始',
        'if len(parts) == 1': lambda S, B, r: ('只有一段：数组本来就非递减，不用改' if len(S.parts) == 1 else f'有 `{len(S.parts)}` 段，需要靠修改来拼接'),
        'return len(nums)': '整个数组本来就是非递减的 → 返回 `{len(nums)}`',
        'x1, y1 = parts[0]': '`[x1, y1]` = 第一段 `{parts[0]}`',
        'res = y1 - x1 + 2': '一段再加 1 个：把相邻的一个数改成合适的值接上去 → `res = {y1} - {x1} + 2 = {res}`',
        'for x2, y2': lambda S, B, r: (f'看下一段 `[{S.x2}, {S.y2}]`，它的前一段是 `[{S.x1}, {S.y1}]`' if 'x2' not in B or (S.x2, S.y2) != (B.x2, B.y2) or S.x1 != B.x1 else '所有相邻两段都看完了'),
        'res = max(res, y2 - x2 + 2)': '这一段单独改一个相邻的数：`res = max({B.res}, {y2} - {x2} + 2) = {res}`',
        'if (y1 > x1': lambda S, B, r: (
            (f'前段末尾 `nums[{S.y1 - 1}] = {S.nums[S.y1 - 1]}` ≤ 后段开头 `nums[{S.x2}] = {S.nums[S.x2]}` → 前段最后一个数改成 `nums[{S.y1 - 1}]` 就 ==能连起来=='
             if S.y1 > S.x1 and S.nums[S.y1 - 1] <= S.nums[S.x2] else
             (f'后段第二个数 `nums[{S.x2 + 1}] = {S.nums[S.x2 + 1]}` ≥ 前段末尾 `nums[{S.y1}] = {S.nums[S.y1]}` → 后段开头改成 `nums[{S.y1}]` 就 ==能连起来=='
              if S.x2 < S.y2 and S.nums[S.x2 + 1] >= S.nums[S.y1] else '改前段末尾或后段开头都连不起来'))),
        'res = max(res, y2 - x1 + 1)': '两段连成一段：长度 `{y2} - {x1} + 1 = {y2 - x1 + 1}`，`res = {res}`',
        'x1, y1 = x2, y2': '当前段变成下一轮的“前一段”：`[x1, y1] = [{x1}, {y1}]`',
        'return res': '最长非递减子数组 `{res}`',
    },
    cards=dict(
        one_liner='先切成非递减段，一次修改最多连接相邻两段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['最多把 `nums` 中的一个元素替换为任意整数',
                 '求替换后的==最长非递减子数组==长度',
                 '示例：`[1,2,5,3,4,2,6]` → `5`'],
        quote='对于划分出来的每个子数组，将其左侧或者右侧的第一个元素修改成更小或者更大的元素，一定能让这个子数组变长，因此对于每个子数组[x, y]，都可以使用其长度再加上1，即y - x + 2来更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历切成若干段尽可能长的非递减子数组',
              '每段至少能“再接一个”：长度 +1；证明了一次修改最多连接两段',
              '相邻两段 `[x1,y1]`、`[x2,y2]`：改前段末尾或后段开头能连上，就用 `y2 - x1 + 1`'],
        result='三段 `[0,2] [3,4] [5,6]`：第一段 +1 = 4，连接 `[0,2]` 和 `[3,4]` 得 `5` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（`parts`）',
                 '只有一段时直接返回 `len(nums)`',
                 '连接条件两种：前段末尾改成 `nums[y1-1]` 能不能 ≤ `nums[x2]`；或后段开头改成 `nums[y1]` 能不能 ≤ `nums[x2+1]`',
                 '长度为 1 的段不用特判连接：+2 的情形已覆盖',
                 '原文为 Python 2 风格，Python 3 下无需修改即可运行',
                 '对比灵神：灵神枚举替换位置用 pre / suf，这里按段处理'],
    ),
)
