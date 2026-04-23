# import pytest
#
# @pytest.mark.parametrize("x,y,z",[
#     (1, 2, 3),
#     (4, 5, 9),
#     (4, 2, 6),
# ])
# def test(x,y,z):
#     print(x,y,z)
#     assert x+y == z

a = [3, 4, 5, 6, 7, 8, 9]
res = list(map(lambda x: "Even" if x % 2 == 0 else "Odd", a))

print(res)