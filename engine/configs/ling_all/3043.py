CONFIG = dict(
    num=3043, title='最长公共前缀的长度', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 整数除 10 取前缀',
    tags=[],
    code='''
class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        st = set()
        for x in arr1:
            while x and x not in st:  # 如果 x 在 st 中，那么剩余前缀也在 st 中
                st.add(x)
                x //= 10

        mx = 0
        for x in arr2:
            while x and x not in st:
                x //= 10
            mx = max(mx, x)
        return len(str(mx)) if mx else 0
''',
    call='Solution().longestCommonPrefix([123, 45, 678], [1290, 6789, 9])',
    expect=3,
    views=[
        dict(type='array', var='arr1', label='arr1', h=130),
        dict(type='array', var='arr2', label='arr2', h=130),
        dict(type='set', var='st', label='st：arr1 的所有前缀', h=150),
        dict(type='text', h=60, fn=lambda S: (f"当前 x = =={S['x']}==　　目前最大公共前缀 mx = =={S['mx']}==" if 'mx' in S else f"当前 x = =={S['x']}==") if 'x' in S else ''),
    ],
    watch=[('x', 'x', 'orange'), ('mx', 'mx', 'green')],
    captions={
        'st = set()': '`st` 用来装 arr1 里所有数的前缀',
        'for x in arr1': lambda S, B, r: '`arr1` 遍历完了，st 里有它所有的前缀' if S.x == 0 and B.get('x') == 0 else f'取 arr1 的数 `x = {S.x}`',
        'while x and x not in st': lambda S, B, r: (
            f'`x = {S.x}`' + ('：已经变成 0，前缀都处理完了' if not S.x else
                              f'：`{S.x}` 已在 st 里 → 它和更短的前缀都存过了，不用再加' if S.x in S.st else
                              '：还不在 st 里 → 继续加入')) if 'mx' not in S else (
            f'`x = {S.x}`' + ('：变成 0，arr2 的这个数没有公共前缀' if not S.x else
                              f'：`{S.x}` 在 st 里 → 它是公共前缀，停止缩短' if S.x in S.st else
                              '：不在 st 里 → 去掉最后一位继续试')),
        'st.add(x)': '把前缀 `{x}` 加入 st',
        'x //= 10': '去掉最后一位：`x` → {x}（得到更短的前缀）',
        'mx = 0': '`mx` 记录所有公共前缀里的最大值：数值越大，位数越多',
        'for x in arr2': lambda S, B, r: '`arr2` 也遍历完了' if S.x == 0 and B.get('x') == 0 else f'取 arr2 的数 `x = {S.x}`，从最长前缀开始往短了试',
        'mx = max': '`mx = max({B.mx}, {x}) = {mx}`（`x` 是 0 说明没有公共前缀）',
        'return len': '`mx = {mx}` → 位数 = =={ret}==',
    },
    cards=dict(
        one_liner='整数除 10 就是去掉最后一位，数值最大的公共前缀位数最多',
        complexity='时间 `O((n+m) log U)`，空间 `O(n log U)`',
        problem=['两个正整数数组 `arr1`、`arr2`，各取一个数，求它们的最长公共前缀的长度',
                 '前缀指最左边的若干位，例如 `123` 是 `12345` 的前缀',
                 '本视频：`[123,45,678]` 和 `[1290,6789,9]` → 最长公共前缀 `678`，长度 ==3=='],
        quote='不断地把元素 x 除以 10（下取整）直到 0，例如 123→12→1→0，这个过程中的数即为 x 的前缀。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 arr1 所有前缀放进集合：`x //= 10` 一路得到 `x` 的各个前缀',
              '==如果 x 已在 st 中，剩余前缀也一定在==，所以可以提前停止',
              '对 arr2 的每个数一路除 10，遇到第一个在集合中的就是它最长的公共前缀；取数值最大的，最后再算位数'],
        summary=['时间 `O((n+m) log U)`，空间 `O(n log U)`',
                 '"取数值最大" 等价于 "取位数最长"，最后用 `len(str(mx))` 一次性转换',
                 '易错：`mx` 为 0 时要返回 0，不能算 `len("0")`',
                 '方法一：把前缀当字符串存进集合，复杂度多一个 log'],
    ),
)
