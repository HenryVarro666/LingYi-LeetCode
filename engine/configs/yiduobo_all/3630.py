def _b(v, w):
    return format(v, f'0{w}b')


def _txt(S):
    nums = S['nums']
    w = max(nums).bit_length()
    inner = S.get('_inner', {})
    ln = S['_line']
    if 'calc' in inner or ('f' in inner and 'ac' in inner and 'length' in inner):
        f = inner.get('f') or []
        basis = '　'.join(f"f[{k}]=`{_b(v, w)}`" for k, v in enumerate(f) if v) or '（空）'
        s = f"线性基：{basis}"
        if 'best' in inner:
            s += f"　best = ==`{_b(inner['best'], w)}`=="
        return s
    if 'state' in S and 'ac' in S:
        inB = [nums[k] for k in range(len(nums)) if S['state'] >> k & 1]
        parts = [f"state = `{_b(S['state'], len(nums))}` → B = `{inB}`，A∪C = `{S['ac']}`"]
        if 'xor' in S:
            parts.append(f"XOR(A∪C) = `{S['xor']}`，s = `{S['s']}`，b = `{S.get('b')}`，res = ==`{S['res']}`==")
        return '\n'.join(parts)
    return '枚举哪些数属于 B（二进制掩码），其余的给 A 和 C'


