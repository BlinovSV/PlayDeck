### БИБЛИОТЕКИ ###
import math as m
import numpy as np
import streamlit as st
import plotly.graph_objects as go

#### НАСТРОЙКА СТРАНИЦЫ ###
st.set_page_config(
    page_title='PLAY Deck', # Заголовок страницы
    page_icon='P', # Иконка страницы
    initial_sidebar_state='expanded', #Стартовое положение сайд-бара
    layout='wide', #Ширина страницы
    menu_items={
        'Get help': 'https://playcad.pro/help',
        'Report a bug': 'https://forms.yandex.ru/cloud/66c8846bf47e7330d8e212a7/',
        'About': 'Это приложение часть проекта PlayCAD. v.0.5'
    }
)

### СПРАВОЧНЫЕ ДАННЫЕ ###
# Расчетные характеристики материалов
Grades = {
    220: {'R_y': 215, 'R_s': 125, 'R_lp': 145},
    250: {'R_y': 245, 'R_s': 140, 'R_lp': 160},
    280: {'R_y': 270, 'R_s': 155, 'R_lp': 175},
    320: {'R_y': 310, 'R_s': 180, 'R_lp': 190},
    350: {'R_y': 330, 'R_s': 190, 'R_lp': 200},
    390: {'R_y': 370, 'R_s': 215, 'R_lp': 210},
    420: {'R_y': 400, 'R_s': 230, 'R_lp': 225},
    450: {'R_y': 425, 'R_s': 245, 'R_lp': 240}
}

# Коэффициенты для определения предельной поперечной силы по СП 260.1325800.2023
C_coef = {
    'Закреплённая на опоре': {
        'На одну полку': {
            'Концевая': {'C': 3, 'C_r': 0.08, 'C_b': 0.70, 'C_h': 0.055},
            'Промежуточная': {'C': 8, 'C_r': 0.10, 'C_b': 0.17, 'C_h': 0.004}},
        'На две полки': {
            'Концевая': {'C': 9, 'C_r': 0.12, 'C_b': 0.14, 'C_h': 0.040},
            'Промежуточная': {'C': 10, 'C_r': 0.11, 'C_b': 0.21, 'C_h': 0.020}}},
    'Не закреплённая на опоре': {
        'На одну полку': {
            'Концевая': {'C': 3, 'C_r': 0.08, 'C_b': 0.70, 'C_h': 0.055},
            'Промежуточная': {'C': 8, 'C_r': 0.10, 'C_b': 0.17, 'C_h': 0.004}},
    'На две полки': {
        'Концевая': {'C': 6, 'C_r': 0.16, 'C_b': 0.17, 'C_h': 0.050},
        'Промежуточная': {'C': 17, 'C_r': 0.10, 'C_b': 0.10, 'C_h': 0.046}}}
}

# Размеры профлистов по ГОСТ 24045-2016 
Decks_GOST24045_2016 = {
    'Н57-750': {'h': 57, 'b': 187.5, 'b_wf': 93, 'b_tf': 44, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 0, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 0, 'h_1': 57, 'h_s1': 0, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 4},
    'Н60-845': {'h': 60, 'b': 211.25, 'b_wf': 122, 'b_tf': 50, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 0, 'b_wfs': 16, 'h_wfs': 5, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 0, 'h_1': 60, 'h_s1': 0, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 3.5, 'n_cor': 4},
    'Н75-750': {'h': 75, 'b': 187.5, 'b_wf': 92, 'b_tf': 50, 'n_wfs' : 1, 'n_tfs': 0, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 8, 'h_1': 48, 'h_s1': 7, 'h_2': 0, 'h_s2':0, 'r': 5, 'r_s': 4, 'n_cor': 4},
    'Н114-600': {'h': 114, 'b': 200.0, 'b_wf': 104, 'b_tf': 60, 'n_wfs': 1, 'n_tfs': 1, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 18, 'h_tfs': 7, 'h_ws': 8, 'h_1': 81, 'h_s1': 7, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 3},
    'Н114-750': {'h': 114, 'b': 250.0, 'b_wf': 126, 'b_tf': 80, 'n_wfs': 2, 'n_tfs': 1, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 42, 'b_tfs': 18, 'h_tfs': 7, 'h_ws': 8, 'h_1': 81, 'h_s1': 7, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 3},
    'Н153-850': {'h': 153, 'b': 284.0, 'b_wf': 120, 'b_tf': 43, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 29, 'h_wfs': 5, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 7, 'h_1': 30, 'h_s1': 11, 'h_2': 71, 'h_s2': 11, 'r': 3, 'r_s': 3, 'n_cor': 3}
    }

# Размеры профилей по СТО 57398459-18-2024
Decks_STO_57398459_18_2024 = {
    'Н57-750': {'h': 57, 'b': 187.5, 'b_wf': 95, 'b_tf': 44, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 0, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 0, 'h_1': 57, 'h_s1': 0, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 4},
    'Н60-845': {'h': 60, 'b': 211.25, 'b_wf': 122, 'b_tf': 50, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 0, 'b_wfs': 16, 'h_wfs': 5, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 0, 'h_1': 60, 'h_s1': 0, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 4},
    'Н75-750': {'h': 75, 'b': 187.5, 'b_wf': 92, 'b_tf': 50, 'n_wfs' : 1, 'n_tfs': 0, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 8, 'h_1': 47.5, 'h_s1': 7.5, 'h_2': 0, 'h_s2':0, 'r': 5, 'r_s': 4, 'n_cor': 4},
    'Н105-1270': {'h': 105, 'b': 423, 'b_wf': 158, 'b_tf': 52, 'n_wfs' : 2, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 29, 'h_wfs': 5, 'b_wfs_s': 61, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 5, 'h_1': 16, 'h_s1': 8, 'h_2': 57, 'h_s2':8, 'r': 5, 'r_s': 4, 'n_cor': 4},    
    'Н114-600': {'h': 114, 'b': 200.0, 'b_wf': 104, 'b_tf': 60, 'n_wfs': 1, 'n_tfs': 1, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 18, 'h_tfs': 7, 'h_ws': 8, 'h_1': 81, 'h_s1': 7, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 3},
    'Н114-750': {'h': 114, 'b': 250.0, 'b_wf': 126, 'b_tf': 80, 'n_wfs': 2, 'n_tfs': 1, 'n_ws': 1, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 42, 'b_tfs': 18, 'h_tfs': 7, 'h_ws': 8, 'h_1': 81, 'h_s1': 7, 'h_2': 0, 'h_s2': 0, 'r': 5, 'r_s': 4, 'n_cor': 3},
    'Н127-1100': {'h': 127, 'b': 366.7, 'b_wf': 160, 'b_tf': 54, 'n_wfs': 2, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 29, 'h_wfs': 5, 'b_wfs_s': 61, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 5, 'h_1': 19, 'h_s1': 11, 'h_2': 67, 'h_s2': 11, 'r': 5, 'r_s': 4, 'n_cor': 3},  
    'Н135-1000': {'h': 135, 'b': 333.3, 'b_wf': 160, 'b_tf': 54, 'n_wfs': 2, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 29, 'h_wfs': 5, 'b_wfs_s': 61, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 5, 'h_1': 19.6, 'h_s1': 12.9, 'h_2': 70, 'h_s2': 12.9, 'r': 5, 'r_s': 4, 'n_cor': 3},  
    'Н144-960': {'h': 144, 'b': 320.0, 'b_wf': 124.4, 'b_tf': 60.2, 'n_wfs': 2, 'n_tfs': 1, 'n_ws': 2, 'b_wfs': 29, 'h_wfs': 5, 'b_wfs_s': 50, 'b_tfs': 29, 'h_tfs': 5, 'h_ws': 6, 'h_1': 40, 'h_s1': 7.5, 'h_2': 49, 'h_s2': 7.5, 'r': 5, 'r_s': 4, 'n_cor': 3},
    'Н153-900': {'h': 153, 'b': 300.0, 'b_wf': 120.0, 'b_tf': 61.0, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 7, 'h_1': 40, 'h_s1': 9, 'h_2': 63, 'h_s2': 9, 'r': 5, 'r_s': 3.5, 'n_cor': 3},
    'Н157-800': {'h': 157, 'b': 266.7, 'b_wf': 121.0, 'b_tf': 62.0, 'n_wfs': 1, 'n_tfs': 0, 'n_ws': 2, 'b_wfs': 18, 'h_wfs': 7, 'b_wfs_s': 0, 'b_tfs': 0, 'h_tfs': 0, 'h_ws': 8.25, 'h_1': 43, 'h_s1': 7.5, 'h_2': 66, 'h_s2': 7.5, 'r': 5, 'r_s': 3.5, 'n_cor': 3}
}

### Боковая панель ###
with st.sidebar:
    st.subheader('Нормы')
    code = st.selectbox('Методика расчёта', ['СП 260.1325800.2023','EN 1993-1-3:2005'], index = 0, label_visibility = 'visible', disabled = True) # Выбор норм для расчёта
    standard = st.selectbox('Стандарт на профиль',['ГОСТ 24045-2016', 'СТО 57398459-18-2024'], index = 0, label_visibility = 'visible', disabled = False) #Выбор стандарта на настил
    #st.checkbox('Несущую способность по поперечной силе определять по EN 1993-1-3', value=True, label_visibility = 'visible', disabled = False) #Выбор формулы для определения несущей способность при действии поперечной силы
    Q_en = False

    st.subheader('Настройки расчёта')
    with st.expander('Единицы измерения и точность', expanded=False):
        U_Length = st.selectbox('Размеры', ['мм', 'см', 'м'], index=2, label_visibility='visible', disabled=False)
        U_Dimensions = st.selectbox('Размеры сечений и деформации', ['мм', 'см', 'м'], index=0, label_visibility='visible', disabled=False)
        U_SectionProperties = st.selectbox('Свойства сечений',['ммⁿ', 'смⁿ', 'мⁿ'], index=1, label_visibility='visible', disabled=False)
        U_Load_Area = st.selectbox('Нагрузки',['Па', 'кПа', 'кгс/м²', 'тс/м²'], index = 1, label_visibility='visible', disabled=False)
        U_Force = st.selectbox('Силы',['Н', 'кН', 'кгс', 'тс'], index=1, label_visibility='visible', disabled=False)
        U_Moments = st.selectbox('Моменты', ['Н·мм','Н·см', 'Н·м', 'кН·мм', 'кН·см', 'кН·м', 'кгс·мм', 'кгс·см', 'кгс·м', 'тс·мм','тс·см', 'тс·м'], index=5, label_visibility='visible', disabled=False)
        U_Stress = st.selectbox('Напряжения', ['Па', 'кПа', 'МПа', 'кН/см²', 'кгс/cм²'], index=2, label_visibility='visible', disabled=False)
        
        precision = st.selectbox('Точность', ['0', '0.0', '0.00', '0.000', '0.0000', 'o_O'], index=2, label_visibility='visible', disabled=False)    

    UD_Length = {
        'мм': 1000.0,
        'см': 100.0,
        'м': 1.0}
    UF_Length = UD_Length.get(U_Length, 0.0) / UD_Length.get('м', 0)

    UD_Dimensions = {
        'мм': 1000.0,
        'см': 100.0,
        'м': 1.0}
    UF_Dimensions = UD_Dimensions.get(U_Dimensions, 0.0) / UD_Dimensions.get('м', 0)

    UD_SectionProperties = {
        'ммⁿ': 1000.0,
        'смⁿ': 100.0,
        'мⁿ': 1.0}
    UF_SectionProperties = UD_SectionProperties.get(U_SectionProperties, 0.0)

    UD_Forces = {
        'Н': 1.0,
        'кН': 0.001,
        'кгс': 0.101971621,
        'тс': 0.000101971621}
    UF_Forces = UD_Forces.get(U_Force, 0.0) / UD_Forces.get('кН',0)

    UD_Load_Area = {
        'Па': 1.0,
        'кПа': 0.001,
        'кгс/м²': 0.101971621,
        'тс/м²': 0.000101971621}
    UF_Load_Area = UD_Load_Area.get(U_Load_Area, 0.0)

    UD_Moments = {
        'Н·мм': 1000.0,
        'Н·см': 100.0,
        'Н·м': 1.0,
        'кН·мм': 1.0,
        'кН·см': 0.1,
        'кН·м': 0.001,
        'кгс·мм': 101.971621,
        'кгс·см': 10.1971621,
        'кгс·м': 0.101971621,
        'тс·мм': 0.101971621,
        'тс·см': 0.0101971621,
        'тс·м': 0.000101971621}
    UF_Moments = UD_Moments.get(U_Moments, 0.0) / UD_Moments.get('кН·м', 0)

    UD_Stress = {
        'Па': 1.0,
        'кПа': 0.001,
        'МПа': 0.000001,
        'кН/см²': 0.0000001,
        'кгс/см²': 0.0000101971621}
    UF_Stress = UD_Stress.get(U_Stress, 0.0)

    precision_dict = {
        '0': 0,
        '0.0': 1,
        '0.00': 2,
        '0.000': 3,
        '0.0000': 4,
        'o_O': 17}
    precision_value = precision_dict.get(precision,17)

    st.subheader('Профилированный лист') # Заголовок страницы
    if standard == 'ГОСТ 24045-2016':
        deck = st.selectbox('Настил', ['Н57-750', 'Н60-845', 'Н75-750','Н114-600', 'Н114-750', 'Н153-850'], index = 2, label_visibility = 'visible', disabled = False) #Настилы по ГОСТ 24045-2016
    elif standard == 'СТО 57398459-18-2024':
        deck = st.selectbox('Настил', ['Н57-750','Н60-845','Н75-750','Н105-1270','Н114-600','Н114-750','Н127-1100','Н135-1000','Н144-960','Н153-900','Н157-800'], index = 2, label_visibility = 'visible', disabled = False)
    
    grade = int(st.selectbox('Марка стали листа по ГОСТ 14918-2020', ('220', '250', '280', '320', '350', '390', '420', '450'))) # Класс прочности стали
    t_nom = float(st.slider('Номинальная толщина стенки', min_value=0.00060 * UF_Dimensions, max_value=0.0015 * UF_Dimensions, value=0.00080 * UF_Dimensions, step=0.00005 * UF_Dimensions, format='%.2f')) * UD_Dimensions.get('м', 0.0) / UF_Dimensions # Номинальная толщина стенки
    t_coat = float(st.slider('Класс покрытия', min_value=60.0, max_value=430.0, value=350.0, step=5.0, format='%f')) * (7/100) / 1000000 # Толщина защитного покрытия
    orient = st.selectbox('Ориентация широкой полки', ('Вверх','Вниз'),) # Сжатые полки

    if Q_en == False:
        st.subheader('Условия опирания')
        Q_parameter_1 = st.selectbox('Конструкция опоры и полок', ['Закреплённая на опоре', 'Не закреплённая на опоре'], index = 0, label_visibility = 'visible')
        Q_parameter_2 = st.selectbox('Опорная реакция или локальная нагрузка', ['На одну полку','На две полки'], index = 0, label_visibility = 'visible')
        Q_parameter_3 = st.selectbox('Опора', ['Концевая','Промежуточная'], index=1, label_visibility='visible')

        C=C_coef.get(Q_parameter_1,{}).get(Q_parameter_2,{}).get(Q_parameter_3,{}).get('C',0)
        C_r=C_coef.get(Q_parameter_1,{}).get(Q_parameter_2,{}).get(Q_parameter_3,{}).get('C_r',0)
        C_b=C_coef.get(Q_parameter_1,{}).get(Q_parameter_2,{}).get(Q_parameter_3,{}).get('C_b',0)
        C_h=C_coef.get(Q_parameter_1,{}).get(Q_parameter_2,{}).get(Q_parameter_3,{}).get('C_h',0)

    l_a = float(st.slider('Ширина опоры', min_value=0.05 * UF_Dimensions, max_value=0.2 * UF_Dimensions, value=0.1 * UF_Dimensions, step=0.001 * UF_Dimensions, format='%f')) * UD_Dimensions.get('м', 0.0) / UF_Dimensions # Ширина опоры

    st.header('Расчетная схема')
    number_spans = st.slider('Количество пролётов', min_value=1, max_value=5, value=3)
    span = st.number_input('Пролёт', min_value=0.0 * UF_Length, max_value=12.0 * UF_Length, value=3.0 * UF_Length, step=0.01 * UF_Length, format='%.2f') * UD_Length.get('м', 0.0) / UF_Length
    load_uls = st.number_input('Расчётная кратковременная нагрузка', min_value=0.0 * UF_Load_Area, max_value=10000.0 * UF_Load_Area, value=1000.0 * UF_Load_Area, step=1.0 * UF_Load_Area) * UD_Load_Area.get('кПа',0.0) / UF_Load_Area
    load_sls = st.number_input('Нормативная длительная нагрузка', min_value=0.0 * UF_Load_Area, max_value=10000.0 * UF_Load_Area, value=1000.0 * UF_Load_Area, step=1.0 * UF_Load_Area) * UD_Load_Area.get('кПа',0.0) / UF_Load_Area
    def_method = st.radio('Предельный прогиб',['Обратная норма', 'Значение'], index=0, label_visibility='visible', disabled=False)
    if def_method == 'Обратная норма':
        def_n = st.number_input('Обратная норма прогиба', min_value=120, max_value=300, value=200, step=1, label_visibility='visible', disabled=False)
    else:
        def_f = st.number_input('Предельный прогиб', min_value=0.0001* UF_Dimensions, value = 0.003 * UF_Dimensions, label_visibility='visible', disabled=False, format='%.2f') * UD_Dimensions.get('м', 0.0) / UF_Dimensions # Ширина опоры
    #Height = st.slider('Высота этажа', min_value=0.0, max_value=12.0, value = 3.0, step = 0.1, label_visibility='visible', disabled=False)


