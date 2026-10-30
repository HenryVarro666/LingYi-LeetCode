CONFIG = dict(
    num=457, title='环形数组是否存在循环', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='原地标记轮次 · 模拟行走',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def circularArrayLoop(self, nums):

        for index in range(len(nums)):
            if nums[index] < 0:
                nums[index] = -(-nums[index] % len(nums))
            else:
                nums[index] %= len(nums)

        cnt = 0
        for index, num in enumerate(nums):
            if num > 1000:
                continue

            next_pos = (index + num + len(nums)) % len(nums)
            if next_pos == index:
                cnt += 1
                nums[index] = 1000 + cnt
                continue

            now = index
            cnt += 1
            while next_pos != index and nums[next_pos] <= 1000 and nums[next_pos] * nums[now] > 0:
                nums[now] = 1000 + cnt
                now = next_pos
                next_pos = (now + nums[now] + len(nums)) % len(nums)
            
            if next_pos == index or nums[next_pos] == nums[index]:
                return True
            
            nums[now] = 1000 + cnt
''',
    call='Solution().circularArrayLoop([-3,-3,-3,1,-2,-1])',
    expect=True,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue', 'now': 'cyan', 'next_pos': 'pink'}, h=260, cell=110,
             color=lambda S, i, v: 'orange' if v > 1000 else None,
             dim=lambda S, i, v: v > 1000),
        dict(type='text', fn=lambda S: f"轮次 cnt = =={S['cnt']}==；值 > 1000 表示已在第 `值−1000` 轮走过" if 'cnt' in S else '先把每个数对 n 取模，压缩成不超过一圈的步长'),
    ],
    watch=['cnt', ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('next_pos', 'next_pos', 'pink')],
    captions={
        'for index in range(len(nums))': '第一遍：把每个数 ==化成不超过一圈的步长==，保留正负号',
        'nums[index] < 0': lambda S, B, ret: ('`nums[index]` < 0 → 反方向走，保留负号' if B.nums[B.index] < 0 else '`nums[index]` ≥ 0 → 往前走'),
        '-(-nums[index]': '负数：先取绝对值再取模再加回负号 → `{nums[index]}`',
        'nums[index] %= len': '正数直接取模 → `{nums[index]}`',
        'cnt = 0': '`cnt` 记录当前是第几轮出发',
        'for index, num in enumerate': '第二遍：每个没用过的点都当一次起点',
        'if num > 1000': lambda S, B, ret: ('`num` > 1000 → 之前轮次走过，不再出发' if B.num > 1000 else '`num` ≤ 1000 → 没走过，可以当起点'),
        'next_pos = (index + num': '下一个位置 `(index + num + n) % n` = ==`{next_pos}`==（加 n 防止负数）',
        'if next_pos == index or': lambda S, B, ret: ('==走回起点，形成循环（同向、长度 > 1）== → 返回 True' if B.next_pos == B.index
                                                       else ('走到本轮标过的点 → 也是循环，返回 True' if B.nums[B.next_pos] == B.nums[B.index]
                                                             else '没有成环：要么方向相反，要么走进旧轮次的点')),
        'if next_pos == index': lambda S, B, ret: ('走回自己 → 长度为 1 的环，不算循环，标记后跳过' if B.next_pos == B.index else '下一个位置不是自己，开始沿路走'),
        'nums[index] = 1000 + cnt': '长度 1 的自环：标成 `1000 + cnt` = {nums[index]}',
        'nums[now] = 1000 + cnt': '给 `nums[{now}]` 盖上本轮的章 `1000 + cnt` = {nums[now]}',
        'now = index': '`now` 从起点出发',
        'cnt += 1': '轮次加一：这一轮走过的点都标成 `1000 + {cnt}`',
        'while next_pos != index': lambda S, B, ret: (
            '没回到起点、下一个点没被标过、方向相同 → 继续走' if (B.next_pos != B.index and B.nums[B.next_pos] <= 1000 and B.nums[B.next_pos] * B.nums[B.now] > 0)
            else ('走回起点了 → 停' if B.next_pos == B.index else ('下一个点已被标过（>1000）→ 停' if B.nums[B.next_pos] > 1000 else '下一个点方向相反 → 停'))),
        'now = next_pos': '`now` 前进到 `{now}`',
        'next_pos = (now + nums[now]': '再算下一个位置 → `{next_pos}`',
        'return True': '存在循环，返回 `True`',
    },
    cards=dict(
        one_liner='沿着走，走过的点盖上“第几轮”的章',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['环形数组 `nums`：`nums[i]` 是正数就向前走这么多步，负数向后走',
                 '循环要求：==长度大于 1==、==全部同向==（全正或全负）',
                 '本视频：`[-3,-3,-3,1,-2,-1]` → `True`'],
        quote='无法往后走的情况有三种：走回当前轮次中的点（存在循环）；走到反方向的点；走到之前轮次用过的点。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点最多被走一次：之前轮次没找到环，后面走进去也必然找不到',
              '用 `1000 + cnt` 在原数组上打标记，不用额外空间',
              '值 > 1000 表示走过；减去 1000 就知道是第几轮，和当前轮次相同才是成环'],
        summary=['时间 `O(n)`，空间 `O(1)`（会改写输入数组）',
                 '先对 `n` 取模：保证一步不会绕多圈，并让自环（长度 1）能被识别',
                 '`next_pos == index` 且只走一格：长度 1 不算循环，要排除',
                 '没找到循环时原函数不写 `return`，返回 `None`，本题示例选了会返回 True 的输入',
                 '原文就是 Python 3 可运行的写法，无需修改'],
    ),
)
