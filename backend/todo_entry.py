def todo_entry(entry):
    return {
        "id": entry[0],
        "createdAt": entry[1],
        "updatedAt": entry[2],
        "content": entry[3],
        "title": entry[4],
        "completed": entry[5],
    }
