CONFIG = dict(
    num=2007, title='从双倍数组中还原原数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 双指针配对',
    tags=['排序', '双指针'],
    code='''
class Solution(object):
    def findOriginalArray(self, changed):

        changed = sorted(changed)

        used = set()

        res = []
        p = 1
        for index in range(len(changed)):
            if index not in used:
                if p <= index:
                    p = index + 1
                while p < len(changed) and changed[p] != changed[index] + changed[index]:
                    p += 1
                if p == len(changed):
                    return []
                
                used.add(index)
                used.add(p)
                res.append(changed[index])

                p += 1
                
        
        return res
''',
    call='Solution().findOriginalArray([3,2,1,16,2,6,4,1,8,2])',
    expect=[1, 1, 2, 3, 8],
    views=[
        dict(type='array', var='changed', label='changed 排序后（灰 = 已剔除，蓝 = index，粉 = p）', cell=84, h=210,
             pointers={'index': 'blue', 'p': 'pink'},
             dim=lambda S, i, v: i in S.get('used', ()),
             color=lambda S, i, v: ('blue' if i == S.get('index') and i not in S.get('used', ()) else None)),
        dict(type='set', var='used', label='used（已剔除的下标）', fmt=lambda x: str(x), h=130),
        dict(type='array', var='res', label='res（原数组）', cell=84, h=130, index=False),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'changed = sorted': '先排序：原数组存在时，最小值 ==一定来自原数组==',
        'used = set()': '`used`：记录哪些位置已经被剔除，不用真的删元素',
        'res = []': '`res` 保存还原出的原数组',
        'p = 1': '`p`：当前找 2x 的位置，初始为 1',
        'for index in range': '枚举 `index = {index}`，即 `changed[{index}]` = `{changed[index]}`',
        'if index not in used': lambda S, B, ret: (f'下标 `{S.index}` 已被剔除（它是某个 x 的双倍）→ 跳过' if S.index in S.used
                                                  else f'下标 `{S.index}` 还在 → `{S.changed[S.index]}` 是当前最小值，==必属于原数组=='),
        'if p <= index': lambda S, B, ret: (f'`p = {S.p} <= index = {S.index}`：2x 一定在 x 后面' if S.p <= S.index
                                            else f'`p = {S.p}` 已在 `index` 后面，不用动'),
        'p = index + 1': '`p` 挪到 `index + 1` = `{p}`',
        'while p < len(changed)': lambda S, B, ret: (
            f'`changed[{S.p}] = {S.changed[S.p]}` ≠ 2x = `{2 * S.changed[S.index]}` → 继续向后找' if S.p < len(S.changed) and S.changed[S.p] != 2 * S.changed[S.index]
            else (f'`changed[{S.p}] = {S.changed[S.p]}` 正好是 2x，找到了' if S.p < len(S.changed) else '`p` 走到末尾，没找到 2x')),
        'p += 1': lambda S, B, ret: (f'`p` → {S.p}' ),
        'if p == len(changed)': lambda S, B, ret: ('`p` 走到末尾：没有 2x 可配 → ==无解==，返回空数组' if S.p == len(S.changed)
                                                  else f'`p = {S.p}` 在范围内：找到了 2x = `{S.changed[S.p]}`'),
        'return []': '返回 `[]`',
        'used.add(index)': '剔除 x：`used` 加入 `{index}`',
        'used.add(p)': '剔除 2x：`used` 加入 `{p}`',
        'res.append': '`{changed[index]}` 属于原数组：`res = {res}`',
        'return res': '全部配对完，返回 `{res}`',
    },
    cards=dict(
        one_liner='排序后，最小值必来自原数组：找到它的双倍，一起剔除',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`changed` 是原数组每个数乘 2 再加入后打乱得到的',
                 '是双倍数组就返回原数组，否则返回 `[]`',
                 '本视频：`[3,2,1,16,2,6,4,1,8,2]` → `[1,1,2,3,8]`'],
        quote='如果原数组存在的话，那么双倍数组中的最小值必然来自于原数组。设这个最小值为x，那么就可以从双倍数组中剔除x和2x。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，每次最小的没剔除的数 `x` 必在原数组，它的 `2x` 要被剔除',
              '`x` 递增，`2x` 也递增 → 用指针 `p` 只往后走，不回头',
              '用 `used` 集合标记剔除的位置，不真的删除元素'],
        summary=['`index` 遍历每个位置一次，`p` 也至多走一遍，主体 `O(n)`；排序 `O(n log n)`',
                 '`p` 要保证 `> index`：2x 必在 x 的后面，所以 `p <= index` 时挪到 `index + 1`',
                 '易错：`p == len(changed)` 说明找不到 2x，必须返回 `[]`',
                 '对比灵神：灵神用哈希表计数 + 消消乐，免排序；这里是排序 + 双指针'],
    ),
)
