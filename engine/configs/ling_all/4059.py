def _b(x):
    return format(x, '03b')


def _groups(S):
    g = S.get('groups')
    if g is None:
        return ''
    return '  ‖  '.join('[' + ', '.join(_b(x) for x in a) + ']' for a in g)


def _show(S):
    g = S.get('groups')
    if g is None:
        return '还没有分组'
    i = S.get('i')
    head = f'第 `{i}` 位' if i is not None else ''
    return f'{head}　组（组间有序，组内无序）：`{_groups(S)}`'


def _nxt(S):
    n = S.get('nxt')
    if n is None:
        return ''
    return '下一轮的组：`' + ('  ‖  '.join('[' + ', '.join(_b(x) for x in a) + ']' for a in n) or '（空）') + '`'


CONFIG = dict(
    num=4059, title='字典序最大的答案数组', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='从高位到低位分组排序',
    tags=[],
    code='''
class Solution:
    def largestPower(self, nums: list[int]) -> list[int]:
        ans = [0] * 15
        groups = [nums]

        for i in range(max(nums).bit_length() - 1, -1, -1):
            nxt = []
            cnt = 0

            for j, a in enumerate(groups):
                # 手动排 groups[j]
                ones = []
                zeros = []
                for x in a:
                    if x >> i & 1:
                        ones.append(x)
                    else:
                        zeros.append(x)

                cnt += len(ones)
                # 1 排前面，0 排后面
                if ones:
                    nxt.append(ones)
                if zeros:
                    nxt.append(zeros)
                    # 遇到 0，剩下的 groups[j] 不再排序
                    nxt += groups[j + 1:]
                    break

            ans[14 - i] = cnt
            groups = nxt

        return ans
''',
    call='Solution().largestPower([7,5,2,1])',
    expect=[0] * 12 + [2, 1, 3],
    views=[
        dict(type='text', fn=_show, size=30, h=90),
        dict(type='text', fn=lambda S: (f"正在看 `{_b(S['x'])}` 的第 `{S['i']}` 位" if 'x' in S and 'i' in S and S.get('_line') is not None else ''), size=28, h=60),
        dict(type='text', fn=_nxt, size=30, h=90),
        dict(type='array', var='ans', cell=56, label='ans（下标 12 对应第 2 位）', h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'yellow'), ('ones', 'ones', 'green'), ('zeros', 'zeros', 'pink')],
    captions={
        'ans = [0] * 15': '答案 15 个位置，高位的 0 不用管',
        'groups = [nums]': '一开始只有一个大组，里面无序',
        'for i in range': '从 `nums` 最高位 `{i}` 往低位处理：==高位优先==，因为字典序先比高位',
        'nxt = []': '新一轮的分组从空开始，`cnt` 统计这一位的最长全 1 前缀',
        'for j, a in enumerate': '依次看第 `{j}` 组：`{a}`（组间顺序已定，组内可随意排）',
        'ones = []': '组内按这一位分成两堆：1 的堆和 0 的堆',
        'if x >> i & 1': lambda S, B, r: (f'`{S.x}` 的第 `{S.i}` 位是 `1` → 放进 `ones`' if S.x >> S.i & 1
                                          else f'`{S.x}` 的第 `{S.i}` 位是 `0` → 放进 `zeros`'),
        'cnt += len(ones)': '这组有 `{len(ones)}` 个数该位为 1 → 全 1 前缀累计 `cnt` = =={cnt}==',
        'if ones': '1 排前面：有 1 的话单独成一组',
        'nxt.append(zeros)': '0 排后面，也单独成一组：这一位的 1 到此为止',
        'nxt += groups[j + 1:]': '前缀 1 在这里被 0 截断，后面的组这一位已经没用 → ==保持无序==，原样接上',
        'break': '已经截断，后面不用再看这一位',
        'ans[14 - i] = cnt': '`ans[{14 - i}] = {cnt}`：第 `{i}` 位最长全 1 前缀长度',
        'groups = nxt': '换成新分组，处理下一位',
        'return ans': '得到字典序最大的 `power` 数组：`{ret[12:]}`（前 12 个为 0）',
    },
    skip=['ones.append(x)', 'zeros.append(x)', 'ones = []', 'nxt = []', 'break', 'cnt = 0'],
    max_steps=110,
    cards=dict(
        one_liner='高位优先分组：只在被 0 截断之前才需要排序',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['重排 `nums`，`power[i]` 是第 `14-i` 位全为 1 的最长前缀长度',
                 '要让 `power` 字典序最大：先比高位',
                 '示例：`[7,5,2,1]` → 末三项 `[2,1,3]`，前面全是 0'],
        quote='在最高位的前缀 1 尽可能长的前提下，次高位的最长前缀 1（竖着看）的长度只能是 1。其他元素的次高位是 0 还是 1 不重要，可以一视同仁。',
        quote_src='—— 灵茶山艾府题解',
        idea=['朴素写法：每处理一位，把截断后无用的位置 0，再整体倒序排序',
              '优化：不用真排序，用「组」表示：==1 的堆在前、0 的堆在后==',
              '遇到 0 截断后，后面的组保持原样，留给更低位去排'],
        summary=['时间 `O(n log U)`，`U` 是最大值；组展开后恰好 `n` 个元素',
                 '题解先给了「置 0 再排序」的 `O(n log n log U)` 写法，这里演示的是手动分组的优化写法',
                 '易错：`ans[14 - i]`，位 `i` 对应下标 `14 - i`',
                 '同类：位运算思维题，高位优先的贪心'],
    ),
)
