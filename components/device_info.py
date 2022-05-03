import sys, socket
if '../' not in sys.path:
    sys.path.append('../')
import colors, fonts

padding = 10
font = fonts.font_lg

def draw(screen, rect, props):

    y_padding = (rect.height - (font.get_height() + font.get_height()))//2
    ip_address = socket.gethostbyname(socket.gethostname())

    # Draw IP Address
    ip_text = font.render(f'IP Address: {ip_address}', 1, colors.white)
    ip_text_rect = ip_text.get_rect()
    ip_text_rect.topleft = (rect.x + padding, rect.y + y_padding)
    screen.blit(ip_text, ip_text_rect)
