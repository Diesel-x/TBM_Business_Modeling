import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Настройка шрифтов для поддержки кириллицы
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_idef0_frame(ax, node="A-0", title="Выполнить розничную продажу товаров в магазине", 
                     c_num="1", context="TOP", author="Баянов Д.", project="ТБМ (Розничная торговля)", 
                     date="27.10.2026", rev="1.0"):
    """Отрисовка официальной рамки стандарта IDEF0"""
    # Внешняя рамка
    outer_box = patches.Rectangle((1.5, 1.5), 97.0, 97.0, fill=False, edgecolor='#0F172A', linewidth=2.0)
    ax.add_patch(outer_box)
    
    # Верхний колонтитул (Y от 92.5 до 98.5)
    ax.plot([1.5, 98.5], [92.5, 92.5], color='#0F172A', linewidth=1.5)
    
    # Вертикальные разделители верхнего колонтитула
    ax.plot([20.0, 20.0], [92.5, 98.5], color='#0F172A', linewidth=1.2)
    ax.plot([60.0, 60.0], [92.5, 98.5], color='#0F172A', linewidth=1.2)
    ax.plot([82.0, 82.0], [92.5, 98.5], color='#0F172A', linewidth=1.2)
    
    # Горизонтальные разделители в среднем блоке шапки
    ax.plot([20.0, 60.0], [95.5, 95.5], color='#0F172A', linewidth=1.0)
    ax.plot([40.0, 40.0], [92.5, 95.5], color='#0F172A', linewidth=1.0)
    
    # Текст верхнего колонтитула
    ax.text(2.5, 97.5, 'USED AT:', fontsize=8, color='#475569', weight='bold')
    
    ax.text(21.0, 97.5, f'AUTHOR: {author}', fontsize=9, color='#0F172A', weight='bold')
    ax.text(21.0, 94.0, f'DATE: {date}', fontsize=8.5, color='#334155')
    ax.text(41.0, 94.0, f'REV: {rev}', fontsize=8.5, color='#334155')
    
    ax.text(61.0, 97.5, f'PROJECT: {project}', fontsize=9, color='#0F172A', weight='bold')
    ax.text(61.0, 94.0, 'NOTES:  1  2  3  4  5  6  7  8  9  10', fontsize=8, color='#475569')
    
    # Блок статуса
    ax.text(83.0, 97.2, '[ ] WORKING', fontsize=8, color='#64748B')
    ax.text(83.0, 95.5, '[X] DRAFT', fontsize=8, color='#0F172A', weight='bold')
    ax.text(83.0, 93.8, '[ ] RECOMMENDED', fontsize=8, color='#64748B')
    
    # Нижний колонтитул (Y от 1.5 до 6.5)
    ax.plot([1.5, 98.5], [6.5, 6.5], color='#0F172A', linewidth=1.5)
    ax.plot([18.0, 18.0], [1.5, 6.5], color='#0F172A', linewidth=1.2)
    ax.plot([78.0, 78.0], [1.5, 6.5], color='#0F172A', linewidth=1.2)
    ax.plot([88.0, 88.0], [1.5, 6.5], color='#0F172A', linewidth=1.2)
    
    ax.text(2.5, 4.0, f'NODE:\n{node}', fontsize=10, color='#0F172A', weight='bold', va='center')
    ax.text(20.0, 4.0, f'TITLE:\n{title}', fontsize=9.5, color='#0F172A', weight='bold', va='center')
    ax.text(79.0, 4.0, f'NUMBER:\n{c_num}', fontsize=9, color='#0F172A', weight='bold', va='center')
    ax.text(89.0, 4.0, f'CONTEXT:\n{context}', fontsize=9, color='#0F172A', weight='bold', va='center')


