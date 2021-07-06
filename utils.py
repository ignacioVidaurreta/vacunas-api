poblaciones_provincias = {
    '2': 3078836,
    '6': 17709598,
    '10': 418991,
    '14': 3798261,
    '18': 1130320,
    '22': 1216247,
    '26': 629181,
    '30': 1398510,
    '34': 610019,
    '38': 779212,
    '42': 779212,
    '46': 398648,
    '50': 2010363,
    '54': 1274992,
    '58': 672461,
    '62': 757052,
    '66': 1441988,
    '70': 789489,
    '74': 514610,
    '78': 374756,
    '82': 3563390,
    '86': 988245,
    '90': 1714487,
    '94': 177697
}

def grab_info_by_state(df, dose_col):
    by_state = df.groupby(
        by=["jurisdiccion_codigo_indec", "jurisdiccion_nombre"]
    ).sum().reset_index()

    response = dict()


    response["headers"] = [
        *list(by_state.columns[0:2].to_numpy()),
        "poblacion_vacunada_provincia"
    ]

    content = []
    for i in range(0, len(by_state)):
        row = list(by_state.iloc[i].to_numpy())
        vac_qty = row[2] if dose_col == "primera_dosis_cantidad" else row[3]
        vac_qty /=  poblaciones_provincias[str(row[0])] * 100
        data = [*row[0:2], vac_qty]
        data[0] = int(data[0])
        data[2] = int(data[2])
        content.append(data)

    response["content"] = content
    return response

