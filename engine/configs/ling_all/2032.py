CONFIG = dict(
    num=2032, title='至少在两个数组中出现的值', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='位掩码标记出现位置（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def twoOutOfThree(self, nums1: List[int], nums2: List[int], nums3: List[int]) -> List[int]:
        ans = []
        mask = defaultdict(int)
        for i, a in enumerate([nums1, nums2, nums3]):
            for v in a:
                mask[v] |= 1 << i # 标记 v 在哪些数组中出现过
        for v, m in mask.items():
            if m > 2 and m != 4: # 二进制包含至少两个 1，即 3 5 6 7。也可以用 bits.OnesCount8 来求
                ans.append(v)
        return ans
''',
    call='Solution().twoOutOfThree([1,1,3,2], [2,3], [3])',
    expect=[3, 2],
    views=[
        dict(type='array', var='nums1', label='nums1（第 0 个数组 → 第 0 位）', cell=70, h=100, index=False,
             color=lambda S, i, v: 'yellow' if S['_line'] in (6, 7) and S.get('i') == 0 and S.get('v') == v else None),
        dict(type='array', var='nums2', label='nums2（第 1 个数组 → 第 1 位）', cell=70, h=100, index=False,
             color=lambda S, i, v: 'yellow' if S['_line'] in (6, 7) and S.get('i') == 1 and S.get('v') == v else None),
        dict(type='array', var='nums3', label='nums3（第 2 个数组 → 第 2 位）', cell=70, h=100, index=False,
             color=lambda S, i, v: 'yellow' if S['_line'] in (6, 7) and S.get('i') == 2 and S.get('v') == v else None),
        dict(type='map', var='mask', label='mask（值 → 出现位置的二进制，低位 = nums1）', fmt=lambda k, v: f"{k}: {v:03b}", h=150, font=34),
        dict(type='array', var='ans', label='ans（mask 至少两个 1）', cell=70, h=100, index=False),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v', 'cyan'), ('m', 'bin(m)', 'orange'), ('ans', 'ans', 'green')],
    max_steps=70,
    captions={
        'ans = []': '`ans` 存答案',
        'mask = defaultdict': '`mask[v]` 用一个小整数的二进制位记录：`v` 出现在哪几个数组里',
        'for i, a in enumerate': '看第 `{i}` 个数组，它对应二进制的第 `{i}` 位',
        'for v in a': '数组里的值 `v = {v}`',
        'mask[v] |= 1 << i': '把第 `{i}` 位置 1：`mask[{v}] = {mask[v]:03b}`（重复出现也只是再置一次，不会变）',
        'for v, m in mask.items()': '遍历 `mask`：`v = {v}`，`m = {m:03b}`',
        'if m > 2 and m != 4': lambda S, B, ret: (f'`m = {S.m}`（二进制 {S.m:03b}）至少两个 1 → ==至少在两个数组中出现==，收下'
                                                  if (S.m > 2 and S.m != 4) else f'`m = {S.m}`（二进制 {S.m:03b}）只有一个 1 → 只在一个数组中出现，不要'),
        'ans.append(v)': '`{v}` 加入答案：`ans = {ans}`',
        'return ans': '返回 `{ans}`（顺序任意）',
    },
    cards=dict(
        one_liner='用二进制位标记「在哪个数组出现」，至少两个 1 就收下',
        complexity='时间 `O(n1 + n2 + n3)`，空间 `O(n1 + n2 + n3)`',
        problem=['给三个整数数组，返回==至少在两个数组中出现==的所有值，答案元素互不相同，顺序任意',
                 '示例：`[1,1,3,2]`、`[2,3]`、`[3]` → `[3,2]`'],
        quote='标记 v 在哪些数组中出现过；二进制包含至少两个 1，即 3 5 6 7。也可以用 bits.OnesCount8 来求',
        quote_src='—— 灵茶山艾府题解（代码注释）',
        idea=['第 `i` 个数组对应第 `i` 位：`mask[v] |= 1 << i`',
              '同一数组重复出现，置位是幂等的，天然去重',
              '`mask` 取值 1 2 4 是只在一个数组出现；3 5 6 7 才至少两个 1'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]int8` → `defaultdict(int)`，`range` → `enumerate` / `.items()`）',
                 '时间、空间都是 `O(n1 + n2 + n3)`',
                 '易错：`m > 2 and m != 4` 排除 1、2、4（单个 1），剩下 3 5 6 7；Go 的 map 遍历无序，Python 按插入顺序，所以答案顺序是 `[3, 2]`',
                 '数值范围小也可以用数组代替字典'],
    ),
)