CONFIG = dict(
    num=3630, title='划分数组得到最大异或运算和与运算之和', difficulty='Hard', category='位运算',
    author='yiduobo', technique='枚举 B + 异或线性基 + 两层剪枝',
    tags=['灵神题单·位运算', '位运算 · 七、线性基', '难度分 2744'],
    code='''
class Solution(object):
    def maximizeXorAndXor(self, nums):

        res = 0
        n = len(nums)

        def calc(ac):
            if not ac:
                return 0
            length = len(bin(max(ac))) - 2
            f = [None] * (length + 1)
            for x in ac:
                for index in range(length, -1, -1):
                    if x & (1 << index) == (1 << index):
                        if f[index] is None:
                            f[index] = x
                            break
                        else:
                            x ^= f[index]

            best = 0
            for index in range(length, -1, -1):
                if f[index] and (best & (1 << index) == 0):
                    best ^= f[index]
            
            return best

        for state in range(1 << n):
            b = None
            ac = []
            xor = 0
            s = 0
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    if b is None:
                        b = nums[index]
                    else:
                        b &= nums[index]
                else:
                    ac.append(nums[index])
                    s += nums[index]
                    xor ^= nums[index]
            
            if b is None:
                b = 0

            if s + b <= res:
                continue

            s = 0
            for index, v in enumerate(ac):
                ac[index] = v ^ (v & xor)
                s += ac[index]

            if s * 2 + xor + b <= res:
                continue

            res = max(res, b + calc(ac) * 2 + xor)

        return res
''',
    call='Solution().maximizeXorAndXor([2, 3])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（state 的第 k 位 = 1 表示 nums[k] 进 B）', h=170),
        dict(type='array', var='ac', label='ac：不在 B 里的数（要分给 A 和 C）', h=170),
        dict(type='array', var=lambda S: S['_inner'].get('f') if isinstance(S.get('_inner', {}).get('f'), list) else None,
             label='线性基 f[index]（空 = 没有）', h=170, color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_txt, size=25, h=160),
    ],
    watch=[('state', 'state', 'cyan'), ('b', 'b', 'blue'), ('xor', 'xor', 'pink'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for state in range(1 << n)': lambda S, B, r: (f'`state = {S.state}`：二进制每一位表示对应元素是否进 B（共 `{1 << S.n}` 种）' if 'state' in S else '枚举 B 的所有子集结束'),
        'if state & (1 << index)': lambda S, B, r: (f"`nums[{S.index}]` 在 B 里 → 参与按位与" if S.state & (1 << S.index) == (1 << S.index)
                                                    else f"`nums[{S.index}]` 不在 B 里 → 放进 `ac`，留给 A 和 C"),
        'b = nums[index]': 'B 里的第一个元素：`b = {b}`',
        'b &= nums[index]': 'B 的按位与继续累积 → `b = {b}`',
        'ac.append': '`ac` = {ac}，`s` = {s}（先不细算，只是求个和做剪枝）',
        35: lambda S, B, r: ('B 里还没有元素 → 这个数是第一个' if S.b is None else 'B 里已有元素 → 继续按位与'),
        44: '一个也没进 B 时 `b` 还是 None → 空集的 AND 当作 0',
        'if s + b <= res': lambda S, B, r: (f"粗剪枝：`s + b = {S.s + S.b}` <= `res = {S.res}` → ==肯定不会更优，跳过=="
                                            if S.s + S.b <= S.res else f"`s + b = {S.s + S.b}` > `res = {S.res}` → 还有希望"),
        'ac[index] = v ^ (v & xor)': '去掉 `XOR(ac) = {xor}` 里为 1 的位：`{v}` → `{ac[index]}`',
        'if s * 2 + xor + b <= res': lambda S, B, r: (f"细剪枝：`2s + xor + b = {S.s * 2 + S.xor + S.b}` <= `res = {S.res}` → ==跳过=="
                                                      if S.s * 2 + S.xor + S.b <= S.res else
                                                      f"`2s + xor + b = {S.s * 2 + S.xor + S.b}` > `res = {S.res}` → 去算线性基"),
        'res = max(res, b + calc(ac) * 2 + xor)': '调用 `calc(ac)`：求 `ac` 里选若干个数的最大异或，再算 `b + 2·calc + xor`',
        'if not ac': 'ac 为空就没有数可选，最大异或为 0',
        'length = len(bin(max(ac))) - 2': '`bin()` 带 `0b` 前缀，最高位个数 = `{length}`',
        'f[index] = x': '`f[{index}] = {x}`：新增一个基，换下一个数 → `break`',
        'x ^= f[index]': '`f[{index}]` 已有 → 用它消去 x 的这一位 → `x = {x}`',
        'best ^= f[index]': '这一位还是 0 且有基 → 异或后变 1：`best = {best}`',
        'if f[index] and': lambda S, B, r: (f"`f[{S.index}]` 为空，这一位没有基" if not S.f[S.index] else (f"`best` 第 `{S.index}` 位是 0 且 `f[{S.index}]` 存在 → 异或" if S.best & (1 << S.index) == 0 else f"`best` 第 `{S.index}` 位已经是 1 → 不动")),
        'return best': '`ac` 里选若干数的最大异或 = ==`{best}`==',
        'return res': '答案 = ==`{res}`==',
    },
    skip=['res = 0', 'n = len(nums)', 'b = None', 'ac = []', 'xor = 0', 's = 0', 'b = 0'],
    max_steps=64,
    cards=dict(
        one_liner='枚举 B，剩下的 A、C 的和用线性基求最大',
        complexity='时间 `O(2^n · n · log U)`，空间 `O(n)`',
        problem=['把 `nums` 划成三个可空子序列 `A、B、C`，最大化 `XOR(A) + AND(B) + XOR(C)`',
                 '空序列的运算结果按 0 算',
                 '本视频：`[2,3]` → `5`（B=[2]，A 或 C 里放 3）'],
        quote='在这里可以考虑枚举B中有哪些元素，然后考虑剩下元素组成A和C时可能得到的最优划分是什么。',
        quote_src='—— yiduobo 题解原文',
        idea=['`XOR(A) ^ XOR(C) = XOR(arr)` 固定：`XOR(arr)` 里为 1 的位，对和的贡献固定是 `2^p`',
              '为 0 的位要么 0+0，要么 1+1，尽量让高位拆成 1+1',
              '先把每个数中 `XOR(arr)` 为 1 的位去掉，得 `ac`；`ac` 的最大异或 ×2 再加 `XOR(arr)`'],
        summary=['时间 `O(2^n · n · log U)`，空间 `O(n)`',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '两层剪枝：`s + b` 和 `2s + xor + b` 都不超过 `res` 就跳过',
                 '易错点：`bin()` 结果带 `0b`，位数要减 2；B 为空时 AND 记为 0',
                 '对比灵神：灵神预处理子集 AND/XOR/OR 再剪枝；yiduobo 每个状态现算'],
    ),
)
