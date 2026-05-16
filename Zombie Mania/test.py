from tkinter import *
from random import *

# Функции ------------------------------------------------------------

def format_counter(counter):
    """Форматирование счётчика в строку из трёх символов."""
    return f'{counter:03}'

def final_show(frame=0):
    """Анимация завершения игры."""
    canvas.itemconfigure(game_over_id, image=overs[frame], anchor='nw')
    canvas.itemconfig(your_score_text_id, state='normal')
    canvas.itemconfig(game_over_text_id, state='normal')

    if frame + 1 < len(overs):
        canvas.after(50, final_show, frame + 1)

def game_over():
    """Функция обработки конца игры."""
    global gameover
    gameover = True
    canvas.itemconfig(game_over_id, state='normal')
    formatted_score = format_counter(score)

    for i in range(len(formatted_score)):
        canvas.itemconfigure(score_text_ids[i], image=list_score[int(formatted_score[i])], state='normal')

    final_show()

def update_timer():
    """Обновление таймера."""
    global time, gameover
    time -= 1
    if time < 0:
        game_over()
    else:
        canvas.itemconfig(timer_id, text=f'Таймер: {time}')
        canvas.after(1000, update_timer)

def hit():
    """Обработка попадания в зомби."""
    global score
    score += 1
    canvas.itemconfig(text_id, text=f'Очки: {score}')
    spawn()

def collision_detection(x, y):
    """Обработка коллизий."""
    position = canvas.coords(zombie_id)
    left, top = position[0], position[1]
    right, bottom = left + npc_width, top + npc_height
    return left <= x <= right and top <= y <= bottom

def animate_frame(frame=0):
    """Анимация зомби."""
    canvas.itemconfigure(zombie_id, image=photos[frame], anchor='nw')
    canvas.after(200, animate_frame, (frame + 1) % len(photos))

def move_to():
    """Движение зомби."""
    global zombie_vx, zombie_vy
    x = canvas.coords(zombie_id)[0] + zombie_vx
    y = canvas.coords(zombie_id)[1] + zombie_vy

    if x < 0 or x > game_width - npc_width:
        zombie_vx = -zombie_vx
    if y < 0 or y > game_height - npc_height:
        zombie_vy = -zombie_vy

    canvas.moveto(zombie_id, x, y)
    canvas.after(10, move_to)

def mouse_motion(event):
    """Обработка движения мыши."""
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y
    canvas.moveto(bita_id, mouse_x - 100, mouse_y - 100)

def game_update():
    """Обновление состояния игры."""
    spawn()
    canvas.after(1000, game_update)

def spawn():
    """Создание нового положения зомби."""
    global zombie_vx, zombie_vy
    x, y = randint(0, game_width - npc_width), randint(0, game_height - npc_height)

    if abs(mouse_x - x) < 100 and abs(mouse_y - y) < 100:
        x = (x + 200) % game_width
        y = (y + 200) % game_height

    canvas.moveto(zombie_id, x, y)
    zombie_vx, zombie_vy = choice(koef) * randint(1, 5), choice(koef) * randint(1, 5)

def mouse_click_down(event):
    """Обработка нажатия кнопки мыши."""
    if collision_detection(mouse_x - 100, mouse_y - 100):
        hit()
    canvas.itemconfig(bita_id, image=bita2, anchor=N)

def mouse_click_up(event):
    """Обработка отпускания кнопки мыши."""
    canvas.itemconfig(bita_id, image=bita, anchor=CENTER)

# Область глобальных переменных ------------------------------------------------------------

game_width, game_height = 750, 621
npc_width, npc_height = 150, 150
score, time, n = 0, 5, 0
gameover = False
mouse_x, mouse_y = 0, 0
zombie_vx, zombie_vy = 3, 5
koef = [-1, 1]

# Создание окна и виджетов ------------------------------------------------------------

window = Tk()
window.title('Зомбимания')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height)

# Загрузка изображений ------------------------------------------------------------

photos = [PhotoImage(file=f'Pvz_{i}.png') for i in range(1, 3)]
overs = [PhotoImage(file=f'Game_over_{i}.png') for i in range(1, 11)]
list_score = [PhotoImage(file=f'{i}.png') for i in range(10)]

background = PhotoImage(file='Руины_фон.png')
zombie_image = PhotoImage(file='Pvz_1.png')
bita = PhotoImage(file='Bita.png')
bita2 = PhotoImage(file='Bita2.png')

# Инициализация игровых объектов ------------------------------------------------------------

canvas.create_image(0, 0, image=background, anchor=NW)
zombie_id = canvas.create_image(0, 0, image=zombie_image, anchor=NW)
bita_id = canvas.create_image(mouse_x, mouse_y, image=bita, anchor=CENTER)

text_id = canvas.create_text(game_width - 10, 10, fill='black', font='Times 20 bold', text=f'Очки: {score}', anchor=NE)
timer_id = canvas.create_text(game_width - 10, 50, fill='black', font='Times 20 bold', text=f'Таймер: {time}', anchor=NE)

game_over_id = canvas.create_image(0, 0, image=overs[0], anchor=NW)
canvas.itemconfig(game_over_id, state='hidden')


game_over_text = PhotoImage(file='game_over_text.png')
game_over_text_id = canvas.create_image(100,50,image=game_over_text,anchor=NW,state='hidden')
your_score_text = PhotoImage(file='your_score_text.png')
your_score_text_id = canvas.create_image(60,300,image=your_score_text,anchor=NW,state='hidden')


# Инициализация таблицы очков ------------------------------------------------------------
score_text_ids = [
    canvas.create_image(550 + i * 60, 390, image=list_score[0], anchor=NW, state='hidden') for i in range(3)
]

# Связывание событий ------------------------------------------------------------

canvas.bind('<ButtonPress>', mouse_click_down)
canvas.bind('<ButtonRelease>', mouse_click_up)
canvas.bind('<Motion>', mouse_motion)
canvas.pack()

# Запуск игры ------------------------------------------------------------

update_timer()
animate_frame()
move_to()
game_update()

window.mainloop()
