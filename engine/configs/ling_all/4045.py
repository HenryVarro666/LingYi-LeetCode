CONFIG = dict(
    num=4045, title='统计机器人组数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='正序遍历 + 单调栈',
    tags=['栈', '邻项消除', '难度分 1888'],
    code='''
class Solution:
    def countGroups(self, position: list[int], speed: list[int], distance: int) -> int:
        n = len(position)
        st = [-1]  # 哨兵
        for i, p in enumerate(position):
            # 找到这一组的最右侧机器人
            if i == n - 1 or position[i + 1] - p > distance:
                v = speed[i]
                while st[-1] > v:
                    st.pop()  # 栈顶机器人速度更快，一段时间后与机器人 i 合并
                st.append(v)
        return len(st) - 1  # 减去哨兵
''',
    call='Solution().countGroups([1,2,3,10,12,20,21], [5,1,4,3,2,9,6], 2)',
    expect=2,
    views=[
        dict(type='array', var='position', pointers={'i': 'blue'}, label='position', h=170,
             color=lambda S, i, v: 'green' if 'i' in S and i < len(S['position']) - 1 and S['position'][i + 1] - v > S.get('distance', 0) or i == len(S['position']) - 1 else None),
        dict(type='array', var='speed', pointers={'i': 'blue'}, label='speed', h=170),
        dict(type='stack', var='st', fmt=lambda x: '哨兵' if x == -1 else f'v={x}', label='栈（速度）', h=250),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'cyan'), ('v', 'v', 'pink'), ('st', 'st', 'green')],
    captions={
        'st = [-1]': '栈里放「组最右侧机器人」的速度；`-1` 是哨兵，保证栈不会空',
        'if i == n - 1': lambda S, B, r: (f'`position[{S.i+1}] - {S.p} = {S.position[S.i+1]-S.p}` ≤ `{S.distance}`：t=0 就和右边合并，不是最右侧，跳过'
                                          if S.i < S.n - 1 and S.position[S.i+1] - S.p <= S.distance
                                          else '这是一组的最右侧机器人（绿色位置），组的速度就是它的速度'),
        'v = speed[i]': '这一组的速度 `v = {v}`',
        'while st[-1] > v': lambda S, B, r: (f'栈顶 `{S.st[-1]}` > `{S.v}`：栈顶更快，会追上 `v` 并合并 → 成立' if S.st[-1] > S.v
                                             else f'栈顶 `{S.st[-1]}` ≤ `{S.v}`：追不上，停止弹栈'),
        'st.pop()': '栈顶那组被合并掉（合并后继承右边的速度），弹出，栈 `{st}`',
        'st.append(v)': '`{v}` 入栈：栈从底到顶速度不降，谁也追不上右边 → `{st}`',
        'return len': '栈里剩下的就是最终的组：`{len(st)} - 1 = {len(st)-1}`',
    },
    cards=dict(
        one_liner='先合并 t=0 的组，再用栈弹掉会被追上的组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['机器人在数轴上向右匀速跑，距离 `<= distance` 就合并成组',
                 '合并后的组取最右侧机器人的位置和速度，求最终组数',
                 '示例：`position=[1,5,6,20]`，`speed=[4,3,2,3]`，`distance=1` → `2`'],
        quote='如果当前机器人的速度比栈顶小，那么栈顶机器人就会在一定时间后与当前机器人合并，于是弹出栈顶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先找出 t=0 就合并的：相邻间距 `> distance` 处就是一组的「最右侧机器人」',
              '只看这些最右侧机器人的速度：左边更快的会追上右边更慢的',
              '栈顶更快就弹出，最后栈内速度单调不降，谁也追不上谁'],
        after=[dict(heading='另一种写法', lines=['倒序遍历，维护「最右侧机器人」速度的最小值 `mn`', '速度 `<= mn` 且间距 `> distance` 就答案加一，空间 `O(1)`'])],
        summary=['时间 `O(n)`：每个元素至多入栈出栈各一次',
                 '易错：只有「最右侧机器人」才入栈，t=0 就合并的要先跳过',
                 '栈顶速度相等时不弹：追不上，不会合并',
                 '同类题：853 车队、1776 车队 II'],
    ),
)