### ИСХОДНЫЕ ДАННЫЕ ###

# Расчётные характеристики материалов 
ρ_s = 7850 # Плотность стали [кг/м³]
E_s = 206000 # Модуль упругости стали [МПа]
ν = 0.3 # Коэффициент поперечной деформации стали [-]
R_y = Grades.get(grade, {}).get('R_y', 0) # Расчётный предел текучести стали при растяжении, сжатии и изгибе [МПа]
R_s = Grades.get(grade, {}).get('R_s', 0) # Расчётный предел текучести стали на сдвиг [МПа]
R_lp = Grades.get(grade, {}).get('R_lp', 0) # Расчётный предел прочности стали на смятие [МПа]

# Выбор сортамента настилов
if standard == 'ГОСТ 24045-2016': Decks = Decks_GOST24045_2016
elif standard == 'СТО 57398459-18-2024': Decks = Decks_STO_57398459_18_2024

# Размеры профилированного настила
t = t_nom - 2 * t_coat # Расчётная толщина листа [м]
h = Decks.get(deck, {}).get('h', 0)/1000 # Высота профиля [м]
b = Decks.get(deck, {}).get('b', 0)/1000 # Шаг гофры [м]
b_wf = Decks.get(deck, {}).get('b_wf', 0)/1000 # Ширина широкой полки [м]
b_tf = Decks.get(deck, {}).get('b_tf', 0)/1000 # Ширина узкой полки [м]
r = Decks.get(deck, {}).get('r', 0)/1000 # Радиус скруглений гофр [м]
r_s = Decks.get(deck, {}).get('r_s', 0)/1000 # Радиус скруглений ребер жесткости [м]
    # Ребра широкой полки
n_wfs = Decks.get(deck, {}).get('n_wfs', 0) # Количество ребер широкой полки [шт.]
b_wfs = Decks.get(deck, {}).get('b_wfs', 0)/1000 # Ширина ребра жесткости по широкой полке [м]
h_wfs = Decks.get(deck, {}).get('h_wfs', 0)/1000 # Высота ребра жесктости по широкой полке [м]
b_wfs_s = Decks.get(deck, {}).get('b_wfs_s', 0)/1000 # Шаг ребер жестокости по широкой полке [м]
    # Ребра узкой полки
n_tfs = Decks.get(deck, {}).get('n_tfs', 0) # Количество ребер узкой полки [шт.]
b_tfs = Decks.get(deck, {}).get('b_tfs', 0)/1000 # Ширина ребра жесткости по узкой полке [м]
h_tfs = Decks.get(deck, {}).get('h_tfs', 0)/1000 # Высота ребра жесткости по узкой полке [м]
    # Ребра стенки
n_ws = Decks.get(deck, {}).get('n_ws', 0) #Количетсво ребер стенки [шт.]
h_ws = Decks.get(deck, {}).get('h_ws', 0)/1000 # Высота ребра жесткости по стенке [м]
h_1 = Decks.get(deck, {}).get('h_1', 0)/1000 # Высота участка стенки, ближайшего к широкой полке [м]
h_s1 = Decks.get(deck,{}).get('h_s1', 0)/1000 # Высота ребра жесткости, ближайшего к широкой полке [м]
h_2 = Decks.get(deck, {}).get('h_2', 0)/1000 # Высота среднего участка стенки [м]
h_s2 = Decks.get(deck, {}).get('h_s2', 0)/1000 # Высота ребра жесткости, дальнего от широкой полки [м]
    # Дополнительные данные
n_cor = Decks.get(deck, {}).get('n_cor', 0) # Количество гофр в одном листе [шт.]

# Коэффициенты для расчётов
k_σ, ψ = 4, 1

### ВЫЧИСЛЕНИЯ НЕДОСТАЮЩИХ ДАННЫХ О ГЕОМЕТРИИ ПРОФИЛЯ ###

b_w = (b - b_wf - b_tf)/2 # Горизонтальная проекция стенки
h_3 = 0 if n_ws == 0 else (h - h_1 - h_s1) if n_ws == 1 else (h - h_1 - h_s1 - h_2 - h_s2) if n_ws == 2 else None # Вертикальная проекция нижнего участка стенки [м]
b_wf_ps = (b_wf - b_wfs_s - b_wfs) / 2 if n_wfs == 2 else (b_wf - b_wfs) / 2 # Ширина крайнего плоского участка широкой полки [м]
b_wf_pm = 0 if (n_wfs == 0 or n_wfs == 1) else (b_wf - n_wfs * (b_wf_ps + b_wfs)) # Ширина среднего плоского участка широкой полки [м]
b_tf_ps = (b_tf - b_tfs) / 2 if n_tfs == 1 else b_tf / 2 # Ширина крайнего плоского участка узкой полки [м]

α = m.asin((n_ws * h_ws) / (m.sqrt(b_w**2 + h**2))) + m.atan(h / b_w) # Угол наклона стенки к горизонтали [рад.]
β = 0 if n_ws == 0 else α - m.pi / 2 + m.atan((h_s1 / m.tan(α) + h_ws / m.sin(α)) / h_s1) # Угол ребер стенки [рад.]
γ_wfs = m.atan(2 * h_wfs / b_wfs) # Угол ребер широкой полки [рад.]
γ_tfs = 0 if n_tfs == 0 else m.atan(2 * h_tfs / b_tfs) # Угол ребер узкой полки [рад.]
ω = 0 if n_ws == 0 else α - β # Угол наклона ребер стенки к горизонтали [рад.]

s_1 = h_1 / m.sin(α) # Длина верхнего участка стенки [м]
s_2 = 0 if (n_ws == 0 or n_ws == 1) else h_2 / m.sin(α) # Длина среднего участка стенки [м]
s_3 = 0 if n_ws == 0 else h_3 / m.sin(α) # Длина нижнего участка стенки [м]
s_s1 = 0 if n_ws == 0 else (h_s1 / m.tan(α) + h_ws / m.sin(α)) / m.cos(ω) # Длина верхнего ребра [м]
s_s2 = 0 if (n_ws == 0 or n_ws == 1) else s_s1 # Длина нижнего ребра [м]
s_wfs = m.sqrt((b_wfs / 2)**2 + h_wfs**2) # Длина полуребра на широкой полке [м]
s_tfs = m.sqrt((b_tfs / 2)**2 + h_tfs**2) # Длина полуребра на узкой полке [м]

### ПРОВЕРКА ТРЕБОВАНИЙ СП 260.1325800.2023 ПО СООТНОШЕНИЮ РАЗМЕРОВ ЭЛЕМЕНТОВ ПРОФИЛЕЙ ###

if (b_wf / t_nom > 300) or (b_tf / t_nom > 300):
    st.warning(' Не выполняется требование таблицы 7.1 СП 260.1325800.2023 по отношению ширины полки и толщины стенки', icon='⚠️')
elif (h / t_nom > 300) or (h / t_nom > 300 * m.sin(α)):
    st.warning(' Не выполняется требование таблицы 7.1 СП 260.1325800.2023 по соотношению высоты профиля и толщины стенки', icon='⚠️')
elif (0.25 > α / m.pi) or (α / m.pi > 0.5):
    st.warning(' Не выполняется требование таблицы 7.1 СП 260.1325800.2023 по углу наклона стенки', icon='⚠️')
elif max(r, r_s) > 0.04 * t_nom * E_s / R_y:
    st.warning(' Не выполняется требование п.7.2.8 СП 260.1325800.2023', icon='⚠️')
elif (b_wf/t_nom > 250 * h / b_wf) and (b_tf / t_nom > 250 * h / b_tf):
    st.warning(' Не выполняется требование п.7.3.1.2 СП 260.1325800.2023', icon='⚠️')
elif (h / t_nom > 220) or (min(r, r_s) / t_nom > 10):
    st.warning(' Не выполняется требование к профлию для определения несущей способность по поперечной силе', icon='⚠️')

### ГЕОМЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ ПОЛНОГО СЕЧЕНИЯ ###

h_gr_c = ((b_tf_ps * h + n_tfs * s_tfs * (h - h_tfs / 2) + s_3 * (h - h_3 / 2) + s_s2 * (h - h_3 - h_s2 / 2) + s_2 * (h_1 + h_s1 + h_2 / 2) + s_s1 * (h_1 + h_s1 / 2) + s_1 * (h_1 / 2) + n_wfs * s_wfs * h_wfs / 2) 
           / (b_tf_ps + n_tfs * s_tfs + s_3 + s_s2 + s_2 + s_s1 + s_1 + b_wf_ps + n_wfs * s_wfs + b_wf_pm / 2)) # Привязка центра тяжести полного сечения к широкой полке
