'''
    Contains some functions to preprocess the data used in the visualisation.
'''
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
     # Regrouper les données par 'Player' et 'Act', en sommant le nombre de lignes
    data_grouped = (
        my_df.groupby(['Player', 'Act'])
        .agg({'Line': 'sum'})
        .reset_index()
        .rename(columns={'Line': 'PlayerLine'})
    )

    # Calculer le total des lignes par acte
    total_lines_per_act = data_grouped.groupby('Act')['PlayerLine'].transform('sum')

    # Calculer le pourcentage des lignes de chaque joueur par rapport au total de l'acte
    data_grouped['PlayerPercent'] = (data_grouped['PlayerLine'] / total_lines_per_act) * 100

    # Trier les données pour une meilleure lisibilité
    data_grouped = data_grouped.sort_values(by=['Act', 'Player'], ascending=[True, True])

    return data_grouped


def replace_others(my_df, top_n= 5):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other players
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
    # Vérifier si la colonne "Line" est bien utilisée pour compter les répliques
    my_df['Line'] = 1  # Chaque ligne représente une réplique

    # Identifier les top_n joueurs ayant le plus de répliques sur toute la pièce
    top_players_global = (
        my_df.groupby('Player')['Line'].count()  # Compter les répliques totales par joueur
        .reset_index()
        .sort_values(by='Line', ascending=False)  # Trier pour obtenir le top N global
        .head(top_n)  # Garder les premiers N joueurs sur toute la pièce
    )

    top_players_set = set(top_players_global['Player'])  # Ensemble des top joueurs

    # Remplacer les joueurs en dehors du top_n global par "Other"
    my_df['PlayerCategory'] = my_df.apply(
        lambda row: row['Player'] if row['Player'] in top_players_set else 'Other', axis=1
    )

    # Regrouper par 'PlayerCategory' et 'Act', puis compter le nombre de répliques
    data_grouped = (
        my_df.groupby(['PlayerCategory', 'Act'])
        .agg({'Line': 'count'})  # Compter les répliques et non les sommer
        .reset_index()
        .rename(columns={'Line': 'LineCount', 'PlayerCategory': 'Player'})
    )

    # Calculer le total des répliques par acte
    total_lines_per_act = data_grouped.groupby('Act')['LineCount'].transform('sum')

    # Calculer le pourcentage des répliques prononcées par catégorie de joueur
    data_grouped['LinePercent'] = (data_grouped['LineCount'] / total_lines_per_act) * 100

    # Trier pour une meilleure lisibilité
    data_grouped = (
    data_grouped.sort_values(['Act', 'Player'], ascending=[True, True])
    .reset_index(drop=True)
)

    return data_grouped


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    if 'Player' not in my_df.columns:
        raise ValueError("Le DataFrame doit contenir une colonne 'Player'")
    
    # Créer une copie pour éviter de modifier le DataFrame original
    df_copy = my_df.copy()
    
    # Appliquer .title() à chaque nom de joueur, en préservant 'OTHER' tel quel
    df_copy['Player'] = df_copy['Player'].apply(
        lambda x: x if x == 'OTHER' else x.title()
    )
    return df_copy

df = pd.read_csv(r"C:\Users\LENOVO\OneDrive\Documents\TP2_viz\code\code\src\assets\data\romeo_and_juliet.csv")
print(clean_names(replace_others(df, top_n=5)))
