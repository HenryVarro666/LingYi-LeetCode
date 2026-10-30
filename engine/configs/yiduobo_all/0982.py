def _cl(S):
    if 'check_list' not in S:
        return ''
    cl = S['check_list']
    head = ', '.join(str(v) for v in cl[:8]) + (' …' if len(cl) > 8 else '')
    return f"`check_list`（共 `{len(cl)}` 个）：`[{head}]`"


def _bits(S):
    if 'x' not in S or 'p' not in S:
        return ''
    x, p = S['x'], S['p']
    return f"`x` = `{x:016b}`，检查第 `{p}` 位：" + ('==是 1，跳过==' if x & (1 << p) else '是 0，可以放 0 或 1')


CONFIG = dict(
    num=982, title='按位与为零的三元组', difficulty='Hard', category='位运算',
    author='yiduobo', technique='哈希表计数 + 预生成可行 key 列表',
    tags=['位运算'],
    code='''
class Solution(object):
    def countTriplets(self, A):

        cnt_dict = {}
        for x in A:
            for y in A:
                z = x & y
                cnt_dict[z] = cnt_dict.get(z, 0) + 1
        
        res = 0
        for x in A:
            check_pow = range(16)
            check_list = [0]
            for p in check_pow:
                if x & (1 << p):
                    continue
                check_list.extend([y + (1 << p) for y in check_list])
            
            res += sum([cnt_dict.get(y, 0) for y in check_list])

        return res
''',
    call='Solution().countTriplets([65535, 43690, 21845])',
    expect=12,
    views=[
        dict(type='text', fn=lambda S: '`A` = `[0xFFFF, 0xAAAA, 0x5555]` = `[65535, 43690, 21845]`（16 位：全 1、1010…、0101…）', size=24, h=60),
        dict(type='map', var='cnt_dict', label='cnt_dict：A[i] & A[j] 的结果 → 出现次数', h=240),
        dict(type='text', fn=_bits, size=24, h=60),
        dict(type='text', fn=_cl, size=24, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('p', 'p', 'cyan'), ('res', 'res', 'green')],
    skip=['check_pow = range(16)', 'z = x & y', 'for p in check_pow', 'continue', 'for y in A:', 'if x & (1 << p)'],
    max_steps=60, max_events=200000,
    captions={
        'cnt_dict = {}': '先把所有 `A[i] & A[j]` 的结果出现次数记进哈希表',
        'cnt_dict[z] =': '`{x} & {y} = {z}`，`cnt_dict[{z}]` = {cnt_dict[z]}',
        'res = 0': '哈希表建完。接着枚举 `A[k]`：找满足 `A[k] & key == 0` 的 key',
        'check_list = [0]': '`A[k] = {x}`：key 的二进制里，`{x}` 为 1 的位必须是 0。先放一个 0',
        'for p in check_pow': '逐位 `p` 决定 key 的这一位怎么放',
        'if x & (1 << p)': lambda S, B, r: (f'`x` 的第 `{S.p}` 位是 1 → key 这一位只能是 0，跳过（`continue`）' if S.x & (1 << S.p)
                                            else f'`x` 的第 `{S.p}` 位是 0 → key 这一位可以是 0 或 1'),
        'continue': '这一位是 1：不扩展 `check_list`',
        'check_list.extend': '把现有每个 key 都加上 `1 << {p}`（这一位放 1），列表翻倍 → `{len(check_list)}` 个',
        'res += sum': '`check_list` 里的每个 key，在 `cnt_dict` 里查次数并累加：`res` = =={res}==',
        'return res': '三元组共 `{res}` 个',
    },
    cards=dict(
        one_liner='先数两个数的 AND，再为第三个数生成所有「AND 为 0」的 key',
        complexity='时间 `O(n^2 + n·2^16)`，空间 `O(2^16)`',
        problem=['数组 `A`，数有多少下标三元组 `(i, j, k)` 满足 `A[i] & A[j] & A[k] == 0`',
                 '示例：`[2,1,3]` → `12`；`[0,0,0]` → `27`',
                 '本视频：`[0xFFFF, 0xAAAA, 0x5555]`（`check_list` 太长，只显示个数和开头）'],
        quote='对于A[k] & key这个操作而言，如果需要结果为0，那么对于A[k]二进制表示中为1的位置而言，key二进制表示中对应的位置应该为0，其他的位置上则可以为0或者1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先枚举 `i, j`，用 `dict` 记录 `A[i] & A[j]` 出现次数',
              '对 `A[k]`：它为 1 的位，key 必须为 0；其余位随意',
              '从 `[0]` 开始逐位扩展，生成全部可行 key，再去 `dict` 里查'],
        summary=['时间：建表 `O(n^2)`，每个 `A[k]` 生成并查询至多 `2^16` 个 key',
                 '易错点：`A[k]` 为 1 的位要 `continue`，不能扩展',
                 '原文本身可直接在 Python 3 运行，未改代码',
                 '对比灵神：他反过来枚举「补集的子集」累加 `cnt`，不用生成列表'],
    ),
)
