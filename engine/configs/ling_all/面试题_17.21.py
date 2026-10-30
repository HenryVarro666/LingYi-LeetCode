H = [0, 1, 0, 2, 1, 0, 1, 3, 2]


def _txt(S):
    if 'st' not in S:
        return ''
    st = S['st']
    if 'bottom_h' in S and 'left' in S and S.get('_line') in (11, 12):
        h = S['h']
        dh = min(S['height'][S['left']], h) - S['bottom_h']
        return (f"横着算：高 `min({S['height'][S['left']]}, {h}) − {S['bottom_h']}` = =={dh}==，"
                f"宽 `{S['i']} − {S['left']} − 1` = =={S['i'] - S['left'] - 1}==")
    return f'栈（下标）= `{st}`，对应高度 = `{[S["height"][k] for k in st]}`（从栈底到栈顶递减）'


CONFIG = dict(
    num='面试题 17.21', title='直方图的水量', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 横着填坑',
    code='''
class Solution:
    def trap(self, height: List[int]) -> int:
        ans = 0
        st = []
        for i, h in enumerate(height):
            while st and h >= height[st[-1]]:
                bottom_h = height[st.pop()]
                if not st:  # len(st) == 0
                    break
                left = st[-1]
                dh = min(height[left], h) - bottom_h  # 面积的高
                ans += dh * (i - left - 1)
            st.append(i)
        return ans
''',
    call=f'Solution().trap({H!r})',
    expect=5,
    views=[
        dict(type='bars', var='height', label='height（粉 = 当前 i；蓝 = 栈中的柱子）', h=330,
             pointers={'i': 'pink'},
             color=lambda S, k, v: 'pink' if k == S.get('i') else 'blue' if ('st' in S and k in S['st']) else None),
        dict(type='stack', var='st', label='st（柱子下标，栈顶在右）', fmt=lambda k: f'{k}（高{H[k]}）', h=130),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('i', 'i', 'pink'), ('h', 'h'), ('st', 'st', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计水量',
        'st = []': '栈里放下标，高度从栈底到栈顶==递减==',
        'for i, h in enumerate': lambda S, B, r: (f'看第 `{S.i}` 根柱子，高 `{S.h}`' if B.get('i') != S.i else '所有柱子都处理完了，遍历结束'),
        'while st and h >= height[st[-1]]': lambda S, B, r: (
            f'`h = {B.h}` ≥ 栈顶高 `{B.height[B.st[-1]]}`：栈顶柱子找到了「上一个更大元素」右边界 → 它是坑底，弹出'
            if B.st and B.h >= B.height[B.st[-1]] else
            ('栈空了，没有更高的左墙，不再弹' if not B.st else f'`h = {B.h}` < 栈顶高 `{B.height[B.st[-1]]}`：还没碰到右墙，不再弹')),
        'bottom_h = height[st.pop()]': '弹出栈顶，坑底高度 `bottom_h = {bottom_h}`',
        'if not st': lambda S, B, r: ('弹出后栈空：这个坑左边没有墙，接不了水 → `break`' if not B.st else f'栈里还剩 `{B.st}`：栈顶 `{B.st[-1]}` 就是坑的左墙'),
        'left = st[-1]': '左墙 = 新栈顶，下标 `{left}`，高 `{height[left]}`',
        'dh = min': '水位 = 两墙较矮者：`min({height[left]}, {h}) − {bottom_h}` = =={dh}==（面积的高）',
        'ans += dh': '宽 = `i − left − 1` = `{i} − {left} − 1` = {i - left - 1}，`ans += {dh} × {i - left - 1}` → =={ans}==',
        'st.append(i)': '`i = {i}` 入栈：弹完后栈里全比它高（或栈空）',
        'return ans': '返回总水量 =={ret}==',
    },
    cards=dict(
        one_liner='找上一个更大元素，在找的过程中「横着」填坑',
        complexity='时间 `O(n)`，空间 `O(min(n, U))`',
        problem=['`height[i]` 是宽为 1 的直方图柱子，倒水后能存多少水',
                 '示例：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`',
                 '本视频：`[0,1,0,2,1,0,1,3,2]` → `5`'],
        quote='单调栈的做法相当于「横着」计算面积。这个方法可以总结成 16 个字：找上一个更大元素，在找的过程中填坑。',
        quote_src='—— 灵茶山艾府题解',
        idea=['栈中保持高度递减；来了更高（或相等）的 `h`，栈顶就是坑底',
              '弹出坑底后，新栈顶是左墙、`h` 是右墙，水位取两墙较矮者',
              '这一层的水 = 高 `dh` × 宽 `i − left − 1`，一层一层填满'],
        summary=['时间 `O(n)`：每根柱子最多入栈、出栈各一次，虽是二重循环',
                 '`while` 里用 `>=`：栈中没有重复高度，重复多时更省空间',
                 '弹出后栈空要 `break`：没有左墙，这个坑接不了水',
                 '方法一：前后缀分解 `O(n)` 空间；方法二：相向双指针 `O(1)` 空间（「竖着」算）'],
    ),
)