s_gr_n = h_gr_c / m.sin(α) if (n_ws == 0 or n_ws == 1) else (h_gr_c - h_1 - h_s1)/m.sin(α) if n_ws == 2 else None # Длина сжатой зоны участка стенки
s_gr_m = s_1 - s_gr_n if (n_ws == 0 or n_ws == 1) else (s_2 - s_gr_n) if n_ws == 2 else None # Длина растянутой зоны участка стенки
L_gr = 2 * (b_tf_ps + n_tfs * s_tfs + s_3 + s_s2 + s_2 + s_s1 + s_1 + b_wf_ps + n_wfs * s_wfs + b_wf_pm / 2) # Длина полного участка
δ = 0.43 * (4 * r * α/(m.pi/2) + n_ws * 4 * r_s * β/(m.pi/2) + n_wfs * 4 * r_s * γ_wfs/(m.pi/2) + n_tfs * 4 * r_s * γ_tfs/(m.pi/2)) / L_gr # Коэффициент, учитывающий скругления профиля [-]
A_gr = L_gr * t * (1 - δ) # Площадь полного сечения на метр
P_gr = (L_gr + (b_tf + n_tfs * (2 * s_tfs - b_tfs))/n_cor) * t_nom * ρ_s * 1 / b # Примерная масса квадратного метра профилированного настила

# Определение моментов инерции и моментов сопротивления полного сечения
if n_ws == 0 or n_ws == 1:
    I_gr = (((b_wf_pm * t**3)/12 + b_wf_pm * t * (h_gr_c)**2)
             + 2 * n_wfs * ((s_wfs * t**3)/12 * m.cos(γ_wfs)**2 + (t * s_wfs**3)/12 * m.sin(γ_wfs)**2 + s_wfs * t * (h_gr_c - h_wfs / 2)**2)
             + 2 * ((b_wf_ps * t**3)/12 + b_wf_ps * t * (h_gr_c)**2)
             + 2 * ((s_gr_n * t**3)/12 * m.cos(α)**2 + (t * s_gr_n**3)/12 * m.sin(α)**2 + s_gr_n * t * (s_gr_n * m.sin(α) / 2)**2)
             + 2 * ((s_gr_m * t**3)/12 * m.cos(α)**2 + (t * s_gr_m**3)/12 * m.sin(α)**2 + s_gr_m * t * (s_gr_m * m.sin(α) / 2)**2)
             + 2 * ((s_s1 * t**3)/12 * m.cos(ω)**2 + (t * s_s1**3)/12 * m.sin(ω)**2 + s_s1 * t * (h_gr_c - h_1 - h_s1 / 2)**2)
             + 2 * ((s_3 * t**3)/12 * m.cos(α)**2 + (t * s_3**3)/12 * m.sin(α)**2 + s_3 * t * (h - h_3 / 2 - h_gr_c)**2)
             + 2 * ((b_tf_ps * t**3)/12 + b_tf_ps * t * (h - h_gr_c)**2)
             + 2 * n_tfs * ((s_tfs * t**3)/12 * m.cos(γ_tfs)**2 + (t * s_tfs**3)/12 * m.sin(γ_tfs)**2 + s_tfs * t * (h - h_gr_c - h_tfs / 2)**2)) * 1 / b * (1 - 2 * δ) # Момент инерции полного сечения без ребер стенок с учётом скруглений
elif n_ws == 2:
    I_gr = (((b_wf_pm * t**3)/12 + b_wf_pm * t * (h_gr_c)**2)
            + 2 * n_wfs * ((s_wfs * t**3)/12 * m.cos(γ_wfs)**2 + (t * s_wfs**3)/12 * m.sin(γ_wfs)**2 + s_wfs * t * (h_gr_c - h_wfs / 2)**2)
            + 2 * ((b_wf_ps * t**3)/12 + b_wf_ps * t * (h_gr_c)**2)
            + 2 * ((s_1 * t**3)/12 * m.cos(α)**2 + (t * s_1**3)/12 * m.sin(α)**2 + s_1 * t * (h_gr_c - h_1 / 2)**2)
            + 2 * ((s_s1 * t**3)/12 * m.cos(ω)**2 + (t * s_s1**3)/12 * m.sin(ω)**2 + s_s1 * t * (h_gr_c - h_1 - h_s1 / 2)**2)
            + 2 * ((s_gr_n * t**3)/12 * m.cos(α)**2 + (t * s_gr_n**3)/12 * m.sin(α)**2 + s_gr_n * t * (s_gr_n * m.sin(α) / 2)**2)
            + 2 * ((s_gr_m * t**3)/12 * m.cos(α)**2 + (t * s_gr_m**3)/12 * m.sin(α)**2 + s_gr_m * t * (s_gr_m * m.sin(α) / 2)**2)
            + 2 * ((s_s2 * t**3)/12 * m.cos(ω)**2 + (t * s_s2**3)/12 * m.sin(ω)**2 + s_s2 * t * (h_1 + h_s1 + h_2 + h_s2 / 2 - h_gr_c)**2)
            + 2 * ((s_3 * t**3)/12 * m.cos(α)**2 + (t * s_3**3)/12 * m.sin(α)**2 + s_3 * t * (h - h_3 / 2 - h_gr_c)**2)
            + 2 * ((b_tf_ps * t**3)/12 + b_tf_ps * t * (h - h_gr_c)**2)
            + 2 * n_tfs * ((s_tfs * t**3)/12 * m.cos(γ_tfs)**2 + (t * s_tfs**3)/12 * m.sin(γ_tfs)**2 + s_tfs * t * (h - h_gr_c - h_tfs / 2)**2)) * 1 / b * (1 - 2 * δ) # Момент инерции полного сечения с двумя ребрами на стенке с учётом скруглений

W_gr_wf = I_gr/h_gr_c # Момент сопротивления широких полок с учётом скруглений
W_gr_tf = I_gr/(h - h_gr_c) # Момент сопротивления узких полок с учётом скруглений

### ГЕОМЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ ЭФФЕКТИВНОГО СЕЧЕНИЯ ###
def effective_section_properties(flange):
    z_ini = 1 # Смещение центра тяжести от начального положения до начала итерации
    z = 0 # Смещение центра тяжести от начального положения для расчёта 

    if flange == 'Широкая':
        while abs(z - z_ini) > 0.000001:
            z_ini = z
            
            # Немного геометрии для старта
            h_c = h_gr_c + z # Положение центра тяжести с учётом редукции
            s_n = h_c / m.sin(α) if (n_ws == 0 or n_ws == 1) else (h_c - h_1 - h_s1)/m.sin(α) if n_ws == 2 else None # Длина сжатой зоны среднего участка стенки с учётом редукции
            s_m = s_1 - s_n if (n_ws == 0 or n_ws == 1) else s_2 - s_n if n_ws == 2 else None # Длина растянутой зоны среднего участка стенки с учётом редукции

            # Местная устойчивость крайнего участка сжатой широкой полки
            σ_ps_cr = k_σ * (m.pi**2 * E_s * t**2)/(12 * (1 - ν**2) * b_wf_ps**2) # Критические напряжения потери устойчивости плоского участка широкой полки
            λ_ps = m.sqrt(R_y/σ_ps_cr) # Коэффициент для плоского участка широкой полки
            ρ_ps = 1.0 if λ_ps <= 0.673 else (λ_ps - 0.055 * (3 + ψ)) / (λ_ps**2) # Коэффициент редукции для плоского участка широкой полки
            b_ps_ef = ρ_ps * b_wf_ps # Эффективаня ширина плоского участка широкой полки
            b_ps_ef_e = b_ps_ef / 2 # Плоловина ширины плоского участка широкой полки

            # Местная устойчивость среднего участка сжатой широкой полки
            σ_pm_cr = k_σ * (m.pi**2 * E_s * t**2)/(12 * (1 - ν**2) * b_wf_pm**2) if n_wfs == 2 else 0 # Критические напряжения потери устойчивости плоского участка широкой полки
            λ_pm = m.sqrt(R_y/σ_pm_cr) if n_wfs == 2 else 0 # Коэффициент для плоского участка широкой полки
            ρ_pm = 1.0 if λ_pm <= 0.673 else (λ_pm - 0.055 * (3 + ψ)) / (λ_pm**2) if n_wfs == 2 else 0 # Коэффициент редукции для плоского участка широкой полки
            b_pm_ef = ρ_pm * b_wf_pm if n_wfs == 2 else 0 # Эффективная ширина плоского участка широкой полки
            b_pm_ef_e = b_pm_ef / 2 if n_wfs == 2 else 0 # Плоловина ширины плоского участка широкой полки

            # Устойчивость формы сечения сжатой широкой полки
            if n_wfs == 0:
                σ_cr_s = 0
            else:
                b_p_i = min(15 * t, b_wf_ps / 2) # Ширина свеса крайних плоских участков широкой полки для определения момента инерции
                b_pm_i = min(15 * t, b_wf_pm / 2) if n_wfs == 2 else 0 # Ширина свеса среднего плоского участка широкой полки для определения момента инерции
                A_s_i = (2 * b_p_i + 2 * b_pm_i + 2 * n_wfs * s_wfs) * t # Площадь поперечного сечения элемента жесткости сжатой широкой полки
                h_tfs_c = 2 * n_wfs * (s_wfs * h_wfs / 2) / (2 * (b_p_i + b_pm_i + n_wfs * s_wfs)) # Привязка центра тяжести элемента жесткости
                I_wfs = 2 * (((b_p_i + b_pm_i) * t**3) / 12 + ((b_p_i + b_pm_i) * t * h_tfs_c**2) + n_wfs * ((s_wfs * t**3)/12 * m.cos(γ_wfs)**2 + (t * s_wfs**3)/12 * m.sin(γ_wfs)**2 + (s_wfs * t * (h_wfs/2 - h_tfs_c)**2))) # Момент инерции элемента жесткости широкой полки
                
                # Критические напряжения потери устойчивости формы сечения полки:
                if n_wfs == 1:
                    σ_cr_s = (4.2 * E_s)/A_s_i * m.sqrt((I_wfs * t**3)/(4 * b_wf_ps**2 * (2 * b_wf_ps + 3 * 2 * s_wfs)))
                elif n_wfs == 2:
                    b_l = b_wf_ps + b_wfs / 2
                    b_e = 2 * b_wf_ps + b_wf_pm + 4 * s_wfs
                    σ_cr_s = (4.2 * E_s)/A_s_i * m.sqrt((I_wfs * t**3)/(8 * b_l**2 * (3 * b_e - 4 * b_l))) 

            # Местная устойчивость сжатого участка стенки
            s_ef_0 = 0.76 * t * m.sqrt(E_s/R_y) # Базовая эффективная ширина стенки
            if n_ws == 0:
                s_ef_1_ini = s_ef_0
                s_ef_n_ini = 1.5 * s_ef_0
                s_ef_1 = 0.4 * s_n if s_ef_1_ini + s_ef_n_ini > s_n else s_ef_1_ini
                s_ef_2 = 0
                s_ef_3 = 0
                s_ef_n = 0.6 * s_n if s_ef_1_ini + s_ef_n_ini > s_n else s_ef_n_ini
            elif n_ws == 1:
                s_ef_1_ini = s_ef_0 # Начальная ширина более сжатой зоны верхнего участка стенки
                s_ef_n_ini = 1.5 * s_ef_0 # Начальная ширина менее сжатой зоны среднего участка стенки
                s_ef_1 = s_ef_1_ini if s_ef_1_ini + s_ef_n_ini <= s_n else s_ef_1_ini / (s_ef_1_ini + s_ef_n_ini) * s_n # Ширина более сжатой зоны участка стенки
                s_ef_2 = 0
                s_ef_3 = 0
                s_ef_n = s_ef_n_ini if s_ef_1_ini + s_ef_n_ini <= s_n else s_ef_n_ini / (s_ef_1_ini + s_ef_n_ini) * s_n # Ширина менее сжатой зоны участка стенки
            elif n_ws == 2:
                s_ef_1_ini = s_ef_0 # Начальная ширина более сжатой зоны верхнего участка стенки
                s_ef_2_ini = (1 + h_1 / (2 * h_c)) * s_ef_0 # Начальная ширина менее сжатой зоны верхнего участка стенки
                s_ef_3_ini = (1 + (h_1 + h_s1) / (2 * h_c)) * s_ef_0 # Начальная ширина более сжатой зоны среднего участка стенки
                s_ef_n_ini = 1.5 * s_ef_0 # Начальная ширина менее сжатой зоны среднего участка стенки
                s_ef_1 = s_ef_1_ini if s_ef_1_ini + s_ef_2_ini <= s_1 else s_ef_1_ini / (s_ef_1_ini + s_ef_2_ini) * s_1 # Ширина более сжатой зоны верхнего участка стенки
                s_ef_2 = s_ef_2_ini if s_ef_1_ini + s_ef_2_ini <= s_1 else s_ef_2_ini / (s_ef_1_ini + s_ef_2_ini) * s_1 # Ширина менее сжатой зоны верхнего участка стенки
                s_ef_3 = s_ef_3_ini if s_ef_3_ini + s_ef_n_ini <= s_n else s_ef_3_ini / (s_ef_3_ini + s_ef_n_ini) * s_n # Ширина более сжатой зоны среднего участка стенки
                s_ef_n = s_ef_n_ini if s_ef_3_ini + s_ef_n_ini <= s_n else s_ef_n_ini / (s_ef_3_ini + s_ef_n_ini) * s_n # Ширина менее сжатой зоны среднего участка стенки

            # Устойчивость формы сечения стенки
            if n_ws == 0 or n_ws == 1:
                σ_cr_sa = 0 # Критические напряжения потери устойчивости формы сечения стенки
            else:
                if n_ws == 1:
                    s_l = 0.9 * (s_1 + s_s1 + s_3) # Размер 1
                elif n_ws == 2:
                    s_l = s_1 + s_s1 + s_2 + (s_s2 + s_3) / 2 # Размер 1
                s_e = s_l - s_1 - s_s1 / 2 # Размер 2
                s_i2 = min(s_ef_1, s_1/2) # Ширина свеса плоских участков ребер для определения момента инерции
                s_i3 = min(s_ef_1, s_2/2) # Ширина свеса плоских участков ребер для определения момента инерции
                A_sa_i = (s_i2 + s_s1 + s_i3) * t # Площадь поперечного сечения ребра стенки
                h_ws_c = (s_i3 * h_ws + s_s1 * h_ws/2)/(s_i2 + s_s1 + s_i3) # Положение центра тяжести ребра стенки
                I_ws = (s_i3 * t**3)/12 + (s_i3 * t * h_ws_c**2) + (s_i2 * t**3)/12 + s_i2 * t * (h_ws - h_ws_c)**2 + (s_s1 * t**3)/12 * m.cos(β)**2 + (t * s_s1**3)/12 * m.sin(β)**2 + s_s1 * t * (h_ws/2 - h_ws_c)**2 # Момент инерции ребра стенки
                σ_cr_sa = (1.05 * E_s * m.sqrt(I_ws * t**3 * s_l))/(A_sa_i * s_e * (s_l - s_e)) # Критические напряжения потери устойчивости формы сечения стенки

            # Учёт взаимного влияние ребер стенки и полки
            if n_ws == 2:
                β_s = 1 - (h_1 + h_s1/2) / h_c # Коэффициент
                σ_cr_mod = σ_cr_s / (1 + (β_s * σ_cr_s/σ_cr_sa)**4)**0.25 # Критические напряжения поетри устойчивости
            else:
                β_s = 0 # Коэффициент
                σ_cr_mod = σ_cr_s # Критические напряжения потери устойчивости

            # Редукция толщин ребер полок и стенок
            λ_d = m.sqrt(R_y/σ_cr_mod) # Коэффициент
            if λ_d <= 0.65: χ_d = 1.0
            elif 0.65 < λ_d < 1.38: χ_d = 1.47 - 0.723 * λ_d
            else: χ_d = 0.66/λ_d

            t_ef_f = χ_d * t # Редуцированная толщина элемента жесткость полки
            if n_ws == 2:
                t_ef_w = min(χ_d * t * m.sqrt(h_c/(h_c - h_1 - h_s1/2)), t) # Редуцированная толщина элемента жесткости стенки
            else:
                t_ef_w = t

            # Геометрические характеристики сечения с учётом редукции
            h_ef_c = ((n_tfs * s_tfs * t * (h - h_tfs / 2) + b_tf_ps * t * h
                        + s_3 * t * (h - h_3 / 2) + s_s1 * t_ef_w * (h_1 + h_s1 / 2) + s_s2 * t * (h - h_3 - h_s2 / 2) + s_m * t * (h_c + s_m * m.sin(α) / 2) + s_ef_n * t * (h_c - s_ef_n * m.sin(α) / 2) + s_ef_3 * t_ef_w * (h_1 + h_s1 + s_ef_3 * m.sin(α) / 2) + s_ef_2 * t_ef_w * (h_1 - s_ef_2 * m.sin(α) / 2)
                        + s_ef_1 * t * (s_ef_1 * m.sin(α) / 2) + n_wfs * s_wfs * t_ef_f * (h_wfs / 2))
                        /(n_tfs * s_tfs * t + b_tf_ps * t + s_3 * t + s_s2 * t + s_m * t + s_ef_n * t + s_ef_3 * t_ef_w + s_s1 * t_ef_w + s_ef_2 * t_ef_w + s_ef_1 * t + b_ps_ef_e * t + b_ps_ef_e * t_ef_f + n_wfs * s_wfs * t_ef_f + b_pm_ef_e * t_ef_f))
            z = abs(h_ef_c - h_gr_c)
    
        if n_ws == 0:
            I_ef = (2 * n_tfs * ((s_tfs * t**3) / 12 * m.cos(γ_tfs)**2 + (t * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t * (h - h_ef_c - h_tfs / 2)**2)
                    + 2 * ((b_tf_ps * t**3) / 12 + b_tf_ps * t * (h - h_ef_c)**2)
                    + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                    + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                    + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                    + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * h_ef_c**2)
                    + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * h_ef_c**2)
                    + 2 * n_wfs * ((s_wfs * t_ef_f**3) / 12 * m.cos(γ_wfs)**2 + (t_ef_f * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t_ef_f * (h_ef_c - h_wfs / 2)**2)
                    + 2 * ((b_pm_ef_e * t_ef_f**3) / 12 + b_pm_ef_e * t_ef_f * h_ef_c**2))* 1/b * (1 - 2 * δ) # Момент инерции эффективного сечения
        elif n_ws == 1:
            I_ef = (2 * n_tfs * ((s_tfs * t**3) / 12 * m.cos(γ_tfs)**2 + (t * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t * (h - h_ef_c - h_tfs / 2)**2)
                    + 2 * ((b_tf_ps * t**3) / 12 + b_tf_ps * t * (h - h_ef_c)**2)
                    + 2 * ((s_3 * t**3) / 12 * m.cos(α)**2 + (t * s_3**3)/ 12 * m.sin(α)**2 + s_3 * t * (h - h_ef_c - h_3 / 2)**2)
                    + 2 * ((s_s1 * t_ef_w**3) / 12 * m.cos(ω)**2 + (t_ef_w * s_s1**3) / 12 * m.sin(ω)**2 + s_s1 * t_ef_w * (h_ef_c - h_1 - h_s1 / 2)**2)
                    + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                    + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                    + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                    + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * h_ef_c**2)
                    + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * h_ef_c**2)
                    + 2 * n_wfs * ((s_wfs * t_ef_f**3) / 12 * m.cos(γ_wfs)**2 + (t_ef_f * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t_ef_f * (h_ef_c - h_wfs / 2)**2)
                    + 2 * ((b_pm_ef_e * t_ef_f**3) / 12 + b_pm_ef_e * t_ef_f * h_ef_c**2))* 1/b * (1 - 2 * δ) # Момент инерции эффективного сечения
        elif n_ws == 2:
            I_ef = (2 * n_tfs * ((s_tfs * t**3) / 12 * m.cos(γ_tfs)**2 + (t * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t * (h - h_ef_c - h_tfs / 2)**2)
                    + 2 * ((b_tf_ps * t**3) / 12 + b_tf_ps * t * (h - h_ef_c)**2)
                    + 2 * ((s_3 * t**3) / 12 * m.cos(α)**2 + (t * s_3**3)/ 12 * m.sin(α)**2 + s_3 * t * (h - h_ef_c - h_3 / 2)**2)
                    + 2 * ((s_s2 * t**3) / 12 * m.cos(ω)**2 + (t * s_s2**3) / 12 * m.sin(ω)**2 + s_s2 * t * (h - h_ef_c - h_3 - h_s2 / 2)**2)
                    + 2 * ((s_s1 * t_ef_w**3) / 12 * m.cos(ω)**2 + (t_ef_w * s_s1**3) / 12 * m.sin(ω)**2 + s_s1 * t_ef_w * (h_ef_c - h_1 - h_s1 / 2)**2)
                    + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                    + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                    + 2 * ((s_ef_3 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_3**3) / 12 * m.sin(α)**2 + s_ef_3 * t_ef_w * (h_ef_c - h_1 - h_s1 - s_ef_3 * m.sin(α)/2)**2)
                    + 2 * ((s_ef_2 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_2**3) / 12 * m.sin(α)**2 + s_ef_2 * t_ef_w * (h_ef_c - h_1 + s_ef_2 * m.sin(α)/2)**2)
                    + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                    + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * h_ef_c**2)
                    + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * h_ef_c**2)
                    + 2 * n_wfs * ((s_wfs * t_ef_f**3) / 12 * m.cos(γ_wfs)**2 + (t_ef_f * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t_ef_f * (h_ef_c - h_wfs / 2)**2)
                    + 2 * ((b_pm_ef_e * t_ef_f**3) / 12 + b_pm_ef_e * t_ef_f * h_ef_c**2))* 1/b * (1 - 2 * δ) # Момент инерции эффективного сечения

        # Моменты сопротивления
        W_ef_wf = I_ef / h_ef_c # Момент сопротивления широкой полки
        W_ef_tf = I_ef / (h - h_ef_c) # Момент сопротивления узкий полки

    elif flange == 'Узкая':
        while abs(z-z_ini) > 0.000001:
            z_ini = z

            # Немного геометрии для старта
            h_c = (h - h_gr_c) + z # Положение центра тяжести с учётом редукции
            s_n = h_c / m.sin(α) if n_ws == 0 else (h_c - h_3 - h_s1) / m.sin(α) if n_ws == 1 else (h_c - h_3 - h_s2) / m.sin(α) if n_ws == 2 else None # Длина сжатой зоны среднего участка стенки с учётом редукции
            s_m = s_1 - s_n if (n_ws == 0 or n_ws == 1) else (s_2 - s_n) if n_ws == 2 else None # Длина растянутой зоны среднего участка стенки с учётом редукции

            # Местная устойчивость сжатой узкой полки
            if n_tfs == 0:
                σ_ps_cr = k_σ * (m.pi**2 * E_s * t**2)/(12 * (1 - ν**2) * (2 * b_tf_ps)**2) # Критические напряжения потери устойчивости плоского участка узкой полки
                λ_ps = m.sqrt(R_y / σ_ps_cr) # Коэффициент для плоского участка узкой полки
                ρ_ps = 1.0 if λ_ps <= 0.673 else (λ_ps - 0.055 * (3 + ψ)) / (λ_ps**2) # Коэффициент редукции для плоского участка узкой полки
                b_ps_ef = ρ_ps * (2 * b_tf_ps) # Эффективаня ширина плоского участка узкой полки
                b_ps_ef_e = b_ps_ef / 2 # Половина ширины плоского участка широкой полки
            elif n_tfs == 1:
                σ_ps_cr = k_σ * (m.pi**2 * E_s * t**2)/(12 * (1 - ν**2) * b_tf_ps**2) # Критические напряжения потери устойчивости плоского участка узкой полки
                λ_ps = m.sqrt(R_y / σ_ps_cr) # Коэффициент для плоского участка узкой полки
                ρ_ps = 1.0 if λ_ps <= 0.673 else (λ_ps - 0.055 * (3 + ψ)) / (λ_ps**2) # Коэффициент редукции для плоского участка узкой полки
                b_ps_ef = ρ_ps * b_tf_ps # Эффективаня ширина плоского участка узкой полки
                b_ps_ef_e = b_ps_ef / 2 # Половина ширины плоского участка широкой полки   
            b_pm_ef_e = 0.0         

            # Устойчивость формы сечения сжатой широкой полки
            if n_tfs == 0:
                σ_cr_s = 0
            elif n_tfs == 1:
                b_p_i = min(15 * t, b_tf_ps / 2) # Ширина свеса крайних плоских участков широкой полки для определения момента инерции
                A_s_i = (2 * b_p_i + 2 * s_tfs) * t # Площадь поперечного сечения элемента жесткости сжатой широкой полки
                h_tfs_c = 2 * (s_tfs * h_tfs / 2) / (2 * (b_p_i + s_tfs)) # Привязка центра тяжести элемента жесткости
                I_tfs = 2 * ((b_p_i * t**3) / 12 + (b_p_i * t * h_tfs_c**2) + (s_tfs * t**3)/12 * m.cos(γ_tfs)**2 + (t * s_tfs**3)/12 * m.sin(γ_tfs)**2 + (s_tfs * t * (h_tfs/2 - h_tfs_c)**2)) # Момент инерции элемента жесткости широкой полки
                σ_cr_s = (4.2 * E_s)/A_s_i * m.sqrt((I_tfs * t**3) / (4 * b_tf_ps**2 * (2 * b_tf_ps + 3 * 2 * s_tfs))) # Критические напряжения потери устойчивости формы сечения полки

            # Местная устойчивость сжатого участка стенки
            s_ef_0 = 0.76 * t * m.sqrt(E_s/R_y) # Базовая эффективная ширина стенки
            if n_ws == 0:
                s_ef_1_ini = s_ef_0
                s_ef_n_ini = 1.5 * s_ef_0
                s_ef_1 = 0.4 * s_n if s_ef_1_ini + s_ef_n_ini > s_n else s_ef_1_ini
                s_ef_2 = 0
                s_ef_3 = 0
                s_ef_n = 0.6 * s_n if s_ef_1_ini + s_ef_n_ini > s_n else s_ef_n_ini
            elif n_ws == 1 or n_ws == 2:
                s_ef_1_ini = s_ef_0 # Начальная ширина более сжатой зоны верхнего участка стенки
                s_ef_2_ini = (1 + h_3 / (2 * h_c)) * s_ef_0 # Начальная ширина менее сжатой зоны верхнего участка стенки
                s_ef_3_ini = ((1 + (h_3 + h_s1) / (2 * h_c)) * s_ef_0) if n_ws == 1 else ((1 + (h_3 + h_s1) / (2 * h_c)) * s_ef_0) if n_ws == 2 else None # Начальная ширина более сжатой зоны среднего участка стенки
                s_ef_n_ini = 1.5 * s_ef_0 # Начальная ширина менее сжатой зоны среднего участка стенки
                s_ef_1 = s_ef_1_ini if s_ef_1_ini + s_ef_2_ini <= s_3 else s_ef_1_ini / (s_ef_1_ini + s_ef_2_ini) * s_3 # Ширина более сжатой зоны верхнего участка стенки
                s_ef_2 = s_ef_2_ini if s_ef_1_ini + s_ef_2_ini <= s_3 else s_ef_2_ini / (s_ef_1_ini + s_ef_2_ini) * s_3 # Ширина менее сжатой зоны верхнего участка стенки
                s_ef_3 = s_ef_3_ini if s_ef_3_ini + s_ef_n_ini <= s_n else s_ef_3_ini / (s_ef_3_ini + s_ef_n_ini) * s_n # Ширина более сжатой зоны среднего участка стенки
                s_ef_n = s_ef_n_ini if s_ef_3_ini + s_ef_n_ini <= s_n else s_ef_n_ini / (s_ef_3_ini + s_ef_n_ini) * s_n # Ширина менее сжатой зоны среднего участка стенки
            
            # Устойчивость формы сечения стенки
            if n_ws == 0:
                σ_cr_sa = 0 # Критические напряжения потери устойчивости формы сечения стенки
            elif n_ws == 1 or n_ws == 2:
                s_i2 = min(s_ef_1, s_3/2) # Ширина свеса плоских участков ребер для определения момента инерции
                s_i3 = min(s_ef_1, s_1/2) # Ширина свеса плоских участков ребер для определения момента инерции            
                if n_ws == 1:
                    s_l = 0.9 * (s_3 + s_s1 + s_1) # Размер 1
                    s_e = s_l - s_3 - s_s1 / 2 # Размер 2
                    A_sa_i = (s_i2 + s_s1 + s_i3) * t # Площадь поперечного сечения ребра стенки
                    h_ws_c = (s_i3 * h_ws + s_s1 * h_ws / 2)/(s_i2 + s_s1 + s_i3) # Положение центра тяжести ребра стенки
                    I_ws = (s_i3 * t**3) / 12 + (s_i3 * t * h_ws_c**2) + (s_i2 * t**3) / 12 + s_i2 * t * (h_ws - h_ws_c)**2 + (s_s1 * t**3)/12 * m.cos(β)**2 + (t * s_s1**3)/12 * m.sin(β)**2 + s_s1 * t * (h_ws/2 - h_ws_c)**2 # Момент инерции ребра стенки
                elif n_ws == 2:
                    s_l = s_3 + s_s2 + s_2 + (s_s1 + s_1) / 2 # Размер 1
                    s_e = s_l - s_3 - s_s2 / 2 # Размер 2
                    A_sa_i = (s_i2 + s_s2 + s_i3) * t # Площадь поперечного сечения ребра стенки
                    h_ws_c = (s_i3 * h_ws + s_s2 * h_ws / 2)/(s_i2 + s_s2 + s_i3) # Положение центра тяжести ребра стенки
                    I_ws = (s_i3 * t**3)/12 + (s_i3 * t * h_ws_c**2) + (s_i2 * t**3)/12 + s_i2 * t * (h_ws - h_ws_c)**2 + (s_s2 * t**3)/12 * m.cos(β)**2 + (t * s_s2**3)/12 * m.sin(β)**2 + s_s2 * t * (h_ws/2 - h_ws_c)**2 # Момент инерции ребра стенки
                σ_cr_sa = (1.05 * E_s * m.sqrt(I_ws * t**3 * s_l))/(A_sa_i * s_e * (s_l - s_e)) # Критические напряжения потери устойчивости формы сечения стенки
            
            # Учёт взаимного влияние ребер стенки и полки
            if n_tfs == 0:
                β_s = 0
                σ_cr_mod = σ_cr_sa
            elif n_tfs == 1:
                if n_ws == 0:
                    σ_cr_mod = σ_ps_cr
                elif n_ws == 1:
                    β_s = 1 - (h_3 + h_s1 / 2) / h_c # Коэффициент
                    σ_cr_mod = σ_cr_s / (1 + (β_s * σ_cr_s/σ_cr_sa)**4)**0.25 # Критические напряжения поетри устойчивости
                elif n_ws == 2:
                    β_s = 1 - (h_3 + h_s2 / 2) / h_c # Коэффициент
                    σ_cr_mod = σ_cr_s / (1 + (β_s * σ_cr_s/σ_cr_sa)**4)**0.25 # Критические напряжения поетри устойчивости
                    
            # Редукция толщин ребер полок и стенок
            if σ_cr_mod == 0:
                χ_d = 1
            else:
                λ_d = m.sqrt(R_y/σ_cr_mod) # Коэффициент
                if λ_d <= 0.65: χ_d = 1.0
                elif 0.65 < λ_d < 1.38: χ_d = 1.47 - 0.723 * λ_d
                else: χ_d = 0.66/λ_d

            if n_tfs == 0:
                t_ef_f = 0
            elif n_tfs == 1:
                t_ef_f = χ_d * t # Редуцированная толщина полки
            else: t_ef_f = 0
            
            if n_ws == 0:
                t_ef_w = 0
            elif n_ws == 1:
                t_ef_w = min(χ_d * t * m.sqrt(h_c/(h_c - h_3 - h_s1/2)), t) # Редуцированная толщина элемента жесткости стенки
            elif n_ws == 2:
                t_ef_w = min(χ_d * t * m.sqrt(h_c/(h_c - h_3 - h_s2/2)), t) # Редуцированная толщина элемента жесткости стенки

            # Геометрические характеристики сечения с учётом редукции
            if n_ws == 0:
                h_ef_c = ((b_wf_pm / 2 * t * h + n_wfs * s_wfs * t * (h - h_wfs / 2) + b_wf_ps * t * h + s_m * t * (h_c + s_m * m.sin(α)/2) + s_ef_n * t * (h_c - s_ef_n * m.sin(α)/2) + s_ef_1 * t * (s_ef_1 * m.sin(α)/2) + n_tfs * s_tfs * t_ef_f * (h_tfs / 2))
                        /(b_wf_pm / 2 * t + n_wfs * s_wfs * t + b_wf_ps * t + s_m * t + s_ef_n * t + s_ef_1 * t + b_ps_ef_e * t + b_ps_ef_e * t_ef_f + n_tfs * s_tfs * t_ef_f)) # Привязка центра тяжести редуцированного сечения            
            elif n_ws == 1:
                h_ef_c = ((b_wf_pm / 2 * t * h + n_wfs * s_wfs * t * (h - h_wfs / 2) + b_wf_ps * t * h
                            + s_m * t * (h_c + s_m * m.sin(α)/2) + s_ef_n * t * (h_c - s_ef_n * m.sin(α)/2) + s_ef_3 * t_ef_w * (h_3 + h_s1 + s_ef_3 * m.sin(α)/2) + s_s1 * t_ef_w * (h_3 + h_s1 / 2) + s_ef_2 * t_ef_w * (h_3 - s_ef_2 * m.sin(α)/2) + s_ef_1 * t * (s_ef_1 * m.sin(α)/2)
                            + n_tfs * s_tfs * t_ef_f * (h_tfs / 2))
                        /(b_wf_pm / 2 * t + n_wfs * s_wfs * t + b_wf_ps * t + s_m * t + s_ef_n * t + s_ef_3 * t_ef_w + s_s1 * t_ef_w + s_ef_2 * t_ef_w + s_ef_1 * t + b_ps_ef_e * t + b_ps_ef_e * t_ef_f + n_tfs * s_tfs * t_ef_f)) # Привязка центра тяжести редуцированного сечения
            elif n_ws == 2:
                h_ef_c = ((b_wf_pm / 2 * t * h + n_wfs * s_wfs * t * (h - h_wfs / 2) + b_wf_ps * t * h
                            + s_1 * t * (h - h_1 / 2) + s_s1 * t * (h - h_1 - h_s1 / 2) + s_m * t * (h_c + s_m * m.sin(α)/2) + s_ef_n * t * (h_c - s_ef_n * m.sin(α)/2)
                            + s_ef_3 * t_ef_w * (h_3 + h_s2 + s_ef_3 * m.sin(α)/2) + s_s2 * t_ef_w * (h_3 + h_s2 / 2) + s_ef_2 * t_ef_w * (h_3 - s_ef_2 * m.sin(α)/2)
                            + s_ef_1 * t * (s_ef_1 * m.sin(α)/2) + n_tfs * s_tfs * t_ef_f * (h_tfs / 2))
                        /(b_wf_pm / 2 * t + n_wfs * s_wfs * t + b_wf_ps * t + s_1 * t + s_s1 * t + s_m * t + s_ef_n * t + s_ef_3 * t_ef_w + s_s2 * t_ef_w + s_ef_2 * t_ef_w + s_ef_1 * t + b_ps_ef_e * t + b_ps_ef_e * t_ef_f + n_tfs * s_tfs * t_ef_f)) # Привязка центра тяжести редуцированного сечения
            z = abs(h_ef_c - (h - h_gr_c))
        
        if n_ws == 0:
            I_ef = (((b_wf_pm * t**3) / 12 + b_wf_pm * t * (h - h_ef_c)**2)
                + 2 * n_wfs * ((s_wfs * t**3) / 12 * m.cos(γ_wfs)**2 + (t * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t * (h - h_ef_c - h_wfs / 2)**2)
                + 2 * ((b_wf_ps * t**3) / 12 + b_wf_ps * t * (h - h_ef_c)**2)
                + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * (h_ef_c)**2)
                + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * (h_ef_c)**2)
                + 2 * n_tfs * ((s_tfs * t_ef_f**3) / 12 * m.cos(γ_tfs)**2 + (t_ef_f * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t_ef_f * (h_ef_c - h_tfs / 2)**2)) * 1/b * (1 - 2 * δ) # Момент инерции редуцированного сечения
        elif n_ws == 1:
            I_ef = (((b_wf_pm * t**3) / 12 + b_wf_pm * t * (h - h_ef_c)**2)
                + 2 * n_wfs * ((s_wfs * t**3) / 12 * m.cos(γ_wfs)**2 + (t * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t * (h - h_ef_c - h_wfs / 2)**2)
                + 2 * ((b_wf_ps * t**3) / 12 + b_wf_ps * t * (h - h_ef_c)**2)
                + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                + 2 * ((s_ef_3 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_3**3) / 12 * m.sin(α)**2 + s_ef_3 * t_ef_w * (h_ef_c - h_3 - h_s1 - s_ef_3 * m.sin(α)/2)**2)
                + 2 * ((s_s1 * t_ef_w**3) / 12 * m.cos(ω)**2 + (t_ef_w * s_s1**3) / 12 * m.sin(ω)**2 + s_s1 * t_ef_w * (h_ef_c - h_3 - h_s1 / 2)**2)
                + 2 * ((s_ef_2 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_2**3) / 12 * m.sin(α)**2 + s_ef_2 * t_ef_w * (h_ef_c - h_3 + s_ef_2 * m.sin(α)/2)**2)
                + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * (h_ef_c)**2)
                + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * (h_ef_c)**2)
                + 2 * n_tfs * ((s_tfs * t_ef_f**3) / 12 * m.cos(γ_tfs)**2 + (t_ef_f * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t_ef_f * (h_ef_c - h_tfs / 2)**2)) * 1/b * (1 - 2 * δ) # Момент инерции редуцированного сечения
        elif n_ws == 2:
            I_ef = (((b_wf_pm * t**3) / 12 + b_wf_pm * t * (h - h_ef_c)**2)
                + 2 * n_wfs * ((s_wfs * t**3) / 12 * m.cos(γ_wfs)**2 + (t * s_wfs**3) / 12 * m.sin(γ_wfs)**2 + s_wfs * t * (h - h_ef_c - h_wfs / 2)**2)
                + 2 * ((b_wf_ps * t**3) / 12 + b_wf_ps * t * (h - h_ef_c)**2)
                + 2 * ((s_1 * t**3) / 12 * m.cos(α)**2 + (t * s_1**3) / 12 * m.sin(α)**2 + s_1 * t * (h - h_ef_c - h_1 / 2)**2)
                + 2 * ((s_s1 * t**3) / 12 * m.cos(ω)**2 + (t * s_s1**3) / 12 * m.sin(ω)**2 + s_s1 * t * (h - h_ef_c - h_1 - h_s1 / 2)**2)
                + 2 * ((s_m * t**3) / 12 * m.cos(α)**2 + (t * s_m**3) / 12 * m.sin(α)**2 + s_m * t * (s_m * m.sin(α)/2)**2)
                + 2 * ((s_ef_n * t**3) / 12 * m.cos(α)**2 + (t * s_ef_n**3) / 12 * m.sin(α)**2 + s_ef_n * t * (s_ef_n * m.sin(α)/2)**2)
                + 2 * ((s_ef_3 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_3**3) / 12 * m.sin(α)**2 + s_ef_3 * t_ef_w * (h_ef_c - h_3 - h_s2 - s_ef_3 * m.sin(α)/2)**2)
                + 2 * ((s_s2 * t_ef_w**3) / 12 * m.cos(ω)**2 + (t_ef_w * s_s2**3) / 12 * m.sin(ω)**2 + s_s2 * t_ef_w * (h_ef_c - h_3 - h_s2 / 2)**2)
                + 2 * ((s_ef_2 * t_ef_w**3) / 12 * m.cos(α)**2 + (t_ef_w * s_ef_2**3) / 12 * m.sin(α)**2 + s_ef_2 * t_ef_w * (h_ef_c - h_3 + s_ef_2 * m.sin(α)/2)**2)
                + 2 * ((s_ef_1 * t**3) / 12 * m.cos(α)**2 + (t * s_ef_1**3) / 12 * m.sin(α)**2 + s_ef_1 * t * (h_ef_c - s_ef_1 * m.sin(α)/2)**2)
                + 2 * ((b_ps_ef_e * t**3) / 12 + b_ps_ef_e * t * (h_ef_c)**2)
                + 2 * ((b_ps_ef_e * t_ef_f**3) / 12 + b_ps_ef_e * t_ef_f * (h_ef_c)**2)
                + 2 * n_tfs * ((s_tfs * t_ef_f**3) / 12 * m.cos(γ_tfs)**2 + (t_ef_f * s_tfs**3) / 12 * m.sin(γ_tfs)**2 + s_tfs * t_ef_f * (h_ef_c - h_tfs / 2)**2)) * 1/b * (1 - 2 * δ) # Момент инерции редуцированного сечения

        # Моменты сопротивления
        W_ef_wf = I_ef / (h - h_ef_c) # Момент сопротивления широкой полки
        W_ef_tf = I_ef / h_ef_c # Момент сопротивления узкий полки

    result = [[h_ef_c, s_m, s_ef_n, s_ef_3, s_ef_2, s_ef_1, b_ps_ef_e, b_pm_ef_e],
              [I_ef, W_ef_wf, W_ef_tf],
              χ_d,
              [t_ef_f, t_ef_w]]

    return result

### ГЕОМЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ ###
if orient == 'Вверх':
    I_span = effective_section_properties('Широкая')[1][0]
    W_wf_span = effective_section_properties('Широкая')[1][1]
    W_tf_span = effective_section_properties('Широкая')[1][2]
else:
    I_span = effective_section_properties('Узкая')[1][0]
    W_wf_span = effective_section_properties('Узкая')[1][1]
    W_tf_span = effective_section_properties('Узкая')[1][2]

def capacity_moment(flange):
    W_ef_wf = effective_section_properties(flange)[1][1]
    W_ef_tf = effective_section_properties(flange)[1][2]

    # Несущая способность на изгиб
    M_ult_wf = W_ef_wf * R_y * 10**3 # Максимальный изгибающий момент для широкой полки
    M_ult_tf = W_ef_tf * R_y * 10**3 # Максимальные изгибающий момент для узкой полки

    M_ult = min(M_ult_wf, M_ult_tf)
    
    return M_ult

def capacity_shear():
    if orient == 'Вверх':
        b_d = b_tf - n_tfs * b_tfs + n_tfs * 2 * s_tfs # Длина полки в зоне опирания

        if n_ws == 0:
            k_a_s = 1
        elif n_ws == 1:
            y_w = (h * s_3 * (h_s1 * m.cos(α) - s_s1 * m.sin(α) * m.cos(ω)))/(h_s1 * b_w - h * s_s1 * m.cos(ω)) # Вертикальная координата пересечения прямой с ребром стенки
            x_w = (y_w * b_w)/h # Горизонтальная координата пересечения прямой с ребром стенки
            e_min = (n_ws * h_ws * m.sqrt(x_w**2 + y_w**2))/m.sqrt(b_w**2 + h**2)
            e_max = h_ws - e_min
            k_a_s = min(1.45 - 0.05 * e_max/t, 0.95 + 35000 * t**2 * e_min/(s_3 * b_d**2)) # Коэффициент, учитывающий наличие ребер на стенки
        elif n_ws == 2:
            y_w = (h * s_3 * (h_s2 * m.cos(α) - s_s2 * m.sin(α) * m.cos(ω)))/(h_s2 * b_w - h * s_s2 * m.cos(ω)) # Вертикальная координата пересечения прямой с ребром стенки
            x_w = (y_w * b_w)/h # Горизонтальная координата пересечения прямой с ребром стенки
            e_min = (n_ws * h_ws * m.sqrt(x_w**2 + y_w**2))/m.sqrt(b_w**2 + h**2)
            e_max = h_ws - e_min
            k_a_s = min(1.45 - 0.05 * e_max/t, 0.95 + 35000 * t**2 * e_min/(s_3*b_d**2)) # Коэффициент, учитывающий наличие ребер на стенки
   
    # Несущая способность по поперечной силе
        if Q_en:
            Q_w_p = 0.15 * t**2 * m.sqrt(R_y * E_s * 10**6) * (1 - 0.1 * m.sqrt(r_s/t)) * (0.5 + m.sqrt(0.02*l_a/t)) * (2.4 + (α/(m.pi/2))**2) * k_a_s # Критическая поперечная сила потери устойчивости одной стенки гофра по EN 1993-1-3
        else: Q_w_p = C * t**2 * R_y * m.sin(α) * (1 - C_r * m.sqrt(r/t)) * (1 + C_b * m.sqrt(l_a/t)) * (1 - C_h * m.sqrt(h_1/t)) * k_a_s * 1e3 # Критическая поперечная сила потери устойчивости одной стенки гофра по СП 260.1325800.2023

    else:
        b_d = b_wf - n_wfs * b_wfs + n_wfs * 2 * s_wfs # Длина полки в зоне опирания
        
        if n_ws == 0:
            k_a_s = 1
        elif n_ws == 1:
            y_w = (h * s_1 * (h_s1 * m.cos(α) - s_s1 * m.sin(α) * m.cos(ω)))/(h_s1 * b_w - h * s_s1 * m.cos(ω)) # Вертикальная координата пересечения прямой с ребром стенки
            x_w = (y_w * b_w)/h # Горизонтальная координата пересечения прямой с ребром стенки
            e_max = (n_ws * h_ws * m.sqrt(x_w**2 + y_w**2))/m.sqrt(b_w**2 + h**2)
            e_min = h_ws - e_max
            k_a_s = min(1.45 - 0.05 * e_max/t, 0.95 + 35000 * t**2 * e_min/(s_1 * b_d**2)) # Коэффициент, учитывающий наличие ребер на стенки
        elif n_ws == 2:
            y_w = (h * s_1 * (h_s1 * m.cos(α) - s_s1 * m.sin(α) * m.cos(ω)))/(h_s1 * b_w - h * s_s1 * m.cos(ω)) # Вертикальная координата пересечения прямой с ребром стенки
            x_w = (y_w * b_w)/h # Горизонтальная координата пересечения прямой с ребром стенки
            e_min = (n_ws * h_ws * m.sqrt(x_w**2 + y_w**2))/m.sqrt(b_w**2 + h**2)
            e_max = h_ws - e_min
            k_a_s = min(1.45 - 0.05 * e_max/t, 0.95 + 35000 * t**2 * e_min/(s_1*b_d**2)) # Коэффициент, учитывающий наличие ребер на стенки

        # Несущая способность по поперечной силе
        if Q_en:
            Q_w_p = 0.15 * t**2 * m.sqrt(R_y * E_s * 10**6) * (1 - 0.1 * m.sqrt(r_s/t)) * (0.5 + m.sqrt(0.02*l_a/t)) * (2.4 + (α/(m.pi/2))**2) * k_a_s # Критическая поперечная сила потери устойчивости одной стенки гофра
        else: Q_w_p = C * t**2 * R_y * m.sin(α) * (1 - C_r * m.sqrt(r/t)) * (1 + C_b * m.sqrt(l_a/t)) * (1 - C_h * m.sqrt(h_3/t)) * k_a_s * 1e3 

    Q_ult = 2 * Q_w_p * 1/b # Критическая сила на метр поперечного сечения настила

    return Q_ult

