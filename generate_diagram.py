import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Настройки шрифтов
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri', 'sans-serif']

# Создаем широкоформатную фигуру высокого разрешения
fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Заголовок схемы
ax.text(50, 98.5, 'МНЕМОСХЕМА БИЗНЕС-ПРОЦЕССА «ПРОДАЖА ТОВАРОВ В ПРОДУКТОВОМ МАГАЗИНЕ»', 
        ha='center', va='top', fontsize=16.5, fontweight='bold', color='#1A365D')

# ----------------- ЛЕГЕНДА ТИПОВ ВЗАИМОДЕЙСТВИЯ -----------------
# Рамка легенды: от 2.0 до 98.0 (ширина 96)
legend_box = patches.FancyBboxPatch((2.0, 91.8), 96.0, 4.6, boxstyle='round,pad=0.2,rounding_size=1',
                                   linewidth=1.4, edgecolor='#CBD5E0', facecolor='#F8FAFC')
ax.add_patch(legend_box)
ax.text(3.5, 94.1, 'ТИПЫ ВЗАИМОДЕЙСТВИЯ:', fontsize=9.5, fontweight='bold', color='#2D3748', va='center')

# 1. Устный
ax.plot([18.5, 21.0], [94.1, 94.1], color='#805AD5', lw=2.2, linestyle=':')
ax.scatter([21.0], [94.1], color='#805AD5', marker='>', s=50, zorder=5)
ax.text(21.8, 94.1, 'Устный (речь, диалог)', fontsize=8.6, color='#553C9A', va='center', fontweight='bold')

# 2. Материальный
ax.plot([36.5, 39.0], [94.1, 94.1], color='#2F855A', lw=2.2)
ax.scatter([39.0], [94.1], color='#2F855A', marker='>', s=50, zorder=5)
ax.text(39.8, 94.1, 'Материальный (товары, деньги, карты)', fontsize=8.6, color='#22543D', va='center', fontweight='bold')

# 3. Бумажный
ax.plot([60.5, 63.0], [94.1, 94.1], color='#DD6B20', lw=2.2)
ax.scatter([63.0], [94.1], color='#DD6B20', marker='>', s=50, zorder=5)
ax.text(63.8, 94.1, 'Бумажный (чеки, ценники, отчеты)', fontsize=8.6, color='#C05621', va='center', fontweight='bold')

# 4. Электронный (сигналы, запросы) - четко внутри рамки с запасом
ax.plot([81.0, 83.5], [94.1, 94.1], color='#2B6CB0', lw=2.2)
ax.scatter([83.5], [94.1], color='#2B6CB0', marker='>', s=50, zorder=5)
ax.text(84.3, 94.1, 'Электронный (сигналы, запросы)', fontsize=8.6, color='#2B6CB0', va='center', fontweight='bold')


# ----------------- ВНЕШНИЕ ЗОНЫ И ПОДРАЗДЕЛЕНИЯ -----------------
# 1. Главный внешний контур - Организация: Магазин "Продукты"
shop_box = patches.FancyBboxPatch((2.0, 3.5), 83.0, 86.0, boxstyle='round,pad=0.5,rounding_size=2',
                                  linewidth=2.2, edgecolor='#2B6CB0', facecolor='#F8FAFC', linestyle='--')
ax.add_patch(shop_box)
ax.text(3.8, 87.2, 'ОРГАНИЗАЦИОННАЯ СТРУКТУРА: МАГАЗИН «ПРОДУКТЫ»', fontsize=11.5, fontweight='bold', color='#2B6CB0')

# 2. Зона 1: Торговый зал
z1 = patches.FancyBboxPatch((3.0, 37.0), 18.5, 48.5, boxstyle='round,pad=0.4,rounding_size=1.5',
                            linewidth=1.6, edgecolor='#4299E1', facecolor='#EBF8FF')
ax.add_patch(z1)
ax.text(4.2, 83.3, 'ПОДРАЗДЕЛЕНИЕ:\nТОРГОВЫЙ ЗАЛ', fontsize=9.5, fontweight='bold', color='#2B6CB0')

