from functools import wraps
from pandas import DataFrame
import numpy as np
from copy import deepcopy


def np_cache(
	*,
	arg_num: int = 0,
	arg_name: str = "symbols",
):
	cache = {}

	def decorator(function):
		@wraps(wrapped=function)
		def wrapper(
			*args,
			**kwargs,
		):
			args = list(args)
			indexing_arguments = kwargs.pop(arg_name, None)
			if indexing_arguments is None:
				# Assuming target_arg is the first positional argument
				if len(args) > 0:
					indexing_arguments = args.pop(arg_num)
					kwarg = False
				else:
					raise TypeError("Not enough arguments")
			else:
				kwarg = True

			keys = [(indexing_argument, *tuple(args), *kwargs.items()) for indexing_argument in indexing_arguments]
			evaluate_indexing_arguments = np.array([key[0] for key in keys if key not in cache])

			eval_args = deepcopy(args)
			eval_kwargs = deepcopy(kwargs)
			if kwarg:
				eval_kwargs[arg_name] = evaluate_indexing_arguments
			else:
				eval_args.insert(arg_num, evaluate_indexing_arguments)

			if len(evaluate_indexing_arguments) > 0:
				new_values = function(
					*eval_args,
					**eval_kwargs,
				)

				for indexing_argument, new_value in zip(evaluate_indexing_arguments, new_values):
					cache[(indexing_argument, *tuple(args), *kwargs.items())] = new_value

			result = np.array([cache[(indexing_argument, *tuple(args), *kwargs.items())] for indexing_argument in indexing_arguments])

			return result

		return wrapper

	return decorator


def df_cache(
	*,
	arg_num: int = 0,
	arg_name: str = "symbols",
):
	columns = []
	cache = {}

	def decorator(function):
		@wraps(wrapped=function)
		def wrapper(
			*args,
			**kwargs,
		) -> DataFrame:
			args = list(args)
			indexing_arguments = kwargs.pop(arg_name, None)
			if indexing_arguments is None:
				# Assuming target_arg is the first positional argument
				if len(args) > 0:
					indexing_arguments = args.pop(arg_num)
					kwarg = False
				else:
					raise TypeError("Not enough arguments")
			else:
				kwarg = True

			keys = [(indexing_argument, *tuple(args), *kwargs.items()) for indexing_argument in indexing_arguments]
			evaluate_indexing_arguments = np.array([key[0] for key in keys if key not in cache])

			eval_args = deepcopy(args)
			eval_kwargs = deepcopy(kwargs)
			if kwarg:
				eval_kwargs[arg_name] = evaluate_indexing_arguments
			else:
				eval_args.insert(1, evaluate_indexing_arguments)

			if len(evaluate_indexing_arguments) > 0:
				new_df = function(
					*eval_args,
					**eval_kwargs,
				)

				for indexing_argument in new_df.index:
					cache[(indexing_argument, *tuple(args), *kwargs.items())] = tuple(new_df.loc[indexing_argument])

				if columns == []:
					for column in new_df.columns:
						columns.append(column)

			result = DataFrame.from_dict(
				{key[0]: cache_entry for key, cache_entry in cache.items() if key in keys},
				columns=columns,
				orient="index",
			).sort_index()

			return result

		return wrapper

	return decorator
