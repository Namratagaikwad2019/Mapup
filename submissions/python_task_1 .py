import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
     df = pd.read_csv('dataset-1.csv')
    result_df = df.pivot(index='id_1', columns='id_2', values='car')
    result_df = result_df.fillna(0)
    for i in range(min(result_df.shape[0], result_df.shape[1])):
        result_df.iloc[i, i] = 0
    return result_df
df = 'dataset-1.csv'
result_dataframe = generate_car_matrix(df)
   return result_dataframe

  


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df = pd.read_csv(df)
     conditions = [(df['car'] <= 15),(df['car'] > 15) & (df['car'] <= 25),(df['car'] > 25)]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=choices, right=False)
     type_count = df['car_type'].value_counts().to_dict()

    sorted_type_count = dict(sorted(type_count.items()))
    return sorted_type_count
df = 'dataset-1.csv'
result_type_count = get_type_count(df)
     return result_type_count



   

def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
     mean_bus_value = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()
    bus_indexes.sort()
    return bus_indexes
df = pd.read_csv('dataset-1.csv')

result_indices = get_bus_indexes(df)
    return result_indices




def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    df = pd.read_csv(df)
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    sorted_filtered_routes = sorted(filtered_routes)
    return sorted_filtered_routes
file_path = 'dataset-1.csv'
result_routes = filter_routes(df)
    return result_routes



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
     modified_df = result_dataframe.copy()
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_df = modified_df.round(1)
    return modified_df
matrix=result_dataframe
modified_result_df = multiply_matrix(matrix)
      return modified_result_df



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
        df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    except pd.errors.OutOfBoundsDatetime as e:
        print(f"Error: {e}")
        return pd.Series(False, index=df.index) 
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    completeness_check = (
        (df['duration'] < pd.Timedelta('24 hours')) |
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.dayofweek != 0) |
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.dayofweek != 6)
    )
    return completeness_check
df= 'dataset-2.csv'
df_dataset_2 = pd.read_csv(df)
result_completeness = time_check(df) 
    return result_completeness