def draw_arrow(ax, points, label="", label_pos=None, icom="", ha='center', va='center', 
               color='#0F172A', lw=1.5, fontsize=8.2, label_bg=True, label_offset=(0,0),
               draw_arrowhead=True):
    """Отрисовка ортогональной стрелки с изломами и стрелочным наконечником"""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    # Рисуем все сегменты кроме последнего
    if len(points) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, linewidth=lw, solid_capstyle='butt', zorder=2)
    
    # Рисуем последний сегмент
    p_from = points[-2]
    p_to = points[-1]
    
    if draw_arrowhead:
        ax.annotate('', xy=p_to, xytext=p_from,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, 
                                    shrinkA=0, shrinkB=0, mutation_scale=12),
                    zorder=2)
    else:
        ax.plot([p_from[0], p_to[0]], [p_from[1], p_to[1]], color=color, linewidth=lw, solid_capstyle='butt', zorder=2)
    
    # Отрисовка метки ICOM на старте/конце стрелки
    if icom:
        start_pt = points[0]
        dx = points[1][0] - points[0][0]
        dy = points[1][1] - points[0][1]
        
        icom_x, icom_y = start_pt[0], start_pt[1]
        if dx > 0: # слева направо
            icom_x += 0.8
            icom_y += 1.0
        elif dx < 0: # справа налево
            icom_x -= 0.8
            icom_y += 1.0
        elif dy > 0: # снизу вверх
            icom_x += 1.0
            icom_y += 0.8
        elif dy < 0: # сверху вниз
            icom_x += 1.0
            icom_y -= 0.8
            
        ax.text(icom_x, icom_y, icom, fontsize=8, color='#0369A1', weight='bold',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='#F0F9FF', edgecolor='#BAE6FD', lw=0.8),
                zorder=6)
        
    # Отрисовка текста названия стрелки
    if label:
        if label_pos is None:
            lx = (points[0][0] + points[1][0]) / 2 + label_offset[0]
            ly = (points[0][1] + points[1][1]) / 2 + label_offset[1]
        else:
            lx, ly = label_pos[0] + label_offset[0], label_pos[1] + label_offset[1]
            
        bbox_props = dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='none') if label_bg else None
        ax.text(lx, ly, label, fontsize=fontsize, color='#0F172A', weight='bold',
                ha=ha, va=va, bbox=bbox_props, zorder=6)


def draw_idef0_box(ax, x, y, w, h, text, num_str, fc='#FFFFFF', ec='#0F172A', lw=1.8, text_size=9.5):
    """Отрисовка функционального блока IDEF0"""
    box = patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=4)
    ax.add_patch(box)
    
    # Текст названия работы в центре
    ax.text(x + w / 2, y + h / 2, text, fontsize=text_size, color='#0F172A', weight='bold',
            ha='center', va='center', zorder=5)
    
    # Номер блока в правом нижнем углу
    num_box = patches.Rectangle((x + w - 3.4, y), 3.4, 2.3, facecolor='#F1F5F9', edgecolor=ec, linewidth=1.0, zorder=5)
    ax.add_patch(num_box)
    ax.text(x + w - 1.7, y + 1.15, num_str, fontsize=9.0, color='#0F172A', weight='bold',
            ha='center', va='center', zorder=6)


