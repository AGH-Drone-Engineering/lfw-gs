def add_data_to_gui( data_check, name_x: str):
    start_world = data_check.find(name_x)
    len_specific_name = len(name_x)
    start = len_specific_name + start_world

    first_value = data_check[:start_world]
    second_value = data_check[start:]

    try:
        x_value = float(first_value)

        y_value = float(second_value)
        print(x_value)
        print(y_value)
    except ValueError:
        print('Wrong start type of data, not flat or int')


add_data_to_gui('25123123;angle;-1', ';angle;')