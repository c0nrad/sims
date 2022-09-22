def factorial(a):
    if a == 0:
        return 1
    return a * factorial(a - 1)


print(factorial(200))
print(factorial(200.0))

# print(
#     len(
#         '788657867364790503552363213932185062295135977687173263294742533244359449963403342920304284011984623904177212138919638830257642790242637105061926624952829931113462857270763317237396988943922445621451664240254033291864131227428294853277524242407573903240321257405579568660226031904170324062351700858796178922222789623703897374720000000000000000000000000000000000000000000000000'
#     )
# )

# Over 308 digits, so it's inf for floats