# ==============================================================================
# 1. ГЕНЕРАЦИЯ КОНТЕКСТНОЙ ДИАГРАММЫ A-0
# ==============================================================================
def generate_diagram_a_minus_0(output_path='idef0_a_minus_0.png'):
    fig, ax = plt.subplots(figsize=(22, 14), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Рамка IDEF0
    draw_idef0_frame(ax, node="A-0", title="Выполнить розничную продажу товаров в магазине", 
                     c_num="1", context="TOP")
    
    # Блок «ЦЕЛЬ И ТОЧКА ЗРЕНИЯ»
    purpose_box = patches.Rectangle((3.5, 78.5), 34.0, 12.0, facecolor='#F8FAFC', 
                                    edgecolor='#CBD5E1', linewidth=1.2, zorder=2)
    ax.add_patch(purpose_box)
    ax.text(4.5, 89.0, 'ЦЕЛЬ И ТОЧКА ЗРЕНИЯ:', fontsize=8.5, weight='bold', color='#1E293B')
    ax.text(4.5, 84.5, 'ЦЕЛЬ: Описать функциональную структуру процесса\nрозничной продажи товаров для регламентации\nработы кассиров и автоматизации товароучета.', 
            fontsize=7.8, color='#334155', linespacing=1.2)
    ax.text(4.5, 80.0, 'ТОЧКА ЗРЕНИЯ: Директор магазина (ведущий товаровед).', 
            fontsize=7.8, weight='bold', color='#1E293B')
    
    # Центральный функциональный блок A0
    box_x, box_y, box_w, box_h = 39.0, 38.0, 27.0, 22.0
    draw_idef0_box(ax, box_x, box_y, box_w, box_h, 
                   'Выполнить розничную\nпродажу товаров\nв магазине', '0', 
                   fc='#FFFFFF', ec='#0F172A', lw=2.0, text_size=11.5)
    
    # ---------------- ВХОДЫ (INPUTS) ----------------
    draw_arrow(ax, [(3.5, 54.0), (box_x, 54.0)], 
               label='Продовольственные товары со склада', label_pos=(21.0, 55.5), 
               icom='I1', fontsize=8.5)
    
    draw_arrow(ax, [(3.5, 49.0), (box_x, 49.0)], 
               label='Покупатель (запрос на покупку)', label_pos=(21.0, 50.5), 
               icom='I2', fontsize=8.5)
    
    draw_arrow(ax, [(3.5, 44.0), (box_x, 44.0)], 
               label='Платежные средства (наличные / карта)', label_pos=(21.0, 42.5), 
               icom='I3', fontsize=8.5)
    
    # ---------------- УПРАВЛЕНИЯ (CONTROLS) ----------------
    draw_arrow(ax, [(42.0, 92.5), (42.0, box_y + box_h)], 
               label='Закон РФ «О защите\nправ потребителей»', label_pos=(42.0, 83.0), 
               icom='C1', fontsize=8.0)
    
    draw_arrow(ax, [(47.0, 92.5), (47.0, box_y + box_h)], 
               label='Правила торговли\nтоварами', label_pos=(47.0, 72.0), 
               icom='C2', fontsize=8.0)
    
    draw_arrow(ax, [(52.0, 92.5), (52.0, box_y + box_h)], 
               label='Прейскурант\n(ценники)', label_pos=(52.0, 83.0), 
               icom='C3', fontsize=8.0)
    
    draw_arrow(ax, [(57.0, 92.5), (57.0, box_y + box_h)], 
               label='Инструкции кассира,\nкассовая дисциплина', label_pos=(57.0, 72.0), 
               icom='C4', fontsize=8.0)
    
    draw_arrow(ax, [(62.0, 92.5), (62.0, box_y + box_h)], 
               label='Регламент\nэквайринга банка', label_pos=(62.0, 83.0), 
               icom='C5', fontsize=8.0)
    
    # ---------------- МЕХАНИЗМЫ (MECHANISMS) ----------------
    draw_arrow(ax, [(41.5, 6.5), (41.5, box_y)], 
               label='Кассир-продавец', label_pos=(41.5, 16.0), 
               icom='M1', fontsize=8.0, ha='right', label_offset=(-0.8, 0))
    
    draw_arrow(ax, [(46.5, 6.5), (46.5, box_y)], 
               label='Сканер штрихкодов', label_pos=(46.5, 27.0), 
               icom='M2', fontsize=8.0, ha='right', label_offset=(-0.8, 0))
    
    draw_arrow(ax, [(51.0, 6.5), (51.0, box_y)], 
               label='POS-терминал\nс фискальным рег.', label_pos=(51.0, 16.0), 
               icom='M3', fontsize=8.0)
    
    draw_arrow(ax, [(56.0, 6.5), (56.0, box_y)], 
               label='Банковский терминал\n(пин-пад)', label_pos=(56.0, 27.0), 
               icom='M4', fontsize=8.0)
    
    draw_arrow(ax, [(60.5, 6.5), (60.5, box_y)], 
               label='Товароучетная система\n(1С:Предприятие)', label_pos=(60.5, 16.0), 
               icom='M5', fontsize=8.0, ha='left', label_offset=(0.8, 0))
    
    draw_arrow(ax, [(64.0, 6.5), (64.0, box_y)], 
               label='Администратор /\nТоваровед', label_pos=(64.0, 27.0), 
               icom='M6', fontsize=8.0, ha='left', label_offset=(0.8, 0))
    
    # ---------------- ВЫХОДЫ (OUTPUTS) ----------------
    draw_arrow(ax, [(box_x + box_w, 56.0), (96.5, 56.0)], 
               label='Приобретенный товар у покупателя', label_pos=(81.5, 57.5), 
               icom='O1', fontsize=8.5)
    
    draw_arrow(ax, [(box_x + box_w, 51.5), (96.5, 51.5)], 
               label='Фискальный кассовый чек', label_pos=(81.5, 53.0), 
               icom='O2', fontsize=8.5)
    
    draw_arrow(ax, [(box_x + box_w, 47.0), (96.5, 47.0)], 
               label='Банковский слип-чек', label_pos=(81.5, 48.5), 
               icom='O3', fontsize=8.5)
    
    draw_arrow(ax, [(box_x + box_w, 43.0), (96.5, 43.0)], 
               label='Кассовая выручка (в денежном ящике / на счете)', label_pos=(81.5, 44.5), 
               icom='O4', fontsize=8.5)
    
    draw_arrow(ax, [(box_x + box_w, 39.5), (96.5, 39.5)], 
               label='Отчет об остатках и продажах', label_pos=(81.5, 38.0), 
               icom='O5', fontsize=8.5)
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Context diagram A-0 generated: {output_path}')


# ==============================================================================
# 2. ГЕНЕРАЦИЯ ДИАГРАММЫ ДЕКОМПОЗИЦИИ A0
# ==============================================================================
def generate_diagram_a0(output_path='idef0_a0.png'):
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Рамка IDEF0
    draw_idef0_frame(ax, node="A0", title="Выполнить розничную продажу товаров в магазине", 
                     c_num="2", context="A-0")
    
    # ---------------- 5 ФУНКЦИОНАЛЬНЫХ БЛОКОВ ----------------
    bw, bh = 11.2, 7.2
    
    # Координаты 5 блоков с безупречным шагом и широкими коридорами
    a1_x, a1_y = 12.0, 77.0
    a2_x, a2_y = 27.5, 61.0
    a3_x, a3_y = 43.5, 45.0
    a4_x, a4_y = 59.5, 29.0
    a5_x, a5_y = 75.5, 13.0
    
    draw_idef0_box(ax, a1_x, a1_y, bw, bh, 'Отобрать товар\nв торговом зале', '1', text_size=8.5)
    draw_idef0_box(ax, a2_x, a2_y, bw, bh, 'Зарегистрировать\nтовар на кассе', '2', text_size=8.5)
    draw_idef0_box(ax, a3_x, a3_y, bw, bh, 'Принять оплату\n(провести расчет)', '3', text_size=8.5)
    draw_idef0_box(ax, a4_x, a4_y, bw, bh, 'Сформировать и\nвыдать чек', '4', text_size=8.5)
    draw_idef0_box(ax, a5_x, a5_y, bw, bh, 'Актуализировать\nостатки в 1С', '5', text_size=8.5)
    
    # ---------------- ВХОДЫ (INPUTS, СЛЕВА) ----------------
    # I1: Продовольственные товары со склада -> A1
    draw_arrow(ax, [(3.5, 81.5), (a1_x, 81.5)], 
               label='Продовольственные товары со склада', label_pos=(7.5, 82.7), 
               icom='I1', fontsize=7.8)
    
    # I2: Покупатель (запрос на покупку) -> A1
    draw_arrow(ax, [(3.5, 78.5), (a1_x, 78.5)], 
               label='Покупатель (запрос на покупку)', label_pos=(7.5, 77.3), 
               icom='I2', fontsize=7.8)
    
    # I3: Платежные средства (наличные / карта) -> A3
    draw_arrow(ax, [(3.5, 48.0), (a3_x, 48.0)], 
               label='Платежные средства (наличные / банковская карта)', label_pos=(23.5, 47.0), 
               icom='I3', fontsize=7.8)
    
    # ---------------- ВНУТРЕННИЕ ПОТОКИ (МЕЖДУ БЛОКАМИ) ----------------
    # A1 -> A2: Отобранный товар на кассовой ленте
    draw_arrow(ax, [(a1_x + bw, 81.5), (25.5, 81.5), (25.5, 66.0), (a2_x, 66.0)], 
               label='Отобранный товар\nна кассовой ленте', label_pos=(25.0, 74.0), 
               fontsize=7.2, ha='right')
    
    # A1 -> A2: Покупатель у кассовой зоны
    draw_arrow(ax, [(a1_x + bw, 78.5), (26.6, 78.5), (26.6, 62.5), (a2_x, 62.5)], 
               label='Покупатель\nу кассы', label_pos=(27.0, 71.0), 
               fontsize=7.0, ha='left')
    
    # A2 -> A3: Сумма к оплате (содержимое чека)
    draw_arrow(ax, [(a2_x + bw, 65.5), (41.5, 65.5), (41.5, 50.0), (a3_x, 50.0)], 
               label='Сумма к оплате\n(данные чека)', label_pos=(41.5, 58.0), 
               fontsize=7.2)
    
    # A2 -> A4: Товар к выдаче (готовый к упаковке)
    # Траектория проходит в просторном горизонтальном коридоре Y=40.0
    draw_arrow(ax, [(a2_x + bw, 62.0), (42.5, 62.0), (42.5, 40.0), (57.5, 40.0), (57.5, 34.0), (a4_x, 34.0)], 
               label='Зарегистрированный\nтовар к выдаче', label_pos=(50.0, 41.2), 
               fontsize=7.2)
    
    # A3 -> A4: Подтверждение оплаты (статус транзакции)
    draw_arrow(ax, [(a3_x + bw, 49.5), (56.5, 49.5), (56.5, 31.0), (a4_x, 31.0)], 
               label='Подтверждение оплаты\n(статус транзакции)', label_pos=(56.5, 43.5), 
               fontsize=7.2)
    
    # A4 -> A5: Данные о совершенной продаже
    draw_arrow(ax, [(a4_x + bw, 30.5), (73.5, 30.5), (73.5, 17.5), (a5_x, 17.5)], 
               label='Данные о совершенной\nпродаже (для списания)', label_pos=(73.5, 24.5), 
               fontsize=7.2)
    
    # ОБРАТНАЯ СВЯЗЬ: A5 -> A2 (Сведения о номенклатуре и ценах)
    # Траектория поднимается из A5 вверх, идет в верхнем коридоре Y=72.5 и входит в Control A2
    draw_arrow(ax, [(a5_x + bw/2, a5_y + bh), (a5_x + bw/2, 72.5), (a2_x + 8.5, 72.5), (a2_x + 8.5, a2_y + bh)], 
               label='Сведения о номенклатуре и остатках (обратная связь товароучетной базы «1С»)', 
               label_pos=(54.0, 73.7), fontsize=7.5)
    
    # ---------------- УПРАВЛЕНИЯ (CONTROLS, СВЕРХУ) ----------------
    # C1: Закон РФ «О защите прав потребителей» -> A1 и A4
    draw_arrow(ax, [(14.0, 92.5), (14.0, a1_y + bh)], 
               label='Закон «О защите прав\nпотребителей»', label_pos=(14.0, 88.0), 
               icom='C1', fontsize=7.2)
    # Ветвление C1 к A4: идет в высшем коридоре Y=85.0
    draw_arrow(ax, [(14.0, 85.0), (62.0, 85.0), (62.0, a4_y + bh)], 
               label='', draw_arrowhead=True)
    ax.scatter([14.0], [85.0], color='#0F172A', s=16, zorder=7)
    
    # C2: Правила торговли товарами -> A1 и A2
    draw_arrow(ax, [(17.5, 92.5), (17.5, a1_y + bh)], 
               label='Правила торговли\nтоварами', label_pos=(17.5, 88.0), 
               icom='C2', fontsize=7.2)
    # Ветвление C2 к A2: коридор Y=83.5
    draw_arrow(ax, [(17.5, 83.5), (30.0, 83.5), (30.0, a2_y + bh)], 
               label='', draw_arrowhead=True)
    ax.scatter([17.5], [83.5], color='#0F172A', s=16, zorder=7)
    
    # C3: Прейскурант (ценники) -> A1
    draw_arrow(ax, [(20.5, 92.5), (20.5, a1_y + bh)], 
               label='Прейскурант\n(ценники)', label_pos=(20.5, 88.0), 
               icom='C3', fontsize=7.2)
    
    # C4: Должностные инструкции и кассовая дисциплина -> A2, A3, A4, A5
    draw_arrow(ax, [(33.0, 92.5), (33.0, a2_y + bh)], 
               label='Инструкции кассира,\nкассовая дисциплина', label_pos=(33.0, 88.0), 
               icom='C4', fontsize=7.2)
    # Ветвление C4 к A3:
    draw_arrow(ax, [(33.0, 79.5), (46.5, 79.5), (46.5, a3_y + bh)], 
               label='', draw_arrowhead=True)
    ax.scatter([33.0], [79.5], color='#0F172A', s=16, zorder=7)
    # Ветвление C4 к A4:
    draw_arrow(ax, [(46.5, 56.0), (65.0, 56.0), (65.0, a4_y + bh)], 
               label='', draw_arrowhead=True)
    ax.scatter([46.5], [56.0], color='#0F172A', s=16, zorder=7)
    # Ветвление C4 к A5:
    draw_arrow(ax, [(65.0, 42.0), (84.0, 42.0), (84.0, a5_y + bh)], 
               label='', draw_arrowhead=True)
    ax.scatter([65.0], [42.0], color='#0F172A', s=16, zorder=7)
    
    # C5: Регламент эквайринга банка -> A3
    draw_arrow(ax, [(50.5, 92.5), (50.5, a3_y + bh)], 
               label='Регламент эквайринга\nбанка', label_pos=(50.5, 88.0), 
               icom='C5', fontsize=7.2)
    
    # ---------------- МЕХАНИЗМЫ (MECHANISMS, СНИЗУ) ----------------
    # M1: Кассир-продавец -> A2, A3, A4
    draw_arrow(ax, [(29.0, 6.5), (29.0, a2_y)], 
               label='Кассир-продавец', label_pos=(29.0, 10.5), 
               icom='M1', fontsize=7.2, ha='right', label_offset=(-0.6, 0))
    # Ветвление M1 к A3:
    draw_arrow(ax, [(29.0, 26.0), (45.5, 26.0), (45.5, a3_y)], 
               label='', draw_arrowhead=True)
    ax.scatter([29.0], [26.0], color='#0F172A', s=16, zorder=7)
    # Ветвление M1 к A4:
    draw_arrow(ax, [(45.5, 26.0), (61.5, 26.0), (61.5, a4_y)], 
               label='', draw_arrowhead=True)
    ax.scatter([45.5], [26.0], color='#0F172A', s=16, zorder=7)
    
    # M2: Сканер штрихкодов -> A2
    draw_arrow(ax, [(32.0, 6.5), (32.0, a2_y)], 
               label='Сканер штрихкодов', label_pos=(32.0, 15.5), 
               icom='M2', fontsize=7.2, ha='right', label_offset=(-0.6, 0))
    
    # M3: POS-терминал с фискальным регистратором -> A2, A3, A4
    draw_arrow(ax, [(35.5, 6.5), (35.5, a2_y)], 
               label='POS-терминал\nс фискальным рег.', label_pos=(35.5, 10.5), 
               icom='M3', fontsize=7.2)
    # Ветвление M3 к A3:
    draw_arrow(ax, [(35.5, 23.0), (49.5, 23.0), (49.5, a3_y)], 
               label='', draw_arrowhead=True)
    ax.scatter([35.5], [23.0], color='#0F172A', s=16, zorder=7)
    # Ветвление M3 к A4:
    draw_arrow(ax, [(49.5, 23.0), (64.5, 23.0), (64.5, a4_y)], 
               label='', draw_arrowhead=True)
    ax.scatter([49.5], [23.0], color='#0F172A', s=16, zorder=7)
    
    # M4: Банковский терминал (пин-пад) -> A3
    draw_arrow(ax, [(53.0, 6.5), (53.0, a3_y)], 
               label='Банковский терминал\n(пин-пад)', label_pos=(53.0, 10.5), 
               icom='M4', fontsize=7.2)
    
    # M5: Товароучетная система (сервер «1С:Предприятие») -> A2 и A5
    draw_arrow(ax, [(77.5, 6.5), (77.5, a5_y)], 
               label='Товароучетная система (1С)', label_pos=(77.5, 9.8), 
               icom='M5', fontsize=7.2, ha='right', label_offset=(-0.6, 0))
    # Ветвление M5 к A2: коридор Y=7.8
    draw_arrow(ax, [(77.5, 7.8), (38.0, 7.8), (38.0, a2_y)], 
               label='', draw_arrowhead=True)
    ax.scatter([77.5], [7.8], color='#0F172A', s=16, zorder=7)
    
    # M6: Администратор / Товаровед магазина -> A5
    draw_arrow(ax, [(83.5, 6.5), (83.5, a5_y)], 
               label='Администратор /\nТоваровед', label_pos=(83.5, 9.8), 
               icom='M6', fontsize=7.2, ha='left', label_offset=(0.6, 0))
    
    # ---------------- ВЫХОДЫ (OUTPUTS, СПРАВА) ----------------
    # O3: Банковский слип-чек (из A3)
    draw_arrow(ax, [(a3_x + bw, 49.0), (96.5, 49.0)], 
               label='Банковский слип-чек', label_pos=(88.5, 50.2), 
               icom='O3', fontsize=7.8)
    
    # O4: Кассовая выручка (из A3)
    draw_arrow(ax, [(a3_x + bw, 46.0), (96.5, 46.0)], 
               label='Кассовая выручка (в денежном ящике / на счете)', label_pos=(88.5, 44.8), 
               icom='O4', fontsize=7.8)
    
    # O1: Приобретенный товар у покупателя (из A4)
    draw_arrow(ax, [(a4_x + bw, 34.5), (96.5, 34.5)], 
               label='Приобретенный товар у покупателя', label_pos=(88.5, 35.7), 
               icom='O1', fontsize=7.8)
    
    # O2: Фискальный кассовый чек (из A4)
    draw_arrow(ax, [(a4_x + bw, 31.0), (96.5, 31.0)], 
               label='Фискальный кассовый чек', label_pos=(88.5, 29.8), 
               icom='O2', fontsize=7.8)
    
    # O5: Отчет об остатках и продажах (из A5)
    draw_arrow(ax, [(a5_x + bw, 16.5), (96.5, 16.5)], 
               label='Отчет об остатках и продажах', label_pos=(92.5, 17.7), 
               icom='O5', fontsize=7.8)
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Decomposition diagram A0 generated: {output_path}')


if __name__ == '__main__':
    generate_diagram_a_minus_0('idef0_a_minus_0.png')
    generate_diagram_a0('idef0_a0.png')
