'''
    Provides the template for the hover tooltips.
'''
from modes import MODES


def get_hover_template(name, mode):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * A title stating player name with:
                - Font family: Grenze Gotish
                - Font size: 24px
                - Font color: Black
            * The number of lines spoken by the player, formatted as:
                - The number of lines if the mode is 'Count ("X lines").
                - The percent of lines fomatted with two
                    decimal points followed by a '%' symbol
                    if the mode is 'Percent' ("Y% of lines").

        Args:
            name: The hovered element's player's name
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''
    # TODO: Generate and return the over template
    # Start with the player name title using specified font styling
    template = '<span style="font-family: Grenze Gotish; font-size: 24px; color: black;">{}</span><br>'.format(name)
    
    # Add the lines information based on mode
    if mode == 'count':
        template += '%{value} lines'
    elif mode == 'percent':
        template += '%{value:.2f}% of lines'
        
    return template
