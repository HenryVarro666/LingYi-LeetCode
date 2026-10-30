def _sets(S, name):
    P = S.get(name)
    if not P:
        return ''
    return '　'.join(f'选{c}个:{sorted(x)}' for c, x in enumerate(P))


def _top(S):
    if 'first_nums' in S and 'first_cnt' in S:
        return f"枚举前半选 `{S['first_cnt']}` 个、后半选 `{S['second_cnt']}` 个；目标 `target = {S['target']}`"
    if 'first_part' in S and 'second_part' not in S:
        return '预处理：前半 n 个数，按「选了几个」分组，记录所有可能的和'
    if 'second_part' in S:
        return '预处理：后半 n 个数，同样按「选了几个」分组'
    return '把 2n 个数分成前后两半，各自枚举所有选法'


def _two(S):
    if 'now' in S and 'first_p' in S and S['first_p'] < len(S['first_nums']) and S['second_p'] < len(S['second_nums']):
        return f"`{S['first_nums'][S['first_p']]} + {S['second_nums'][S['second_p']]} = {S['now']}`，与 `target = {S['target']}` 比较"
    return ''


CONFIG = dict(
    num=2035, title='将数组分成两个数组并最小化数组和的差', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='折半枚举 + 双指针',
    tags=['灵神题单·链表树与回溯', '难度分 2490'],
    code='''
class Solution(object):
    def minimumDifference(self, nums):

        s = sum(nums)
        target = s // 2

        n = len(nums) // 2
        first_part = [set([0])]
        for index in range(n):
            first_part.append(set())
            for cnt in range(index, -1, -1):
                for num in first_part[cnt]:
                    first_part[cnt + 1].add(num + nums[index])
        
        second_part = [set([0])]
        for index in range(n):
            second_part.append(set())
            for cnt in range(index, -1, -1):
                for num in second_part[cnt]:
                    second_part[cnt + 1].add(num + nums[index + n])

        res = None
        for first_cnt in range(n + 1):
            second_cnt = n - first_cnt
            first_nums = sorted(first_part[first_cnt])
            second_nums = sorted(second_part[second_cnt], reverse = True)

            first_p = second_p = 0

            while first_p < len(first_nums) and second_p < len(second_nums):
                now = first_nums[first_p] + second_nums[second_p]
                if now == target:
                    return s - target - target
                if now < target:
                    if res is None or res > s - now - now:
                        res = s - now - now
                    first_p += 1
                else:
                    if res is None or res > now - (s - now):
                        res = now - (s - now)
                    second_p += 1

        return res
''',
    call='Solution().minimumDifference([3,9,7,3])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var='nums', label='nums（前半 | 后半）', cell=84, h=130,
             color=lambda S, i, v: 'blue' if i < len(S['nums']) // 2 else 'pink'),
        dict(type='text', fn=lambda S: '前半各分组的和：' + _sets(S, 'first_part'), size=22, h=70),
        dict(type='text', fn=lambda S: '后半各分组的和：' + _sets(S, 'second_part'), size=22, h=70),
        dict(type='array', var='first_nums', label='first_nums（升序）', pointers={'first_p': 'blue'}, h=120),
        dict(type='array', var='second_nums', label='second_nums（降序）', pointers={'second_p': 'pink'}, h=120),
        dict(type='text', fn=_two, size=26, h=60),
    ],
    watch=[('s', 's'), ('target', 'target', 'yellow'), ('first_cnt', 'first_cnt', 'blue'), ('now', 'now'), ('res', 'res', 'green')],
    max_steps=110,
    skip=['for cnt in range(index', 'first_part.append', 'second_part.append', 'first_p = second_p', 'for num in', 'second_cnt = n', 'res = None'],
    captions={
        's = sum': '总和 `s = {s}`；两边各取一半，理想情况每边都是 `s / 2`',
        'target = s': '`target = s // 2 = {target}`：前后各选出的数之和越接近它，两数组差越小',
        'n = len': '`n = {n}`：原数组分成前 {n} 个和后 {n} 个，各自只有 `2^{n}` 种选法',
        'first_part = [': '`first_part[c]` = 前半里选 c 个数能得到的所有和；先放 `选 0 个 → {{0}}`',
        'first_part.append': '处理 `nums[{index}] = {nums[index]}`：多出「选了 {index + 1} 个」这一组',
        'for cnt in range(index': '`cnt` ==倒序==枚举：保证每个数只被用一次（类似 01 背包）',
        'first_part[cnt + 1].add': '在「选 {cnt} 个」的和 `{num}` 上再选 `nums[{index}]` → 「选 {cnt + 1} 个」得到 `{num + nums[index]}`',
        'second_part = [': '后半同理，`second_part[c]` 记录后半选 c 个的所有和',
        'second_part.append': '处理 `nums[{index + n}] = {nums[index + n]}`：多出「选了 {index + 1} 个」这一组',
        'second_part[cnt + 1].add': '在「选 {cnt} 个」的和 `{num}` 上加 `nums[{index + n}]` → 「选 {cnt + 1} 个」得到 `{num + nums[index + n]}`',
        'res = None': '`res` 记录目前最小的差，先设为空',
        'for first_cnt': '前半选 `{first_cnt}` 个',
        'second_cnt = n': '总共要选 `n` 个，所以后半必须选 `{second_cnt}` 个',
        'first_nums = sorted': '前半选 {first_cnt} 个的所有和，==升序==排好：`{first_nums}`',
        'second_nums = sorted': '后半选 {second_cnt} 个的所有和，==降序==排好：`{second_nums}`',
        'first_p = second_p': '双指针：前半从最小开始，后半从最大开始',
        'while first_p': lambda S, B, r: ('两个指针都还没越界，继续' if S.first_p < len(S.first_nums) and S.second_p < len(S.second_nums)
                                         else '有一个序列走完了 → 这一组结束，换下一个 `first_cnt`'),
        'now = first': '`now = {first_nums[first_p]} + {second_nums[second_p]} = {now}`：这种选法选出的数之和',
        'if now == target': lambda S, B, r: (f'`now = {S.now}` 恰好等于 `target` → ==刚好平分，差为 0== ，直接返回' if S.now == S.target
                                            else f'`now = {S.now}` ≠ `target = {S.target}`，继续看大小'),
        'if now < target': lambda S, B, r: (f'`{S.now} < {S.target}`：选出的和偏小 → 要==增大== now，让 first_p 右移' if S.now < S.target
                                           else f'`{S.now} > {S.target}`：选出的和偏大 → 要==减小== now，让 second_p 右移'),
        'res > s - now - now': '这一边的和是 `{now}`，另一边是 `s - now`，差为 `s - 2*now = {s - now - now}`，比 `res` 小就更新',
        'res = s - now - now': '更新 `res = {res}`',
        'first_p += 1': 'now 偏小，`first_p` 右移一格，换更大的前半和 → `{first_p}`',
        'res > now - (s - now)': 'now 偏大，差为 `now - (s - now) = {now - (s - now)}`，比 `res` 小就更新',
        'res = now - (s - now)': '更新 `res = {res}`',
        'second_p += 1': 'now 偏大，`second_p` 右移一格，换更小的后半和 → `{second_p}`',
        'return s - target': '`s - 2 × target = {ret}`：刚好平分',
        'return res': '所有分组枚举完，最小差为 `{res}`',
    },
    cards=dict(
        one_liner='30 个数太多，拆成两半各算 2^15 种和，再双指针凑',
        complexity='时间约 `O(2^n · n)`，空间 `O(2^n)`',
        problem=['`2n` 个整数分成两个长度各为 `n` 的数组，使两数组和之差的绝对值最小',
                 '示例：`[3,9,7,3]` → `2`（`[3,9]` 和 `[7,3]`）',
                 '本视频即这个例子'],
        quote='对于本题，同样是将这个30分成两组，然后计算两组中各种可能的选择。接下来也同样是两个序列中各选一个数，使得选择的两个数最接近goal。本题的goal就是所有数的总和除以2。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值可达 `10^7`，背包不行；30 个数直接状压/dfs 也不行',
              '拆成前后两半，各自枚举选法，==按选了几个分组==（要求恰好共选 n 个）',
              '前半选 `c` 个、后半选 `n - c` 个；两个有序序列用==双指针==找最接近 `s/2` 的和'],
        summary=['时间约 `O(2^n · n)`：预处理 `2^n` 种和，排序后双指针线性扫描',
                 '易错点：必须按「选了几个」分组，否则两边个数不是 n',
                 '预处理时 `cnt` 要倒序，否则同一个数会被重复使用',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '灵神题单把它放在「折半搜索」，同类题 1755'],
    ),
)
