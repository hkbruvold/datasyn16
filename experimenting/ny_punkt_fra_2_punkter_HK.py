# Gitt to punkt, finn ny punkt i forlengelsen

def punkt_fra_y(x_0, y_0, a, return_y):
    my_y = return_y
    my_x = (my_y - y_0)/a + x_0
    return (my_x, my_y)


def ny_punkter(punkt_1, punkt_2):
    return_large_y = 100
    return_small_y = 0
    if (punkt_1[1] == punkt_2[1]):
        print("This isn't supposed to happen, samme y verdi")
        return
    if (punkt_1[0] == punkt_2[0]):
        return ((punkt_1[0], return_small_y), (punkt_1[0], return_large_y))
    first = ()
    second = ()
    if (punkt_1[0] < punkt_2[0]):
        first = punkt_1
        second = punkt_2
    else:
        first = punkt_2
        second = punkt_1
    a = (second[1] - first[1])/(second[0] - first[0])
    return_first = punkt_fra_y(first[0], second[0], a, return_small_y)
    return_second = punkt_fra_y(first[0], second[0], a, return_large_y)
    return (return_first, return_second)

print(ny_punkter((1, 1), (1, 2)))
