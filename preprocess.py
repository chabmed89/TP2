'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN

import pandas as pd
from modes import MODE_TO_COLUMN

def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act

    # The sum of lines per player per act
    line_counts = my_df.groupby(['Act', 'Player']).size().reset_index(name='LineCount')
    # Calculate the total lines per act
    total_lines_per_act = my_df.groupby('Act').size().reset_index(name='TotalLines')
    # Merge the line counts with the total lines per act
    merged_df = pd.merge(line_counts, total_lines_per_act, on='Act')
    # Calculate the percentage of lines per player per act
    merged_df['LinePercent'] = (merged_df['LineCount'] / merged_df['TotalLines']) * 100
    merged_df.drop(columns=['TotalLines'], inplace=True)
    
    return merged_df

def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other plyaers
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage
    
    # Calculate the total lines for each player across all acts
    total_lines_per_player = (
        my_df.groupby('Player')
        .agg({'LineCount': 'sum', 'LinePercent': 'sum'})
        .reset_index()
    )

    # Find the top 5 players with the most lines in the entire play
    top_5_players = total_lines_per_player.nlargest(5, 'LineCount')['Player']

    # Filter the original DataFrame to keep only the top 5 players
    top_5_df = my_df[my_df['Player'].isin(top_5_players)]

    # Group the remaining players as 'OTHER' and aggregate their lines and percentages
    others_df = my_df[~my_df['Player'].isin(top_5_players)]
    others_aggregated = (
        others_df.groupby('Act')
        .agg({'LineCount': 'sum', 'LinePercent': 'sum'})
        .reset_index()
    )
    others_aggregated['Player'] = 'OTHER'

    # Combine the top 5 players and the 'OTHER' group
    result_df = pd.concat([top_5_df, others_aggregated], ignore_index=True)

    # Sort the final DataFrame by 'Act' and 'Player'
    result_df = result_df.sort_values(by=['Act', 'Player'], ascending=[True, True])

    return result_df

def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names

    my_df['Player'] = my_df['Player'].str.title()
    my_df = my_df.reset_index(drop=True)
    return my_df

# my_df = pd.read_csv('src/assets/data/romeo_and_juliet.csv')
# merged_df = summarize_lines(my_df)
# result_df = replace_others(merged_df)
# result = clean_names(result_df)
# print(result)