# 3. Зона 2: Кассовый узел
z2 = patches.FancyBboxPatch((32.5, 37.0), 51.5, 48.5, boxstyle='round,pad=0.4,rounding_size=1.5',
                            linewidth=1.6, edgecolor='#DD6B20', facecolor='#FFFAF0')
ax.add_patch(z2)
ax.text(34.0, 83.3, 'ПОДРАЗДЕЛЕНИЕ: КАССОВЫЙ УЗЕЛ (ЗОНА РАСЧЕТА)', fontsize=10.0, fontweight='bold', color='#C05621')

# 4. Зона 3: Бэк-офис и Серверная
z3 = patches.FancyBboxPatch((3.0, 4.5), 81.0, 30.5, boxstyle='round,pad=0.4,rounding_size=1.5',
                            linewidth=1.6, edgecolor='#38A169', facecolor='#F0FFF4')
ax.add_patch(z3)
ax.text(52.0, 32.2, 'ПОДРАЗДЕЛЕНИЕ: БЭК-ОФИС И ИТ-ИНФРАСТРУКТУРА', fontsize=10.0, fontweight='bold', color='#276749')

# 5. Внешняя среда: Банк-эквайер
ext = patches.FancyBboxPatch((86.5, 37.0), 11.5, 48.5, boxstyle='round,pad=0.4,rounding_size=1.5',
                             linewidth=2.2, edgecolor='#805AD5', facecolor='#FAF5FF', linestyle=':')
ax.add_patch(ext)
ax.text(92.2, 82.5, 'ВНЕШНЯЯ СРЕДА:\nБАНК-ЭКВАЙЕР\n(ПРОЦЕССИНГ)', ha='center', va='top', fontsize=9.2, fontweight='bold', color='#6B46C1')


