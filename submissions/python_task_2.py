import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
     unique_ids = df['id'].unique()
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    for i in unique_ids:
        for j in unique_ids:
            if i != j:
                distances_i_to_j = df[(df['id_start'] == i) & (df['id_end'] == j)]['distance'].sum()
                distances_j_to_i = df[(df['id_start'] == j) & (df['id_end'] == i)]['distance'].sum()
                total_distance = distances_i_to_j + distances_j_to_i
                distance_matrix.loc[i, j] = total_distance
                distance_matrix.loc[j, i] = total_distance

    distance_matrix.fillna(0, inplace=True)
    return distance_matrix.astype(float)


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """ unrolled_distance_matrix = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for i in distance_matrix.index:
        for j in distance_matrix.columns:
            if i != j:
                unrolled_distance_matrix = unrolled_distance_matrix.append({'id_start': i, 'id_end': j, 'distance': distance_matrix.loc[i, j]}, ignore_index=True)
    return unrolled_distance_matrix

    

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_avg_distance = unrolled_distance_matrix[unrolled_distance_matrix['id_start'] == reference_value]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    filtered_ids = unrolled_distance_matrix[(unrolled_distance_matrix['distance'] >= reference_avg_distance - threshold) &
                                            (unrolled_distance_matrix['distance'] <= reference_avg_distance + threshold)]['id_start'].unique()
    return sorted(filtered_ids)
   


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
   toll_rates = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle in toll_rates:
        unrolled_distance_matrix[vehicle] = unrolled_distance_matrix['distance'] * toll_rates[vehicle]
    return unrolled_distance_matrix



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                   (time(10, 0, 0), time(18, 0, 0)),
                   (time(18, 0, 0), time(23, 59, 59))]

    discount_factors = [0.8, 1.2, 0.8]

    for i, (start_time, end_time) in enumerate(time_ranges):
        mask = (unrolled_distance_matrix['start_time'] >= start_time) & (unrolled_distance_matrix['start_time'] <= end_time)
        unrolled_distance_matrix.loc[mask, 'distance'] *= discount_factors[i]

    return unrolled_distance_matrix
