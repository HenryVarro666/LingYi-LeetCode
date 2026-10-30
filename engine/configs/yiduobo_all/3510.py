def _cur(S):
    return [x for x in S['nums'] if x is not None]


def _txt(S):
    if 'desc' not in S:
        return ''
    return f"当前数组 `{_cur(S)}`，递减的相邻对 `desc` = =={S['desc']}=="


_IN = '19 <= _line <= 41'
_P = {
    f'index if {_IN} else None': ('blue', 'i'),
    f'nxt[index] if {_IN} and index is not None and nxt[index] is not None else None': ('pink', 'nxt'),
    f'pre[index] if {_IN} and index is not None and pre[index] is not None else None': ('cyan', 'pre'),
}


CONFIG = dict(
    num=3510, title='移除最小数对使数组有序 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='堆 + pre/nxt 数组模拟链表 + 逆序对计数',
    tags=['难度分 2608'],
    code='''
class Solution(object):
    def minimumPairRemoval(self, nums):
        
        heap = []
        n = len(nums)
        pre = [None] * n
        nxt = [None] * n
        s = [0] * n

        desc = 0
        for index in range(n):
            if index > 0:
                pre[index] = index - 1
            if index < n - 1:
                nxt[index] = index + 1
                heapq.heappush(heap, (nums[index] + nums[index + 1], index))
                if nums[index] > nums[index + 1]:
                    desc += 1
        
        res = 0
        while desc > 0:
            v, index = heapq.heappop(heap)
            if nums[index] is not None and nxt[index] is not None and nums[index] + nums[nxt[index]] == v:
                res += 1
                if nums[index] > nums[nxt[index]]:
                    desc -= 1
                
                if nxt[nxt[index]] is not None and nums[nxt[index]] > nums[nxt[nxt[index]]]:
                    desc -= 1
                
                if pre[index] is not None and nums[pre[index]] > nums[index]:
                    desc -= 1

                nums[index] += nums[nxt[index]]
                nums[nxt[index]] = None

                if nxt[nxt[index]] is not None:
                    pre[nxt[nxt[index]]] = index
                    nxt[index] = nxt[nxt[index]]

                    if nums[index] > nums[nxt[index]]:
                        desc += 1
                    
                    heapq.heappush(heap, (nums[index] + nums[nxt[index]], index))
                else:
                    nxt[index] = None

                if pre[index] is not None:
                    if nums[pre[index]] > nums[index]:
                        desc += 1
                    
                    heapq.heappush(heap, (nums[pre[index]] + nums[index], pre[index]))

        return res
''',
    call='Solution().minimumPairRemoval([4,2,5,3,1])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=55),
        dict(type='array', var='nums', label='nums（灰 = 已合并，置为 None）', fmt=lambda v: '' if v is None else str(v),
             pointers={k: v[0] for k, v in _P.items()}, pointer_labels={k: v[1] for k, v in _P.items()}, h=230,
             dim=lambda S, i, v: v is None,
             color=lambda S, i, v: None),
        dict(type='heap', var='heap', label='heap 最小堆（(相邻和, 左下标)）', fmt=lambda x: f'{x[0]},{x[1]}', top_color='orange', h=130),
        dict(type='array', var='nxt', label='nxt（每个下标的下一个存活下标）', h=110),
    ],
    watch=[('res', 'res', 'green'), ('desc', 'desc', 'orange'), ('v', 'v', 'yellow'), ('index', 'index', 'blue')],
    skip=['s = [0] * n', 'heap = []', 'n = len(nums)', 'pre = [None]', 'nxt = [None]', 'desc -= 1', 'desc += 1', 'res = 0'],
    captions={
        'desc = 0': '`desc`：递减（左大右小）的相邻对个数；`pre` / `nxt` 记录前后存活下标，`heap` 存 `(相邻和, 下标)`',
        'for index in range(n)': '枚举下标 `{index}`',
        'if index > 0': '`pre[{index}]` 指向前一个下标',
        'pre[index] = index - 1': '`pre[{index}] = {pre[index]}`',
        'if index < n - 1': lambda S, B, r: ('不是最后一个，和右边凑成一对' if S.index < S.n - 1 else '最后一个下标没有右邻居'),
        'nxt[index] = index + 1': '`nxt[{index}] = {nxt[index]}`',
        'heapq.heappush(heap, (nums[index] + nums[index + 1], index))': '相邻和 `{nums[index]} + {nums[index+1]} = {nums[index] + nums[index+1]}` 连同下标 `{index}` 入堆',
        'if nums[index] > nums[index + 1]': lambda S, B, r: ('`{} > {}` → 逆序对，`desc` 加一'.format(S.nums[S.index], S.nums[S.index + 1]) if S.nums[S.index] > S.nums[S.index + 1] else '`{} ≤ {}`，不算'.format(S.nums[S.index], S.nums[S.index + 1])),
        'while desc > 0': lambda S, B, r: ('`desc = {}` > 0，还没有序，继续操作'.format(S.desc) if S.desc > 0 else '`desc = 0`，已经非递减 → 结束'),
        'v, index = heapq.heappop(heap)': '弹出堆顶：相邻和 `v = {v}`，左边下标 `index = {index}`',
        'if nums[index] is not None and': lambda S, B, r: (
            '堆顶有效：`index` 还在，右邻居还在，和仍是 `{}` → ==真的是当前最小对==，执行合并'.format(S.v)
            if (S.nums[S.index] is not None and S.nxt[S.index] is not None and S.nums[S.index] + S.nums[S.nxt[S.index]] == S.v)
            else '堆顶==过期==（元素已合并或和变了）→ 直接丢掉，什么也不做'),
        'res += 1': '合并一次：`res = {res}`',
        25: lambda S, B, r: ('合并前 `{} > {}` 是逆序对，合并后消失 → `desc` 减一'.format(S.nums[S.index], S.nums[S.nxt[S.index]]) if S.nums[S.index] > S.nums[S.nxt[S.index]] else '合并前 `{} ≤ {}`，不影响 `desc`'.format(S.nums[S.index], S.nums[S.nxt[S.index]])),
        'if nxt[nxt[index]] is not None and nums[nxt[index]] >': lambda S, B, r: (
            '右边那对 `(被并元素, 下下个)` 也要拆掉：它是逆序对 → `desc` 减一' if (S.nxt[S.nxt[S.index]] is not None and S.nums[S.nxt[S.index]] > S.nums[S.nxt[S.nxt[S.index]]])
            else '右边那对 `(被并元素, 下下个)` 不是逆序对（或不存在），`desc` 不变'),
        'if pre[index] is not None and nums[pre[index]] > nums[index]': lambda S, B, r: (
            '左边那对 `(前一个, index)` 旧值是逆序对 → 先减一，合并后再重新判断' if (S.pre[S.index] is not None and S.nums[S.pre[S.index]] > S.nums[S.index])
            else '左边那对旧值不是逆序对（或不存在）'),
        'nums[index] += nums[nxt[index]]': '把右边的数累加到左边：`nums[{index}] = {nums[index]}`',
        'nums[nxt[index]] = None': '右边的数删除，标记为 `None`',
        'if nxt[nxt[index]] is not None:': lambda S, B, r: ('被删元素后面还有元素，要把链表接上' if S.nxt[S.nxt[S.index]] is not None else '被删元素是最后一个，后面没有元素'),
        'pre[nxt[nxt[index]]] = index': '下下个的 `pre` 改指 `index`（跳过被删元素）',
        'nxt[index] = nxt[nxt[index]]': '`nxt[{index}]` 跳过被删元素 → `{nxt[index]}`',
        41: lambda S, B, r: ('新的 `({}, {})` 是逆序对 → `desc` 加一'.format(S.nums[S.index], S.nums[S.nxt[S.index]]) if S.nums[S.index] > S.nums[S.nxt[S.index]] else '新的 `({}, {})` 不是逆序对'.format(S.nums[S.index], S.nums[S.nxt[S.index]])),
        'heapq.heappush(heap, (nums[index] + nums[nxt[index]], index))': '新的相邻和 `{nums[index] + nums[nxt[index]]}` 入堆（旧的不删，等弹出时判过期）',
        'nxt[index] = None': '后面没有元素了：`nxt[{index}] = None`',
        'if pre[index] is not None:': lambda S, B, r: ('有前一个元素，重新考察 `(pre, index)` 这一对' if S.pre[S.index] is not None else '没有前一个元素，不用管'),
        'if nums[pre[index]] > nums[index]': lambda S, B, r: ('新的 `({}, {})` 是逆序对 → `desc` 加一'.format(S.nums[S.pre[S.index]], S.nums[S.index]) if S.nums[S.pre[S.index]] > S.nums[S.index] else '新的 `({}, {})` 不是逆序对'.format(S.nums[S.pre[S.index]], S.nums[S.index])),
        'heapq.heappush(heap, (nums[pre[index]] + nums[index], pre[index]))': '新的 `(前一个 + index)` 相邻和入堆',
        'return res': '一共操作 `{res}` 次',
    },
    max_steps=150,
    cards=dict(
        one_liner='堆里挑最小相邻和，pre/nxt 接链表，desc 判有序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选相邻对里==和最小==的一对（并列取下标最小），用和替换这两个数',
                 '问数组变成非递减最少要操作多少次',
                 '本视频：`[4,2,5,3,1]` → `3`'],
        quote='若堆顶的二元组与当前剩下的nums不符，那么说明堆顶的二元素已经失效，无需处理。……使用两个数组pre和nxt分别记录每个元素在当前数组中的前一个元素和后一个元素在原始nums中的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组最多缩短 `n` 次，直接模拟：堆找最小和对，`desc` 统计逆序对，为 0 就停',
              '合并 = 右边累加到左边再删右边；用 `pre` / `nxt` 数组像链表一样删除',
              '堆里旧元素不删：弹出时核对 `index` 还在、右邻居还在、和没变，不符就丢弃'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`desc` 要拆掉旧的三对、再加上新的两对，漏一对就会错',
                 '被合并的数置为 `None`，弹出堆顶时靠 `is not None` 和和值判过期',
                 '原文为 Python 2 风格写法，在 Python 3 中可直接运行，未改动代码',
                 '对比灵神：灵神用 `lazy` 计数字典标记失效 pair，yiduobo 靠弹出时重新核对'],
    ),
)
