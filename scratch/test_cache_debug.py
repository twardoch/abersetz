from twat_cache import bcache


@bcache(folder_name="test_debug_cache")
def my_func(a, b):
    print("MY_FUNC CALLED")
    return a + b


print("Call 1:")
print(my_func(1, 2))
print("Call 2:")
print(my_func(1, 2))
