'''
    Creates the theme to be used in our bar chart.
'''
import plotly.graph_objects as go
import plotly.io as pio

THEME = {
    'bar_colors': [
        '#861388',
        '#d4a0a7',
        '#dbd053',
        '#1b998b',
        '#A0CED9',
        '#3e6680'
    ],
    'background_color': '#ebf2fa',
    'font_family': 'Montserrat',
    'font_color': '#898989',
    'label_font_size': 16,
    'label_background_color': '#ffffff'
}


def create_template():
    '''
        Adds a new layout template to pio's templates.

        The template sets the font color and
        font to the values defined above in
        the THEME dictionary.

        The plot background and paper background
        are the background color defined
        above in the THEME dictionary.

        Also, sets the hover label to have a
        background color and font size
        as defined for the label in the THEME dictionary.
        The hover label's font color is the same
        as the theme's overall font color. The hover mode
        is set to 'closest'.

        Also sets the colors for the bars in
        the bar chart to those defined in
        the THEME dictionary.

    '''
    # TODO : Define a theme as defined above
        # Créer un nouveau template
    template = go.layout.Template()

    # Configuration des polices et couleurs globales
    template.layout.font = dict(
        family=THEME['font_family'],
        color=THEME['font_color']
    )

    # Configuration des arrière-plans
    template.layout.plot_bgcolor = THEME['background_color']
    template.layout.paper_bgcolor = THEME['background_color']

    # Configuration des étiquettes au survol
    template.layout.hoverlabel = dict(
        bgcolor=THEME['label_background_color'],
        font=dict(
            size=THEME['label_font_size'],
            color=THEME['font_color']
        )
    )
    template.layout.hovermode = 'closest'

    # Configuration des couleurs des barres
    template.layout.colorway = THEME['bar_colors']

    # Ajouter le template aux templates disponibles de plotly
    pio.templates['custom_theme'] = template

    return template