### ГРАФИК СЕЧЕНИЯ ###
def draw_section(flange, result):
    fig = go.Figure()

    h_ef_c, s_m, s_ef_n, s_ef_3, s_ef_2, s_ef_1, b_ps_ef_e, b_pm_ef_e = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7]
    χ_d = result[2]

    if orient == 'Вверх':
        if flange == 'Широкая':
            if n_wfs == 1 and n_ws == 0 and n_tfs == 0:
                main_points = [
                    [(-b / 2 , 0),
                    (-b / 2 + b_tf / 2, 0),
                    (-b / 2 + b_tf / 2 + (s_m + s_ef_n) * m.cos(α),(s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wf / 2, h),
                    (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_ps_ef_e - b_wfs / 2, h),
                    (-b_wfs / 2, h),
                    (0, h - h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_m + s_ef_n) * m.cos(α),(s_m + s_ef_n) * m.sin(α)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_ps_ef_e - b_wfs / 2, h)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 0:
                main_points = [
                    [(-b / 2 , 0),
                    (-b / 2 + b_tf / 2, 0),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α), s_3 * m.sin(α)),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), s_3 * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wf / 2, h),
                    (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wfs / 2 - b_ps_ef_e, h),
                    (-b_wfs / 2, h),
                    (0, h - h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_ps_ef_e - b_wfs / 2, h)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2 , h_tfs),
                     (-b / 2 + b_tfs / 2, 0),
                     (-b / 2 + b_tf / 2, 0),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α), s_3 * m.sin(α)),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), s_3 * m.sin(α) + s_s1 * m.sin(ω)),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                     (-b_wf / 2, h),
                     (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wfs / 2 - b_ps_ef_e, h),
                     (-b_wfs / 2, h),
                     (0, h - h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                     (-b_ps_ef_e - b_wfs / 2, h)]]
            elif n_wfs == 2 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2 , h_tfs),
                    (-b / 2 + b_tfs / 2, 0),
                    (-b / 2 + b_tf / 2, 0),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α), s_3 * m.sin(α)),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), s_3 * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wf / 2, h),
                    (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2, h),
                    (-b_wfs_s / 2, h - h_wfs),
                    (-b_wfs_s / 2 + b_wfs / 2 , h),
                    (-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h)],
                    [(-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h),
                    (0,h)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h_tfs),
                    (-b / 2 + b_tfs / 2, 0),
                    (-b / 2 + b_tf / 2, 0),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h_3),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2),
                    (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2 + (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wf / 2, h),
                    (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_wf / 2 - s_1 * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1),
                    (-b_wf / 2 - s_1 * m.cos(α), h - h_1),
                    (-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α))],
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2, h),
                    (-b_wfs_s / 2, h - h_wfs),
                    (-b_wfs_s / 2 + b_wfs / 2, h),
                    (-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h)],
                    [(-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h),
                    (0,h)]]                 
            elif n_wfs == 1 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b/2, 0),
                    (-b/2 + b_tf/2, 0),
                    (-b/2 + b_tf/2 + s_3 * m.cos(α), h_3),
                    (-b/2 + b_tf/2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2),
                    (-b/2 + b_tf/2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2 + (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wfs/2 - b_wf_ps - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wfs/2 - b_wf_ps, h), 
                    (-b_wfs/2 - b_wf_ps + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wfs/2 - b_wf_ps - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_wfs/2 - b_wf_ps - s_1 * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1),
                    (-b_wfs/2 - b_wf_ps - s_1 * m.cos(α), h - h_1),
                    (-b_wfs/2 - b_wf_ps - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α))],
                    [(-b_wfs/2 - b_ps_ef_e, h),
                    (-b_wfs/2, h),
                    (0, h - h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b / 2, 0),
                    (-b / 2 + b_tf / 2, 0),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h_3),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2),
                    (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h_3 + h_s2 + (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_wf / 2, h),
                    (-b_wf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_wf / 2 - s_1 * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1),
                    (-b_wf / 2 - s_1 * m.cos(α), h - h_1),
                    (-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α))],
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2, h),
                    (-b_wfs_s / 2, h - h_wfs),
                    (-b_wfs_s / 2 + b_wfs / 2, h),
                    (-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), (s_3 + s_m + s_ef_n) * m.sin(α) + s_s1 * m.sin(ω)),
                    (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_1 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h - h_1 + s_ef_2 * m.sin(α)),
                    (-b_wf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, h),
                    (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, h)],
                    [(-b_wfs_s / 2 + b_wfs / 2 + b_pm_ef_e, h),
                    (0,h)]]
        elif flange == 'Узкая':
            if n_wfs == 1 and n_ws == 0 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h - h_wfs),
                    (-b / 2 + b_wfs / 2, h),
                    (-b / 2 + b_wf / 2, h),
                    (-b / 2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e,0)]]
                reduced_segments = []
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α)),
                     (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                     (0, 0)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 0:
                main_points = [
                    [(-b/2, h - h_wfs),
                    (-b/2 + b_wfs / 2, h),
                    (-b/2 + b_wf / 2, h),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                    (0, 0)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b/2, h - h_wfs),
                    (-b/2 + b_wfs / 2, h),
                    (-b/2 + b_wf / 2, h),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, 0),
                    (-b_tfs / 2, 0),
                    (0, h_tfs)]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                    (-b_tfs / 2 - b_ps_ef_e, 0)]]
            elif n_wfs == 2 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h),
                    (-b / 2 + b_wf_pm /2, h),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h - h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, h),
                    (-b/2 + b_wf / 2, h),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, 0),
                    (-b_tfs / 2, 0),
                    (0, h_tfs)]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                    (-b_tfs / 2 - b_ps_ef_e, 0)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h),
                    (-b / 2 + b_wf_pm /2, h),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h - h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, h),
                    (-b / 2 + b_wf / 2, h),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α), h - s_1 * m.sin(α)),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α) + s_s2 * m.cos(ω), h - s_1 * m.sin(α) - h_s2),
                    (-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_1 + s_m + s_ef_n) * m.sin(α) - h_s2)],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, 0),
                    (-b_tfs / 2, 0),
                    (0, h_tfs)]]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_1 + s_m + s_ef_n) * m.sin(α) - h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                    (-b_tfs / 2 - b_ps_ef_e, 0)]]          
            elif n_wfs == 1 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b/2, h - h_wfs),
                    (-b/2 + b_wfs/2, h),
                    (-b/2 + b_wfs/2 + b_wf_ps, h),
                    (-b/2 + b_wfs/2 + b_wf_ps + s_1 * m.cos(α), h - h_1),
                    (-b/2 + b_wfs/2 + b_wf_ps + s_1 * m.cos(α) + s_s1 * m.cos(ω), h - h_1 - h_s1),
                    (-b/2 + b_wfs/2 + b_wf_ps + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_1 - h_s1 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf/2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf/2, 0),
                    (-b_tf/2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf/2 - (s_3 + s_ef_3) * m.cos(α) - s_s2 * m.cos(ω), h_3 + h_s2 + s_ef_3 * m.sin(α)),
                    (-b_tf/2 - s_3 * m.cos(α) - s_s2 * m.cos(ω), h_3 + h_s2),
                    (-b_tf/2 - s_3 * m.cos(α), h_3),
                    (-b_tf/2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))]]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_1 + s_m + s_ef_n) * m.sin(α) - h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, 0),
                    (0, 0)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h),
                    (-b / 2 + b_wf_pm /2, h),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h - h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, h),
                    (-b / 2 + b_wf / 2, h),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α), h - s_1 * m.sin(α)),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α) + s_s2 * m.cos(ω), h - s_1 * m.sin(α) - h_s2),
                    (-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_1 + s_m + s_ef_n) * m.sin(α) - h_s2)],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_tf / 2, 0),
                    (-b_tf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_1 + s_m + s_ef_n) * m.sin(α) - h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,0),
                    (0, 0)]]

    elif orient == 'Вниз':
        if flange == 'Широкая':
            if n_wfs == 1 and n_ws == 0 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wfs / 2  - b_ps_ef_e, 0),
                     (-b_wfs / 2, 0),
                     (0, h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_m + s_ef_n) * m.cos(α), h - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs / 2  - b_ps_ef_e, 0)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 0:
                main_points = [
                    [(-b/2, h),
                    (-b / 2 + b_tf / 2, h),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h - h_3),
                    (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b/2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                    (-b_wf / 2, 0),
                    (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs / 2, 0),
                     (0, h_wfs)]]
                inactive_segments = [
                    [(-b/2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                    (-b_wfs / 2 - b_ps_ef_e, 0)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h - h_tfs),
                     (-b / 2 + b_tfs / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h - h_3),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs / 2, 0),
                     (0, h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs / 2 - b_ps_ef_e, 0)]]
            elif n_wfs == 2 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h - h_tfs),
                     (-b / 2 + b_tfs / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + h_3 * m.cos(α), h - h_3),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2, 0),
                     (-b_wfs_s / 2, h_wfs),
                     (-b_wf_pm / 2, 0),
                     (-b_wf_pm / 2 + b_pm_ef_e, 0)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h - h_3 - h_s1 - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2 - b_pm_ef_e, 0)],
                    [(-b_wf_pm / 2 + b_pm_ef_e, 0),
                     (0, 0)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 1:
                main_points = [
                    [(-b / 2, h - h_tfs),
                     (-b / 2 + b_tfs / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h - h_3),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α)),
                     (-b_wf / 2 - s_1 * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1),
                     (-b_wf / 2 - s_1 * m.cos(α), h_1),
                     (-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2, 0),
                     (-b_wfs_s / 2, h_tfs),
                     (-b_wf_pm / 2, 0),
                     (-b_wf_pm / 2 + b_pm_ef_e, 0)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2 - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, 0)],
                    [(-b_wf_pm / 2 + b_pm_ef_e, 0),
                     (0, 0)]]          
            elif n_wfs == 1 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h - h_3),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2 - (s_m + s_ef_n) * m.sin(α))],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α)),
                     (-b_wf / 2 - s_1 * m.cos(α) - s_s2 * m.cos(ω), h_1 + h_s1),
                     (-b_wf / 2 - s_1 * m.cos(α), h_3),
                     (-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs / 2, 0),
                     (0, h_wfs)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - h_3 - h_s2 - (s_m + s_ef_n) * m.sin(α)),
                     (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs / 2 - b_ps_ef_e, 0)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h),
                     (-b / 2 + b_tf / 2, h),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α), h - s_3 * m.sin(α)),
                     (-b / 2 + b_tf / 2 + s_3 * m.cos(α) + s_s2 * m.cos(ω), h - s_3 * m.sin(α) - h_s2),
                     (-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_3 + s_m + s_ef_n) * m.sin(α) - h_s2)],
                    [(-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α)),
                     (-b_wf / 2, 0),
                     (-b_wf / 2 + b_ps_ef_e, 0)]]
                reduced_segments = [
                    [(-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α)),
                     (-b_wf / 2 - s_1 * m.cos(α) - s_s1 * m.cos(ω), h_3 + h_s1),
                     (-b_wf / 2 - s_1 * m.cos(α), h_3),
                     (-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α))],
                    [(-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2, 0),
                     (-b_wfs_s / 2, h_wfs),
                     (-b_wf_pm / 2, 0),
                     (-b_wf_pm / 2 + b_pm_ef_e, 0)]]
                inactive_segments = [
                    [(-b / 2 + b_tf / 2 + (s_3 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), h - (s_3 + s_m + s_ef_n) * m.sin(α) - h_s2),
                     (-b_wf / 2 - (s_1 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h_1 + h_s1 + s_ef_3 * m.sin(α))],
                    [(-b_wf / 2 - s_1 * m.cos(α) + s_ef_2 * m.cos(α), h_3 - s_ef_2 * m.sin(α)),
                     (-b_wf / 2 - s_ef_1 * m.cos(α), s_ef_1 * m.sin(α))],
                    [(-b_wf / 2 + b_ps_ef_e, 0),
                     (-b_wfs_s / 2 - b_wfs / 2 - b_ps_ef_e, 0)],
                    [(-b_wf_pm / 2 + b_pm_ef_e, 0),
                     (0, 0)]]  
        elif flange == 'Узкая':
            if n_wfs == 1 and n_ws == 0 and n_tfs == 0:
                main_points = [
                    [(-b / 2, h_wfs),
                     (-b / 2 + b_wfs / 2, 0),
                     (-b / 2 + b_wf / 2, 0),
                     (-b / 2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                     (-b_tf / 2, h),
                     (-b_tf / 2 + b_ps_ef_e,h)]]
                reduced_segments = []
                inactive_segments = [
                    [((-b / 2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α))),
                     (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                     (0, h)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 0:
                main_points = [
                    [(-b/2, h_wfs),
                    (-b/2 + b_wfs / 2, 0),
                    (-b/2 + b_wf / 2, 0),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf / 2, h),
                    (-b_tf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                    (0, h)]]
            elif n_wfs == 1 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b/2, h_wfs),
                    (-b/2 + b_wfs / 2, 0),
                    (-b/2 + b_wf / 2, 0),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf / 2, h),
                    (-b_tf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, h),
                    (-b_tfs / 2, h),
                    (0, h - h_tfs)]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                    (-b_tfs / 2 - b_ps_ef_e, h)]]
            elif n_wfs == 2 and n_ws == 1 and n_tfs == 1:
                main_points = [
                    [(-b / 2, 0),
                    (-b / 2 + b_wf_pm /2, 0),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, 0),
                    (-b/2 + b_wf / 2, 0),
                    (-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf / 2, h),
                    (-b_tf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, h),
                    (-b_tfs / 2, h),
                    (0, h - h_tfs)]]
                inactive_segments = [
                    [(-b/2 + b_wf / 2 + (s_m + s_ef_n) * m.cos(α), (s_m + s_ef_n) * m.sin(α)),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                    (-b_tfs / 2 - b_ps_ef_e, h)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 1:
                main_points = [
                    [(-b / 2, 0),
                    (-b / 2 + b_wf_pm /2, 0),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, 0),
                    (-b / 2 + b_wf / 2, 0),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α), s_1 * m.sin(α)),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α) + s_s2 * m.cos(ω), s_1 * m.sin(α) + h_s2),
                    (-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), (s_1 + s_m + s_ef_n) * m.sin(α) + h_s2)],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf / 2, h),
                    (-b_tf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))],
                    [(-b_tfs / 2 - b_ps_ef_e, h),
                    (-b_tfs / 2, h),
                    (0, h - h_tfs)]]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), (s_1 + s_m + s_ef_n) * m.sin(α) + h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                    (-b_tfs / 2 - b_ps_ef_e, h)]]          
            elif n_wfs == 1 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b/2, h_wfs),
                    (-b/2 + b_wfs/2, 0),
                    (-b/2 + b_wfs/2 + b_wf_ps, 0),
                    (-b/2 + b_wfs/2 + b_wf_ps + s_1 * m.cos(α), h_1),
                    (-b/2 + b_wfs/2 + b_wf_ps + s_1 * m.cos(α) + s_s1 * m.cos(ω), h_1 + h_s1),
                    (-b/2 + b_wfs/2 + b_wf_ps + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s1 * m.cos(ω), h_1 + h_s1 + (s_m + s_ef_n) * m.sin(α))],
                    [(-b_tf/2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf/2, h),
                    (-b_tf/2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf/2 - (s_3 + s_ef_3) * m.cos(α) - s_s2 * m.cos(ω), h - h_3 - h_s2 - s_ef_3 * m.sin(α)),
                    (-b_tf/2 - s_3 * m.cos(α) - s_s2 * m.cos(ω), h - h_3 - h_s2),
                    (-b_tf/2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf/2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))]]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), (s_1 + s_m + s_ef_n) * m.sin(α) + h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e, h),
                    (0, h)]]
            elif n_wfs == 2 and n_ws == 2 and n_tfs == 0:
                main_points = [
                    [(-b / 2, 0),
                    (-b / 2 + b_wf_pm /2, 0),
                    (-b / 2 + b_wf_pm / 2 + b_wfs / 2, h_wfs),
                    (-b / 2 + b_wf_pm / 2 + b_wfs, 0),
                    (-b / 2 + b_wf / 2, 0),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α), s_1 * m.sin(α)),
                    (-b / 2 + b_wf / 2 + s_1 * m.cos(α) + s_s2 * m.cos(ω), s_1 * m.sin(α) + h_s2),
                    (-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), (s_1 + s_m + s_ef_n) * m.sin(α) + h_s2)],
                    [(-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α)),
                    (-b_tf / 2, h),
                    (-b_tf / 2 + b_ps_ef_e, h)]]
                reduced_segments = [
                    [(-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α)),
                    (-b_tf / 2 - s_3 * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1),
                    (-b_tf / 2 - s_3 * m.cos(α), h - h_3),
                    (-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α))],]
                inactive_segments = [
                    [(-b / 2 + b_wf / 2 + (s_1 + s_m + s_ef_n) * m.cos(α) + s_s2 * m.cos(ω), (s_1 + s_m + s_ef_n) * m.sin(α) + h_s2),
                    (-b_tf / 2 - (s_3 + s_ef_3) * m.cos(α) - s_s1 * m.cos(ω), h - h_3 - h_s1 - s_ef_3 * m.sin(α))],
                    [(-b_tf / 2 - s_3 * m.cos(α) + s_ef_2 * m.cos(α), h - h_3 + s_ef_2 * m.sin(α)),
                    (-b_tf / 2 - s_ef_1 * m.cos(α), h - s_ef_1 * m.sin(α))],
                    [(-b_tf / 2 + b_ps_ef_e,h),
                    (0, h)]]

    reduced_color = 'rgb(' + str(int(255 * (1 - χ_d))) + ',' + str(int(0)) + ',' + str(int(255 * χ_d)) + ')'

    # Рисуем нередуцированные участки
    for i, segment in enumerate(main_points):
        x = [p[0] * UF_Dimensions for p in segment]
        y = [p[1] * UF_Dimensions for p in segment]

        # Основной сегмент
        fig.add_trace(go.Scatter(x=x, y=y,
            mode='lines', line=dict(color='blue', width=4),
            showlegend=(i==0), legendgroup='ini', name = 'Без редукции'))
        
        # Зеркальное отражение
        x_mirror = [-p[0] * UF_Dimensions for p in segment]
        fig.add_trace(go.Scatter(x=x_mirror, y=y,
            mode='lines', line=dict(color='blue', width=4),
            showlegend=False, legendgroup='ini', name = 'Без редукции'))

    # Рисуем редуцированные участки

    for i, segment in enumerate(reduced_segments):
        x = [p[0] * UF_Dimensions for p in segment]
        y = [p[1] * UF_Dimensions for p in segment]
        
        fig.add_trace(go.Scatter(x=x, y=y,
            mode='lines', line=dict(color=reduced_color, width=4 * χ_d),
            showlegend=(i==0), legendgroup='red', name = 'Редуцированно'))
        
        # Зеркальное отражение
        x_mirror = [-p[0] * UF_Dimensions for p in segment]
        fig.add_trace(go.Scatter(x=x_mirror, y=y,
            mode='lines', line=dict(color=reduced_color, width=4 * χ_d),
            showlegend=False, legendgroup='red', name = 'Редуцированно'))
    
    # Рисуем выключенные участки серым
    for i, segment in enumerate(inactive_segments):
        x = [p[0] * UF_Dimensions for p in segment]
        y = [p[1] * UF_Dimensions for p in segment]
        
        fig.add_trace(go.Scatter(x=x, y=y,
            mode='lines', line=dict(color='gray', width=2, dash='dash'),
            showlegend=(i==0), legendgroup='off', name = 'Выключено'))
        
        # Зеркальное отражение
        x_mirror = [-p[0] * UF_Dimensions for p in segment]
        fig.add_trace(go.Scatter(x=x_mirror, y=y,
            mode='lines', line=dict(color='gray', width=2, dash='dash'),
            showlegend=False, legendgroup='off', name = 'Выключено'))

    if orient == 'Вверх':
        if flange == 'Широкая':
            c_gr = h - h_gr_c
            c_ef = h - h_ef_c
        elif flange == 'Узкая':
            c_gr = h - h_gr_c
            c_ef = h_ef_c
    elif orient == 'Вниз':
        if flange == 'Широкая':
            c_gr = h_gr_c
            c_ef = h_ef_c
        elif flange == 'Узкая':
            c_gr = h_gr_c
            c_ef = h - h_ef_c

    # Главные оси инерции
    fig.add_trace(go.Scatter(x=[-b * UF_Dimensions / 2, b * UF_Dimensions / 2], y=[c_gr * UF_Dimensions, c_gr * UF_Dimensions],
        mode='lines', line=dict(color='blue', width=1, dash='dashdot'), showlegend=False, name='ini'))
    fig.add_trace(go.Scatter(x=[-b * UF_Dimensions / 2, b * UF_Dimensions / 2], y=[c_ef * UF_Dimensions, c_ef * UF_Dimensions],
        mode='lines', line=dict(color=reduced_color, width=1, dash='dashdot'), showlegend=False, name='red'))

    # Центр тяжести
    fig.add_trace(go.Scatter(x=[0], y=[c_gr * UF_Dimensions],
        mode='markers', marker=dict(color='blue', size=7.5),
        showlegend=False, name='ini'))
    fig.add_trace(go.Scatter(x=[0], y=[c_ef * UF_Dimensions],
        mode='markers', marker=dict(color=reduced_color, size=7.5),
        showlegend=False, name='red'))

    # Настройки графика
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, zeroline=True, mirror=True, ticks='outside', range=[-b * UF_Dimensions / 2, b * UF_Dimensions / 2], side='bottom', tickformat=f'.{precision_value}f'),
        yaxis=dict(scaleanchor="x", scaleratio=1, range=[0, h * UF_Dimensions], zeroline=True, mirror=True, ticks='outside', side='left', tickformat=f'.{precision_value}f'),
        xaxis2=dict(overlaying='x', side='top', ticks='outside', mirror=True),
        yaxis2=dict(overlaying='y', side='right', ticks='outside', mirror=True),
        legend=dict(bgcolor = 'rgba(0,0,0,0)', tracegroupgap=0, orientation='h', x=.5, y=-.1, xanchor='center'),
        showlegend=True, height = 400, template='plotly_dark')

    return fig

