'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

from hover_template import get_hover_template
from modes import MODES, MODE_TO_COLUMN
from template import THEME, create_template


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'.

        Returns:
            fig: The figure which will display the bar chart
    '''
    # Initialiser la figure vide
    fig = go.Figure()

    # S'assurer que le template personnalisé est créé
    create_template()

    # Modifier le layout pour éviter les erreurs d'affichage
    fig.update_layout(
        template="simple_white+custom_theme",  # Utilisation de simple_white seulement pour éviter les erreurs
        title=dict(
            text="Lines per Act",
            font=dict(
                family=THEME.get('font_family', "Arial"),  # Vérifier que THEME est bien défini
                color=THEME.get('font_color', "black")     # Vérifier que THEME est bien défini
            )
        ),
         # Add these lines to control size
        width=800,   # Wider figure
        height=500,  # Taller figure
        margin=dict(l=50, r=50, t=50, b=50), # Adjust margins for better spacing

        xaxis=dict(
            title="Act",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Act 1', 'Act 2', 'Act 3', 'Act 4', 'Act 5']
        ),
        yaxis=dict(
            title="Lines",
            autorange = True,  # Valeur par défaut, sera mise à jour plus tard
            showline=True,
            zeroline=True
        ),
        barmode = 'stack'
    )

    return fig


def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode
    # Vérifier si le mode est valide
    mode = mode.lower()

    if mode not in ['count', 'percent']:
        raise ValueError("Invalid mode. Choose 'LineCount' or 'LinePercent'.")
    # Sélectionner la bonne colonne
    y_col = MODE_TO_COLUMN[MODES[mode]]
    y_axis_title = "Lines(Count)" if mode == "count" else "Lines(%)"

    fig.data = []

    # Ajouter les barres pour chaque joueur
    for player in data['Player'].unique():
        player_data = data[data['Player'] == player]
        fig.add_trace(go.Bar(name=player, x=player_data['Act'], y=player_data[y_col], hovertemplate= get_hover_template (player, mode)))

    # Mettre à jour le layout
    fig.update_layout(
        title="Lines per Act",
        xaxis_title="Act",
        yaxis_title=y_axis_title,
        barmode='stack',  # Appliquer la bonne répartition
    )
    return fig

def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    # Vérifier si le mode est valide
    if mode not in ['count', 'percent']:
        raise ValueError("Invalid mode. Choose 'count' or 'percent'.")

    # Définir le titre de l'axe Y en fonction du mode
    y_axis_title = "Lines(Count)" if mode == "count" else "Lines(%)"

    # Mettre à jour le layout de l'axe Y
    fig.update_layout(
      yaxis_title = y_axis_title
    )

    return fig  # Retourne la figure mise à jour