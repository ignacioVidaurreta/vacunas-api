def grab_info_by_state(df, dose_col):
    by_state = df.groupby(
        by=["jurisdiccion_codigo_indec", "jurisdiccion_nombre"]
    ).sum().reset_index()

    response = dict()


    response["headers"] = [
        *list(by_state.columns[0:2].to_numpy()),
        "cant_vacunas"
    ]

    content = []
    for i in range(0, len(by_state)):
        row = list(by_state.iloc[i].to_numpy())
        vac_qty = row[2] if dose_col == "primera_dosis_cantidad" else row[3]
        data = [*row[0:2], vac_qty]
        data[0] = int(data[0])
        data[2] = int(data[2])
        content.append(data)

    response["content"] = content
    return response