### РЕЗУЛЬТАТЫ РАСЧЁТА ###
if orient == 'Вверх':
    M_ult_span = capacity_moment('Широкая')
    M_ult_sup = capacity_moment('Узкая')
else:
    M_ult_span = capacity_moment('Узкая')
    M_ult_sup = capacity_moment('Широкая')

Q_ult = capacity_shear()

### СТАТИЧЕСКИЙ РАСЧЁТ МНОГОПРОЛЁТНОЙ БАЛКИ ###
#Определение внутренних усилий
factors = {
    1: {'k_m': 0.125, 'k_q': 0.500, 'k_f': 0.01300},
    2: {'k_m': 0.125, 'k_q': 1.250, 'k_f': 0.00520},
    3: {'k_m': 0.100, 'k_q': 1.100, 'k_f': 0.00677},
    4: {'k_m': 0.107, 'k_q': 1.143, 'k_f': 0.00630},
    5: {'k_m': 0.105, 'k_q': 1.132, 'k_f': 0.00646}
}

k_m = factors.get(number_spans, {}).get('k_m', 0)
k_q = factors.get(number_spans, {}).get('k_q', 0)
k_f = factors.get(number_spans, {}).get('k_f', 0)


M_uls = k_m * load_uls * span**2 # Изгибающий момент в наиболее опасном сечении
Q_uls = k_q * load_uls * span # Поперечная сила в наиболее опасном сечении

