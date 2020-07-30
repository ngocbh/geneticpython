from geneticpython.utils import visualize_fronts

visualize_fronts(title='haha',
                 save=True,
                 show=True,
                 pareto_dict={'nsgaii_pareto': [[1, 2], [3, 4]],
                              'moead_pareto': [[4, 5], [5, 6]]})
