
def align_time_axis(t_target, t):
    chosen_indice = [False] * len(t)
    index_current = 0
    for t_current in t_target:
        while t[index_current] < t_current:
            index_current += 1
        chosen_indice[index_current] = True
    return t[chosen_indice], chosen_indice