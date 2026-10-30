CONFIG = dict(
    num=898, title='子数组按位或操作', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='LogTrick：原地更新 + 提前退出',
    tags=['LogTrick', '难度分 2133'],
    code='''
class Solution:
    def subarrayBitwiseORs(self, arr: List[int]) -> int:
        st = set()
        for i, x in enumerate(arr):
            st.add(x)
            for j in range(i - 1, -1, -1):
                if arr[j] | x == arr[j]:
                    break
                arr[j] |= x
                st.add(arr[j])
        return len(st)
''',
    call='Solution().subarrayBitwiseORs([1,2,1,4])',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"右端点 i={S['i']}：`arr[j]` 现在存的是 ==子数组 [j..{S['i']}] 的 OR=="
                                        if 'i' in S else '')),
        dict(type='array', var='arr', pointers={'i': 'blue', 'j': 'pink'}, h=220,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='set', var='st', fmt=lambda x: str(x), h=170, label='st（所有不同的 OR 值）'),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('j', 'j', 'pink'), ('len(st)', 'len(st)', 'green')],
    captions={
        'st = set()': '`st` 用来给所有子数组的 OR 去重',
        'st.add(x)': '单个元素本身也是子数组：`{x}` 加入 `st`（当前共 {len(st)} 个不同值）',
        'for j in range': '从 `i-1` 往左倒着走，把 `x` 并进每个 `arr[j]`',
        'if arr[j] | x == arr[j]': lambda S, B, r: (
            f'`{S.arr[S.j]} | {S.x} = {S.arr[S.j] | S.x}`' +
            (f' 等于 `arr[j]` → ==x 是它的子集==，更左边的数又是它的超集，全都不会变，==直接 break==' if S.arr[S.j] | S.x == S.arr[S.j]
             else f' ≠ `{S.arr[S.j]}` → `arr[j]` 能变大，继续更新')),
        'arr[j] |= x': '`arr[{j}]` 变成 `[{j}..{i}]` 的 OR = =={arr[j]}==',
        'st.add(arr[j])': '`{arr[j]}` 加入 `st`（集合自动去重）→ 共 {len(st)} 个',
        'break': '提前退出内层循环：后面的 OR 值早就记录过了',
        'return len': '不同的 OR 值一共 ==`{len(st)}`== 个',
    },
    cards=dict(
        one_liner='OR 只会变大：每个位置至多变 30 次，x 是子集就停',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['求 `arr` 所有非空子数组的按位或，有多少个==不同的值==',
                 '示例：`[1,1,2]` → `3`（结果为 1,1,2,1,3,3）',
                 '本视频：`[1,2,1,4]` → `6`（1,2,3,4,5,7）'],
        quote='如果 arr[j] | x = arr[j]，从集合的角度看，此时 x 不仅是 arr[j] 的子集，同时也是 arr[k] (k<j) 的子集，所以后续的循环都不会改变元素值，退出内层循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把二进制数看成集合，OR 就是==并集==',
              '倒着更新 `arr[j] |= x`，`arr[j]` 保存 `[j..i]` 的 OR，左边的数是右边的超集',
              '遇到 `x` 已是子集就停：每个数字至多增大 30 次，总共 `O(n log U)`'],
        summary=['时间 `O(n log U)`，`U` 是最大值，每个数至多增大 30 次',
                 '==单个元素也是子数组==，要先 `st.add(x)`',
                 '会修改输入数组；退出条件必须是 `arr[j] | x == arr[j]`',
                 '同一模板可解 AND / GCD 版本（LogTrick）'],
    ),
)