M_sls = k_m * load_sls * span**2 # Изгибающий момент в наиболее опасном сечении

if orient == 'Вверх':
    σ_gr = M_sls / W_gr_wf
    σ_f = M_sls / W_wf_span
else:
    σ_gr = M_sls / W_gr_tf
    σ_f = M_sls / W_tf_span

I_f = I_gr - σ_gr / σ_f * (I_gr - I_span) # Момент инерции для определения прогибов
deflection = k_f * load_sls * span**4 / (E_s * I_f) * 1e-3 # Прогиб

# Предельные прогибы
#f_u_table = [120, 150, 200, 250, 300]
#Height_table = [1, 3, 6, 12, 24] if Height > 6.0 else [1, 3, 6, 12, 24]
if def_method == 'Обратная норма':
    f_u = span / def_n
elif def_method == 'Значение':
    f_u = def_f
    
#f_u = np.intrep(Height_table, f_u_table, Height)

### ПРОВЕРКИ ###
if number_spans == 1:
    U_m = M_uls/M_ult_span
    color_result_m = 'lime' if U_m <= 1 else 'red'
    U_s = Q_uls/Q_ult
    color_result_s = 'lime' if U_s <= 1 else 'red'
    U = max(U_m, U_s)
    color_result = 'lime' if U <= 1 else 'red'
else:
    U = max(Q_uls/Q_ult, M_uls/M_ult_sup, Q_uls / (1.25 * Q_ult) + M_uls / (1.25 * M_ult_sup))
    color_result = 'lime' if U <= 1 else 'red'

if deflection <= f_u:
    color_result_def = 'lime'
else: 
    color_result_def = 'red'

### Область прочности профилированного настила ###
def draw_capasity_contour():
    fig = go.Figure()

    M_ult = M_ult_span if number_spans == 1 else M_ult_sup

    points = [
        [(0, M_ult),
         (0.25 * Q_ult, M_ult),
         (Q_ult, 0.25 * M_ult),
         (Q_ult, 0)]]

    for point in points:
        x = [p[0] * UF_Forces for p in point]
        y = [p[1] * UF_Moments for p in point]
        
        # Основной сегмент
        fig.add_trace(go.Scatter(x=x, y=y,
            mode='lines', line=dict(color='deepskyblue', width=2),
            fill='tozerox', fillcolor='rgba(0,191,255,0.2)', name='Capacity Line'))

    if number_spans == 1:
        fig.add_trace(go.Scatter(x=[Q_uls * UF_Forces], y=[0],
            mode='markers', marker=dict(color=color_result_s, size=7.5),
            showlegend=False, name = f'{U_s:.2f}'))
        fig.add_trace(go.Scatter(x=[0], y=[M_uls * UF_Moments],
            mode='markers', marker=dict(color=color_result_m, size=7.5),
            showlegend=False, name = f'{U_m:.2f}')) 
    else:
        fig.add_trace(go.Scatter(x=[Q_uls * UF_Forces], y=[M_uls * UF_Moments],
            mode='markers', marker=dict(color=color_result, size=7.5),
            showlegend=False, name = 'ULS=' + f'{U:.2f}')) 

    fig.update_layout(
        margin=dict(l=0, r=0, t=25, b=0),
        xaxis=dict(title='Поперечная сила', showgrid=True, range=[0.0, 1.05 * Q_ult * UF_Forces], tickformat=f'.{precision_value}f'),
        yaxis=dict(title='Момент x-x', showgrid=True, range=[0.0, 1.05 * M_ult * UF_Moments], tickformat=f'.{precision_value}f'),
        showlegend=False, height = 1000, template='plotly_dark')

    return fig

#Результаты:

col_l, col_r = st.columns([2, 3])
with col_l:
    st.header('Сечение гофры настила', divider = 'gray') # Заголовок страницы
    tab_span, tab_sup = st.tabs(['В пролете', 'На опоре'])

    with tab_span:
        flange = 'Широкая' if orient == 'Вверх' else 'Узкая' if orient == 'Вниз' else None
        effective_section = effective_section_properties(flange)        
        I_ef, W_ef_wf, W_ef_tf = effective_section[1]
        t_ef_f, t_ef_w = effective_section[3]        
        st.plotly_chart(draw_section(flange, effective_section))

        st.subheader('Полное сечение', divider = 'gray')
        st.latex('t_{cor}='+f'{t * UF_Dimensions:.{precision_value}f}')
        st.latex('I_{g}='+f'{I_gr * UF_SectionProperties**4:.{precision_value}f}' + '\;'*4 +'W_{g.wf}='+f'{W_gr_wf * UF_SectionProperties**3:.{precision_value}f}' + '\;'*4 + 'W_{g.tf}='+f'{W_gr_tf * UF_SectionProperties**3:.{precision_value}f}')
        
        st.subheader('Редуцированное сечение', divider='gray')
        if 0 < t_ef_f < t and 0 < t_ef_w < t:
            st.latex('t_{ef.f}='+f'{t_ef_f * UF_Dimensions:.{precision_value}f}' + '\;'*4 + 't_{ef.w}='+f'{t_ef_w * UF_Dimensions:.{precision_value}f}')
        elif 0 < t_ef_f < t:
            st.latex('t_{ef.f}='+f'{t_ef_f * UF_Dimensions:.{precision_value}f}')
        elif 0 < t_ef_w < t:
            st.latex('t_{ef.w}='+f'{t_ef_w * UF_Dimensions:.{precision_value}f}')
        
        st.latex('I_{ef}='+f'{effective_section_properties(flange)[1][0] * UF_SectionProperties**4:.{precision_value}f}' + '\;'*4 + 'W_{ef.wf}='+f'{effective_section_properties(flange)[1][1] * UF_SectionProperties**3:.{precision_value}f}' + '\;'*4 + 'W_{ef.tf}='+f'{effective_section_properties(flange)[1][2] * UF_SectionProperties**3:.{precision_value}f}')
        st.latex('M_{ult}='+f'{M_ult_span * UF_Moments:.{precision_value}f}' + '\;'*4 + 'Q_{ult}='+f'{Q_ult * UF_Forces:.{precision_value}f}' + '\;'*4 + 'f_{ult}='+f'{f_u * UF_Dimensions:.{precision_value}f}')

        st.subheader('Результаты расчёта', divider='gray')
        st.latex('M='+f'{M_uls * UF_Moments:.{precision_value}f}' + '\;'*4 + 'Q='+f'{Q_uls * UF_Forces:.{precision_value}f}' + '\;'*4 + 'f='+f'{deflection * UF_Dimensions:.{precision_value}f}')

    with tab_sup:
        flange = 'Узкая' if orient == 'Вверх' else 'Широкая' if orient == 'Вниз' else None
        effective_section = effective_section_properties(flange)
        I_ef, W_ef_wf, W_ef_tf = effective_section[1]
        t_ef_f, t_ef_w = effective_section[3]
        st.plotly_chart(draw_section(flange, effective_section))

        st.subheader('Полное сечение', divider = 'gray')
        st.latex('t_{cor}='+f'{t * UF_Dimensions:.{precision_value}f}')
        st.latex('I_{g}='+f'{I_gr * UF_SectionProperties**4:.{precision_value}f}' + '\;'*4 +'W_{g.wf}='+f'{W_gr_wf * UF_SectionProperties**3:.{precision_value}f}' + '\;'*4 + 'W_{g.tf}='+f'{W_gr_tf * UF_SectionProperties**3:.{precision_value}f}')
        
        st.subheader('Редуцированное сечение', divider='gray')
        if 0 < t_ef_f < t and 0 < t_ef_w < t:
            st.latex('t_{ef.f}='+f'{t_ef_f * UF_Dimensions:.{precision_value}f}' + '\;'*4 + 't_{ef.w}='+f'{t_ef_w * UF_Dimensions:.{precision_value}f}')
        elif 0 < t_ef_f < t:
            st.latex('t_{ef.f}='+f'{t_ef_f * UF_Dimensions:.{precision_value}f}')
        elif 0 < t_ef_w < t:
            st.latex('t_{ef.w}='+f'{t_ef_w * UF_Dimensions:.{precision_value}f}')

        st.latex('I_{ef}='+f'{effective_section_properties(flange)[1][0] * UF_SectionProperties**4:.{precision_value}f}' + '\;'*4 + 'W_{ef.wf}='+f'{effective_section_properties(flange)[1][1] * UF_SectionProperties**3:.2f}' + '\;'*4 + 'W_{ef.tf}='+f'{effective_section_properties(flange)[1][2] * UF_SectionProperties**3:.{precision_value}f}')
        st.latex('M_{ult}='+f'{M_ult_sup * UF_Moments:.{precision_value}f}' + '\;'*4 + 'Q_{ult}='+f'{Q_ult * UF_Forces:.{precision_value}f}')

        st.subheader('Результаты расчёта', divider='gray')
        st.latex('M='+f'{M_uls * UF_Moments:.{precision_value}f}' + '\;'*4 + 'Q='+f'{Q_uls * UF_Forces:.{precision_value}f}')

with col_r:
    st.header('Область прочности', divider = 'gray')
    st.plotly_chart(draw_capasity_contour(), use_container_width=False, wight = 1000)

    st.markdown(f'''
        <div style="text-align: center;">
            <span style='color: {color_result}; font-size: 16px;'>
                Коэффициент использования по прочности: {U:.2f}
            </span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div style="text-align: center;">
            <span style='color: {color_result_def}; font-size: 16px;'>
                Коэффициент использования по жесткости: {deflection / f_u:.2f}
            </span>
        </div>
        ''', unsafe_allow_html=True)
