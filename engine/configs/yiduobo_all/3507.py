CODE = '''
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
'''

CONFIG = dict(
    num=3507, title='移除最小数对使数组有序 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='堆 + 前驱/后继数组 · 懒删除',
    tags=[],
    code=CODE,
    call='Solution().minimumPairRemoval([5, 2, 3, 1])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"逆序对个数 `desc = {S['desc']}`：==降到 0== 就有序了" if 'desc' in S else ''), size=26, h=60),
        dict(type='array', var='nums', label='nums（合并后，被吞掉的位置变成 None）', cell=90, h=250, pointers={'index': 'blue'},
             color=lambda S, k, v: 'dim' if v is None else None, dim=lambda S, k, v: v is None),
        dict(type='array', var='pre', label='pre[i]：i 的前一个原始下标', cell=90, h=150),
        dict(type='array', var='nxt', label='nxt[i]：i 的后一个原始下标', cell=90, h=150),
        dict(type='heap', var='heap', label='heap：(相邻和, 起点下标)', fmt=lambda x: f'{x[0]},{x[1]}', h=200),
    ],
    watch=[('index', 'index', 'blue'), ('desc', 'desc', 'pink'), ('res', 'res', 'green'), ('v', 'v')],
    skip=['n = len', 'pre = [None]', 'nxt = [None]', 's = [0]', 'heap = []', 'for index in range',
          'if index > 0', 'if index < n - 1'],
    max_steps=100,
    captions={
        'desc = 0': '`desc` 统计逆序对（`nums[i] > nums[i+1]`）个数',
        'pre[index] = index - 1': '`pre[{index}] = {index - 1}`：记下前一个元素的下标',
        'nxt[index] = index + 1': '`nxt[{index}] = {index + 1}`：记下后一个元素的下标',
        'heapq.heappush(heap, (nums[index] + nums[index + 1]': '把相邻数对 `({nums[index]}, {nums[index + 1]})` 的和 `{nums[index] + nums[index + 1]}` 连同下标 `{index}` 放进堆',
        'if nums[index] > nums[index + 1]': lambda S, B, ret: (f'`{S.nums[S.index]} > {S.nums[S.index + 1]}` → 逆序对，`desc` = =={S.desc}==' if S.nums[S.index] > S.nums[S.index + 1] else f'`{S.nums[S.index]} ≤ {S.nums[S.index + 1]}` → 不是逆序对'),
        'res = 0': '`res` 记操作次数',
        'while desc > 0': lambda S, B, ret: (f'`desc = {S.desc} > 0` → 还没有序，继续合并' if S.desc > 0 else '`desc = 0` → 已经非递减，结束'),
        'v, index = heapq.heappop': '弹出堆顶 `(v, index) = ({v}, {index})`：当前==和最小==的相邻对（和相同取下标小的）',
        'if nums[index] is not None': lambda S, B, ret: ('懒删除检查：`index` 没被吞掉、有后继、且现在的和仍等于 `v` → ==有效== 执行合并' if S.nums[S.index] is not None and S.nxt[S.index] is not None and S.nums[S.index] + S.nums[S.nxt[S.index]] == S.v
                                                       else '堆顶是旧数据（`nums` 已变）→ ==失效==，直接丢掉'),
        'res += 1': '`res` → {res}，做一次操作',
        24: lambda S, B, ret: (f'这一对 `({S.nums[S.index]}, {S.nums[S.nxt[S.index]]})` 本身是逆序对 → 合并后它消失，下一步 `desc` 减 1' if S.nums[S.index] > S.nums[S.nxt[S.index]] else f'这一对 `({S.nums[S.index]}, {S.nums[S.nxt[S.index]]})` 不是逆序对，`desc` 不变'),
        27: lambda S, B, ret: (f'右边的对 `({S.nums[S.nxt[S.index]]}, {S.nums[S.nxt[S.nxt[S.index]]]})` 是逆序对 → 后者被吞掉，这个对消失，下一步 `desc` 减 1' if S.nxt[S.nxt[S.index]] is not None and S.nums[S.nxt[S.index]] > S.nums[S.nxt[S.nxt[S.index]]] else '右边没有对，或右边的对不是逆序对，`desc` 不变'),
        30: lambda S, B, ret: (f'左边的对 `({S.nums[S.pre[S.index]]}, {S.nums[S.index]})` 是逆序对 → 合并后值会变，旧的先减掉：`desc` 减 1' if S.pre[S.index] is not None and S.nums[S.pre[S.index]] > S.nums[S.index] else '左边没有对，或左边的对不是逆序对，`desc` 不变'),
        'nums[index] += nums[nxt[index]]': '把后一个数累加到 `nums[{index}]` → `{nums[index]}`',
        'nums[nxt[index]] = None': '后一个位置被吞掉，标成 `None`（相当于从链表删除）',
        'pre[nxt[nxt[index]]] = index': '链表式删除：让 `nxt[nxt[index]]` 的前驱改成 `index`',
        'nxt[index] = nxt[nxt[index]]': '`nxt[{index}]` 跳过被吞掉的节点 → `{nxt[index]}`',
        39: lambda S, B, ret: (f'合并后的新值 `{S.nums[S.index]}` 与右邻 `{S.nums[S.nxt[S.index]]}` 比较' + ('：逆序 → `desc` 加 1' if S.nums[S.index] > S.nums[S.nxt[S.index]] else '：不逆序')),
        'heapq.heappush(heap, (nums[index] + nums[nxt[index]], index))': '右边出现新的相邻对，和 `{nums[index] + nums[nxt[index]]}`，放进堆',
        'nxt[index] = None': '后面已经没有元素了：`nxt[{index}] = None`',
        48: lambda S, B, ret: (f'合并后的新值 `{S.nums[S.index]}` 与左邻 `{S.nums[S.pre[S.index]]}` 比较' + ('：逆序 → `desc` 加 1' if S.nums[S.pre[S.index]] > S.nums[S.index] else '：不逆序')),
        'heapq.heappush(heap, (nums[pre[index]] + nums[index], pre[index]))': '左边出现新的相邻对，和 `{nums[pre[index]] + nums[index]}`，放进堆',
        'return res': '`desc = 0`，数组已非递减，一共操作了 =={ret}== 次',
    },
    cards=dict(
        one_liner='堆找最小和数对，pre/nxt 数组当链表删元素，desc 数逆序对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选相邻==和最小==的一对（并列取最左），用它们的和替换这一对',
                 '求使数组==非递减==所需的最少操作次数',
                 '示例：`[5,2,3,1]` → `2`（`[5,2,4]` → `[5,6]`）'],
        quote='对于找最小和这一步，这是一个动态全局最小值问题，可以使用堆来处理。……对于删除操作依然可以使用懒删除的处理方法，若堆顶的二元组与当前剩下的nums不符，那么说明堆顶的二元素已经失效。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次操作数组长度减 1，所以直接模拟；`desc` 统计逆序对，降到 0 就停',
              '堆里放 `(相邻和, 下标)`；合并后旧的对失效，弹出时用「和是否还对得上」判断（懒删除）',
              '`pre`/`nxt` 记录每个元素当前的前后邻居，合并相当于链表删除，新邻居对再入堆'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；这题 `n ≤ 50`，3510 是 `10^5`，思路相同',
                 '合并前后要把 3 个受影响的相邻对从 `desc` 里减掉、再把新形成的对加回去',
                 '被吞掉的位置标 `None`；弹出堆顶要先检查是否失效',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（代码本身未改）',
                 '代码里变量 `s = [0] * n` 没有用到，是原文遗留'],
    ),
)
