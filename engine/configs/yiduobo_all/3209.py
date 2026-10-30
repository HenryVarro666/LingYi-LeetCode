def _b(x, w=3):
    return format(x, 'b').zfill(w) if x is not None else '-'


def _txt(S):
    if 'index' not in S:
        return ''
    return (f"右端点 `index = {S['index']}`：窗口 left 段 AND =`{S.get('left_now')}`，right 段 AND =`{S.get('right_now')}`　"
            f"（`k = {S['k']}`）")


def _win(S, i, v):
    return None


CONFIG = dict(
    num=3209, title='子数组按位与值为 K 的数目', difficulty='Hard', category='位运算',
    author='yiduobo', technique='双滑窗 + 每位计数',
    tags=['灵神题单·位运算', '难度分 2050'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, k):

        res = 0
        left_now = None
        right_now = None
        left = None
        right = None
        left_freq = [0] * 30
        right_freq = [0] * 30
        res = 0
        for index, v in enumerate(nums):
            if left_now is None:
                left_now = v
                left = index
                for d in range(30):
                    if v & (1 << d) == (1 << d):
                        left_freq[d] += 1
            
            else:
                left_now &= v
                if right is not None:
                    right_now &= v
                for d in range(30):
                    if v & (1 << d) == (1 << d):
                        left_freq[d] += 1
                        if right is not None:
                            right_freq[d] += 1

                while left_now < k and left < index:
                    x = nums[left]
                    t = 0
                    for d in range(30):
                        if x & (1 << d) == (1 << d):
                            left_freq[d] -= 1
                        elif left_freq[d] == index - left:
                            t |= (1 << d)
                    
                    left_now |= t
                    left += 1
                
            if left_now < k:
                left_now = None
                left = None
                left_freq = [0] * 30
                right_now = None
                right = None
                right_freq = [0] * 30

            elif left_now == k:
                if right is None or right < left:
                    right_now = left_now
                    right_freq = left_freq[:]
                    right = left
                    
                while right < index:
                    x = nums[right]
                    t = 0
                    for d in range(30):
                        if (x & (1 << d) == 0) and right_freq[d] == index - right:
                            t |= (1 << d)
                    
                    if (right_now | t) == k:
                        for d in range(30):
                            if x & (1 << d) == (1 << d):
                                right_freq[d] -= 1
                        right_now |= t
                        right += 1
                    else:
                        break

                res += right - left + 1

        return res
''',
    call='Solution().countSubarrays([3,7,3,1], 3)',
    expect=5,
    skip=['for d in range', '(1 << d)', 'freq[d]', 't = 0', 'x = nums', 'left_freq = [', 'right_freq = [', 'if right is not None', 7, 8, 11, 'right_freq = left_freq', 'left += 1', 'right += 1', 'if left_now is None', 4, 44, 46, 47],
    views=[
        dict(type='text', fn=lambda S: (f"右端点 `index={S['index']}`　left 段 `[{S.get('left')}, {S['index']}]` AND=`{S.get('left_now')}`　"
                                        f"right 段 `[{S.get('right')}, {S['index']}]` AND=`{S.get('right_now')}`　`k={S['k']}`") if 'index' in S else '', h=60),
        dict(type='array', var='nums', label='nums（蓝 = 最长的 AND ≥ k 窗口起点 left，粉 = 满足 AND = k 的最右起点 right）',
             pointers={'left': 'blue', 'right': 'pink', 'index': 'green'}, h=290,
             window=('left', 'right'),
             dim=lambda S, i, v: 'index' in S and i > S['index']),
    ],
    watch=[('index', 'index', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('left_now', 'left_now', 'blue'), ('right_now', 'right_now', 'pink'), ('res', 'res', 'green')],
    captions={
        43: '重置：`left`、`right` 两个窗口全部清空，等下一个右端点重新开始',
        5: '`left` 段：以 `index` 结尾、AND ==仍 ≥ k== 的最长窗口起点；`left_now` 是该窗口的 AND',
        6: '`right` 段：AND 恰好 `== k` 的最短窗口起点（最靠右）。两个窗口夹出来的就是答案区间',
        'left_freq = [0] * 30': '`freq[d]`：窗口里第 `d` 位为 1 的元素个数——AND 的某位只有“窗口内全是 1”才为 1，所以出窗时要靠它还原',
        'for index, v in': lambda S, B, r: ('所有右端点都处理完了' if B.get('index') == S.index and 'index' in B else
                                           f'右端点 `index = {S.index}`，`v = {S.v}`'),
        'if left_now is None': lambda S, B, r: ('当前没有活跃窗口：`v` 单独作为新窗口' if B.get('left_now') is None
                                                else '已有活跃窗口：`v` 并进来'),
        'left_now = v': '新窗口只含 `v`：`left_now = {left_now}`；同时把 `v` 的各位计入 `left_freq`',
        'left_now &= v': '把 `v` 并进来：`left_now = {B.left_now} & {v} = {left_now}`（AND 只会变小）',
        'right_now &= v': '`right` 段也同样 AND：`right_now = {right_now}`',
        'while left_now < k': lambda S, B, r: (
            f'`left_now = {S.left_now} < k = {S.k}`：窗口 AND 太小了 → 要把最左边的数移出，AND 才会变大'
            if S.left_now < S.k and S.left < S.index else
            f'`left_now = {S.left_now}`，不再 `< k` 或窗口只剩一个数 → ==left 窗口定了=='),
        'left_now |= t': '移出 `nums[{left}]` 后，只有它是唯一的 0 的位会变成 1：`left_now` → {left_now}；`left` 右移到 {left + 1}',
        'left += 1': '`left` 右移到 {left}',
        'if left_now < k': lambda S, B, r: (f'窗口收到只剩 `v` 仍然 `left_now = {S.left_now} < k = {S.k}`：以它结尾的子数组全都不合法 → ==整体重置=='
                                            if S.left_now < S.k else f'`left_now = {S.left_now} ≥ k`：这个窗口里至少有合法或可能合法的起点'),
                'elif left_now == k': lambda S, B, r: (f'`left_now == k = {S.k}`：最左端起点 AND 恰好等于 k，存在合法子数组 → 去找右边界 `right`'
                                               if S.left_now == S.k else
                                               f'`left_now = {S.left_now} > k`：最长窗口 AND 都比 k 大，没有等于 k 的子数组'),
        'if right is None': lambda S, B, r: ('`right` 窗口还没建立或落在 `left` 左侧 → 从 `left` 起步复制一份' if (B.get('right') is None or B.get('right') < S.left)
                                              else '`right` 窗口已有，沿用上一轮'),
        'right = left': '`right = left = {right}`，`right_now = left_now = {right_now}`',
        'while right < index': lambda S, B, r: (f'`right = {S.right} < index`：试试能不能把 `nums[{S.right}]` 移出而 AND 仍恰好等于 k'
                                                if S.right < S.index else f'`right = index`：窗口只剩 `v`，不能再右移'),
        '(right_now | t) == k': lambda S, B, r: (f'移出后 AND 会变成 `{S.right_now | S.t}` == k → ==可以移出，right 右移=='
                                                 if (S.right_now | S.t) == S.k else
                                                 f'移出后 AND 会变成 `{S.right_now | S.t}` ≠ k（超过 k） → ==不能再移了=='),
        'right_now |= t': '`right_now` 变成 `{right_now}`；`right` 右移到 {right + 1}（被移出的数是某些位唯一的 0，补成 1）',
        'right += 1': '`right` 右移到 {right}',
        'break': '`right` 不能再右移，停下',
        'res += right - left + 1': '合法起点范围是 `[{left}, {right}]`，共 `{right} - {left} + 1 = {right - left + 1}` 个 → `res` = =={res}==',
        'return res': '总共 `{res}` 个子数组',
    },
    cards=dict(
        one_liner='固定右端点，AND 值依次经历 <k、=k、>k 三段，找出 =k 的左右边界',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['数出 `nums` 中有多少个子数组，所有元素按位 AND 的结果恰好是 `k`',
                 '示例：`[1,1,2]`，`k=1` → `3`；`[1,2,3]`，`k=2` → `2`',
                 '本视频：`[3,7,3,1,3]`，`k=3` → `6`'],
        quote='参与运算的数越多，按位与的结果就越小，因此在这里就可以固定住子数组的右边界index，那么所有以index为右边界的子数组的按位与结果将会经历小于k、等于k、大于k这三个阶段',
        quote_src='—— yiduobo 题解原文',
        idea=['以 `index` 结尾的子数组，起点越靠左 AND 越小：先 ==大于 k==，再 ==等于 k==，再 ==小于 k==',
              '`left` 窗口：AND ≥ k 的最左起点；`right` 窗口：AND == k 的最右起点；两者之间都合法',
              'index 右移时两个窗口只会右移 → 双滑动窗口；用 `freq[d]` 记每一位 1 的个数来还原 AND'],
        summary=['时间 `O(n log U)`，每次右移最多遍历 30 位',
                 '窗口里 AND 某位变 1，当且仅当移出的元素是该位唯一的 0：`freq[d] == 窗口长度`',
                 '代码无 Python 2 专有语法，未做改动',
                 '对比灵神：灵神 LogTrick 原地维护 AND 值；yiduobo 用双滑窗 + 位计数，不改动原数组'],
    ),
)