# ----------------- КАРТОЧКИ СУЩНОСТЕЙ -----------------
def draw_card(x, y, w, h, title, subtitle, header_color='#2B6CB0', is_subject=False):
    card = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.2,rounding_size=1',
                                  linewidth=1.5, edgecolor=header_color, facecolor='#FFFFFF', zorder=3)
    ax.add_patch(card)
    
    header_h = 3.2
    header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, boxstyle='round,pad=0.2,rounding_size=1',
                                    linewidth=0, facecolor=header_color, zorder=3)
    ax.add_patch(header)
    
    card_type = 'СУБЪЕКТ' if is_subject else 'ОБЪЕКТ'
    ax.text(x + w/2, y + h - header_h/2, f'[{card_type}]', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#FFFFFF', zorder=4)
    
    ax.text(x + w/2, y + (h - header_h)/2 + 0.8, title, ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1A202C', zorder=4)
    if subtitle:
        ax.text(x + w/2, y + 1.2, subtitle, ha='center', va='bottom', fontsize=7.4, color='#718096', zorder=4)

# 1. Торговый зал:
draw_card(4.2, 69.5, 16.0, 12.5, 'Витрина / Полка\nс продуктами', 'Продукты, ценники', '#3182CE', False)
draw_card(4.2, 40.5, 16.0, 23.0, 'Покупатель\n(Клиент магазина)', 'Потребитель товаров', '#2B6CB0', True)

# 2. Кассовый узел:
# Верхний ряд (y=69.5..82.0)
draw_card(34.0, 69.5, 13.0, 12.5, 'Кассир-продавец\n(Оператор кассы)', 'Сотрудник расчета', '#DD6B20', True)
draw_card(62.0, 69.5, 13.0, 12.5, 'Сканер штрихкодов\n(Считыватель)', 'Лазерное сканирование', '#4A5568', False)

# Нижний ряд (y=40.5..55.5)
draw_card(34.0, 40.5, 13.0, 15.0, 'POS-терминал / ККМ\n(Фискальный рег.)', 'Кассовый ПК и принтер', '#C05621', False)
draw_card(62.0, 40.5, 13.0, 15.0, 'Банковский терминал\n(Пин-пад / Ридер)', 'Безналичная оплата', '#6B46C1', False)

# 3. Бэк-офис:
draw_card(4.2, 7.5, 30.0, 21.0, 'Товароучетная система\n(Сервер 1С:Предприятие)', 'База данных остатков и цен', '#38A169', False)
draw_card(52.0, 7.5, 30.0, 21.0, 'Администратор / Товаровед\n(Управляющий персоналом)', 'Контроль учета и остатков', '#276749', True)

# 4. Внешняя среда:
draw_card(87.5, 41.5, 9.5, 28.0, 'Процессинговый\nцентр банка\n(Сервер эквайера)', 'Авторизация и списание\nсредств со счета', '#805AD5', False)


# ----------------- ФУНКЦИЯ ОТРИСОВКИ СТРЕЛОК -----------------
def draw_flow(p1, p2, label, ftype='mat', label_pos=0.5, label_offset=(0, 0), font_size=7.2):
    colors = {
        'mat': ('#2F855A', '-'),
        'paper': ('#DD6B20', '-'),
        'elec': ('#2B6CB0', '-'),
        'oral': ('#805AD5', ':')
    }
    color, ls = colors[ftype]
    
    # Строго прямая стрелка, shrinkA=0, shrinkB=0 гарантирует четкую видимость начала и конца стрелки
    arrow = patches.FancyArrowPatch(p1, p2,
                                    arrowstyle='-|>,head_length=6.0,head_width=3.8',
                                    shrinkA=0, shrinkB=0,
                                    linewidth=1.9, linestyle=ls, color=color, zorder=2)
    ax.add_patch(arrow)
    
    # Расчет координаты подписи
    xm = p1[0] + (p2[0] - p1[0]) * label_pos + label_offset[0]
    ym = p1[1] + (p2[1] - p1[1]) * label_pos + label_offset[1]
    
    ax.text(xm, ym, label, fontsize=font_size, color=color, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.20', facecolor='#FFFFFF', edgecolor=color, linewidth=1.0, alpha=0.98), zorder=5)


# ----------------- 1. ТОРГОВЫЙ ЗАЛ (ВЕРТИКАЛЬНЫЕ СТРЕЛКИ) -----------------
# Витрина (y=69.5) -> Покупатель (y=63.5)
# Две параллельные строго вертикальные стрелки в левой части
draw_flow((8.0, 69.5), (8.0, 63.5), 'Товар (продукты)', 'mat', label_pos=0.5)
draw_flow((14.5, 69.5), (14.5, 63.5), 'Ценник (информация о цене)', 'paper', label_pos=0.5)


# ----------------- 2. ПОКУПАТЕЛЬ <-> POS-ТЕРМИНАЛ (ГОРИЗОНТАЛЬНЫЕ СТРЕЛКИ) -----------------
# Покупатель (x=20.2) <-> POS-терминал (x=34.0)
# 1. Оплата картой / наличными
draw_flow((20.2, 46.5), (34.0, 46.5), 'Банковская карта / наличные', 'mat', label_pos=0.5)
# 2. Сдача / слип-чек
draw_flow((34.0, 41.5), (20.2, 41.5), 'Сдача (наличные) / слип-чек', 'mat', label_pos=0.5)


# ----------------- 3. ПОКУПАТЕЛЬ <-> КАССИР (5 СТРОГО ПАРАЛЛЕЛЬНЫХ СТРЕЛОК БЕЗ ПЕРЕСЕЧЕНИЙ) -----------------
# Все 5 стрелок строго параллельны (dy = 19.0, dx = 13.8), монотонно упорядочены по высоте:
# y на Кассире (34.0): 81.5 > 78.5 > 75.5 > 72.5 > 69.5
# y на Покупателе (20.2): 62.5 > 59.5 > 56.5 > 53.5 > 50.5
# Пересечения математически исключены (0 перехлестов), все наконечники и истоки видны на 100%!

# 1. Упакованный товар в пакете (Кассир -> Покупатель)
draw_flow((34.0, 81.5), (20.2, 62.5), 'Упакованный товар в пакете', 'mat', label_pos=0.20, font_size=7.2)

# 2. Кассовый чек фискальный (Кассир -> Покупатель)
draw_flow((34.0, 78.5), (20.2, 59.5), 'Кассовый чек (фискальный)', 'paper', label_pos=0.65, font_size=7.2)

# 3. Товар на кассовой ленте (Покупатель -> Кассир)
draw_flow((20.2, 56.5), (34.0, 75.5), 'Товар на кассовой ленте', 'mat', label_pos=0.80, font_size=7.2)

# 4. Вопрос о товаре / скидке (Покупатель -> Кассир)
draw_flow((20.2, 53.5), (34.0, 72.5), 'Вопрос о товаре / скидке', 'oral', label_pos=0.35, font_size=7.2)

# 5. Сумма к оплате / ответ (Кассир -> Покупатель)
draw_flow((34.0, 69.5), (20.2, 50.5), 'Сумма к оплате / ответ', 'oral', label_pos=0.20, font_size=7.2)


# ----------------- 4. КАССОВЫЙ УЗЕЛ (ВНУТРЕННИЕ ПОТОКИ) -----------------
# Кассир -> Сканер (строго горизонтальная стрелка в зазоре 15.0 единиц!)
draw_flow((47.0, 77.5), (62.0, 77.5), 'Штрихкод на упаковке', 'elec', label_pos=0.5)

# Сканер -> POS-терминал (прямая диагональ в просторном пространстве)
draw_flow((62.0, 69.5), (47.0, 55.5), 'Цифровой код товара', 'elec', label_pos=0.5)

# POS-терминал -> Кассир (строго вертикальная стрелка справа, без сближения с другими стрелками!)
draw_flow((44.0, 55.5), (44.0, 69.5), 'Кассовый чек (печать)', 'paper', label_pos=0.5)

# POS-терминал <-> Банковский терминал (две строго горизонтальные стрелки в зазоре 15.0 единиц!)
draw_flow((47.0, 50.5), (62.0, 50.5), 'Сумма к списанию', 'elec', label_pos=0.5)
draw_flow((62.0, 44.5), (47.0, 44.5), 'Статус оплаты (успех)', 'elec', label_pos=0.5)


# ----------------- 5. БАНКОВСКИЙ ТЕРМИНАЛ <-> БАНК (ГОРИЗОНТАЛЬНЫЕ СТРЕЛКИ) -----------------
# Банковский терминал (x=75.0) <-> Банк (x=87.5) (зазор 12.5 единиц!)
draw_flow((75.0, 50.5), (87.5, 50.5), 'Запрос на авторизацию', 'elec', label_pos=0.5, font_size=7.1)
draw_flow((87.5, 44.5), (75.0, 44.5), 'Код подтверждения (одобрение)', 'elec', label_pos=0.5, font_size=7.1)


# ----------------- 6. POS-ТЕРМИНАЛ <-> СЕРВЕР 1С (ПРЯМЫЕ ДИАГОНАЛИ) -----------------
# Сервер 1С (x=4.2..34.2, y=7.5..28.5) <-> POS-терминал (x=34.0..47.0, y=40.5..55.5)
# Зазор по вертикали 12 единиц. Три параллельные диагонали с четким началом и концом

# 1. Запрос цены: сверху-справа вниз-влево
draw_flow((37.0, 40.5), (25.0, 28.5), 'Запрос цены и наличия', 'elec', label_pos=0.65, font_size=7.3)

# 2. Сведения о товаре: снизу-влево вверх-вправо
draw_flow((29.0, 28.5), (41.0, 40.5), 'Сведения о цене и товаре', 'elec', label_pos=0.50, font_size=7.3)

# 3. Данные о списании: сверху-справа вниз-влево
draw_flow((45.0, 40.5), (33.0, 28.5), 'Данные о списании проданного товара', 'elec', label_pos=0.35, font_size=7.3)


# ----------------- 7. СЕРВЕР 1С -> АДМИНИСТРАТОР (ГОРИЗОНТАЛЬНАЯ СТРЕЛКА) -----------------
# Сервер 1С (x=34.2) -> Администратор (x=52.0) (зазор 17.8 единиц!)
draw_flow((34.2, 18.0), (52.0, 18.0), 'Отчет о продажах и остатках', 'paper', label_pos=0.5)


plt.tight_layout()
plt.savefig('mnemoscheme_store.png', dpi=300, bbox_inches='tight')
print('Zero-intersection mnemoscheme generated successfully!')
